import os
import subprocess
from urllib.parse import urlparse

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox

from config import PATHS

def open_file(path: str) -> None:
    try:
        if path.lower().endswith(('.txt', '.py', '.md', '.json')):
            # Text file
            subprocess.Popen(['notepad.exe', path])
        elif path.lower().endswith('.bat'):
            # Batch file
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            subprocess.Popen([path], shell=False, startupinfo=startupinfo)
        else:
            # Other files
            os.startfile(path)
    except Exception as e:
        show_error("Error", f"Failed to open file: {str(e)}")

def open_url(url: str) -> None:
    try:
        subprocess.Popen([PATHS["CHROME"], "--incognito", url])
    except Exception as e:
        show_error("Error", f"Failed to open URL: {str(e)}")
    
def open_urls(urls: list) -> None:
    """Open all URLs in a new window"""
    chrome_command = [
        PATHS["CHROME"],
        "--new-window",
        "--incognito"
    ]
    chrome_command.extend(urls)
    subprocess.Popen(chrome_command)

def is_url(text: str) -> bool:
    try:
        result = urlparse(text)
        return all([result.scheme in ['http', 'https']])
    except:
        return False
    
def show_error(title: str, message: str) -> None:
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Icon.Critical)
    dialog.setWindowTitle(title)
    dialog.setText(message)
    
    icon = QIcon(os.path.join(PATHS['ROOT'], PATHS['ICON']))
    dialog.setWindowIcon(icon)
    
    dialog.exec()
