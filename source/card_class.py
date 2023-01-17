import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, \
    QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPixmap, QIcon, QFontMetrics
from ui.card_ui import Ui_Form
from source.database_handler import Handler
from source.modded_text_edit import AutoResizingTextEdit

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
SAVE_BUTTON_SIZE: tuple = (225, 30)
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
        self.setStyleSheet('''background-color: #f5f5f5;
        border-radius: 5px''')
        self.add_task_button.setFixedWidth(340)

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
            self.hide()
            self.deleteLater()
            self.update()
            self.widget_delete_signal.emit()

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

                self.current_plaintext.creating = False
                self.update()
            else:
                self.verticalLayout.itemAt(pos).widget().setFocus()
        except AttributeError:
            pass

    def update_note_content(self: AutoResizingTextEdit):
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
        plaintext = AutoResizingTextEdit(self.card_id, new=True)
        plaintext.setPlainText(text)
        plaintext.textChanged.connect(self.update_note_content)
        plaintext.enter_save.connect(self.approve_task)
        if height:
            plaintext.setFixedHeight(height)
        self.update()
        return plaintext

    def approve_drag_plaintext(self, plaintext):
        plaintext.creating = False
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

    def load_notes(self):
        for i in self.db_handler.load_notes(self.card_id):
            if not i[1]:
                self.db_handler.delete_note(i[0])
                continue
            self.current_plaintext = AutoResizingTextEdit(self.card_id, new=False, content=i[1],
                                                          note_id=i[0])
            self.current_plaintext.enter_save.connect(self.approve_task)
            self.current_plaintext.textChanged.connect(self.update_note_content)
            self.current_plaintext.creating = False
            self.current_plaintext.setPlainText(i[1])

            pos = self.verticalLayout.count() - 2
            self.verticalLayout.insertWidget(pos, self.current_plaintext)
            self.update()

            self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CardWidget(0)
    ex.show()
    sys.exit(app.exec())
