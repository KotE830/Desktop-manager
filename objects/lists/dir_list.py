from objects.lists.list import *

class DirList(List):
    def __init__(self, parent, current_path):
        super().__init__(parent, current_path)
        self.load_contents()

    def toolbar_actions(self):
        add_action = QAction(QIcon(), "Add", self)
        add_action.triggered.connect(lambda: self.add())
        self.toolbar.addAction(add_action)

    def add(self):
        """Add file to DB and db_list"""
        if not self.list.selectedItems():
            return
        path = os.path.join(self.current_path, self.list.selectedItems()[0].text()).replace("\\", "/")
        self.parent.get_db_list().add_file(path)
