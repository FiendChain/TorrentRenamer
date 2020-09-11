import os
from src.util import parse_directory
from .ParserResults import ParserResults

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
import json

class App(QObject):
    basedirsUpdate = pyqtSignal(list)
    parserUpdate = pyqtSignal(ParserResults)
    onError = pyqtSignal(str)

    def __init__(self, api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = api

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
    
    def get_sub_dir(self):
        try:
            return self.sub_dirs[self.idx]
        except IndexError:
            return None
    
    def get_base_dir(self):
        subdir = self.get_sub_dir()
        if subdir is None or self.root_dir is None:
            return None
        return os.path.join(self.root_dir, subdir)
        
    def update_series_data(self, data):
        basedir = self.get_base_dir()
        if basedir is None:
            return
        filepath = os.path.join(basedir, "series.json")
        with open(filepath, "w+") as fp:
            json.dump(data, fp, indent=1)

        self.refresh_episodes_data_from_sid(data.get("id"))
    
    def refresh_episodes_data(self):
        basedir = self.get_base_dir()
        if basedir is None:
            return

        try:
            filepath = os.path.join(basedir, "series.json")
            with open(filepath, "r") as fp:
                sdata = json.load(fp)
            sid = sdata.get("id")
            self.refresh_episodes_data_from_sid(sid)
        except IOError:
            self.onError.emit(f"unable to open series.json")
    
    def refresh_episodes_data_from_sid(self, sid):
        basedir = self.get_base_dir()
        if basedir is None:
            return
        data = self.api.get_series_episodes(sid)
        if data is None:
            return
        filepath = os.path.join(basedir, "episodes.json")
        with open(filepath, "w+") as fp:
            json.dump(data, fp, indent=1) 
        self.update_parser()

    def update_parser(self):
        base_dir = self.get_base_dir()
        try:
            p = parse_directory(base_dir)
        except IOError:
            p = {}
        self.parser_results = ParserResults(p) 
        self.parserUpdate.emit(self.parser_results)