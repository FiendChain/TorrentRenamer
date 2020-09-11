from PyQt5.QtWidgets import QApplication, QWidget, QSplitter
from src.widgets import RenameView, DirectoryList
from src import parse_directory
import os
from argparse import ArgumentParser

class Entry:
    def __init__(self, old_path, new_path):
        self.enabled = True
        self.old_path = old_path
        self.new_path = new_path

class App:
    def __init__(self, view, dir_list):
        self.root_dir = "F:/TV Shows/"
        self.sub_dirs = []

        for sub_dir in os.listdir(self.root_dir):
            base_dir = os.path.join(self.root_dir, sub_dir)
            if not os.path.isdir(base_dir):
                continue
            self.sub_dirs.append(sub_dir)
        

        def index_listener(i):
            self.idx = i
            self.update_view()
           
        dir_list.indexChanged.connect(index_listener)

        self.view = view
        self.dir_list = dir_list

        self.model = []
        self.idx = 0

        dir_list.update_list(self.sub_dirs)
    
    def update_view(self):
        if len(self.sub_dirs) == 0:
            return
            
        base_dir = os.path.join(self.root_dir, self.sub_dirs[self.idx])

        print(self.sub_dirs[self.idx])

        p = parse_directory(base_dir)
        renames = p.get('renames')

        self.model = [Entry(old, new) for old, new in renames]
        self.view.set_model(self.model)
    
def main():
    app = QApplication([])
    app.setStyle("Fusion")

    widget = RenameView()
    dir_list = DirectoryList()

    mg = App(widget, dir_list)

    splitter = QSplitter()
    splitter.addWidget(dir_list)
    splitter.addWidget(widget)

    splitter.show()


    app.exec_()

if __name__ == '__main__':
    main()