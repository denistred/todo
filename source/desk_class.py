import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon, QKeyEvent
from ui.desk_ui import DeskUi
from source.card_class import CardWidget
from source.database_handler import Handler
from source.css_consts import DESK_WIDGET_STYLE

BG_COLOR: str = '#87FFD2'
CROSS_ICON: str = 'icons/cross.png'
PLUS_ICON: str = 'icons/plus.png'
FONT_NAME: str = 'Arial'
FONT_SIZE: int = 11
ON_MOUSE_COLOR: str = '#76D7C4'
WIDGET_GEOMETRY = (300, 300, 300, 300)
MAX_CARDS_COUNT: int = 6


def get_nearest_item(layout, pos):
    # for i in range(layout.count()):
    # print(layout.itemAt(i).widget())
    pos_y = pos.y() - 40
    possible_positions = []
    for note_pos in range(layout.count() - 3):
        try:
            possible_positions.append(layout.itemAt(note_pos + 2).widget().y())
        except:
            pass
    button_widget = layout.itemAt(
        layout.count() - 1).widget().y()  # Позиция чуть выше кнопки добавления задачи
    possible_positions.append(button_widget)  # Добавляем позицию чуть выше кнопки добавления задачи
    nearest_pos, nearest_number = None, 10000000
    for i, possible_position in enumerate(possible_positions):
        if nearest_number > abs(pos_y - possible_position):
            nearest_number = abs(pos_y - possible_position)
            nearest_pos = i + 2
    # print(possible_positions)
    return nearest_pos


class DeskWidget(QWidget, DeskUi):
    delete_change_desk_button = pyqtSignal(int)

    def __init__(self, stacked_widget_id=None, is_new=True, desk_id=None, name=None):
        super().__init__()

        self.stack_widget_id = stacked_widget_id
        self.setObjectName('Form')

        self.in_database = False
        self.db_id = desk_id
        self.start_desk_name = name

        self.setupUi(self)
        self.init_ui()
        self.desk_name.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.desk_name.setFocus()
        self.db_handler = Handler()

        self.setAcceptDrops(True)

        if not is_new:
            self.desk_name.setText(str(name))
            self.load_cards()

        self.desk_name.editingFinished.connect(self.desk_name_editing_finish)
        self.widget_count_check()

    def init_ui(self):
        self.setGeometry(*WIDGET_GEOMETRY)
        self.setStyleSheet(DESK_WIDGET_STYLE)

        self.delete_desk_button.clicked.connect(self.delete_desk_check)
        pic = QPixmap(CROSS_ICON)
        icon = QIcon()
        icon.addPixmap(pic)
        self.delete_desk_button.setIcon(icon)

        self.create_card_button.setFont(QFont(FONT_NAME, FONT_SIZE - 1))
        pic = QPixmap(PLUS_ICON)
        icon = QIcon()
        icon.addPixmap(pic)
        self.create_card_button.setIcon(icon)

    def dragEnterEvent(self, e) -> None:
        e.accept()

    def dropEvent(self, e) -> None:
        pos = e.pos()
        widget = e.source()
        for card_number in range(self.horizontalLayout.count() - 2):
            card_widget = self.horizontalLayout.itemAt(card_number).widget()
            if 10 + 380 * card_number < pos.x() < card_number * 380 + 370:
                if card_widget.creating_plaintext:  # проверяем делается ли новая заметка
                    card_widget.approve_task()
                layout = card_widget.verticalLayout
                card_widget_height = layout.itemAt(layout.count() - 1).widget().y() + 40
                card_widget_y = card_widget.y()
                if 70 < pos.y() < card_widget_y + card_widget_height:
                    text = widget.toPlainText()
                    new_plain_text = card_widget.create_plain_text(text)
                    new_plain_text.setPlainText(new_plain_text.toPlainText())
                    new_plain_text.creating = False
                    nearest_item = get_nearest_item(layout, pos)
                    layout.insertWidget(nearest_item, new_plain_text)
            else:
                widget.show()

    def delete_desk_check(self) -> None:
        cards_count = self.horizontalLayout.count() - 2
        if cards_count > 0:
            confirmation = QMessageBox()
            confirmation.setText('Вы уверены что хотите удалить доску?')
            confirmation.setWindowTitle('Удалить доску?')
            confirmation.setIcon(QMessageBox.Question)
            confirmation.setStyleSheet('background-color: rgb(255, 255, 255);color: rgb(0, 0, 0);')
            confirmation.addButton('Да', QMessageBox.YesRole)
            confirmation.addButton('Отмена', QMessageBox.RejectRole)
            value = confirmation.exec()
            if value == 0:
                self.delete_desk()
        else:
            self.delete_desk()

    def delete_desk(self):
        if self.in_database:
            self.db_handler.delete_desk(self.db_id)
        self.delete_change_desk_button.emit(self.stack_widget_id)
        self.deleteLater()

    def enable_create_card_button(self) -> None:
        self.create_card_button.clicked.connect(self.create)

    def desk_name_editing_finish(self) -> None:
        if not self.in_database:
            if self.desk_name.text() not in self.db_handler.return_desk_names():
                self.db_handler.create_desk(self.desk_name.text())
                self.in_database = True
                self.db_id = self.db_handler.return_desk_id(self.desk_name.text())
                self.enable_create_card_button()
            else:
                msg = QMessageBox()
                msg.critical(self, 'Ошибка', 'Доска с таким названием уже есть!', QMessageBox.Ok)
                self.desk_name.setFocus()
        else:
            self.db_handler.update_desk(self.db_id, self.desk_name.text())

    def widget_count_check(self) -> None:
        if self.horizontalLayout.count() == MAX_CARDS_COUNT and self.create_card_button.isHidden():
            self.create_card_button.show()
            self.repaint()
        elif self.horizontalLayout.count() == MAX_CARDS_COUNT:
            self.create_card_button.hide()
            self.repaint()

    def create(self, **kwargs) -> None:
        if self.horizontalLayout.count() < MAX_CARDS_COUNT:
            widget = CardWidget(self.db_handler.return_desk_id(self.desk_name.text()))
            widget.widget_delete_signal.connect(self.widget_count_check)
            pos = self.horizontalLayout.count() - 2
            self.horizontalLayout.insertWidget(pos, widget)
        self.widget_count_check()

    def load_cards(self) -> None:
        for i in self.db_handler.load_cards(self.db_id):
            widget = CardWidget(self.db_id, new=False, name=i[1], id=i[0])
            widget.widget_delete_signal.connect(self.widget_count_check)
            pos = self.horizontalLayout.count() - 2
            self.horizontalLayout.insertWidget(pos, widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DeskWidget()
    ex.show()
    sys.exit(app.exec())
