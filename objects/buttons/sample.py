from objects.buttons.button import *

# This is a Sample Button
class SampleButton(Button):
    def __init__(self, parent):
        super().__init__(parent, "Title")
        self.set_tooltip("Tooltip")

    def execute(self):
        try:
            pass
        except Exception as e:
            show_error("Error", f"Error: {str(e)}")