from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget)
from tableViewer import TableView

data = {'Account': ['1', '2', '11', '4'],
        'User': ['11', '22222aaaaa2', '1', '3'],
        'Password': ['2', '1', '2', '1']}

class AccPage(QWidget):
    def __init__(self, acc_page, parent):
        super(AccPage, self).__init__()
        acc_lo = QVBoxLayout()
        list_lo = QVBoxLayout()
        list_lo.addWidget(QLabel("All accounts"))
        search_lo = QHBoxLayout()
        self.search_label = QLabel("Search here")
        self.search = QLineEdit()
        search_lo.addWidget(self.search_label)
        search_lo.addWidget(self.search)
        list_lo.addLayout(search_lo)
        self.table = TableView(data, 4, 3)
        self.search.textChanged.connect(lambda: self.table.findName(self))

        list_lo.addWidget(self.table)
        # entry layout
        entry_lo = QFormLayout()

        # button to quit
        close_acc = QPushButton('Close')
        close_acc.setMaximumWidth(100)
        close_acc.clicked.connect(parent.close)

        # add buttons to account
        entry_lo.addWidget(QLabel("Selected account"))

        entry_lo.addRow("Account:", QLineEdit())
        entry_lo.addRow("Data:", QLineEdit())
        entry_lo.addRow(close_acc)

        # set the original page's layout
        acc_lo.addLayout(list_lo)
        acc_lo.addLayout(entry_lo)
        acc_page.setLayout(acc_lo)
