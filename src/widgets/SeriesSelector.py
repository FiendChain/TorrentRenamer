from PyQt5.QtWidgets import\
    QPushButton, QLabel, QMainWindow, QDialog,\
    QLineEdit, QVBoxLayout, QHBoxLayout,\
    QTableWidget, QLabel, QWidget, QHeaderView, QAbstractItemView

class SeriesEntry:
    def __init__(self, data):
        self.data = data
        self.columns = [
            data.get('seriesName'),
            str(data.get('id')),
            data.get('status'),
            data.get('firstAired')
        ]

class SeriesSelector(QDialog):
    def __init__(self, api, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.api = api
        self.search_text = ""

        self.model = []
        self.selected = None

        layout = QVBoxLayout()
        layout.addWidget(self.create_search_bar())
        layout.addWidget(self.create_result_table())
        layout.addWidget(self.create_button_group())
        self.setLayout(layout)
    
    def create_search_bar(self):
        def update_search_text(txt):
            self.search_text = txt

        group = QWidget()
        layout = QHBoxLayout()
        self.search_box = QLineEdit(self.search_text)
        self.search_box.textEdited.connect(update_search_text)

        self.search_btn = QPushButton("Search")
        self.search_btn.pressed.connect(self.search)
        layout.addWidget(self.search_box)
        layout.addWidget(self.search_btn)

        group.setLayout(layout)
        return group
    
    def create_result_table(self):
        self.table = QTableWidget(0, 4)
        # self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.table.horizontalHeader().setSelectionMode(QAbstractItemView.NoSelection)
        # self.table.verticalHeader().setSelectionMode(QAbstractItemView.SingleSelection)

        self.table.cellClicked.connect(self.on_cell_select)

        self.table.setHorizontalHeaderLabels(['Name', 'id', 'status', 'air date'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        return self.table
    
    def create_button_group(self):
        group = QWidget()
        layout = QHBoxLayout()

        def cancel():
            self.reject()

        def submit():
            self.accept()

        self.cancel_btn = QPushButton("cancel")
        self.submit_btn = QPushButton("Submit")
        self.cancel_btn.pressed.connect(cancel)
        self.submit_btn.pressed.connect(submit)
        layout.addWidget(self.cancel_btn)
        layout.addWidget(self.submit_btn)

        group.setLayout(layout)
        return group

    def on_cell_select(self, row, col):
        self.table.selectRow(row)
        self.selected = row 

    def update_result_table(self):
        N = len(self.model)
        self.table.setRowCount(N)
        for i, entry in enumerate(self.model):
            for j, txt in enumerate(entry.columns):
                label = QLabel(txt)
                label.setContentsMargins(2, 1, 2, 1)
                self.table.setCellWidget(i, j, label)
        
        self.table.resizeColumnsToContents()
    
    def set_search_text(self, text):
        self.search_text = text
        self.search_box.setText(text)
    
    def search(self):
        res = self.api.search_series(self.search_text)
        if res is None:
            res = []
        model = [SeriesEntry(entry) for entry in res]
        self.cached_result = res
        self.model = model
        self.update_result_table()
        self.selected = None

    def exec_(self):
        super().exec_()
        if self.result() == QDialog.Accepted and self.selected != None:
            return self.cached_result[self.selected]
        return None

