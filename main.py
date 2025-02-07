import sys
import subprocess
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import qdarkstyle

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop Manager")
        self.setGeometry(300, 300, 400, 400)
        self.setWindowIcon(QIcon("icon.png"))


        btn1 = QPushButton(text="Backup", parent=self)
        btn1.move(10, 10)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton(text="Run", parent=self)
        btn2.move(10, 60)
        btn2.clicked.connect(self.btn2_clicked)

        btn3 = QPushButton(text="Test", parent=self)
        btn3.move(10, 110)
        btn3.clicked.connect(self.btn3_clicked)

        btn4 = QPushButton(text="App", parent=self)
        btn4.move(10, 160)
        btn4.clicked.connect(self.btn4_clicked)

        btn_clear = QPushButton(text="Clear", parent=self)
        btn_clear.move(10, 210)
        btn_clear.clicked.connect(self.btn_clear_clicked)


    def btn1_clicked(self):

        try:
            batch_file_path = "D:/Backup/backup.bat"
            subprocess.run(batch_file_path, shell=True)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"배치 파일 실행 중 오류 발생: {str(e)}")

    def btn2_clicked(self):
        try:
            batch_file_path = "D:/bat/run.bat"
            subprocess.run(batch_file_path, shell=True)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"배치 파일 실행 중 오류 발생: {str(e)}")

    def btn3_clicked(self):
        try:
            url = "https://www.google.com"
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
            subprocess.Popen([chrome_path, "--incognito", url])
        except Exception as e:
            QMessageBox.critical(self, "오류", f"배치 파일 실행 중 오류 발생: {str(e)}")

    def btn4_clicked(self):
        try:
            app_path = "D:/Programming/Microsoft VS Code/Code.exe"
            subprocess.Popen(app_path)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"배치 파일 실행 중 오류 발생: {str(e)}")

    def btn_clear_clicked(self):
        try:
            subprocess.run('PowerShell.exe -NoProfile -Command Clear-RecycleBin -Force', shell=True)
        except Exception as e:
            QMessageBox.critical(self, "오류", f"배치 파일 실행 중 오류 발생: {str(e)}")


app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
window = MyWindow()
window.show()
app.exec()

# https://wikidocs.net/71681
