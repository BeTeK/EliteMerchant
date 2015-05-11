
import ui.MainWindowUI
from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow, ui.MainWindowUI.Ui_MainWindow):
  def __init__(self, db):
    super(QtWidgets.QMainWindow, self).__init__()
    self.setupUi(self)
    self.retranslateUi(self)
    self.searchBtn.clicked.connect(self.searchBtnPressed)
    self.db = db
    self.model = MainWindow.TableModel(None)
    self.SearchResultTable.setModel(self.model)

  def searchBtnPressed(self):
    currentSystem = self.currentSystemTxt.text()
    windowSize = float(self.windowSizeTxt.text())
    maxDistance = float(self.maxDistanceTxt.text())
    minProfit = int(self.minProfitTxt.text())
    systems = self.db.getSystemByName(currentSystem)
    if len(systems) == 0:
      return

    system = systems[0]
    pos = system.getPosition()
    self.db.queryProfitWindow(pos[0], pos[1], pos[2], windowSize, maxDistance, minProfit)
    
  class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent):
      super().__init__(parent)

    def rowCount(self, parent):
      return 1

    def columnCount(self, parent):
      return 2

    def data(self, index, role):
      if index.column() == 0:
        return "foo"
      elif index.column() == 1:
        return "bar"
      else:
        return None
