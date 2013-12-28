import sys, os
import urllib, urllib2, json
from PySide.QtGui import QApplication, QSystemTrayIcon, QMenu, QIcon
from PySide.QtCore import QBuffer, QByteArray, QIODevice, QThread


APP_NAME = 'Insta'
VERSION = '1.0.0'
API_KEY = 'YOUR_IMGUR_API_KEY'
ICON_PATH = 'icon.png'

def build_path_in_resource(filename):
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS
    else:
        basedir = os.path.dirname(__file__)

    return os.path.normpath(os.path.join(basedir, filename))


class Insta:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.clipboard = QApplication.clipboard()
        self.tray = QSystemTrayIcon(QIcon(build_path_in_resource(ICON_PATH)))
        self.setupUI()


    def setupUI(self):
        menu = QMenu()
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(sys.exit)
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip(APP_NAME)
        self.tray.showMessage('Insta', 'Start monitor')
        self.clipboard.dataChanged.connect(self.copyHandler)


    def run(self):
        sys.exit(self.app.exec_())


    def copyHandler(self):
      if self.clipboard.mimeData().hasImage():
          image = self.clipboard.image()
          byteArray = QByteArray()
          buf = QBuffer(byteArray)
          buf.open(QIODevice.WriteOnly)
          image.save(buf, "PNG")
          self.tray.showMessage('Insta', 'Start uploading')
          self.thread = NetThread(str(byteArray.toBase64()))
          self.thread.finished.connect(self.onUploadFinished)
          self.thread.start()


    def onUploadFinished(self):
        link = self.thread.getLink()
        self.clipboard.setText(link)
        self.tray.showMessage('Finished uploading', link)


class NetThread(QThread):

    def __init__(self, base64):
        super(NetThread, self).__init__()
        self.base64 = base64


    def run(self):
        value = {
            'key': API_KEY,
            'image': self.base64
        }
        data = urllib.urlencode(value)
        f = urllib2.urlopen(
            url='http://api.imgur.com/2/upload.json',
            data=data
        )
        response = json.load(f)
        self.link = response[u'upload'][u'links'][u'original']


    def getLink(self):
        return self.link


if __name__ == '__main__':
    Insta().run()
