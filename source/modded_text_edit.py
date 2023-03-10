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
        menu.addAction('??????????????', self.delete_widget)

    def delete_widget(self):
        if not self.creating:
            self.db_handler.delete_note(self.note_id)
            self.deleteLater()
        else:
            msg = QMessageBox()
            msg.critical(self, '????????????', "?????????????? ?????????????????? ?????????????? ?????? ?????????????? ???????????? '????????????'")

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Return and self.creating:
            self.enter_save.emit()
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        if not (self.toPlainText()) and not self.creating:
            self.deleteLater()
            self.db_handler.delete_note(self.note_id)
        super().focusOutEvent(event)

    def mouseMoveEvent(self, e):
        super().mouseMoveEvent(e)
        if e.buttons() == Qt.RightButton and not self.creating:
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
        self.setMinimumSize(self.minimumSize().width(), self.lineCountToWidgetHeight(num_lines))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        margins = self.contentsMargins()

        if width >= margins.left() + margins.right():
            document_width = width - margins.left() - margins.right()
        else:
            document_width = 0

        document = self.document().clone()
        document.setTextWidth(document_width)

        return margins.top() + document.size().height() + margins.bottom()

    def sizeHint(self):
        original_hint = super(AutoResizingTextEdit, self).sizeHint()
        return QSize(original_hint.width(), self.heightForWidth(original_hint.width()))

    def lineCountToWidgetHeight(self, num_lines):
        assert num_lines >= 0

        widget_margins = self.contentsMargins()
        document_margin = self.document().documentMargin()
        font_metrics = QFontMetrics(self.document().defaultFont())

        return (
                widget_margins.top() +
                document_margin +
                max(num_lines, 1) * font_metrics.height() +
                self.document().documentMargin() +
                widget_margins.bottom()
        )

        return QSize(original_hint.width(), minimum_height_hint)
