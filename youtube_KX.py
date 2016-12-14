from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.lmusic = []
        self.Input_url = QLineEdit()

        Layout = QVBoxLayout()
        self.setFixedWidth(1000)

        Layout.addWidget(QLabel("Put the Youtube Url you want to download"))
        Layout.addWidget(self.Input_url)

        self.B_sbm_url = QPushButton("Submit Url")
        self.B_sbm_url.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_sbm_url)
        self.B_sbm_url.clicked.connect(self.increaseList)
        
        self.B_shw_lst = QPushButton("Show list of Urls")
        self.B_shw_lst.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_shw_lst)
        self.B_shw_lst.clicked.connect(self.showList)

        self.B_cln_url = QPushButton("Clean list of Urls")
        self.B_cln_url.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_cln_url)
        self.B_cln_url.clicked.connect(self.clearList)

        self.B_dwnld = QPushButton("Download")
        self.B_dwnld.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_dwnld)
        self.B_dwnld.clicked.connect(self.StartDownload)

        mainLayout = QGridLayout()
        mainLayout.addLayout(Layout, 0, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Youtube downloader by Kyriakos Hadjiyiannakou")
    def increaseList(self):
        name = self.Input_url.text()
        self.Input_url.clear()
        if name == "":
            QMessageBox.information(self, "Empty Field","Please enter a url.")
            return
        else:
            self.lmusic.append(name)
            QMessageBox.information(self, "Success", "url added")
    def showList(self):
        string=''
        for x in self.lmusic:
            string += x
            string += '\n'
        QMessageBox.information(self, "List of Urls", string)
    def clearList(self):
        self.lmusic = []
        QMessageBox.information(self, "Warning", "The list of urls has been cleaned")
    def StartDownload(self):
        import time
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)
        self.completed = 0
        while self.completed < 10:
            time.sleep(1) 
            self.completed += 1
            self.progress.setValue(self.completed)
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())
