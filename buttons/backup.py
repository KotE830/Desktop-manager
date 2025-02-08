from buttons.button import *

class BackupButton(Button):
    def __init__(self, parent, title="Button"):
        super().__init__(parent, title)


    @pyqtSlot()
    def btn_clicked(self):
        try:
            path = "D:/Backup/backup.bat"
            subprocess.run(path, shell=True)
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error: {str(e)}")