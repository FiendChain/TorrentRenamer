from PyQt5.QtWidgets import QWidget, QSplitter, QMainWindow, QTabWidget
from PyQt5.QtWidgets import QListWidget

from .DirectoryList import DirectoryList
from .RenameView import RenameView

class AppView(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        splitter = QSplitter()

        self.dir_list = DirectoryList()
        central_panel = self.create_central_panel()
        splitter.addWidget(self.dir_list)
        splitter.addWidget(central_panel)

        self.setCentralWidget(splitter)
    
    def create_central_panel(self):
        tab_view = QTabWidget()
        
        self.rename_view = RenameView()
        self.conflict_view = QListWidget()
        self.ignore_view = QListWidget()

        tab_view.addTab(self.rename_view, "Renames")
        tab_view.addTab(self.conflict_view, "Conflicts")
        tab_view.addTab(self.ignore_view, "Ignores")
       
        return tab_view

    def set_app(self, app):
        self.app = app
        app.basedirsUpdate.connect(self.dir_list.update_list)
        self.dir_list.indexChanged.connect(app.select_base_dir)
        app.parserUpdate.connect(self.on_parser_update)
    
    def on_parser_update(self, parser):
        renames = parser.renames
        self.rename_view.set_model(renames)

        self.conflict_view.clear()
        self.ignore_view.clear()

        for conflict in parser.conflicts:
            self.conflict_view.addItem(conflict)
        
        for ignore in parser.ignores:
            self.ignore_view.addItem(ignore)