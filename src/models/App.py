import os
from .TVDirectory import TVDirectory
from .Errors import AppError, AppWarning


from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread
import json

def catch_errors(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except AppError as ex:
            self.onError.emit(ex.msg)
        except AppWarning as ex:
            self.onError.emit(ex.msg)
    return wrapper 

class HardRefreshThread(QThread):
    def __init__(self, app):
        super().__init__(parent=app)
        self.app = app
    
    def run(self):
        self.app.refresh_root_dir()
        for directory in self.app.directories:
            directory.update_parser()

class App(QObject):
    directoriesUpdate = pyqtSignal(list)
    onDirectorySelect = pyqtSignal(TVDirectory)
    onError = pyqtSignal(str)
    onWarning = pyqtSignal(str)

    def __init__(self, api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = api

        self.root_dir = None 
        self.directories = []
        self.parser_results = None
        self.idx = 0

        self.hard_refresh_thread = HardRefreshThread(self)

    def refresh_root_dir(self):
        if self.root_dir is None:
            return

        self.directories = []
        for filename in os.listdir(self.root_dir):
            filepath = os.path.join(self.root_dir, filename)
            if not os.path.isdir(filepath):
                continue
            directory = TVDirectory(filepath, self.api)
            self.directories.append(directory)
        self.directoriesUpdate.emit(self.directories)
    
    def set_root_dir(self, root_dir):
        self.root_dir = root_dir
        self.refresh_root_dir()
    
    def select_base_dir(self, idx):
        self.idx = idx
        self.onDirectorySelect.emit(self.current_directory)
    
    @property
    def current_directory(self):
        return self.directories[self.idx]
    
    def update_series_data(self, data):
        self.current_directory.update_series_data(data)
    
    def soft_refresh_directories(self):
        pass
        # self.refresh_root_dir(p)
        # for directory in self.directories:
        #     directory.update_parser()
    
    def hard_refresh_directories(self):
        if self.hard_refresh_thread.isRunning():
            return
        self.hard_refresh_thread.start()
        
        
            
    @catch_errors
    def dir_refresh(self):
        self.current_directory.refresh_episodes_data()
        self.current_directory.update_parser()

    @catch_errors
    def dir_rename(self):
        self.current_directory.rename()
        self.current_directory.cleanup()
        self.current_directory.update_parser()

    @catch_errors
    def dir_delete_garbage(self):
        self.current_directory.delete_garbage()
        self.current_directory.cleanup()
        self.current_directory.update_parser()

    @catch_errors
    def dir_cleanup(self):
        self.current_directory.cleanup()
        self.current_directory.update_parser()

    @catch_errors
    def dir_auto(self):
        self.current_directory.rename()
        self.current_directory.delete_garbage()
        self.current_directory.cleanup()
        self.current_directory.update_parser()


