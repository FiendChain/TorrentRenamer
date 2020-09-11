from PyQt5.QtWidgets import\
    QWidget, QSplitter, QMainWindow, QTabWidget,\
    QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox

from .DirectoryList import DirectoryList
from .RenameView import RenameView

from .SeriesSelector import SeriesSelector

from src.util import get_series_from_path

# light wrapper for controlling app
class AppControls:
    def __init__(self, app):
        self.app = app

    def refresh(self):
        self.app.refresh_episodes_data()

    def rename(self):
        self.app.rename()
        self.app.cleanup()
        self.app.update_parser()

    def delete_garbage(self):
        self.app.delete_garbage()
        self.app.cleanup()
        self.app.update_parser()

    def cleanup(self):
        self.app.cleanup()
        self.app.update_parser()

    def auto(self):
        self.app.rename()
        self.app.delete_garbage()
        self.app.cleanup()
        self.app.update_parser()

class AppView(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = app
        self.ctl = AppControls(self.app)

        splitter = QSplitter()
        self.dir_list = DirectoryList()
        self.tabbed_view = self.create_tabbed_view()
        splitter.addWidget(self.dir_list)
        splitter.addWidget(self.tabbed_view)
        splitter.addWidget(self.create_right_panel())
        self.setCentralWidget(splitter)

        # connect app
        app.basedirsUpdate.connect(self.dir_list.update_list)
        self.dir_list.indexChanged.connect(app.select_base_dir)
        self.dir_list.onRefresh.connect(app.refresh_root_dir)
        app.parserUpdate.connect(self.on_parser_update)

        app.onError.connect(self.on_error)
        app.onWarning.connect(self.on_warning)

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
    
    def create_right_panel(self):
        group = QWidget()
        layout = QGridLayout()

        search_btn = QPushButton("Select series")
        search_btn.pressed.connect(self.launch_series_popup)

        ctl = self.ctl 

        refresh_episodes = QPushButton("Refresh episodes")
        refresh_episodes.pressed.connect(ctl.refresh)
        rename_btn = QPushButton("Rename")
        rename_btn.pressed.connect(ctl.rename)
        delete_btn = QPushButton("Remove Garbage")
        delete_btn.pressed.connect(ctl.delete_garbage)
        cleanup_btn = QPushButton("Cleanup")
        cleanup_btn.pressed.connect(ctl.cleanup)
        auto_btn = QPushButton("Auto")
        auto_btn.pressed.connect(ctl.auto)

        layout.addWidget(search_btn)
        layout.addWidget(refresh_episodes)
        layout.addWidget(rename_btn)
        layout.addWidget(delete_btn)
        layout.addWidget(cleanup_btn)
        layout.addWidget(auto_btn)

        group.setLayout(layout)

        return group

    def launch_series_popup(self):
        subdir = self.app.get_sub_dir()
        if subdir is None:
            return

        sname = get_series_from_path(subdir)
            
        w = SeriesSelector(self.app.api)
        w.set_search_text(sname)
        w.search()
        data = w.exec_()
        if data is None:
            return
        self.app.update_series_data(data)
    
    def on_error(self, error):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(str(error))
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()
        
    def on_warning(self, warning):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText(str(warning))
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()
    
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