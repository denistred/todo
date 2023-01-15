import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, \
    QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignremoal
from PyQt5.QtGui import QPaintEvent, QPainter, QColor, QFont, QPixmap, QIcon, QFontMetrics
from ui.card_ui import Ui_Form
from source.modded_plain_text_edit import ModQPlainTextEdit
from source.database_handler import Handler

BG_COLOR: str = '#ECECEC'
ON_MOUSE_COLOR: str = '#A3A4A4'
FONT_NAME: str = 'Arial'

CROSS_ICON: str = 'icons/cross.png'
PLUS_ICON: str = 'icons/plus.png'
FONT_SIZE: int = 10
MODPLAINTEXT_SIZE: tuple = (355, 115)
MODPALINTEXT_SHADOW_BLUR_SIZE: int = 10
MODPLAINTEXT_MAX_TEXT_SIZE: int = 1000
MAINWIDGET_SHADOW_BLUE_SIZE: int = 20
MAINWIDGET_WIDTH: int = 375
SHADOW_COLOR: str = '#565656'
PAINTER_PEN_COLOR: tuple = (255, 255, 255, 0)
SAVE_BUTTON_SIZE: tuple = (240, 30)
CANCEL_BUTTON_SIZE: tuple = (110, 30)
WIDGET_FIRST_OFFSET: int = 160
WIDGET_SECOND_OFFSET: int = 40
TEXT_MANUAL_WRAP_COEFF: int = 343

STYLE_SHEET = '''
QPushButton {
    background-color:#ECECEC;
    border: 0px solid;
    border-radius: 5px;
    padding: 5px 10px 5px;
}
QPushButton:hover{
    background-color:#ACACAC;
    border: 0px solid;
    border-radius: 5px;
    padding: 5px 10px 5px;
}
QPushButton:pressed{
    background-color:#fcfafa;
    border: 0px solid;
    border-radius: 5px;
    padding: 5px 10px 5px;
}
'''


class CardWidget(QWidget, Ui_Form):
    widget_delete_signal = pyqtSignal()

    def __init__(self, desk_id, new=True, name=None, id=None):
        super().__init__()
        self.desk_id = desk_id
        self.setupUi(self)
        self.init_ui()
        self.setFixedWidth(MAINWIDGET_WIDTH)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(SHADOW_COLOR))
        shadow.setBlurRadius(MAINWIDGET_SHADOW_BLUE_SIZE)
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)
        self.db_handler = Handler()

        if new:
            self.db_handler.create_card(self.card_name.text(), self.desk_id)
            self.card_id = self.db_handler.return_card_id(self.card_name.text())[-1][0]
        else:
            self.card_name.setText(str(name))
            self.card_id = id
            self.load_notes()

    def init_ui(self):
        self.delete_widget_button.clicked.connect(self.delete_widget)
        pic = QPixmap(CROSS_ICON)
        icon = QIcon()
        icon.addPixmap(pic)
        self.delete_widget_button.setIcon(icon)

        self.card_name.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.card_name.setFocusPolicy(Qt.StrongFocus)
        self.card_name.editingFinished.connect(self.title_approve)

        pic = QPixmap(PLUS_ICON)
        icon = QIcon()
        icon.addPixmap(pic)
        self.add_task_button.setIcon(icon)
        self.add_task_button.clicked.connect(self.create_task)

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(QColor(*PAINTER_PEN_COLOR))
        last_item = self.verticalLayout.count() - 2
        last_item_x = self.verticalLayout.itemAt(last_item).widget().x()
        last_item_y = self.verticalLayout.itemAt(last_item).widget().y()
        last_item_width = self.verticalLayout.itemAt(last_item).widget().width()
        painter.setBrush(QColor(BG_COLOR))
        if self.verticalLayout.itemAt(last_item).widget().isHidden():
            painter.drawRoundedRect(0, 0, last_item_x * 2 + last_item_width, last_item_y +
                                    WIDGET_FIRST_OFFSET, 5, 5)
        else:
            painter.drawRoundedRect(0, 0, last_item_x * 2 + last_item_width, last_item_y +
                                    WIDGET_SECOND_OFFSET, 5, 5)

    def delete_widget(self):
        confirmation = QMessageBox()
        confirmation.setText('Вы уверены что хотите удалить список?')
        confirmation.setWindowTitle('Удалить список?')
        confirmation.setIcon(QMessageBox.Question)
        confirmation.setStyleSheet('background-color: rgb(255, 255, 255);color: rgb(0, 0, 0);')
        confirmation.addButton('Да', QMessageBox.YesRole)
        confirmation.addButton('Отмена', QMessageBox.RejectRole)
        value = confirmation.exec()
        if value == 0:
            for i in range(self.verticalLayout.count()):
                if self.verticalLayout.itemAt(i).__class__.__name__ == 'QPlainTextEdit':
                    self.verticalLayout.itemAt(i).widget().graphicsEffect().setEnabled(False)
            self.graphicsEffect().setEnabled(False)
            self.update()
            self.db_handler.delete_card(self.card_id)
            self.deleteLater()
            self.widget_delete_signal.emit()
            self.update()

    def title_approve(self):
        if not (self.card_name.text()):
            self.card_name.setText('Список')
        else:
            self.db_handler.update_card(self.card_id, self.card_name.text())

    def approve_task(self):
        try:
            pos = self.verticalLayout.count() - 4
            if self.current_plaintext.toPlainText().strip():
                self.layout.removeWidget(self.layout.itemAt(0).widget())
                self.layout.removeWidget(self.layout.itemAt(0).widget())
                self.verticalLayout.removeItem(self.layout)
                self.add_task_button.show()
                self.update()
                self.current_plaintext.textChanged.connect(self.automatic_plaintext_size_change)

                self.current_plaintext.creating = False
                self.current_plaintext.height_change.connect(self.automatic_plaintext_size_change)
                self.set_start_size()
                self.update()
            else:
                self.verticalLayout.itemAt(pos).widget().setFocus()
        except AttributeError:
            pass

    def automatic_plaintext_size_change(self):
        if self.sender().__class__.__name__ == 'ModQPlainTextEdit':
            self.plain_text_size_change()

    def plain_text_size_change(self: ModQPlainTextEdit):
        doc = self.sender().document()
        tb = doc.findBlockByNumber(doc.blockCount() - 1)
        h = int(self.sender().blockBoundingGeometry(tb).bottom() + 2 * doc.documentMargin())
        self.sender().setFixedHeight(h)
        self.update()

    def check_max_size(self: ModQPlainTextEdit):
        if len(self.sender().toPlainText()) > MODPLAINTEXT_MAX_TEXT_SIZE:
            self.sender().setPlainText(self.sender().toPlainText()[0:MODPLAINTEXT_MAX_TEXT_SIZE])
            self.sender().setFocus()
            self.update()

    def update_note_content(self: ModQPlainTextEdit):
        if "'" in self.sender().toPlainText():
            self.sender().setPlainText(self.sender().toPlainText().replace("'", ''))
        self.db_handler.update_note(self.sender().toPlainText(), self.sender().note_id)

    def cancel_creating_plaintext(self):
        self.db_handler.delete_note(self.current_plaintext.note_id)
        self.current_plaintext.deleteLater()
        self.layout.removeWidget(self.layout.itemAt(0).widget())
        self.layout.removeWidget(self.layout.itemAt(0).widget())
        self.verticalLayout.removeItem(self.layout)
        self.add_task_button.show()
        self.update()

    def create_plain_text(self, text, height=None):
        plaintext = ModQPlainTextEdit(self.card_id, new=True)
        plaintext.setPlainText(text)
        plaintext.textChanged.connect(self.check_max_size)
        plaintext.textChanged.connect(self.update_note_content)
        plaintext.height_change.connect(self.automatic_plaintext_size_change)
        plaintext.enter_save.connect(self.approve_task)
        if height:
            plaintext.setFixedHeight(height)
        self.update()
        return plaintext

    def approve_drag_plaintext(self, plaintext):
        plaintext.textChanged.connect(self.automatic_plaintext_size_change)
        plaintext.creating = False
        plaintext.height_change.connect(self.automatic_plaintext_size_change)
        font = plaintext.document().defaultFont()
        font_metrics = QFontMetrics(font)
        text_size = font_metrics.size(0, plaintext.toPlainText())
        doc = plaintext.document()
        h = int(20 + text_size.width() // TEXT_MANUAL_WRAP_COEFF * 16 + 2 * doc.documentMargin())
        plaintext.setFixedHeight(h)
        return plaintext

    def create_task(self):
        self.current_plaintext = self.create_plain_text('')

        pos = self.verticalLayout.count() - 2
        self.verticalLayout.insertWidget(pos, self.current_plaintext)  # создаем новую линию
        self.add_task_button.hide()  # прячем кнопку добавить задачу
        self.update()

        self.layout = QHBoxLayout()

        button = QPushButton('Сохранить', self)  # создаем новую кнопку добавить задачу
        button.setStyleSheet(STYLE_SHEET)
        button.setFont(QFont(FONT_NAME, FONT_SIZE))
        button.setFixedSize(*SAVE_BUTTON_SIZE)
        button.clicked.connect(self.approve_task)

        cancel_button = QPushButton('Отмена', self)
        cancel_button.setStyleSheet(STYLE_SHEET)
        cancel_button.setFont(QFont(FONT_NAME, FONT_SIZE))
        cancel_button.setFixedSize(*CANCEL_BUTTON_SIZE)
        cancel_button.clicked.connect(self.cancel_creating_plaintext)

        self.layout.addWidget(button)
        self.layout.addWidget(cancel_button)

        self.verticalLayout.insertLayout(pos + 1, self.layout)
        self.verticalLayout.itemAt(pos).widget().setFocus()
        self.update()

    def applying_functions_to_loaded_notes(self: ModQPlainTextEdit):
        self.sender().textChanged.connect(self.automatic_plaintext_size_change)
        self.sender().textChanged.disconnect(self.applying_functions_to_loaded_notes)

    def set_start_size(self):
        font = self.current_plaintext.document().defaultFont()
        font_metrics = QFontMetrics(font)
        text_size = font_metrics.size(0, self.current_plaintext.toPlainText())
        doc = self.current_plaintext.document()
        h = int(20 + text_size.width() // TEXT_MANUAL_WRAP_COEFF * 16 + 2 * doc.documentMargin())
        self.current_plaintext.setFixedHeight(h)
        self.update()

    def load_notes(self):
        for i in self.db_handler.load_notes(self.card_id):
            if not i[1]:
                self.db_handler.delete_note(i[0])
                continue
            self.current_plaintext = ModQPlainTextEdit(self.card_id, new=False, content=i[1],
                                                       note_id=i[0])
            self.current_plaintext.textChanged.connect(self.check_max_size)
            self.current_plaintext.enter_save.connect(self.approve_task)
            self.current_plaintext.textChanged.connect(self.update_note_content)
            self.current_plaintext.textChanged.connect(self.applying_functions_to_loaded_notes)
            self.current_plaintext.creating = False
            self.current_plaintext.setPlainText(i[1])

            pos = self.verticalLayout.count() - 2
            self.verticalLayout.insertWidget(pos, self.current_plaintext)
            self.update()

            self.set_start_size()
            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CardWidget(0)
    ex.show()
    sys.exit(app.exec())
