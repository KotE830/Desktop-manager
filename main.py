import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import qdarkstyle
from objects import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Manager")
        self.setGeometry(300, 300, 400, 400)
        self.setWindowIcon(QIcon("icon.png"))
        
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
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        top_layout.addWidget(left_widget, 4)

        # Top-Right area (text editor section)
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        top_layout.addWidget(right_widget, 6)

        # Bottom area (button section)
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout()
        bottom_widget.setFixedHeight(50)
        bottom_widget.setLayout(bottom_layout)
        main_layout.addWidget(bottom_widget)


        # Add widgets to each section
        # Left buttons
        btn_backup = BackupButton(self, "Backup")
        btn_test = Button(self)
        btn_test1 = Button(self)

        left_layout.addWidget(btn_backup())
        left_layout.addWidget(btn_test())
        left_layout.addWidget(btn_test1())

        # Right text editor
        text_edit = TextEditor()
        btn_save = SaveButton(self, "Save")
        right_layout.addWidget(text_edit())
        right_layout.addWidget(btn_save())

        # Bottom buttons
        btn_clear = ClearButton(self, "Clear")
        btn_run = RunButton(self, "Run")

        bottom_layout.addWidget(btn_clear())
        bottom_layout.addWidget(btn_run())


        

        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        left_layout.setSpacing(5)
        bottom_layout.setSpacing(5)

        





if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
    window = MyWindow()
    window.show()
    app.exec()


# https://wikidocs.net/71681
