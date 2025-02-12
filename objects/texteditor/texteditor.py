from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class TextEditor(QTextEdit):
    def __init__(self, parent=None):
        self.text_edit = QTextEdit()
        #self.text_edit.setReadOnly(True)
        self.text_edit.setFixedHeight(200)
        self.text_edit.setFixedWidth(200)
        self.text_edit.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")
        self.text_edit.setFont(QFont("Arial", 12))
        self.text_edit.setFontWeight(QFont.Weight.Bold)
        self.text_edit.setFontUnderline(True)
        self.text_edit.setPlaceholderText("Enter your text here")


    def __call__(self):
        return self.text_edit


