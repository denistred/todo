""" A text editor that automatically adjusts its height to the height of the text
    in its document when managed by a layout. """
from PyQt5.QtWidgets import QMessageBox, QGraphicsDropShadowEffect, QSizePolicy, QTextEdit
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData, QSize
from PyQt5.QtGui import QCursor, QColor, QFont, QDrag, QPixmap, QFontMetrics

from source.database_handler import Handler
from source.pil_dragimage import create_image

MODPLAINTEXT_SIZE: tuple = (355, 115)
MODPALINTEXT_SHADOW_BLUR_SIZE = 10
SHADOW_COLOR = '#565656'
FONT_NAME: str = 'Arial'
FONT_SIZE: int = 10
MAXIMUM_SIZE: tuple = (355, 16777215)
SHADOW_OFFSET: tuple = (0, 0)


class AutoResizingTextEdit(QTextEdit):
    height_change = pyqtSignal()
    enter_save = pyqtSignal()

    def __init__(self, card_id, new=True, content=None, note_id=None):
        super(AutoResizingTextEdit, self).__init__()

        # This seems to have no effect. I have expected that it will cause self.hasHeightForWidth()
        # to start returning True, but it hasn't - that's why I hardcoded it to True there anyway.
        # I still set it to True in size policy just in case - for consistency.
        size_policy = self.sizePolicy()
        size_policy.setHeightForWidth(True)
        size_policy.setVerticalPolicy(QSizePolicy.Preferred)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(size_policy)
        self.card_id = card_id
        self.db_handler = Handler()
        if new:
            self.db_handler.create_note(self.toPlainText(), card_id)
            self.note_id = self.db_handler.return_note_id(self.toPlainText())
        else:
            self.note_id = note_id
            self.setPlainText(content)

        self.creating = True
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu)

        self.current_text = None

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(MODPALINTEXT_SHADOW_BLUR_SIZE)
        shadow.setOffset(*SHADOW_OFFSET)
        shadow.setColor(QColor(SHADOW_COLOR))
        self.setGraphicsEffect(shadow)

        self.setStyleSheet('border-radius: 5px; background-color: #FFFFFF')
        self.setFont(QFont(FONT_NAME, FONT_SIZE))

        self.textChanged.connect(lambda: self.updateGeometry())

    def context_menu(self):
        self.normal_menu = self.createStandardContextMenu()
        self.add_custom_menu_items(self.normal_menu)
        self.normal_menu.exec_(QCursor.pos())

    def add_custom_menu_items(self, menu):
        menu.addSeparator()
        menu.addAction('Удалить', self.delete_widget)

    def delete_widget(self):
        if not self.creating:
            self.db_handler.delete_note(self.note_id)
            self.deleteLater()
        else:
            msg = QMessageBox()
            msg.critical(self, 'Ошибка', "Сначала сохраните заметку или нажмите кнопку 'Отмена'")

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Return:
            self.enter_save.emit()
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        if not (self.toPlainText()) and not self.creating:
            self.deleteLater()
            self.db_handler.delete_note(self.note_id)
        super().focusOutEvent(event)

    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton and not self.creating:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            pixmap = pixmap.fromImage(create_image(self.toPlainText()))
            drag.setPixmap(pixmap)
            drag.setHotSpot(e.pos())
            drag.exec_(Qt.MoveAction)
            self.db_handler.delete_note(self.note_id)
            self.deleteLater()

    def setMinimumLines(self, num_lines):
        """ Sets minimum widget height to a value corresponding to specified number of lines
            in the default font. """

        self.setMinimumSize(self.minimumSize().width(), self.lineCountToWidgetHeight(num_lines))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        margins = self.contentsMargins()

        if width >= margins.left() + margins.right():
            document_width = width - margins.left() - margins.right()
        else:
            # If specified width can't even fit the margin, there's no space left for the document
            document_width = 0

        # Cloning the whole document only to check its size at different width seems wasteful
        # but apparently it's the only and preferred way to do this in Qt >= 4. QTextDocument does not
        # provide any means to get height for specified width (as some QWidget subclasses do).
        # Neither does QTextEdit. In Qt3 Q3TextEdit had working implementation of heightForWidth()
        # but it was allegedly just a hack and was removed.
        #
        # The performance probably won't be a problem here because the application is meant to
        # work with a lot of small notes rather than few big ones. And there's usually only one
        # editor that needs to be dynamically resized - the one having focus.
        document = self.document().clone()
        document.setTextWidth(document_width)

        return margins.top() + document.size().height() + margins.bottom()

    def sizeHint(self):
        original_hint = super(AutoResizingTextEdit, self).sizeHint()
        return QSize(original_hint.width(), self.heightForWidth(original_hint.width()))

    def lineCountToWidgetHeight(self, num_lines):
        """ Returns the number of pixels corresponding to the height of specified number of lines
            in the default font. """

        # ASSUMPTION: The document uses only the default font

        assert num_lines >= 0

        widget_margins = self.contentsMargins()
        document_margin = self.document().documentMargin()
        font_metrics = QFontMetrics(self.document().defaultFont())

        # font_metrics.lineSpacing() is ignored because it seems to be already included in font_metrics.height()
        return (
                widget_margins.top() +
                document_margin +
                max(num_lines, 1) * font_metrics.height() +
                self.document().documentMargin() +
                widget_margins.bottom()
        )

        return QSize(original_hint.width(), minimum_height_hint)
