
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QHeaderView, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sys

data = {'Account': ['1', '2', '11', '4'],
        'User': ['11', '22222aaaaa2', '1', '3'],
        'Password': ['2', '1', '2', '1']}

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100,100,600,400)
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.table = TableView(data, 4, 3)
        hheader = self.table.horizontalHeader()
        hheader.setSectionResizeMode(QHeaderView.Stretch)
        self.search = QLineEdit()
        self.search.textChanged.connect(lambda: self.table.findName(self))

        layout.addWidget(self.search)
        layout.addWidget(self.table)


class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        #self.data = data
        self.setRowCount(7)
        self.setData(data)
        self.setItem(3, 6, QTableWidgetItem('Lior'))
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setData(self, data):
        horHeaders = []
        for n, key in enumerate((data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

    def findName(self, parent):
        name_to_find = parent.search.text()
        table_rows = parent.table.rowCount()
        if table_rows != 0 and len(name_to_find) != 0:
            for row in range(parent.table.rowCount()):
                acc=parent.table.item(row, 0)
                if acc is None or name_to_find.lower() not in acc.text().lower():
                    parent.table.hideRow(row)
        else:
            for row in range(table_rows):
                parent.table.showRow(row)
def main(args):
    app = QApplication(args)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)