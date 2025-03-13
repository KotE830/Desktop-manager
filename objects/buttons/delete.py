from objects.buttons.button import *

class DeleteButton(Button):
    def __init__(self, parent):
        super().__init__(parent, "Delete")
        self.set_tooltip("Delete button")

    @pyqtSlot()
    def btn_clicked(self):
        try:
            self.delete_mode = not self.delete_mode
            
            for i in range(self.layout.count()):
                widget = self.layout.itemAt(i).widget()
                if widget and isinstance(widget, QPushButton):
                    if self.delete_mode:
                        widget.setStyleSheet(f"background-color: {COLORS['BUTTON']['DELETE_HOVER']};")
                    else:
                        widget.setStyleSheet(f"background-color: {COLORS['BUTTON']['DEFAULT']};")
                        
        except Exception as e:
            show_error("Error", f"Error: {str(e)}")