import sys
from AccPage import AccPage
from PassPage import PassPage
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QFormLayout,
    QLineEdit,
    QStackedLayout,
    QVBoxLayout, QHBoxLayout,
    QWidget, QDialog, QDesktopWidget, QLabel,
)

class PassManager(QWidget):
    tries=3
    def centerScrn(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self):
        super().__init__()
        #self.setGeometry(0,0,600,30) # x,y,w,h
        #self.setMaximumHeight(30)
        self.setBaseSize(400,30)
        self.centerScrn()
        self.setWindowTitle("Password manager")
        # Create a top-level layout (stacked)
        self.stackedLayout = QStackedLayout()
        # page1 - password page
        self.pswd_page = self.CreatePage()
        self.pp=PassPage(self.pswd_page, self)

        # Create the account page
        self.account_page = self.CreatePage()
        self.ap=AccPage(self.account_page, self)


        # add the pages to top level layout
        self.stackedLayout.addWidget(self.pswd_page)
        self.stackedLayout.addWidget(self.account_page)

        # Set the stacked layout to the top-level
        self.setLayout(self.stackedLayout)

    def on_pushButtonOK_clicked(self):
        # validate password
        print("validating password: " + self.pp.enter_pswd.text())
        if self.pp.enter_pswd.text()=="":
            self.showdialog("Can't use empty string")
            return

        if self.pp.enter_pswd.text() in ['xvrubur', 'æ']:
            self.switchPage(1)
            self.setGeometry(0,0,600,500) # x,y,w,h

        else:
            self.tries -= 1
            if self.tries>0:
                self.showdialog("Wrong password, " + str(self.tries) + " tries left")
                self.pp.enter_pswd.setText('')
            else:
                self.close()

    def createPassLine(self):
        enter_pswd = QLineEdit()
        enter_pswd.returnPressed.connect(self.returnPressed)
        return enter_pswd

    def returnPressed(self):
        self.pp.pushButtonOk.click()

    def CreateGrayPallete(self):
        pg_pallete = QPalette()
        pg_pallete.setColor(QPalette.Window, Qt.lightGray)
        return pg_pallete

    def CreatePage(self):
        page = QWidget()
        pg_palette = self.CreateGrayPallete()
        page.setPalette(pg_palette)
        page.setStyleSheet(
            "QPushButton{color: black;"
            "background-color: darkcyan;"
            "border-width: 5 px;"
            "border-color: darkblue;}"
            "QLineEdit { background-color: #cccccc}"
            "QTableView { background-color: #cccccc}")
        page.setAutoFillBackground(True)
        return page

    def switchPage(self, press=-1):
        self.stackedLayout.setCurrentIndex(press)

    def showdialog(self, in_text=None):
        # Create the first page
        dlg = QDialog()
        dlg.setFixedSize(300,200)
        quit_bt = QPushButton("Try again")
        quit_bt.clicked.connect(dlg.close)
        if in_text == None:
            in_text = "Wrong password"
        quit_text = QLabel(in_text)
        quit_text.setAlignment(Qt.AlignCenter)
        quit_text.adjustSize()
        #b2.setFont(24)
        dlg.setWindowTitle("Wrong password")
        dlg.setWindowModality(Qt.ApplicationModal)
        dlgLo = QVBoxLayout()
        dlgLo.addWidget(quit_text)
        dlgLo.addWidget(quit_bt)
        dlg.setLayout(dlgLo)

        #page = QWidget(dlg)
        #page.setLayout(QVBoxLayout())
        dlg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PassManager()
    window.show()
    sys.exit(app.exec_())