import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5.QtGui import QFont, QPixmap, QIcon
from ui.desk_ui import Ui_MainWindow
from source.card_class import CardWidget
from source.database_handler import Handler

BG_COLOR: str = '#87FFD2'
CROSS_ICON: str = 'icons/cross.png'
PLUS_ICON: str = 'icons/plus.png'
FONT_NAME: str = 'Arial'
FONT_SIZE: int = 11
ON_MOUSE_COLOR: str = '#76D7C4'
WIDGET_GEOMETRY = (300, 300, 300, 300)
MAX_CARDS_COUNT: int = 6


class DeskWidget(QMainWindow, Ui_MainWindow):
    delete_change_desk_button = pyqtSignal(int)

    def __init__(self, stacked_widget_id=None, is_new=True, desk_id=None, name=None):
        super().__init__()

        self.stack_widget_id = stacked_widget_id

        self.in_database = False
        self.db_id = desk_id
        self.start_desk_name = name

        self.setupUi(self)
        self.init_ui()
        self.setCentralWidget(self.centralwidget)
        self.desk_name.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.desk_name.setFocus()
        self.db_handler = Handler()

        if not is_new:
            self.desk_name.setText(str(name))
            self.load_cards()

        self.desk_name.editingFinished.connect(self.desk_name_editing_finish)
        self.widget_count_check()

    def init_ui(self):
        self.setGeometry(*WIDGET_GEOMETRY)
        self.setStyleSheet(f'background-color: {BG_COLOR}')

        self.delete_desk_button.clicked.connect(self.delete_desk)
        self.delete_desk_button.setObjectName('delete_desk_button')
        pic = QPixmap(CROSS_ICON)
        icon = QIcon()
        icon.addPixmap(pic)
        self.delete_desk_button.setIcon(icon)
        self.delete_desk_button.installEventFilter(self)

        self.create_card_button.setFont(QFont(FONT_NAME, FONT_SIZE - 1))
        pic = QPixmap(PLUS_ICON)
        icon = QIcon()
        icon.addPixmap(pic)
        self.create_card_button.setIcon(icon)
        self.create_card_button.setObjectName('create_card_button')
        self.create_card_button.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Leave:
            obj.setStyleSheet(f'border: 0px; background-color: {BG_COLOR}')
        elif event.type() == QEvent.Enter:
            obj.setStyleSheet(f'border: 0px; background-color: {ON_MOUSE_COLOR}')

        return super().eventFilter(obj, event)

    def delete_desk(self):
        if self.in_database:
            self.db_handler.delete_desk(self.db_id)
        self.delete_change_desk_button.emit(self.stack_widget_id)
        self.deleteLater()

    def enable_create_card_button(self):
        self.create_card_button.clicked.connect(self.create)

    def desk_name_editing_finish(self):
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

    def widget_count_check(self):
        if self.horizontalLayout.count() == MAX_CARDS_COUNT and self.create_card_button.isHidden():
            self.create_card_button.show()
            self.repaint()
        elif self.horizontalLayout.count() == MAX_CARDS_COUNT:
            self.create_card_button.hide()
            self.repaint()

    def create(self, **kwargs):
        if self.horizontalLayout.count() < MAX_CARDS_COUNT:
            widget = CardWidget(self.db_handler.return_desk_id(self.desk_name.text()))
            widget.widget_delete_signal.connect(self.widget_count_check)
            pos = self.horizontalLayout.count() - 2
            self.horizontalLayout.insertWidget(pos, widget)
        self.widget_count_check()

    def load_cards(self):
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
