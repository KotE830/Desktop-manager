import os

from PyQt6.QtCore import QFileInfo
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from config import *
from utils import *

class List(QWidget):
    def __init__(self, parent, current_path = None):
        super().__init__()

        # UI components
        self.layout = QVBoxLayout(self)
        self.label_layout = QHBoxLayout()
        self.path = QLabel()
        self.list = QListWidget()
        self.toolbar = QToolBar()

        # Properties
        self.current_path = current_path
        self.icon_provider = QFileIconProvider()

        # Parent, db
        self.parent = parent
        self.db = self.parent.db
        
        self.initialize()
        
    def initialize(self):
        self.set_display()
        
        self.list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.list.itemClicked.connect(self.on_item_clicked)
        self.list.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        self.set_toolbar()

    def set_display(self):
        self.path.setText(self.current_path)
        self.label_layout.addWidget(self.path)
        self.layout.addLayout(self.label_layout)
        self.layout.addWidget(self.list)
        
        self.set_style(COLORS['LIST']['DEFAULT'], COLORS['LIST']['SELECTED'], COLORS['LIST']['HOVER'])

    def set_style(self, default_color, selected_color, hover_color):
        # Path label
        self.path.setStyleSheet("""
            QLabel {
                font-family: '맑은 고딕';
                font-size: 14px;
            }
        """)

        # List
        self.list.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['LIST']['DEFAULT']};
                color: white;
                border: none;
                border-radius: 10px;                    
                font-family: '맑은 고딕';
                font-size: 12px;
                padding: 3px;
            }}
            QListWidget::item {{
                background-color: {default_color};
                border-radius: 3px;
                padding: 3px;
            }}
            QListWidget::item:selected {{
                background-color: {selected_color};
                border: 1px solid #666666;
            }}
            QListWidget::item:hover {{
                background-color: {hover_color};
                border: 1px solid #555555;
            }}
            QListWidget::item:selected:hover {{
                background-color: {selected_color};
                border: 1px solid #777777;
            }}
            QListWidget::item[text=".."] {{
                background: transparent;
            }}
        """)

    def on_item_clicked(self, item):
        pass

    def on_item_double_clicked(self, item):
        file_name = item.text()
        
        # Move to parent directory
        if file_name == "..":
            parent_path = os.path.dirname(self.current_path).replace('\\', '/')
            self.current_path = parent_path
            self.load_contents()
            self.set_label(parent_path)
            return

        # Handle double clicked item here
        try:
            full_path = os.path.join(self.current_path, file_name).replace("\\", "/")
            if os.path.isdir(full_path):
                # Directory
                self.current_path = full_path
                self.load_contents()
                
            else:   # File
                open_file(full_path)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")
            
    def set_toolbar(self):
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background: %s;
                border: none;
                padding: 4px;
                spacing: 4px;
                margin: 0;
            }
        """ % COLORS['LIST']['DEFAULT'])
        self.toolbar_actions()
        self.layout.addWidget(self.toolbar)

    def load_contents(self):
        self.list.clear()
        if self.current_path:
            try:
                # Add back item
                parent_path = os.path.dirname(self.current_path).replace('\\', '/')
                if parent_path and parent_path != self.current_path:
                    parent_item = QListWidgetItem("..")
                    parent_item.setIcon(self.get_icon(parent_path))
                    self.list.addItem(parent_item)

                # Get all items in directory
                items = os.listdir(self.current_path)
                
                for item in items:
                    # Get full path
                    full_path = os.path.join(self.current_path, item)
                    
                    list_item = QListWidgetItem(item)
                    list_item.setIcon(self.icon_provider.icon(QFileInfo(full_path)))
                    self.list.addItem(list_item)
                
                self.list.scrollToTop()
                self.set_label(self.current_path)
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load folder contents: {str(e)}")
    
    def toolbar_actions(self):
        pass

    def get_icon(self, path):
        return self.icon_provider.icon(QFileInfo(path))

    def set_label(self, path):
        # Set path label
        self.path.setText(path)

    def get_current_path(self):
        return self.current_path

    def __call__(self):
        return self.layout
