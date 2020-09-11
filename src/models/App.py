import os
from src.util import parse_directory
from .ParserResults import ParserResults

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject

class App(QObject):
    basedirsUpdate = pyqtSignal(list)
    parserUpdate = pyqtSignal(ParserResults)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.root_dir = None 
        self.sub_dirs = []
        self.parser_results = None
        self.idx = 0

    def refresh_root_dir(self):
        if self.root_dir is None:
            return
        self.sub_dirs = []
        for sub_dir in os.listdir(self.root_dir):
            base_dir = os.path.join(self.root_dir, sub_dir)
            if not os.path.isdir(base_dir):
                continue
            self.sub_dirs.append(sub_dir)
        
        self.basedirsUpdate.emit(self.sub_dirs)
    
    def set_root_dir(self, root_dir):
        self.root_dir = root_dir
        self.refresh_root_dir()
    
    def select_base_dir(self, idx):
        self.idx = idx
        self.update_parser()

    def update_parser(self):
        base_dir = os.path.join(self.root_dir, self.sub_dirs[self.idx])
        try:
            p = parse_directory(base_dir)
        except IOError:
            p = {}
        self.parser_results = ParserResults(p) 
        self.parserUpdate.emit(self.parser_results)