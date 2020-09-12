from PyQt5.QtWidgets import\
    QWidget, QTabWidget,\
    QHBoxLayout, QGridLayout,\
    QListWidget

from .RenameView import RenameView

class TVDirectoryView(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.rename_view = RenameView()
        self.conflict_view = RenameView()
        self.delete_view = QListWidget()
        self.ignore_view = QListWidget()
        self.completed_view = QListWidget()

        self.addTab(self.rename_view, "Renames")
        self.addTab(self.conflict_view, "Conflicts")
        self.addTab(self.delete_view, "Deletes")
        self.addTab(self.ignore_view, "Ignores")
        self.addTab(self.completed_view, "Complete")

    def set_directory(self, directory):
        directory.update_parser()
        parser = directory.parser_results

        self.rename_view.set_model(parser.renames)
        self.conflict_view.set_model(parser.conflicts)

        self.ignore_view.clear()
        self.delete_view.clear()
        self.completed_view.clear()
        
        for ignore in parser.ignores:
            self.ignore_view.addItem(ignore)

        for delete in parser.deletes:
            self.delete_view.addItem(delete)
        
        for complete in parser.completed:
            self.completed_view.addItem(complete)

        self.setTabText(0, self.get_tab_text("Renames", len(parser.renames)))
        self.setTabText(1, self.get_tab_text("Conflicts", len(parser.conflicts)))
        self.setTabText(2, self.get_tab_text("Deletes", len(parser.deletes)))
        self.setTabText(3, self.get_tab_text("Ignores", len(parser.ignores)))
        self.setTabText(4, self.get_tab_text("Completed", len(parser.completed)))

    def get_tab_text(self, prefix, n):
        if n == 0:
            return prefix
        return f"{prefix} ({n})"