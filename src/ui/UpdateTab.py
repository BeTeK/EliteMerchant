
import ui.UpdateTabUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QVariant
import ui.TabAbstract
import Options

class UpdateTab(ui.UpdateTabUI.Ui_Dialog, QtWidgets.QWidget, ui.TabAbstract.TabAbstract):
    def __init__(self, db, analyzer, tabName, mainWindow,versioninfo):
        super(QtWidgets.QWidget, self).__init__()
        self.setupUi(self)

        self.mainWindow = mainWindow
        self.tabName = tabName

        html=self.versionlinkTextBrowser.toHtml()
        html=html.replace('%versionstring%',versioninfo['versionTxt'])
        html=html.replace('%currentversionstring%',Options.get("Merchant-version",'?'))
        html=html.replace('%newversionlinkstring%',versioninfo['url'])
        self.versionlinkTextBrowser.setHtml(html)


    def setTabName(self, name):
        self.tabName = name

    def getType(self):
        return "update"

    def getTabName(self):
        return "Update Available!"

    def dispose(self):
        pass
