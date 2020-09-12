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

class RefreshThread(QThread):
    def __init__(self, app):
        super().__init__(parent=app)
        self.app = app
        self.is_hard = False

    def start(self, is_hard, *args, **kwargs):
        self.is_hard = is_hard
        super().start(*args, **kwargs)
    
    def run(self):
        for i, directory in enumerate(self.app.directories):
            try:
                if self.is_hard:
                    directory.refresh_episodes_data()
                directory.update_parser()
                # update directory if selected
                if self.app.idx == i:
                    self.app.onDirectorySelect.emit(self.app.current_directory)
            except AppError as ex:
                self.app.onError.emit(ex.msg)
            except AppWarning as ex:
                self.app.onWarning.emit(ex.msg)

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
        self.directory_lookup = {}
        self.parser_results = None
        self.idx = 0

        self.refresh_thread = RefreshThread(self)

    def refresh_root_dir(self):
        if self.refresh_thread.isRunning():
            self.onWarning.emit("Cannnot scan while refreshing")
            return

        new_directories = []

        for filename in os.listdir(self.root_dir):
            # remove old listeners since garbage collected
            if filename in self.directory_lookup:
                directory = self.directory_lookup[filename]
                try:
                    directory.statusChanged.disconnect()
                except:
                    pass
                new_directories.append(directory)
                continue
            # add new directory
            filepath = os.path.join(self.root_dir, filename)
            if not os.path.isdir(filepath):
                continue
            directory = TVDirectory(filepath, self.api)
            new_directories.append(directory)
            self.directory_lookup[filename] = directory
        # so that we get correct order
        self.directories = new_directories
        self.directoriesUpdate.emit(self.directories)
    
    def set_root_dir(self, root_dir):
        self.root_dir = root_dir
        self.directories = []
        self.directory_lookup = {}
        self.refresh_root_dir()
    
    def select_base_dir(self, idx):
        self.idx = idx

        if not self.refresh_thread.isRunning(): 
            self.current_directory.update_parser()
        self.onDirectorySelect.emit(self.current_directory)
    
    @property
    def current_directory(self):
        return self.directories[self.idx]
    
    def update_series_data(self, data):
        self.current_directory.update_series_data(data)
    
    def soft_refresh_directories(self):
        if self.refresh_thread.isRunning():
            return
        self.refresh_thread.start(False)
    
    def hard_refresh_directories(self):
        if self.refresh_thread.isRunning():
            return
        self.refresh_thread.start(True)

    @catch_errors
    def dir_rescan(self):
        self.current_directory.update_parser()
        self.onDirectorySelect.emit(self.current_directory)
            
    @catch_errors
    def dir_refresh(self):
        self.current_directory.refresh_episodes_data()
        self.current_directory.update_parser()
        self.onDirectorySelect.emit(self.current_directory)

    @catch_errors
    def dir_rename(self):
        self.current_directory.rename()
        self.current_directory.cleanup()
        self.current_directory.update_parser()
        self.onDirectorySelect.emit(self.current_directory)

    @catch_errors
    def dir_delete_garbage(self):
        self.current_directory.delete_garbage()
        self.current_directory.cleanup()
        self.current_directory.update_parser()
        self.onDirectorySelect.emit(self.current_directory)

    @catch_errors
    def dir_cleanup(self):
        self.current_directory.cleanup()
        self.current_directory.update_parser()
        self.onDirectorySelect.emit(self.current_directory)

    @catch_errors
    def dir_auto(self):
        self.current_directory.rename()
        self.current_directory.delete_garbage()
        self.current_directory.cleanup()
        self.current_directory.update_parser()
        self.onDirectorySelect.emit(self.current_directory)


