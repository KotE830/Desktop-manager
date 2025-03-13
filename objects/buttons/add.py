from objects.buttons.button import *

class AddButton(Button):
    def __init__(self, parent):
        super().__init__(parent, "Add")
        self.set_tooltip("Create new button")

    @pyqtSlot()
    def btn_clicked(self):
        try:
            title, ok = QInputDialog.getText(self.parent, "Create new button", "Input button name:")

            if not ok:
                return
            
            if title:
                new_btn = Button(self.parent, title)
            else:
                new_btn = Button(self.parent)
            
            self.layout.addWidget(new_btn())
            self.db.add_button(new_btn)
            self.db_list.load_contents()

        except Exception as e:
            show_error("Error", f"Error: {str(e)}")