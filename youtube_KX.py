from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap

import subprocess
import os
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

        Layout.addWidget(QLabel("Choose quality to download from youtube"))
        self.CB_qlt=QComboBox(self)
        Layout.addWidget(self.CB_qlt)
        self.yt_qlt=171 # default value for the quality
        self.CB_qlt.addItem("171")
        self.CB_qlt.addItem("249")
        self.CB_qlt.activated[str].connect(self.set_download_quality)

        self.B_dir_dwnld = QPushButton("Download Directory")
        self.B_dir_dwnld.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_dir_dwnld)
        self.dir_dwnld = './'
        self.B_dir_dwnld.clicked.connect(self.find_directory)
        
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30,40,200,25)
        self.timer = QBasicTimer()
        self.step = 0
        self.count = 0
        self.B_dwnld = QPushButton("Download")
        self.B_dwnld.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_dwnld)
        Layout.addWidget(self.pbar)
        self.B_dwnld.clicked.connect(self.doAction)
        
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
    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.B_dwnld.setText('Start')
        else:
            self.timer.start(100,self)
            self.B_dwnld.setText('Stop')

    def timerEvent(self,e):
        if self.count == (len(self.lmusic)) or len(self.lmusic) == 0:
            self.timer.stop()
            self.B_dwnld.setText('Download')
            self.step=0
            self.count=0
            return
        self.youtube_dl(self.lmusic[self.count])
        self.count += 1
        self.step = self.step + 100./len(self.lmusic)
        self.pbar.setValue(self.step)

    def set_download_quality(self,qlt):
        self.yt_qlt = int(qlt)

    def find_directory(self):
        self.dialog = QFileDialog()
        self.dialog.setFileMode(QFileDialog.Directory)
        self.dialog.setOption(QFileDialog.ShowDirsOnly)
        directory = self.dialog.getExistingDirectory(self, 'Choose Directory', os.path.curdir)
        self.dir_dwnld = directory + '/'

    def youtube_dl(self,name):
        print(name)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon/youtube.png'))
    screen = Window()
    screen.show()
    sys.exit(app.exec_())
