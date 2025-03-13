import subprocess
from winshell import recycle_bin

from objects.lists.list import *

class TrashList(List):
    def __init__(self, parent):
        super().__init__(parent, "Trash")

    def on_item_double_clicked(self, item):
        pass

    def load_contents(self):
        self.list.clear()
        for item in recycle_bin():
            file_info = (
                f"{item.original_filename().split('\\')[-1]}"
            )
            list_item = QListWidgetItem(file_info)
            list_item.setIcon(self.icon_provider.icon(QFileInfo(item.original_filename())))
            self.list.addItem(list_item)
            
        self.list.scrollToTop()

    def toolbar_actions(self):
        clear_action = QAction(QIcon(), "Clear", self)
        clear_action.triggered.connect(lambda: self.clear())
        self.toolbar.addAction(clear_action)

    def clear(self):
        """Clear trash bin"""
        try:
            subprocess.run('PowerShell.exe -NoProfile -Command Clear-RecycleBin -Force', shell=True)
            self.load_contents()
        except Exception as e:
            show_error("Error", f"Error: {str(e)}")
