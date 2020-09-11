from PyQt5.QtWidgets import QWidget, QSplitter, QMainWindow, QTabWidget
from PyQt5.QtWidgets import QListWidget

from .DirectoryList import DirectoryList
from .RenameView import RenameView

class AppView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        splitter = QSplitter()

        self.dir_list = DirectoryList()
        self.tabbed_view = self.create_tabbed_view()
        splitter.addWidget(self.dir_list)
        splitter.addWidget(self.tabbed_view)

        self.setCentralWidget(splitter)
    
    def create_tabbed_view(self):
        tab_view = QTabWidget()
        
        self.rename_view = RenameView()
        self.conflict_view = RenameView()
        self.delete_view = QListWidget()
        self.ignore_view = QListWidget()
        self.completed_view = QListWidget()

        tab_view.addTab(self.rename_view, "Renames")
        tab_view.addTab(self.conflict_view, "Conflicts")
        tab_view.addTab(self.delete_view, "Deletes")
        tab_view.addTab(self.ignore_view, "Ignores")
        tab_view.addTab(self.completed_view, "Complete")
       
        return tab_view

    def set_app(self, app):
        self.app = app
        app.basedirsUpdate.connect(self.dir_list.update_list)
        self.dir_list.indexChanged.connect(app.select_base_dir)
        app.parserUpdate.connect(self.on_parser_update)
    
    def on_parser_update(self, parser):
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

        self.tabbed_view.setTabText(0, self.get_tab_text("Renames", len(parser.renames)))
        self.tabbed_view.setTabText(1, self.get_tab_text("Conflicts", len(parser.conflicts)))
        self.tabbed_view.setTabText(2, self.get_tab_text("Deletes", len(parser.deletes)))
        self.tabbed_view.setTabText(3, self.get_tab_text("Ignores", len(parser.ignores)))
        self.tabbed_view.setTabText(4, self.get_tab_text("Completed", len(parser.completed)))
    
    def get_tab_text(self, prefix, n):
        if n == 0:
            return prefix
        return f"{prefix} ({n})"