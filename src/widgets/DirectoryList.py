from PyQt5.QtWidgets import\
    QLabel,\
    QListWidget, QWidget,\
    QHBoxLayout, QVBoxLayout,\
    QHeaderView, QSizePolicy,\
    QPushButton

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

class DirectoryList(QWidget):
    basedirChanged = pyqtSignal(str)
    indexChanged = pyqtSignal(int)
    onRefresh = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 3 columns: checkbox, old path, new path
        self.list_widget = QListWidget()
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.list_widget)
        vlayout.addWidget(self.create_controls())

        self.setLayout(vlayout)
        self.basedirs = []

        self.list_widget.currentRowChanged.connect(self.row_change)
    
    def create_controls(self):
        widget = QWidget()
        layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh")
        layout.addWidget(self.refresh_button)

        self.refresh_button.clicked.connect(self.onRefresh.emit)

        widget.setLayout(layout)

        return widget

    def update_list(self, basedirs):
        self.basedirs = basedirs
        self.list_widget.clear()
        for basedir in basedirs:
            self.list_widget.addItem(basedir)

    def row_change(self, i):
        basedir = self.basedirs[i]
        self.basedirChanged.emit(basedir)    
        self.indexChanged.emit(i)

        

