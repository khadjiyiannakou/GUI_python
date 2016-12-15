from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
import subprocess
import os
import sys
import time
import json

def noYoutube_dl():
    QMessageBox.critical(self,'Aborting','youtube-dl has not been found please install it \n using "sudo pip install youtube_dl"')
    sys.exit(-1)

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.lmusic = []
        self.Input_url = QLineEdit()
        self.Input_plst = QLineEdit()
        
        Layout = QVBoxLayout()
        self.setFixedWidth(1000)
        
        Layout.addWidget(QLabel("Put the Youtube Url you want to download"))
        Layout.addWidget(self.Input_url)

        self.B_sbm_url = QPushButton("Submit Url")
        self.B_sbm_url.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_sbm_url)
        self.B_sbm_url.clicked.connect(self.increaseList)

        Layout.addWidget(QLabel("Put the Youtube playlist Url from where you want to extract the urls"))
        Layout.addWidget(self.Input_plst)

        self.B_sbm_plst = QPushButton("Submit Playlist")
        self.B_sbm_plst.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_sbm_plst)
        self.B_sbm_plst.clicked.connect(self.extractPlaylist)
        
        self.B_shw_lst = QPushButton("Show list of Urls")
        self.B_shw_lst.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_shw_lst)
        self.B_shw_lst.clicked.connect(self.showList)

        self.B_cln_url = QPushButton("Clean list of Urls")
        self.B_cln_url.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_cln_url)
        self.B_cln_url.clicked.connect(self.clearList)

        self.B_dmp_list = QPushButton("Dump list to file")
        self.B_dmp_list.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_dmp_list)
        self.B_dmp_list.clicked.connect(self.write_file_list)

        self.B_rd_list = QPushButton("Read list from file")
        self.B_rd_list.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_rd_list)
        self.B_rd_list.clicked.connect(self.read_file_list)

        Layout.addWidget(QLabel("Choose quality to download from youtube"))
        self.CB_qlt=QComboBox(self)
        Layout.addWidget(self.CB_qlt)
        self.yt_qlt='171' # default value for the quality
        self.CB_qlt.addItem("171")
        self.CB_qlt.addItem("249")
        self.CB_qlt.activated[str].connect(self.set_download_quality)

        Layout.addWidget(QLabel("Do you want to convert downloaded files to mp3?"))
        self.ChB_mp3=QCheckBox(self)
#        self.ChB_mp3.setCheckState(Qt.Checked)
        Layout.addWidget(self.ChB_mp3)
        self.cnvrt_mp3=False
        self.ChB_mp3.clicked.connect(self.set_cnvrt_mp3)

        self.B_dir_dwnld = QPushButton("Download Directory")
        self.B_dir_dwnld.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')
        Layout.addWidget(self.B_dir_dwnld)
        self.dir_dwnld = '.'
        self.B_dir_dwnld.clicked.connect(self.find_directory)
        
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30,40,200,25)
        self.timer = QBasicTimer()
        self.step = 0
        self.count = 0
        self.B_dwnld = QPushButton("Download")
        self.B_dwnld.setStyleSheet('QPushButton {background-color: green; color: black;}')
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
    def extractPlaylist(self):
        name = self.Input_plst.text()
        self.Input_plst.clear()
        yt_dl_bin = which('youtube-dl')
        if yt_dl_bin:
            exec_comm = '%s -j --flat-playlist "%s"' % (yt_dl_bin,name)
            p = subprocess.Popen(exec_comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output, err = p.communicate()
            app.processEvents()
            rc = p.returncode
            if rc != 0:
                QMessageBox.warning(self,'Warning', 'youtube-dl exited with error \n %s' % (output.decode()))
            vlj = (output.decode("utf-8")).split('\n')
            prefix='https://www.youtube.com/watch?v='
            for i in vlj:
                if i:
                    self.lmusic.append(prefix + json.loads(i)['url'])
        else:
            noYoutube_dl()
    def showList(self):
        string=''
        for i,x in enumerate(self.lmusic): string += '(%d) %s\n' % (i+1,x)
        QMessageBox.information(self, "List of Urls", string)
    def clearList(self):
        self.lmusic = []
        QMessageBox.information(self, "Warning", "The list of urls has been cleaned")
    def doAction(self):
        self.pbar.setValue(self.step)
        if self.timer.isActive():
            self.timer.stop()
            self.B_dwnld.setText('Start')
            self.B_dwnld.setStyleSheet('QPushButton {background-color: green; color: black;}')
        else:
            self.timer.start(100,self)
            self.B_dwnld.setText('Stop')
            self.B_dwnld.setStyleSheet('QPushButton {background-color: red; color: black;}')
                    

    def timerEvent(self,e):
        if self.count == (len(self.lmusic)) or len(self.lmusic) == 0:
            self.timer.stop()
            self.B_dwnld.setText('Download')
            self.B_dwnld.setStyleSheet('QPushButton {background-color: green; color: black;}')
            self.step=0
            self.count=0
            return
        self.step = self.step + round(100./len(self.lmusic),3)
        self.youtube_dl(self.lmusic[self.count])
        self.count += 1
        self.pbar.setValue(self.step)

    def set_download_quality(self,qlt):
        self.yt_qlt = qlt
    def set_cnvrt_mp3(self,tick):
        self.cnvrt_mp3 = tick

    def write_file_list(self):
        fileName,state = QFileDialog.getSaveFileName(self, 'Choose File ', os.path.curdir)
        if fileName:
            with open(fileName,"w") as fp:
                for name in self.lmusic: fp.write('%s\n' % (name))

    def read_file_list(self):
        fileName,state = QFileDialog.getOpenFileName(self, 'Open File ', os.path.curdir)
        if fileName:
            with open(fileName, "r") as fp:
                for line in fp:
                    self.lmusic.append(line.strip('\n'))
        
    def find_directory(self):
        self.dialog = QFileDialog()
        self.dialog.setFileMode(QFileDialog.Directory)
        self.dialog.setOption(QFileDialog.ShowDirsOnly)
        directory = self.dialog.getExistingDirectory(self, 'Choose Directory', os.path.curdir)
        self.dir_dwnld = directory

    def youtube_dl(self,name):
        yt_dl_bin = which('youtube-dl')
        if self.cnvrt_mp3:
            convertMP3 = '--extract-audio --audio-format mp3'
        else:
            convertMP3 = ''
        pathOut = '--output "%s/%%(title)s.%%(ext)s"' % (self.dir_dwnld)
        if yt_dl_bin:
            exec_comm = '%s --format %s %s %s "%s"' % (yt_dl_bin,self.yt_qlt,convertMP3,pathOut,name)
            p = subprocess.Popen(exec_comm, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            app.processEvents()
            output,err = p.communicate()
            rc = p.returncode
            if rc != 0:
                QMessageBox.warning(self,'Warning', 'youtube-dl exited with error \n %s' % (output.decode()))
        else:
            noYoutube_dl()
if __name__ == '__main__':
    import sys
    global app
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon/youtube.png'))
    screen = Window()
    screen.show()
    sys.exit(app.exec_())
