import subprocess
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import pyqtSlot
from database.database import Database

# parent class for all buttons
class Button:
    def __init__(self, parent, title="Button"):
        self.btn = QPushButton(title, parent)
        self.btn.clicked.connect(lambda: self.btn_clicked())
        self.db = Database()


    # click event : open www.google.com with secret mode
    @pyqtSlot()
    def btn_clicked(self):
        try:
            url = "https://www.google.com"
            path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
            subprocess.Popen([path, "--incognito", url])
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error: {str(e)}")


    def __call__(self):
        return self.btn