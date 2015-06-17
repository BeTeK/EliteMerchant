
import ui.DBloadingTabUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QVariant
import Options
import Queries
import datetime
import EDDB
import EliteLogAnalyzer
import EdceWrapper
import SpaceTime
import time
import ui.TabAbstract

class DBloadingTab(ui.DBloadingTabUI.Ui_Dialog, QtWidgets.QWidget, ui.TabAbstract.TabAbstract):
    def __init__(self, db, analyzer, tabName, mainWindow):
        super(QtWidgets.QWidget, self).__init__()
        self.setupUi(self)

        self.mainWindow = mainWindow
        self.tabName = tabName

    def setTabName(self, name):
        self.tabName = name

    def getType(self):
        return "status"

    def getTabName(self):
        return "Status {0}".format(self.tabName)

    def dispose(self):
        pass
