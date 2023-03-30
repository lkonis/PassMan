from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel


class PassPage(QWidget):
    def __init__(self, pswd_page, parent):
        super(PassPage, self).__init__()
        psw_lo = QVBoxLayout()
        psw_lo1line = QHBoxLayout()
        # add switch button
        self.pushButtonOk = QPushButton('Go')
        #self.pushButtonOk.setFixedSize(200, 40)
        self.pushButtonOk.clicked.connect(parent.on_pushButtonOK_clicked)
        self.pushButtonOk.setAutoDefault(True)

        close_pswd = QPushButton('Close')
        close_pswd.setMaximumWidth(100)
        close_pswd.released.connect(parent.close)
        self.enter_pswd = parent.createPassLine()
        # add widgets to password layout
        psw_lo.addLayout(psw_lo1line)
        psw_lo1line.addWidget(QLabel("Enter password:"))
        psw_lo1line.addWidget(self.enter_pswd)
        psw_lo1line.addWidget(self.pushButtonOk)
        psw_lo.addWidget(close_pswd)
        pswd_page.setLayout(psw_lo)
