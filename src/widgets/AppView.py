from PyQt5.QtWidgets import\
    QWidget, QSplitter, QMainWindow, QTabWidget,\
    QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox

from .DirectoryList import DirectoryList
from .TVDirectoryView import TVDirectoryView
from .SeriesSelector import SeriesSelector

from src.util import get_series_from_path

class AppView(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = app

        splitter = QSplitter()
        self.dir_list = DirectoryList()
        self.dir_view = TVDirectoryView()
        splitter.addWidget(self.dir_list)
        splitter.addWidget(self.dir_view)
        splitter.addWidget(self.create_right_panel())
        self.setCentralWidget(splitter)

        # connect app
        app.directoriesUpdate.connect(self.dir_list.update_directories)
        self.dir_list.indexChanged.connect(app.select_base_dir)
        self.dir_list.onRefresh.connect(app.refresh_root_dir)
        app.onDirectorySelect.connect(self.dir_view.set_directory)

        app.onError.connect(self.on_error)
        app.onWarning.connect(self.on_warning)
    
    def create_right_panel(self):
        group = QWidget()
        layout = QGridLayout()

        search_btn = QPushButton("Select series")
        search_btn.pressed.connect(self.launch_series_popup)

        refresh_episodes = QPushButton("Refresh episodes")
        refresh_episodes.pressed.connect(self.app.refresh)
        rename_btn = QPushButton("Rename")
        rename_btn.pressed.connect(self.app.rename)
        delete_btn = QPushButton("Remove Garbage")
        delete_btn.pressed.connect(self.app.delete_garbage)
        cleanup_btn = QPushButton("Cleanup")
        cleanup_btn.pressed.connect(self.app.cleanup)
        auto_btn = QPushButton("Auto")
        auto_btn.pressed.connect(self.app.auto)

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
    