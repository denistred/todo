from PyQt5.QtWidgets import QLineEdit, QMessageBox


class ModQLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

    def focusOutEvent(self, event) -> None:
        if not self.text():
            msg = QMessageBox()
            msg.setStyleSheet('border: 1px; background-color: #ffffff')
            msg.critical(self, 'Ошибка', 'Введите название доски', QMessageBox.Ok)
            self.setFocus()
        super().focusOutEvent(event)
