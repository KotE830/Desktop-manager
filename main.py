import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import qdarkstyle
from buttons import button, clear, backup, run


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Manager")
        self.setGeometry(300, 300, 400, 400)
        self.setWindowIcon(QIcon("icon.png"))
        print(self)

        btn_backup = backup.BackupButton(self, "Backup")
        btn_run = run.RunButton(self, "Run")
        btn_test = button.Button(self)
        btn_clear = clear.ClearButton(self, "Clear")

        btn_backup.move(10, 10)
        btn_run.move(10, 60)
        btn_test.move(10, 110)
        btn_clear.move(10, 160)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
    window = MyWindow()
    window.show()
    app.exec()


# https://wikidocs.net/71681
