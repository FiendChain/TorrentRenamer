from PyQt5.QtWidgets import\
    QLabel,\
    QListWidget, QWidget, QHBoxLayout,\
    QHeaderView, QSizePolicy

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

class DirectoryList(QWidget):
    basedirChanged = pyqtSignal(str)
    indexChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 3 columns: checkbox, old path, new path
        self.list_widget = QListWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)
        self.basedirs = []

        self.list_widget.currentRowChanged.connect(self.row_change)

    def update_list(self, basedirs):
        self.basedirs = basedirs
        self.list_widget.clear()
        for basedir in basedirs:
            self.list_widget.addItem(basedir)

    def row_change(self, i):
        basedir = self.basedirs[i]
        self.basedirChanged.emit(basedir)    
        self.indexChanged.emit(i)

        

