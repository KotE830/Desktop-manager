from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from config import *
from utils import show_error

# Parent class for all buttons
class Button:
    def __init__(self, parent, title="Button"):
        self.title = title
        self.id = None
        self.parent = parent
        self.layout = self.parent.left_layout
        self.db = self.parent.get_db()
        self.db_list = self.parent.get_db_list()
        self.delete_mode = self.parent.delete_mode
        
        self.btn = QPushButton(self.title, self.parent)
        self.btn.clicked.connect(lambda: self.btn_clicked())
        self.btn.enterEvent = self.btn_enter
        self.btn.leaveEvent = self.btn_leave

    @pyqtSlot()
    def btn_clicked(self):
        if self.delete_mode:
            self.delete()
        else:
            self.execute()

    def delete(self):
        """Delete itself except fixed buttons"""
        if self.__class__.__name__ not in FIXED_BUTTONS:
            self.layout.removeWidget(self.btn)
            self.db.delete_button(self)
            self.btn.deleteLater()
            self.db_list.load_contents()

    def execute(self):
        """Open files and URLs for button_id"""
        self.db.execute_button(self.id)

    def btn_enter(self, event):
        if self.__class__.__name__ not in FIXED_BUTTONS and self.parent.delete_mode:
            self.btn.setStyleSheet(f"background-color: {COLORS['BUTTON']['DELETE']};")
        else:
            self.btn.setStyleSheet(f"background-color: {COLORS['BUTTON']['HOVER']};")

    def btn_leave(self, event):
        if self.__class__.__name__ not in FIXED_BUTTONS and self.parent.delete_mode:
            self.btn.setStyleSheet(f"background-color: {COLORS['BUTTON']['DELETE_HOVER']};")
        else:
            self.btn.setStyleSheet(f"background-color: {COLORS['BUTTON']['DEFAULT']};")

    def get_title(self):
        return self.title
    
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id

    def set_tooltip(self, tooltip):
        self.btn.setToolTip(tooltip)

    def __call__(self):
        return self.btn