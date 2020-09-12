import json
import os
import logging
from src.util import parse_directory, clean

from .ParserResults import ParserResults
from PyQt5.QtCore import pyqtSignal, QObject
from .Errors import AppError, AppWarning

class TVDirectoryStatus:
    SUCCESS = 1
    WARNING = 2
    ERROR = 3
    UNKNOWN = 4

class TVDirectory(QObject):
    statusChanged = pyqtSignal(int)

    def __init__(self, fullpath, api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.isdir(fullpath):
            raise IOError(f"{fullpath} is not a directory")
        self.fullpath = fullpath
        self.rootdir = os.path.dirname(fullpath)
        self.basedir = os.path.basename(fullpath)

        self.api = api

        self._status = TVDirectoryStatus.UNKNOWN
        self.parser_data = {}
        self.parser_results = ParserResults(self.parser_data)
        # self.update_parser()
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, new_status):
        self._status = new_status
        self.statusChanged.emit(self._status)
    
    def update_series_data(self, data):
        filepath = os.path.join(self.fullpath, "series.json")
        with open(filepath, "w+") as fp:
            json.dump(data, fp, indent=1)
        sid = data.get("id")
        self.refresh_episodes_data_from_sid(sid)
    
    def refresh_episodes_data(self):
        try:
            filepath = os.path.join(self.fullpath, "series.json")
            with open(filepath, "r") as fp:
                sdata = json.load(fp)
            sid = sdata.get("id")
            self.refresh_episodes_data_from_sid(sid)
        except IOError:
            raise AppError(f"unable to open series.json")
    
    def refresh_episodes_data_from_sid(self, sid):
        data = self.api.get_series_episodes(sid)
        if data is None:
            return False
        try:
            filepath = os.path.join(self.fullpath, "episodes.json")
            with open(filepath, "w+") as fp:
                json.dump(data, fp, indent=1) 
            return True
        except IOError:
            raise AppError(f"unable to open episodes.json")

    def rename(self):
        if self.parser_results is None:
            raise AppWarning(f"missing metadata")

        for entry in self.parser_results.renames:
            if not entry.enabled:
                continue
            old_path = os.path.join(self.fullpath, entry.old_path)
            new_path = os.path.join(self.fullpath, entry.new_path)

            os.rename(old_path, new_path)
            logging.info(f"[RENAME] {old_path} => {new_path}")
        return True
    
    def delete_garbage(self):
        if self.parser_results is None:
            raise AppWarning(f"missing metadata")

        for path in self.parser_results.deletes:
            filepath = os.path.join(self.fullpath, path) 
            os.remove(filepath)
            logging.info(f"[DELETE] {filepath}")
        return True
    
    def cleanup(self):
        def callback(directory):
            logging.info(f"[CLEAN] {directory}")
        clean(self.fullpath, debug=callback)
        return True

    def update_parser(self):
        try:
            self.parser_data = parse_directory(self.fullpath)
        except IOError:
            self.parser_data = {}
            
        self.parser_results = ParserResults(self.parser_data) 
        self.refresh_status()

    def refresh_status(self):
        nb_renames = len(self.parser_results.renames)
        nb_conflicts = len(self.parser_results.conflicts)
        nb_deletes = len(self.parser_results.deletes)

        nb_completed = len(self.parser_results.completed)

        nb_await = nb_renames+nb_conflicts+nb_deletes
        if nb_await == 0 and nb_completed > 0:
            self.status = TVDirectoryStatus.SUCCESS
        elif nb_await == 0 and nb_completed == 0:
            self.status = TVDirectoryStatus.UNKNOWN
        elif nb_renames == 0 and (nb_conflicts+nb_deletes) > 0:
            self.status = TVDirectoryStatus.WARNING
        else:
            self.status = TVDirectoryStatus.ERROR