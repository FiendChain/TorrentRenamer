from PyQt5.QtWidgets import\
    QCheckBox, QLineEdit, QLabel,\
    QTableWidget, QWidget, QHBoxLayout,\
    QHeaderView, QSizePolicy

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics

def center_wrap(widget):
    wrapper = QWidget()
    layout = QHBoxLayout()
    layout.addWidget(widget)
    wrapper.setLayout(layout)
    return wrapper

class RenameView(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 3 columns: checkbox, old path, new path
        self.table = QTableWidget(0, 3)
        layout = QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.table.setHorizontalHeaderLabels([None, "Old Path", "New Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)

        self.font = QFont("", 0)
        self.font_metric = QFontMetrics(self.font)

    def clear(self):
        self.set_model([])
    
    def set_model(self, model):
        N = len(model)
        self.table.setRowCount(N)
        for i, entry in enumerate(model):
            for j, cell_widget in enumerate(self.create_row(entry)): 
                self.table.setCellWidget(i, j, cell_widget)
        
        self.table.resizeColumnsToContents()
    
    def create_row(self, entry):
        chk = QCheckBox()
        old_path = QLabel(entry.old_path)
        new_path = QLineEdit(entry.new_path)
        # new_path = QLabel(entry.new_path)

        def chk_callback(state):
            if state == Qt.Checked:
                entry.enabled = True
            elif state == Qt.Unchecked:
                entry.enabled = False

        chk.setCheckState(Qt.Checked if entry.enabled else Qt.Unchecked)
        chk.stateChanged.connect(chk_callback)
        
        def path_callback(path):
            if path != entry.new_path:
                chk.setCheckState(Qt.Checked)

            entry.new_path = path 
            w = self.font_metric.width(path)
            new_path.setMinimumWidth(w)
            # new_path.setFixedWidth(w)
            self.table.resizeColumnsToContents()
        
        new_path.textChanged.connect(path_callback)
        new_path.setAlignment(Qt.AlignLeft)
        new_path.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)

        w = self.font_metric.width(entry.new_path)
        new_path.setMinimumWidth(w)

        return (center_wrap(chk), old_path, new_path)
    

    
       


    