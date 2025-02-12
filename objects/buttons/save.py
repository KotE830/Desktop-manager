from objects.buttons.button import *

class SaveButton(Button):
    def __init__(self, parent, title="Button"):
        super().__init__(parent, title)


    @pyqtSlot()
    def btn_clicked(self):
        try:
            file_path = self.db.get_file_path()
            if file_path:
                url = "https://www.google.com"
                path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
                subprocess.Popen([path, "--incognito", url])
        except Exception as e:
            QMessageBox.critical(self.parent, "Error", f"Error: {str(e)}")