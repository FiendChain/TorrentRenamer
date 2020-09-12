from PyQt5.QtWidgets import\
    QLabel,QWidget,\
    QListWidget, QListWidgetItem,\
    QHBoxLayout, QVBoxLayout,\
    QHeaderView, QSizePolicy,\
    QPushButton, QStyle

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from src.models import TVDirectoryStatus

STATUS_LOOKUP = {
    TVDirectoryStatus.SUCCESS: QStyle.SP_DialogApplyButton,
    TVDirectoryStatus.ERROR: QStyle.SP_MessageBoxCritical,
    TVDirectoryStatus.WARNING: QStyle.SP_MessageBoxWarning,
    TVDirectoryStatus.UNKNOWN: QStyle.SP_BrowserReload,
}

class DirectoryList(QWidget):
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
        self.directories = []

        self.list_widget.currentRowChanged.connect(self.row_change)
    
    def create_controls(self):
        widget = QWidget()
        layout = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh")
        layout.addWidget(self.refresh_button)

        self.refresh_button.clicked.connect(self.onRefresh.emit)

        widget.setLayout(layout)

        return widget

    def update_directories(self, directories):
        self.directories = directories
        self.list_widget.clear()
        for directory in directories:
            item = self.create_list_item(directory)
            self.list_widget.addItem(item)
    
    def create_list_item(self, directory):
        item = QListWidgetItem(directory.basedir)
        def set_icon(status):
            qicon = STATUS_LOOKUP[status]
            icon = self.style().standardIcon(qicon)
            item.setIcon(icon)
            
        set_icon(directory.status)
        directory.statusChanged.connect(set_icon)
        return item
    
    def row_change(self, i):
        self.indexChanged.emit(i)

        

