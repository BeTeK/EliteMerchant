
import ui.MainWindowUI
import ui.Options
import ui.SearchTab
import ui.Status
import ui.Options
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QVariant
import Options
import Queries
import datetime
import EDDB
import EliteLogAnalyzer
import ui.EdceVerification
import EdceWrapper
import SpaceTime
import time

class MainWindow(QtWidgets.QMainWindow, ui.MainWindowUI.Ui_MainWindow):
  _edceUpdateTimeout = 90 # 2 min timeout to keep fd happy

  def __init__(self, db):
    super(QtWidgets.QMainWindow, self).__init__()
    self.setupUi(self)
    self.currentStatus = None
    self.optionsMenu.triggered.connect(self._optionsMenuSelected)
    self.exitMenu.triggered.connect(self._exitMenuSelected)
    self.searchMenuItem.triggered.connect(self._addSearchTabSelected)
    self.statusMenuItem.triggered.connect(self._addStatusTabSelected)
    self.db = db
    self.analyzer = EliteLogAnalyzer.EliteLogAnalyzer()
    self.analyzer.setPath(Options.get("Elite-path", ""))
    self._updateEdceIntance()
    self.edceLastUpdated = int(datetime.datetime.now().timestamp())
    self.edceLastUpdateInfo = None
    self.verificationCode = None
    self.startVerification = False

    self.timer = QtCore.QTimer(self)
    self.timer.timeout.connect(self.onTimerEvent)
    self.timer.start(1000)
#    self.tabItems = [("Search", ui.SearchTab.SearchTab(self.db, self.analyzer, "1")),
#                     ("Status", ui.Status.Status(self.db, self.analyzer))]
    self.tabItems = []

    self.mainTab.setTabsClosable(True)
    self.mainTab.tabCloseRequested.connect(self._onTabClosing)

    self._readSettings()
    self._updateTabs()

  def _onTabClosing(self, closeIndex):
    del self.tabItems[closeIndex]


    for index, value in enumerate(self.tabItems):
      value[1].setTabName(index + 1)
      self.tabItems[index] = (value[1].getTabName(), value[1])

    self._updateTabs()

  def _updateTabs(self):
    self.mainTab.clear()

    index = 0
    for name, widget in self.tabItems:
      index += 1
      widget.setTabName(str(index))
      self.mainTab.addTab(widget, QtGui.QIcon(), name)

  def _addTab(self, widget):
    index = len(self.tabItems) + 1
    widget.setTabName(str(index))
    item = (widget.getTabName(), widget)
    self.tabItems.append(item)
    self._updateTabs()

  def _addStatusTabSelected(self):
    self._addTab(ui.Status.Status(self.db, self.analyzer, "", self))

  def _addSearchTabSelected(self):
    self._addTab(ui.SearchTab.SearchTab(self.db, self.analyzer, "", self))

  def _exitMenuSelected(self):
    self.close()

  def _readSettings(self):
    self.restoreGeometry(Options.get("MainWindow-geometry", QtCore.QByteArray()))
    self.restoreState(Options.get("MainWindow-state", QtCore.QByteArray()))

    self.cargoSizeTxt.setText(Options.get("ship_cargo_size", "100"))
    self.jumpRangeTxt.setText(Options.get("ship_jump_range", "15"))
    self.minPadSizeCombo.setCurrentIndex(int(Options.get("ship_landing_pad_size", "0")))

    tabCount = int(Options.get("main_window_tab_count", "0"))

    for index in range(tabCount):
      type = Options.get("main_window_tab_{0}_type".format(index), "")

      if type == "search":
        item = ("Search {0}".format(index + 1), ui.SearchTab.SearchTab(self.db, self.analyzer, str(index + 1),self))
      elif type == "status":
        item = ("Status {0}".format(index + 1), ui.Status.Status(self.db, self.analyzer, str(index + 1),self))

      self.tabItems.append(item)

  def closeEvent(self, event):
    Options.set("main_window_tab_count", len(self.tabItems))
    index = 0
    for name, widget in self.tabItems:
      Options.set("main_window_tab_{0}_type".format(index), widget.getType())
      widget.dispose()
      index += 1

    Options.set("ship_cargo_size", self.cargoSizeTxt.text())
    Options.set("ship_jump_range", self.jumpRangeTxt.text())
    Options.set("ship_landing_pad_size", self.minPadSizeCombo.currentIndex())

    Options.set("MainWindow-geometry", self.saveGeometry())
    Options.set("MainWindow-state", self.saveState())
    self._setInfoText("Waiting for EDCE fetch to complete")
    self.timer.stop()
    if self.edce is not None:
      self.edce.join()

  def _updateEdceIntance(self):
    self.edce = None
    try:
      self.edce = EdceWrapper.EdceWrapper(Options.get("EDCE-path", ""), self.db, self._verificationCheck)
    except Exception as ex:
      print(ex)

  def _setInfoText(self, txt = ""):
    self.statusMessageTxt.setText(txt)

  def onGetCurrentSystemBtnClicked(self):
    if self.currentStatus is None:
      return
    self._setCurrentSystemByname()


  def _setCurrentSystemByname(self):
      systemName = self.analyzer.getCurrentStatus()["System"]
      self.currenlyAtSystemTxt.setText(systemName)
      systems = self.db.getSystemByName(systemName)
      if len(systems) == 0:
          return
      for tab in self.tabItems:
        if tab[1].searchType==0 and self.analyzer.hasDockPermissionGot():
          tab[1].currentSystem = systems[0]
          tab[1].currentSystemTxt.setText(systemName)
          tab[1].model.refeshData()
          tab[1].searchBtnPressed()
        if tab[1].searchType==1:
          tab[1].currentSystem = systems[0]
          tab[1].currentSystemTxt.setText(systemName)
          tab[1].model.refeshData()
          tab[1].searchBtnPressed()

  def onTimerEvent(self):
    self._updateIfNeededEDDB()
    self._checkCurrentStatus()
    self._checkEDCE()
    self._checkVerificationWindow()

  def _checkVerificationWindow(self):
    if self.startVerification:
        self.startVerification = False
        result = self._showVerificationDialog()
        if result is None:
            result = ""
        self.verificationCode = result

  def _showVerificationDialog(self):
      dialog = ui.EdceVerification.EdceVerification(self)
      dialog.setModal(True)
      dialog.exec()
      return dialog.getResult()

  def _verificationCheck(self):
    self.startVerification = True
    while self.verificationCode is None:
        time.sleep(0.1)

    code = self.verificationCode
    self.verificationCode = None
    return code

  def _checkEDCE(self):
    if self.edce is None:
      return

    result = self.edce.updateResults()
    info = self.edce.getLastUpdatedInfo()

    if result:
      self._setInfoText()

    if info["docked"]:
      self.edceLastUpdated = info

    if self.analyzer.getCurrentStatus()["System"] == info["systemName"] and \
        self.analyzer.getCurrentStatus()["Near"] == info["starportName"]:
      return

    if not self.analyzer.hasDockPermissionGot():
      return

    now = int(datetime.datetime.now().timestamp())
    if now - self.edceLastUpdated < MainWindow._edceUpdateTimeout:
      return

    self.edceLastUpdated = now
    self.edce.fetchNewInfo()
    self._setInfoText("Fetching current station data from EDCE")

  def _checkCurrentStatus(self):
    if self.analyzer.poll():
      status = self.analyzer.getCurrentStatus()
      self.currenlyAtSystemTxt.setText(status["System"])
      self.currentlyNearAtTxt.setText(status["Near"])
      #if self.analyzer.hasDockPermissionGot():
      self._setCurrentSystemByname()

  def _updateIfNeededEDDB(self):
    interval = int(Options.get("EDDB-check-interval", 1))
    lastUpdated = int(Options.get("EDDB-last-updated", -1))
    now = datetime.datetime.now().timestamp()

    if interval <= 0:
      return

    if lastUpdated <= 0 or now - lastUpdated > interval * 60 * 60:
      EDDB.update(self.db)


  def _optionsMenuSelected(self):
    options = ui.Options.Options(self.db, self.analyzer)
    options.setModal(True)
    options.exec()


