import subprocess
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import pyqtSlot

# parent class for all buttons
class Button:
    def __init__(self, parent, title="Button"):
        self.btn = QPushButton(title, parent)
        self.btn.clicked.connect(lambda: self.btn_clicked())


    # click event : open www.google.com with secret mode
    @pyqtSlot()
    def btn_clicked(self):
        try:
            url = "https://www.google.com"
            path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
            subprocess.Popen([path, "--incognito", url])
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error: {str(e)}")
    
    # move button to x, y
    def move(self, x, y):
        self.btn.move(x, y)