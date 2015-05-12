
import ui.MainWindowUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QVariant

class MainWindow(QtWidgets.QMainWindow, ui.MainWindowUI.Ui_MainWindow):
  def __init__(self, db):
    super(QtWidgets.QMainWindow, self).__init__()
    self.setupUi(self)
    self.retranslateUi(self)
    self.result = []
    self.searchBtn.clicked.connect(self.searchBtnPressed)
    self.db = db
    self.model = MainWindow.TableModel(None, self)
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

    self.result = self.db.queryProfitWindow(pos[0], pos[1], pos[2], windowSize, maxDistance, minProfit)
    self.model.refeshData()

  class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mw):
      super().__init__(parent)
      self.mw = mw

    def rowCount(self, parent):
      rows = len(self.mw.result)
      return rows

    def columnCount(self, parent):
      return 8

    def data(self, index, role):
      if role != QtCore.Qt.DisplayRole:
        return None

      if not index.isValid():
        return None

      if index.row() >= len(self.mw.result):
        return None

      data = self.mw.result[index.row()]

      if index.column() == 0:
        return data["DistanceSq"] ** 0.5
      elif index.column() == 1:
        return data["BimportPrice"]
      elif index.column() == 2:
        return data["commodityname"]
      elif index.column() == 3:
        return data["Abasename"]
      elif index.column() == 4:
        return data["profit"]
      elif index.column() == 5:
        return data["Bbasename"]
      elif index.column() == 6:
        return data["Asystemname"]
      elif index.column() == 7:
        return data["Bsystemname"]
      else:
        return None

    def headerData(self, section, orientation, role):
      if role != QtCore.Qt.DisplayRole:
        return None
      
      if orientation != QtCore.Qt.Horizontal:
        return None
      
      if section == 0:
        return "DistanceSq"
      elif section == 1:
        return "BimportPrice"
      elif section == 2:
        return "commodityname"
      elif section == 3:
        return "Abasename"
      elif section == 4:
        return "profit"
      elif section == 5:
        return "Bbasename"
      elif section == 6:
        return "Asystemname"
      elif section == 7:
        return "Bsystemname"

    def refeshData(self):
      self.beginResetModel()
      self.endResetModel()
      self.dataChanged.emit(self.createIndex(0,0), self.createIndex(8, len(self.mw.result)), [])
