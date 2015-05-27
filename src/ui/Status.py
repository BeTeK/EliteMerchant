
import ui.StatusUI
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


class Status(ui.StatusUI.Ui_Dialog, QtWidgets.QWidget):
    def __init__(self, db, analyzer, tabName):
        super(QtWidgets.QWidget, self).__init__()
        self.setupUi(self)

        self.tabName = tabName
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._onTimerEvent)
        self.timer.start(1000)
        self.analyzer = analyzer

    def setTabName(self, name):
        self.tabName = name

    def getType(self):
        return "status"

    def getTabName(self):
        return "Status {0}".format(self.tabName)

    def _onTimerEvent(self):
        self._checkCurrentStatus()

    def dispose(self):
        pass

    def _checkCurrentStatus(self):
        status = self.analyzer.getCurrentStatus()
        self.currenlyAtSystemTxt.setText(status["System"])
        self.currentlyNearAtTxt.setText(status["Near"])
        self.dockingRequestStatusTxt.setText("Requested" if self.analyzer.hasDockPermissionGot() else "Not requested")
        self.currentStatus = status
