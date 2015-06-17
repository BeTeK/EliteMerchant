
import ui.GuideTabUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QVariant
import ui.TabAbstract

class GuideTab(ui.GuideTabUI.Ui_Dialog, QtWidgets.QWidget, ui.TabAbstract.TabAbstract):
    def __init__(self, db, analyzer, tabName, mainWindow):
        super(QtWidgets.QWidget, self).__init__()
        self.setupUi(self)

        self.mainWindow = mainWindow
        self.tabName = tabName

    def setTabName(self, name):
        self.tabName = name

    def getType(self):
        return "guide"

    def getTabName(self):
        return "User Guide"

    def dispose(self):
        pass
