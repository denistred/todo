from PyQt5.QtWidgets import QPlainTextEdit, QMessageBox, QGraphicsDropShadowEffect, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData
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


class ModQPlainTextEdit(QPlainTextEdit):
    height_change = pyqtSignal()
    enter_save = pyqtSignal()


    def __init__(self, card_id, new=True, content=None, note_id=None):
        super().__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setMaximumSize(*MAXIMUM_SIZE)
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
        self.setFixedSize(*MODPLAINTEXT_SIZE)
        self.setFont(QFont(FONT_NAME, FONT_SIZE))

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

    def changeEvent(self, event) -> None:
        if not self.creating:
            self.height_change.emit()
        super().changeEvent(event)

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
        if e.buttons() == Qt.LeftButton:
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
            self.cancel_creating()
