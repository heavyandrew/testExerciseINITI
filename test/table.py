import sys
import requests
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import QVBoxLayout, QWidget, QPushButton

'''
self.label = QLabel("Click in this window")
self.setCentralWidget(self.label)
'''

server_url = '127.0.0.1'
n = 10

def request(url: str, cursor: int, lines: int, column: int, reverse: bool):
    data = requests.get(f'http://{url}/get?cursor={cursor}&lines={lines}&column={column}&reverse={reverse}')
    return data.json()

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.columns = ['Name', 'Age', 'Heights', 'Foot', 'English']

    def update_data(self, data):
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.columns[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.sort_column = 0
        self.reverse = 0
        self.scroll = 0

        self.setFixedSize(QSize(542, 372))
        '''
        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(400, 300))
        '''

        self.table = QtWidgets.QTableView()
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)

        button = QPushButton("Press Me!")
        button.clicked.connect(self.the_button_was_clicked)

        data = request(server_url,
                       self.scroll, n,
                       self.sort_column, self.reverse)
        self.model = TableModel(data)
        self.table.setModel(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(button)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def wheelEvent(self, e) -> None:
        self.scroll = self.scroll + e.delta() / 120

    def onHeaderClicked(self, Index):
        if Index != self.sort_column:
            self.reverse = 1
            self.sort_column = Index
        else:
            self.reverse = not self.reverse

    def the_button_was_clicked(self):
        if self.scroll > 0:
            self.scroll = 0
        self.model.update_data(request(server_url,
                                       self.scroll*(-1), n,
                                       self.sort_column, self.reverse))
        self.model.layoutChanged.emit()

app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()