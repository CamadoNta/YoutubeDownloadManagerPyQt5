from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
from os import path
from pytube import YouTube
import os
from PyQt5 import uic
import moviepy.editor as mp
import re
from pytube import Playlist
import math
ui, _ = loadUiType('main.ui')

class MainApp(QMainWindow, ui):
    file_title = ""
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handele_butons()
        self.Handle_ui()
        self.Handle_res()
        self.Handle_type()
        self.Handle_single_milti()
    def Handle_ui(self):
        self.setWindowTitle("DD102")
        self.setFixedSize(587, 325)

    def Handele_butons(self):
        self.download.clicked.connect(self.Handle_download)
        self.browse.clicked.connect(self.Handle_browse)
        self.res.activated.connect(self.Handle_res)
        self.type.activated.connect(self.Handle_type)
        self.single_milti.activated.connect(self.Handle_single_milti)

    def Handle_browse(self):
        self.save_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.lineEdit_2.setText(self.save_path)
        print(self.save_path)

    def Handle_res(self):
        self.resolution = self.res.currentText()
        print(self.resolution)
    def Handle_type(self):
        self.download_type = self.type.currentText()
        print(self.download_type)
    def Handle_Progress(self,totalsize):
        blocknum = 10
        blocksize = totalsize / blocknum
        readed_data = blocknum * blocksize
        if totalsize > 0 :
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(int(download_percentage))
        QApplication.processEvents()

    def Handle_single_milti(self):
        self.singleOrmulti = self.single_milti.currentText()
        print(self.singleOrmulti)

    def Handle_download(self):
        try:
            self.lineEdit_3.setText("")
            self.url = self.lineEdit.text()
            self.save_path = self.lineEdit_2.text()
            self.counter = 0
            if self.url !="" and self.save_path != "":
                self.lineEdit_3.setText("Download Started")
                if self.singleOrmulti == "Single Download":
                    QMessageBox.warning(self, "Status", "Download started Hold on")
                    self.progressBar.setValue(50)
                    if self.download_type == "video":
                        if self.resolution == "720p":
                            yt = YouTube(self.url).streams.get_highest_resolution().download(self.save_path)
                        if self.resolution == "360p":
                            yt = YouTube(self.url).streams.filter(res="360p").first().download(self.save_path)
                        self.progressBar.setValue(100)
                    if self.download_type == "audio":
                        yt = YouTube(str(self.url))
                        video = yt.streams.filter(only_audio=True).first()
                        destination = str(self.save_path)
                        out_file = video.download(output_path=destination)
                        base, ext = os.path.splitext(out_file)
                        new_file = base + '.mp3'
                        os.rename(out_file, new_file)
                        self.progressBar.setValue(100)
                if self.singleOrmulti == "Playlist Download":
                    YOUTUBE_STREAM_AUDIO = '140'
                    DOWNLOAD_DIR = self.save_path
                    playlist = Playlist(self.url)
                    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
                    print(leng := len(playlist.video_urls))
                    self.prog =100/leng
                    self.prog = math.ceil(self.prog)
                    if self.download_type == "video":
                        if self.resolution == "720p":
                            for url in playlist.video_urls:
                                QtCore.QCoreApplication.processEvents()
                                self.counter = self.counter + self.prog
                                yt = YouTube(url).streams.get_highest_resolution().download(self.save_path)
                                print(str(url) + "  Downloaded")
                                self.progressBar.setValue(self.counter)
                        if self.resolution == "360p":
                            for url in playlist.video_urls:
                                QtCore.QCoreApplication.processEvents()
                                self.counter = self.counter + self.prog
                                yt = YouTube(url).streams.filter(res="360p").first().download(self.save_path)
                                print(str(url) + "  Downloaded")
                                self.progressBar.setValue(self.counter)
                    if self.download_type == "audio":
                        for url in playlist.video_urls:
                            QtCore.QCoreApplication.processEvents()
                            self.counter = self.counter + self.prog
                            yt = YouTube(str(url))
                            video = yt.streams.filter(only_audio=True).first()
                            destination = str(self.save_path)
                            out_file = video.download(output_path=destination)
                            base, ext = os.path.splitext(out_file)
                            new_file = base + '.mp3'
                            os.rename(out_file, new_file)
                            print(str(url) + "  Downloaded")
                            self.progressBar.setValue(self.counter)
        except Exception:
            self.lineEdit_3.setText("Download uncompleted")
            QMessageBox.warning(self, "Status", "Download finished with errors")
            return
        self.lineEdit_3.setText("Download completed successfully")
        QMessageBox.warning(self, "Status", "Download finished")




def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()