from PyQt6.QtCore import Qt

from objects.lists.list import *

class DBList(List):
    def __init__(self, parent):
        self.current_button_id = None
        self.delete_mode = False

        super().__init__(parent)

    def on_item_clicked(self, item):
        if item.text() == "..":
            self.current_button_id = None
        else:
            self.current_button_id = item.data(Qt.UserRole)
        
        self.toolbar_actions()

    def on_item_double_clicked(self, item):
        # Move to parent directory
        if item.text() == "..":
            self.current_button_id = None
            self.current_path = None

        # Execute file / URL
        elif self.current_button_id and self.current_path:
            file_path = item.data(Qt.UserRole + 1)
            if is_url(file_path):
                open_url(file_path)
            else:
                open_file(file_path)
            return

        # Display button's file/url list
        else:
            self.current_path = item.text()
            
        self.load_contents()

    def load_contents(self):
        self.list.clear()
        try:
            # Display buttons
            if self.current_button_id is None:
                # Run button
                self.delete_mode = False
                btn_run = self.parent.btn_run
                list_item = QListWidgetItem(btn_run.get_title())
                list_item.setData(Qt.UserRole, btn_run.get_id())
                self.list.addItem(list_item)
                
                # Other buttons in DB
                buttons = self.db.get_buttons()
                for button in buttons:
                    list_item = QListWidgetItem(button.get_title())
                    list_item.setData(Qt.UserRole, button.get_id())
                    self.list.addItem(list_item)

            # Display file/url list
            else:
                # Add back item
                back_item = QListWidgetItem("..")
                self.list.addItem(back_item)
                
                # Selected button's files/urls
                files = self.db.get_files(self.current_button_id)
                urls = self.db.get_urls(self.current_button_id)
                
                for file in files:
                    if os.path.exists(file['file_path']):
                        list_item = QListWidgetItem(file['file_name'])
                        list_item.setData(Qt.UserRole, file['id'])
                        list_item.setData(Qt.UserRole + 1, file['file_path'])
                        list_item.setIcon(self.icon_provider.icon(QFileInfo(file['file_path'])))
                        self.list.addItem(list_item)
                    else:   # Remove file if it doesn't exist
                        self.db.delete_file(file['id'])
                
                for url in urls:
                    list_item = QListWidgetItem(url['name'])
                    list_item.setData(Qt.UserRole, url['id'])
                    list_item.setData(Qt.UserRole + 1, url['url'])
                    list_item.setIcon(self.icon_provider.icon(QFileInfo(PATHS['CHROME'])))
                    self.list.addItem(list_item)
            
            self.list.scrollToTop()
            self.set_label(self.current_path if self.current_path else "Buttons")
            self.toolbar_actions()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load contents: {str(e)}")

    def toolbar_actions(self):
        self.toolbar.clear()

        run_action = QAction(QIcon(), "Run", self)
        run_action.triggered.connect(lambda: self.run())
        self.toolbar.addAction(run_action)

        if self.current_button_id is not None:
            add_action = QAction(QIcon(), "Add", self)
            add_action.triggered.connect(lambda: self.add())
            self.toolbar.addAction(add_action)

            # Show Delete when item is selected, not button
            if self.current_path:
                delete_action = QAction(QIcon(), "Delete", self)
                delete_action.triggered.connect(lambda: self.delete())
                self.toolbar.addAction(delete_action)

            # Show Edit when URL is selected 
            current_item = self.list.currentItem()
            if current_item and current_item.text() != "..":
                item_path = current_item.data(Qt.UserRole + 1)
                if item_path and is_url(item_path):
                    edit_action = QAction(QIcon(), "Edit", self)
                    edit_action.triggered.connect(lambda: self.edit())
                    self.toolbar.addAction(edit_action)

    def run(self):
        """Run the button"""
        self.db.execute_button(self.current_button_id)

    def add(self):
        """Add URL to DB"""
        try:
            dialog, name_input, url_input = self.create_url_dialog()
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                name = name_input.text().strip()
                url = url_input.text().strip()
                
                if url and name:
                    if is_url(url):
                        self.db.add_url(self.current_button_id, name, url)
                        self.load_contents()
                    else:
                        show_error("Warning", "Invalid URL format.\nURL must start with 'http://' or 'https://'")
                else:
                    show_error("Warning", "Please enter both URL and name.")
            
        except Exception as e:
            show_error("Error", f"Failed to add URL: {str(e)}")

    def create_url_dialog(self):
        """Create a dialog to input name and URL and return it."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add URL")
        layout = QVBoxLayout()

        # Name input field
        name_label = QLabel("Name:")
        name_input = QLineEdit()
        layout.addWidget(name_label)
        layout.addWidget(name_input)

        # URL input field
        url_label = QLabel("URL:")
        url_input = QLineEdit()
        layout.addWidget(url_label)
        layout.addWidget(url_input)

        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        return dialog, name_input, url_input

    def delete(self):
        """Delete mode on/off"""
        self.delete_mode = not self.delete_mode
        
        # Click event handler
        click_handler = self.item_delete if self.delete_mode else self.on_item_clicked
        self.list.itemClicked.disconnect()
        self.list.itemClicked.connect(click_handler)
        
        # Change colors
        new_color = COLORS['LIST']['DELETE'] if self.delete_mode else COLORS['LIST']['DEFAULT']
        new_hover_color = COLORS['LIST']['DELETE_HOVER'] if self.delete_mode else COLORS['LIST']['HOVER']
        self.set_style(new_color, new_color, new_hover_color)

    def item_delete(self, item):
        """Delete item"""
        id = item.data(Qt.UserRole)
        path = item.data(Qt.UserRole + 1)
        if is_url(path):
            self.db.delete_url(id)
        else:
            self.db.delete_file(id)
        self.load_contents()

    def edit(self):
        """Edit URL"""
        try:
            item = self.list.currentItem()
            if not item:
                return
                
            # Get current item's name and URL
            current_name = item.text()
            current_url = item.data(Qt.UserRole + 1)
            id = item.data(Qt.UserRole)

            # URL edit dialog
            dialog, name_input, url_input = self.create_url_dialog()
            name_input.setText(current_name)
            url_input.setText(current_url)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                name = name_input.text().strip()
                url = url_input.text().strip()
                
                # Update URL
                if url and name:
                    if url.startswith(('http://', 'https://')):
                        self.db.update_url(id, name, url)
                        item.setText(name)
                        item.setData(Qt.UserRole + 1, url)
                    else:
                        QMessageBox.warning(self, "Warning", "Invalid URL format.\nURL must start with 'http://' or 'https://'")
                else:
                    QMessageBox.warning(self, "Warning", "Please enter both URL and name.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to edit URL: {str(e)}")

    def add_file(self, path):
        """Add file from dir_list to DB"""
        if self.current_button_id:
            self.db.add_file(self.current_button_id, path)
            self.load_contents()
        else:
            QMessageBox.warning(self, "Warning", "Please select a button to add the file.")
