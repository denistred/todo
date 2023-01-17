import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton
from PyQt5.QtGui import QFont, QPixmap, QIcon
from ui.main_window_ui import Ui_MainWindow
from source.modded_qlineedit import ModQLineEdit
from source.desk_class import DeskWidget
from source.database_handler import Handler

BG_COLOR = '#F7F9F9'
ON_MOUSE_COLOR = '#C6C6C6'

WINDOW_GEOMETRY = (150, 150, 1000, 700)
FONT_NAME: str = 'Arial'
FONT_SIZE: int = 10
MAX_DESK_NAME_LENGTH: int = 20
MAX_DESK_COUNT: int = 20
PLUS_ICON: str = 'icons/plus.png'
WINDOW_ICON: str = 'icons/window_icon.png'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.stack_widget = QStackedWidget(self)
        self.init_ui()
        self.stack_widget_ids = []
        self.stack_widget_buttons = []
        self.db_handler = Handler()
        self.load_desks()
        self.create_desk_button.setFont(QFont(FONT_NAME, FONT_SIZE))
        pic = QPixmap(PLUS_ICON)
        icon = QIcon()
        icon.addPixmap(pic)
        self.create_desk_button.setIcon(icon)
        self.setWindowTitle('ToDo')
        self.setWindowIcon(QIcon(WINDOW_ICON))

    def init_ui(self):
        self.setGeometry(*WINDOW_GEOMETRY)
        self.stack_widget.setStyleSheet(''' QStackedWidget{
                               background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                               stop:0 rgba(0, 255, 147, 255), stop:1 rgba(0, 255, 244, 255));
                               border: 0px solid;
                               border-radius: 5px;}
                               ''')

        self.horizontalLayout.addWidget(self.stack_widget)

        self.create_desk_button.clicked.connect(self.create_desk)
        self.create_desk_button.clicked.connect(self.picked_button_show)

    def picked_button_show(self):
        for i in self.stack_widget_buttons:
            i.setStyleSheet('''QPushButton{
                                        background-color:transparent;
                                        border: 1px outset rgb(220, 220, 220);
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }
                                    QPushButton:hover{
                                        background-color:rgb(220, 220, 220);
                                        border: 0px solid;
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }
                                    QPushButton:pressed{
                                        background-color:rgb(200, 200, 200);
                                        border: 0px solid;
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }''')
        self.stack_widget_buttons[self.stack_widget.currentIndex()].setStyleSheet('''QPushButton{
                                        background-color:rgb(220, 220, 220);
                                        border: 0px outset rgb(238, 238, 238);
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }
                                    QPushButton:hover{
                                        background-color:rgb(220, 220, 220);
                                        border: 0px solid;
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }
                                    QPushButton:pressed{
                                        background-color:rgb(200, 200, 200);
                                        border: 0px solid;
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }''')

    def create_desk(self):
        note_widget = DeskWidget(self.stack_widget.count())

        self.stack_widget_ids.append(note_widget.desk_name)
        note_widget.desk_name.textChanged.connect(self.desk_name_changed)
        note_widget.delete_change_desk_button.connect(self.delete_desk_change_button)
        note_widget.delete_change_desk_button.connect(self.check_desks_count)
        self.stack_widget.addWidget(note_widget)
        self.stack_widget.setCurrentIndex(self.stack_widget.count() - 1)
        note_widget.desk_name.setFocus()

        button = QPushButton('Доска', self)
        button.setStyleSheet('''QPushButton{
                                        background-color:transparent;
                                        border: 1px outset rgb(220, 220, 220);
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }
                                    QPushButton:hover{
                                        background-color:rgb(220, 220, 220);
                                        border: 0px solid;
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }
                                    QPushButton:pressed{
                                        background-color:rgb(200, 200, 200);
                                        border: 0px solid;
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }''')

        self.stack_widget_buttons.append(button)
        button.clicked.connect(
            lambda: self.stack_widget.setCurrentIndex(note_widget.stack_widget_id))
        button.clicked.connect(self.picked_button_show)
        self.verticalLayout.insertWidget(self.verticalLayout.count() - 1, button)

        self.check_desks_count()

    def check_desks_count(self):
        if self.verticalLayout.count() <= MAX_DESK_COUNT and self.create_desk_button.isHidden():
            self.create_desk_button.show()
        elif self.verticalLayout.count() == MAX_DESK_COUNT:
            self.create_desk_button.hide()

    def delete_desk_change_button(self, desk_id):
        self.stack_widget_buttons[desk_id].deleteLater()
        self.stack_widget_buttons.pop(desk_id)
        self.stack_widget.removeWidget(self.stack_widget_ids[desk_id])
        self.stack_widget_ids.pop(desk_id)
        for i in range(self.stack_widget.count()):
            if i > desk_id:
                self.stack_widget.widget(i).stack_widget_id -= 1

    def desk_name_changed(self: ModQLineEdit):
        index = self.stack_widget_ids.index(self.sender())
        if len(self.sender().text().strip()) > MAX_DESK_NAME_LENGTH:
            self.verticalLayout.itemAt(index).widget().setText(
                f'{self.sender().text()[:MAX_DESK_NAME_LENGTH].strip()}...')
        else:
            self.verticalLayout.itemAt(index).widget().setText(self.sender().text().strip())

    def load_desks(self):
        desks = self.db_handler.load_desks()
        for i in desks:
            self.create_loaded_desks(i)
        self.picked_button_show()

    def create_loaded_desks(self, desk_content):
        note_widget = DeskWidget(self.stack_widget.count(), is_new=False, desk_id=desk_content[0],
                                 name=desk_content[1])

        note_widget.enable_create_card_button()
        note_widget.in_database = True
        self.stack_widget_ids.append(note_widget.desk_name)
        note_widget.desk_name.textChanged.connect(self.desk_name_changed)
        note_widget.delete_change_desk_button.connect(self.delete_desk_change_button)
        self.stack_widget.addWidget(note_widget)
        self.stack_widget.setCurrentIndex(self.stack_widget.count() - 1)

        button = QPushButton(f'{desk_content[1]}', self)
        button.setStyleSheet('''QPushButton{
                                        background-color:transparent;
                                        border: 1px outset rgb(220, 220, 220);
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }
                                    QPushButton:hover{
                                        background-color:rgb(220, 220, 220);
                                        border: 0px solid;
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }
                                    QPushButton:pressed{
                                        background-color:rgb(200, 200, 200);
                                        border: 0px solid;
                                        border-radius: 5px;
                                        padding: 5px 10px 5px; 
                                    }''')

        self.stack_widget_buttons.append(button)
        button.clicked.connect(
            lambda: self.stack_widget.setCurrentIndex(note_widget.stack_widget_id))
        self.verticalLayout.insertWidget(self.verticalLayout.count() - 1, button)
        button.clicked.connect(self.picked_button_show)

        index = self.stack_widget_ids.index(note_widget.desk_name)
        if len(note_widget.desk_name.text().strip()) > MAX_DESK_NAME_LENGTH:
            self.verticalLayout.itemAt(index).widget().setText(
                f'{note_widget.desk_name.text()[:MAX_DESK_NAME_LENGTH].strip()}...')


# TODO: Сделать порядочный дизайн

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
