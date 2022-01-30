from src.ui import *
import libtorrent as lt
import time
import sys
import threading

class Torrent:
    def __init__(self):
        self.status = False
        self.session = lt.session()

    def del_old_torrent(self, torrent):
        pass

    def add_new_torrent(self, torrent, delete_old=False):
        if delete_old == True:
            pass

def resetUIstate():
    pass


th = Torrent()
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())