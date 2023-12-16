import datetime

from PyQt5.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget)
from tableViewer import TableView
from NewAccountManager import NewAccountManager, Repeated

'''data = {'Account': ['1', '2', '11', '4'],
        'User': ['11', '22222aaaaa2', '1', '3'],
        'Password': ['2', '1', '2', '1']}
'''
data_header =['Account', 'User', 'Password', 'Time', 'Comment']
date_format = "%Y-%m-%d %H:%M:%S"
now = datetime.datetime.now().strftime(date_format)
init_data = [data_header,
             ['new account','username','password',now,'my_comment']]

class AccPage(QWidget):
    def __init__(self, acc_page, parent):
        super(AccPage, self).__init__()
        self.parent = parent
        acc_lo = QVBoxLayout()
        list_lo = QVBoxLayout()
        list_lo.addWidget(QLabel("All accounts"))
        search_lo = QHBoxLayout()
        self.search_label = QLabel("Search here")
        self.search = QLineEdit()
        search_lo.addWidget(self.search_label)
        search_lo.addWidget(self.search)
        list_lo.addLayout(search_lo)
        self.table = TableView(init_data, 7, 5)
        self.search.textChanged.connect(lambda: self.table.findName(self))
        self.table.cellChanged.connect(self.table.handle_item_changed_by_user)

        list_lo.addWidget(self.table)
        # entry layout
        entry_lo = QHBoxLayout()

        # button to quit
        close_acc = QPushButton('Close')
        close_acc.setMaximumWidth(100)
        close_acc.clicked.connect(parent.close)

        # button to add new
        add_new = QPushButton('Add new')
        add_new.setMaximumWidth(100)
        add_new.clicked.connect(self.add_new_entry)

        # button to delete row
        delete_row = QPushButton('delete row')
        delete_row.setMaximumWidth(100)
        delete_row.clicked.connect(self.delete_selected_row)

        # button to change pass
        chn_pass = QPushButton("Change password")
        chn_pass.setMaximumWidth(100)

        # button to save current state
        save_db = QPushButton("Save")
        save_db.setMaximumWidth(100)
        save_db.clicked.connect(self.save_data)

        # add all buttons
        entry_lo.addWidget(close_acc)
        entry_lo.addWidget(add_new)
        entry_lo.addWidget(delete_row)
        entry_lo.addWidget(save_db)
        entry_lo.addWidget(chn_pass)
#        entry_lo.addRow(close_acc)

        # set the original page's layout
        acc_lo.addLayout(list_lo)
        acc_lo.addLayout(entry_lo)
        acc_page.setLayout(acc_lo)

    def add_new_entry(self):
        self.table.add_row()
        pass
    def delete_selected_row(self):
        selectedRow = self.table.delete_row()
        print("selectedrow=",selectedRow)
    def reload_data(self, account):
        data = [data_header]
        for item in account.recDatabase:
            last_record = item['Records'].item_list[-1]
            reorder = [
                item['Account'],
                last_record['user'],
                last_record['pass'],
                last_record['time'].strftime(date_format),
                item['Comment']]
            data.append(reorder)
        nRow = len(data)-1
        self.table.setBetterData(data)
        #self.table = TableView(data, nRow, 5)
    def save_data(self):
        account = self.parent.acc
        data = self.table.getData()
        for item in data:
            time_elapsed = datetime.datetime.now() - datetime.datetime.strptime(item[3], date_format)
            if time_elapsed < datetime.timedelta(minutes=.1):
                if not item[0]=='new account':
                    account.add_record(ac=item[0], usr=item[1], psw=item[2], comment=item[4])

        #account.recDatabase = data
        account.save_dataBase()
        pass