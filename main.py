import os
import sys

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import qdarkstyle

from config import *
from database import Database
from objects import *
from utils import show_error

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(TITLE)
        self.setGeometry(300, 300, 400, 400)
        
        # Icon path
        icon_path = os.path.join(PATHS['ROOT'], PATHS['ICON'])
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)
        
        self.delete_mode = False    # button delete mode
        self.db = Database(self)
        self.display_window()
        
    def display_window(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Top area (left-right split)
        top_widget = QWidget()
        top_layout = QHBoxLayout()
        top_widget.setLayout(top_layout)
        main_layout.addWidget(top_widget)

        # Top-Left area (button section)
        left_widget = QWidget()
        self.left_layout = QVBoxLayout()
        left_widget.setLayout(self.left_layout)
        top_layout.addWidget(left_widget, 4)

        # Top-Right area (text editor section)
        right_tabs = QTabWidget()
        self.C_list = DirList(self, PATHS['C'])
        tab1 = QWidget()
        tab1.setLayout(self.C_list())
        self.D_list = DirList(self, PATHS['D'])
        tab2 = QWidget()
        tab2.setLayout(self.D_list())
        self.db_list = DBList(self)
        tab3 = QWidget()
        tab3.setLayout(self.db_list())
        self.trash_list = TrashList(self)
        tab4 = QWidget()
        tab4.setLayout(self.trash_list())
        
        right_tabs.addTab(tab1, " C ")
        right_tabs.addTab(tab2, " D ")
        right_tabs.addTab(tab3, " DB ")
        right_tabs.addTab(tab4, " Trash ")

        right_tabs.currentChanged.connect(self.on_tab_changed)

        top_layout.addWidget(right_tabs, 6)

        # Bottom area (button section)
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout()
        bottom_widget.setFixedHeight(50)
        bottom_widget.setLayout(bottom_layout)
        main_layout.addWidget(bottom_widget)

        # Bottom left layout
        bottom_left_layout = QHBoxLayout()
        bottom_left_widget = QWidget()
        bottom_left_widget.setFixedHeight(40)
        bottom_left_widget.setLayout(bottom_left_layout)
        bottom_layout.addWidget(bottom_left_widget, 4)

        # Bottom right layout
        bottom_right_layout = QHBoxLayout()
        bottom_right_widget = QWidget()
        bottom_right_widget.setFixedHeight(40)
        bottom_right_widget.setLayout(bottom_right_layout)
        bottom_layout.addWidget(bottom_right_widget, 6)

        # Add widgets to each section
        # Left buttons
        for btn in self.db.get_buttons():
            self.left_layout.addWidget(btn())

        # Bottom buttons
        btn_add = AddButton(self)
        btn_delete = DeleteButton(self)
        self.btn_run = RunButton(self)
        self.btn_shutdown = ShutdownButton(self)
        
        # Add buttons to layouts
        bottom_left_layout.addWidget(btn_add(), 1)
        bottom_left_layout.addWidget(btn_delete(), 1)
        bottom_right_layout.addWidget(self.btn_shutdown(), 1)
        bottom_right_layout.addWidget(self.btn_run(), 2)

        # Remove layout margins
        bottom_left_layout.setContentsMargins(0, 0, 0, 0)
        bottom_right_layout.setContentsMargins(0, 0, 0, 0)

    def on_tab_changed(self, index):
        if index == 0:
            self.C_list.load_contents()
        elif index == 1:
            self.D_list.load_contents()
        elif index == 2:
            self.db_list.load_contents()
        elif index == 3:
            self.trash_list.load_contents()

    def closeEvent(self, event):
        try:
            self.db.close()
            
        except Exception as e:
            show_error(
                'Error',
                f'An error occurred while closing the program: {str(e)}'
            )

        # call parent closeEvent
        super().closeEvent(event)

    def get_db(self):
        return self.db
    
    def get_db_list(self):
        return self.db_list

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
    window = MyWindow()
    window.show()
    app.exec()
