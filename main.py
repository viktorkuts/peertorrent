from src.ui import *
import libtorrent as lt
import time
import sys
import threading
import socket
import os
import humanize

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.sock.connect(("167.114.96.182", 3292))

    def send_msg(self, msg):
        self.sock.send(("*&chatcmd" + msg).encode('utf-8'))

    def disconnect(self):
        self.sock.send("*&disconn".encode('utf-8'))
        self.sock.close()

    def receiveHandler(self):
        dat = self.sock.recv(2066).decode('utf-8')
        if dat != "":
            ui.recvClass.recvData.emit(ui.areaMsg.toPlainText() + "\n" + dat)


class Torrent:
    def __init__(self):
        self.current_torrent = None
        self.session = lt.session()
        self.updateThread = None
        self.handle = None
        self.savepath = None

    def updateUIhandle(self):
        while self.handle != None:
            status = self.handle.status()
            state_dic = ['Queued', 'Checking', 'Downloading Metadata', 'Downloading', 'Finished', 'Seeding', 'Allocating']
            ui.recvClass.updateUI.emit(status.name, f"{status.num_seeds} / {status.num_peers}", f"{status.upload_rate / 1000} KB/s", f"{status.download_rate / 1000} KB/s", self.savepath, state_dic[status.state] + f"\nSize: {humanize.naturalsize(status.total)}", status.progress * 100)
            time.sleep(1)

    def stop_torrent(self):
            hdl = self.handle
            self.handle = None
            if hdl != None:
                self.session.remove_torrent(hdl)
            self.current_torrent = None
            resetUIstate()

    def add_new_torrent(self, params):
        self.savepath = params["save_path"]
        # The URI/File is in the params, so that makes our job easier
        if self.current_torrent == None:
            self.handle = self.session.add_torrent(params)
            self.current_torrent = True
            self.updateThread = threading.Thread(target=self.updateUIhandle, daemon=True)
            self.updateThread.start()
        else:
            self.stop_torrent()
            self.add_new_torrent(params)


def resetUIstate():
    ui.clearLabels()

def handleTorrentFile():
    file_path = ui.promptTorrentFile()
    save_path = ui.promptDownloadDirectory()
    info = lt.torrent_info(file_path[0])
    params = {
        "ti": info,
        "save_path": save_path,
        "storage_mode": lt.storage_mode_t.storage_mode_sparse
    }
    th.add_new_torrent(params)
    

def handleMagnet():
    magnet = ui.promptMagnetLink()
    torrent_param = None
    # we need to check if the magnet is valid, if not, display alert and return
    # if valid, prompt for install directory
    try:
        torrent_param = lt.parse_magnet_uri(magnet)
    except:
        ui.alertDialog("Error", "Please enter a valid magnet uri!")
    else:
        downPath = ui.promptDownloadDirectory()
        ui.alertDialog("Torrent", f"Torrent will start shortly.\nWill be saved in {downPath}")
        params = {
            "save_path": downPath,
            "storage_mode": lt.storage_mode_t.storage_mode_sparse,
            "url": magnet
        }
        th.add_new_torrent(params)
        

cc = ChatClient()

def loopHandler_chat():
    while True:
        cc.receiveHandler()
        time.sleep(1)

def sendMessage():
        msg = ui.inputMsg.text()
        if msg != "" or msg != " ":
            ui.inputMsg.setText("")
            cc.send_msg(msg)

chatthread = threading.Thread(target=loopHandler_chat, daemon=True)
chatthread.start()

def onClose():
    cc.disconnect()
    th.stop_torrent()

th = Torrent()
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

ui.magnetBtn.triggered.connect(handleMagnet)
ui.torrentBtn.triggered.connect(handleTorrentFile)
app.aboutToQuit.connect(onClose)
ui.sendMsg.clicked.connect(sendMessage)
ui.actionStop_Torrent.triggered.connect(th.stop_torrent)

sys.exit(app.exec_())