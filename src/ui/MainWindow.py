
import ui.MainWindowUI
import ui.Options
import ui.SearchTab
import ui.CommodityTab
import ui.Status
import ui.DBloadingTab
import ui.GuideTab
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
import Sounds
import time
import sys
import PassThroughFile
from time import gmtime, strftime
import ThreadWorker

class MainWindow(QtWidgets.QMainWindow, ui.MainWindowUI.Ui_MainWindow):
  _edceUpdateTimeout = 90 # keep sparse to keep fd happy
  _logLinesToShow = 200
  edceFinished = QtCore.pyqtSignal([dict])
  dbupdated = QtCore.pyqtSignal()

  def __init__(self, db):
    super(QtWidgets.QMainWindow, self).__init__()
    self.setupUi(self)
    self._setupLog()
    self.currentStatus = None
    self.optionsMenu.triggered.connect(self._optionsMenuSelected)
    self.exitMenu.triggered.connect(self._exitMenuSelected)
    self.searchMenuItem.triggered.connect(self._addSearchTabSelected)
    self.statusMenuItem.triggered.connect(self._addStatusTabSelected)
    self.commodityMenuItem.triggered.connect(self._addCommodityTabSelected)
    self.guideMenuItem.triggered.connect(self._addGuideTabSelected)
    self.edceFinished.connect(self.onEdceUpdated)
    self.db = db
    self.analyzer = EliteLogAnalyzer.EliteLogAnalyzer()
    self.analyzer.setPath(Options.get("Elite-path", ""))
    self._updateEdceInstance()
    self.edceLastUpdated = int(datetime.datetime.now().timestamp()) -self._edceUpdateTimeout +15
    self.edceLastUpdateInfo = None
    self.verificationCode = None
    self.startVerification = False
    self.sounds=Sounds.Sounds()

    self.timer = QtCore.QTimer(self)
    self.timer.timeout.connect(self.onTimerEvent)
    self.timer.start(1000)
    self.tabItems = []

    self.mainTab.setTabsClosable(True)
    self.mainTab.tabCloseRequested.connect(self._onTabClosing)

    #self.mainTab.currentChanged.connect(self._onTabChanged)

    newbutton=QtWidgets.QPushButton("New Search",self.mainTab)
    newbutton.clicked.connect(self._addSearchTabSelected)
    buttonlayout=QtWidgets.QStackedLayout()
    buttonlayout.addWidget(newbutton)
    buttonwidget=QtWidgets.QWidget()
    buttonwidget.setLayout(buttonlayout)

    self.mainTab.setCornerWidget ( buttonwidget, 0)

    self.edceState = "notStation"

    if self.db.dbEmpty:
      print("db load failed or doesn't exist - downloading...")
      self.dbupdated.connect(self.loadSettingsAndUI)

      # display 'db downloading' tab
      self.mainTab.clear()
      widget=ui.DBloadingTab.DBloadingTab(self.db, self.analyzer, "", self)
      widget.setTabName(str(1))
      #item = (widget.getTabName(), widget)
      self.mainTab.addTab(widget, QtGui.QIcon(), 'DB loading...')

      self.mainTab.setEnabled(False)
      ThreadWorker.ThreadWorker(lambda: EDDB.update(self.db,force=True), lambda result: self.dbupdated.emit() ).start()
    else:
      self.loadSettingsAndUI()

  def loadSettingsAndUI(self):
    self.mainTab.setEnabled(True)
    self._readSettings()
    self._updateTabs()
    self.sounds.play("startup")


  def _setupLog(self):
    curStdOut = sys.stdout
    file = PassThroughFile.PassThroughFile(curStdOut)
    sys.stdout = file
    file.addListener(self._lineAddedToLog)

  def _lineAddedToLog(self, txt):
    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    stdOutLine = txt.replace("\r", "").replace("\n", "")
    if len(stdOutLine) == 0:
      return

    line = "[{0}] {1}".format(now, stdOutLine)
    self.logCombo.insertItem(0, line)

    while self.logCombo.count() > MainWindow._logLinesToShow:
      self.logCombo.removeItem(self.logCombo.count() - 1)

    self.logCombo.setCurrentIndex(0)

  def _onTabChanged(self, idx):
    pass

  def _onTabClosing(self, closeIndex):
    del self.tabItems[closeIndex]

    for index, value in enumerate(self.tabItems):
      value[1].setTabName(index + 1)
      self.tabItems[index] = (value[1].getTabName(), value[1])

    self._updateTabs()

  def _updateTabs(self):
    if len(self.tabItems)==0: # there should always be some tab open
      self._addSearchTabSelected()
      return

    self.mainTab.clear()

    index = 0
    for name, widget in self.tabItems:
      index += 1
      widget.setTabName(str(index))
      #name=widget.searchTypeCombo.currentText()
      self.mainTab.addTab(widget, QtGui.QIcon(), name)

  def _addTab(self, widget):
    index = len(self.tabItems) + 1
    widget.setTabName(str(index))
    item = (widget.getTabName(), widget)
    self.tabItems.append(item)
    self._updateTabs()
    self.mainTab.setCurrentWidget(widget)

  def _addStatusTabSelected(self):
    self._addTab(ui.Status.Status(self.db, self.analyzer, "", self))

  def _addGuideTabSelected(self):
    self._addTab(ui.GuideTab.GuideTab(self.db, self.analyzer, "", self))

  def _addSearchTabSelected(self):
    self._addTab(ui.SearchTab.SearchTab(self.db, self.analyzer, "", self))

  def _addCommodityTabSelected(self):
    self._addTab(ui.CommodityTab.CommodityTab(self.db, self.analyzer, "", self))

  def _exitMenuSelected(self):
    self.close()

  def _readSettings(self):

    versionstring="?"
    try:
      with open("version.txt", "r") as f:
          versionstring = f.readline()
    except IOError:
      print("could not read version file")

    self.setWindowTitle("Elite Merchant   v"+versionstring)


    self.restoreGeometry(Options.get("MainWindow-geometry", QtCore.QByteArray()))
    self.restoreState(Options.get("MainWindow-state", QtCore.QByteArray()))

    self.cargoSizeSpinBox.setValue(int(Options.get("ship_cargo_size", "100")))
    self.jumpRangeSpinBox.setValue(float(Options.get("ship_jump_range", "16")))
    self.minPadSizeCombo.setCurrentIndex(int(Options.get("ship_landing_pad_size", "0")))

    tabCount = int(Options.get("main_window_tab_count", "0"))

    for index in range(tabCount):
      type = Options.get("main_window_tab_{0}_type".format(index), "")

      if type == "search":
        item = ("Search {0}".format(index + 1), ui.SearchTab.SearchTab(self.db, self.analyzer, str(index + 1),self))
      elif type == "status":
        item = ("Status {0}".format(index + 1), ui.Status.Status(self.db, self.analyzer, str(index + 1),self))
      elif type == "guide":
        item = ("User Guide", ui.GuideTab.GuideTab(self.db, self.analyzer, "", self))
      elif type == "commodity":
        item = ("Commodities {0}".format(index + 1), ui.CommodityTab.CommodityTab(self.db, self.analyzer, str(index + 1),self))

      self.tabItems.append(item)
    if len(self.tabItems)==0:
      self._addGuideTabSelected()

  def closeEvent(self, event):
    self.sounds.quit() # unload soundsystem

    for tab in self.tabItems: # shut down any searches in progress
      if tab[1].getType() == "search" and tab[1].currentWorker is not None:
        tab[1].currentWorker.terminate()
        tab[1].currentWorker = None

    Options.set("main_window_tab_count", len(self.tabItems))
    index = 0
    for name, widget in self.tabItems:
      Options.set("main_window_tab_{0}_type".format(index), widget.getType())
      widget.dispose()
      index += 1

    Options.set("ship_cargo_size", self.cargoSizeSpinBox.value())
    Options.set("ship_jump_range", self.jumpRangeSpinBox.value())
    Options.set("ship_landing_pad_size", self.minPadSizeCombo.currentIndex())

    Options.set("MainWindow-geometry", self.saveGeometry())
    Options.set("MainWindow-state", self.saveState())
    print("Waiting for EDCE fetch to complete")
    self.timer.stop()
    if self.edce is not None:
      self.edce.join()

  def _updateEdceInstance(self):
    self.edce = None
    try:
      postMarketData = Options.get("EDCE-uploads-results", "1") != "0"
      self.edce = EdceWrapper.EdceWrapper(Options.get("EDCE-path", ""), self.db, postMarketData, self._verificationCheck)
      self.edce.addFinishedListener(self._edceUpdated)

    except Exception as ex:
      print(ex)

  def onEdceUpdated(self, data):
    print(data)

  def _edceUpdated(self, data):
    self.edceFinished.emit(data)

  def _setInfoText(self, txt = ""):
    self.statusMessageTxt.setText(txt)

  def onGetCurrentSystemBtnClicked(self):
    if self.currentStatus is None:
      return
    self._setCurrentSystemToTabs()


  def _setCurrentSystemToTabs(self):

      if self.currentStatus is None or self.currentStatus['System'] == '':
          return

      triggeredasearch=False
      for tab in self.tabItems:
        if tab[1].getType() != "search":
          continue
        if tab[1].searchType==0 and self.analyzer.hasDockPermissionGot() and self.currentStatus['Base'] != '':
          tab[1].setCurrentSystem(self.currentStatus['System'])
          tab[1].setCurrentBase(self.currentStatus['Base'])
          tab[1].refreshData()
          tab[1].searchBtnPressed()
          triggeredasearch=True
        if tab[1].searchType==1:
          tab[1].setCurrentSystem(self.currentStatus['System'])
          tab[1].setCurrentBase(self.currentStatus['Base'])
          tab[1].refreshData()
          tab[1].searchBtnPressed()
          triggeredasearch=True

      if triggeredasearch:
        print('Triggered automatic search...')
        self.sounds.play('search')


  def onTimerEvent(self):
    self._updateIfNeededEDDB()
    analyzerupdated=self._checkCurrentStatus()
    edceupdated=self._checkEDCE()
    self._checkVerificationWindow()

    if self.edce is not None:
      self.edceUpToDateLabel.setText('EDCE')
      if edceupdated:
        self.edceUpToDateLabel.setStyleSheet("background:rgb(128,255,128)")
      else:
        self.edceUpToDateLabel.setStyleSheet("background:rgb(255,128,128)")


    if edceupdated:
      now = datetime.datetime.now().timestamp()
      #print("edceupdated  ",now-self.edce.resultsLastUpdated)
      if now-self.edce.resultsLastUpdated<1 and Options.get("search-auto-edce-enabled", "0")=='1':
        self._setCurrentSystemToTabs()
    elif analyzerupdated:
      #print("analyzerupdated")
      if Options.get("search-auto-log-enabled", "1")=='1':
        self._setCurrentSystemToTabs()

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
      return False

    now = int(datetime.datetime.now().timestamp())

    result = self.edce.updateResults()
    info = self.edce.getLastUpdatedInfo()

    if info["docked"]:
      self.edceLastUpdateInfo = info

    # log unreliable version - check if edce station is in analyzer system
    if self.edceLastUpdateInfo is not None and \
        self.currentStatus["System"] == self.edceLastUpdateInfo["systemName"]: # has data, systems match
      if self.currentStatus['Base']!='': # base already resolved
        return True

      # base not resolved - does it match edce report?
      if self.currentStatus['Base']=='' and \
        self.edceLastUpdateInfo["starportName"] in [o.getName() for o in self.db.getBasesOfSystemByName(self.currentStatus["System"])]:
        print('EDCE station data matching log')
        self.currentStatus['Base']=self.edceLastUpdateInfo["starportName"]
        self.currentlyNearAtTxt.setText(self.currentStatus["Base"])
        return True

    # log station version
    #if self.edceLastUpdateInfo is not None and \
    #    self.analyzer.getCurrentStatus()["System"] == self.edceLastUpdateInfo["systemName"] and \
    #    self.analyzer.getCurrentStatus()["Near"] == self.edceLastUpdateInfo["starportName"]:
    #  return True

    if now - self.edceLastUpdated < MainWindow._edceUpdateTimeout:
      return False

    if not self.analyzer.hasDockPermissionGot():
      return False

    self.edceLastUpdated = now
    self.edce.fetchNewInfo()
    print("Fetching current station data from EDCE")

  def _checkCurrentStatus(self):
    if self.analyzer.poll():
      newstatus = self.analyzer.getCurrentStatus()
      if self.currentStatus is not None and newstatus['System']==self.currentStatus['System'] and newstatus['Near']==self.currentStatus['Near']:
        return False
      else:
        self.currentStatus=newstatus

      if self.currentStatus["Near"] in [o.getName() for o in self.db.getBasesOfSystemByName(self.currentStatus["System"])]:
        self.currentStatus["Base"]=self.currentStatus["Near"]
      else:
        self.currentStatus["Base"]=''
      self.currenlyAtSystemTxt.setText(self.currentStatus["System"])
      self.currentlyNearAtTxt.setText(self.currentStatus["Base"])
      return True
    else:
      return False

  def _updateIfNeededEDDB(self):
    interval = int(Options.get("EDDB-check-interval", 1))
    lastUpdated = int(Options.get("EDDB-last-updated", -1))
    now = datetime.datetime.now().timestamp()

    if interval <= 0:
      return

    if lastUpdated <= 0 or now - lastUpdated > interval * 60 * 60:
      ThreadWorker.ThreadWorker(lambda :EDDB.update(self.db)).start()


  def _optionsMenuSelected(self):
    options = ui.Options.Options(self.db, self.analyzer,self)
    options.setModal(True)
    options.exec()


