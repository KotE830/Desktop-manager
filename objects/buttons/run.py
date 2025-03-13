from objects.buttons.button import *

class RunButton(Button):
    def __init__(self, parent):
        super().__init__(parent, "Run")
        self.set_id(IDS['RUN'])
        self.set_tooltip("Trading Start <b>Button</b>")