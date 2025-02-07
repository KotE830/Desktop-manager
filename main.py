import sys
import subprocess
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My HTS v1.0")
        self.setGeometry(300, 300, 400, 400)
        self.setWindowIcon(QIcon("pie-chart.png"))

        btn1 = QPushButton(text="Backup", parent=self)
        btn1.move(10, 10)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton(text="Run", parent=self)
        btn2.move(10, 60)
        btn2.clicked.connect(self.btn2_clicked)

        btn3 = QPushButton(text="Test", parent=self)
        btn3.move(10, 110)
        btn3.clicked.connect(self.btn3_clicked)


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


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec()

# https://wikidocs.net/71681
