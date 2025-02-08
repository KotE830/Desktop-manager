from buttons.button import *

class ClearButton(Button):
    def __init__(self, parent, title="Button"):
        super().__init__(parent, title)



    @pyqtSlot()
    def btn_clicked(self):
        try:
            subprocess.run('PowerShell.exe -NoProfile -Command Clear-RecycleBin -Force', shell=True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")