from PyQt5.QtWidgets import\
    QLabel,QWidget,\
    QListWidget, QListWidgetItem,\
    QHBoxLayout, QVBoxLayout,\
    QHeaderView, QSizePolicy,\
    QPushButton, QStyle

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from models import TVDirectoryStatus

STATUS_LOOKUP = {
    TVDirectoryStatus.SUCCESS: QStyle.SP_DialogApplyButton,
    TVDirectoryStatus.ERROR: QStyle.SP_MessageBoxCritical,
    TVDirectoryStatus.WARNING: QStyle.SP_MessageBoxWarning,
    TVDirectoryStatus.UNKNOWN: QStyle.SP_BrowserReload,
}

class DirectoryList(QWidget):
    indexChanged = pyqtSignal(int)
    onScan = pyqtSignal()
    onSoftRefresh = pyqtSignal()
    onHardRefresh = pyqtSignal()

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
        
        scan_btn = QPushButton("Scan Folders")
        soft_refresh_btn = QPushButton("Soft Refresh")
        hard_refresh_btn = QPushButton("Hard Refresh")

        layout.addWidget(scan_btn)
        layout.addWidget(soft_refresh_btn)
        layout.addWidget(hard_refresh_btn)

        scan_btn.clicked.connect(self.onScan.emit)
        soft_refresh_btn.clicked.connect(self.onSoftRefresh.emit)
        hard_refresh_btn.clicked.connect(self.onHardRefresh.emit)

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

        

