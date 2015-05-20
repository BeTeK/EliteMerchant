
import ui.MainWindowUI
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QVariant
import Options

class MainWindow(QtWidgets.QMainWindow, ui.MainWindowUI.Ui_MainWindow):
  def __init__(self, db):
    super(QtWidgets.QMainWindow, self).__init__()
    self.setupUi(self)
    self.retranslateUi(self)
    self.result = []
    self.currentSystem = None
    self.searchBtn.clicked.connect(self.searchBtnPressed)
    self.db = db
    self.model = MainWindow.TableModel(None, self)
    self.SearchResultTable.setModel(self.model)
    self._readSettings()

  def searchBtnPressed(self):

    #self.searchBtn.setText('- - - - S e a r c h i n g - - - -') # unfortunately these never show with synchronous ui

    currentSystem = self.currentSystemTxt.text()
    windowSize = float(self.windowSizeTxt.text())
    maxDistance = float(self.maxDistanceTxt.text())
    minProfit = int(self.minProfitTxt.text())
    minPadSize = int(self.minPadSize.currentIndex())
    #twoway = bool(self.twoWayBool.????)
    systems = self.db.getSystemByName(currentSystem)

    if len(systems) == 0:
      return

    system = systems[0]
    pos = system.getPosition()

    self.currentSystem=system
    self.result = self.db.queryProfitWindow(pos[0], pos[1], pos[2], windowSize, maxDistance, minProfit,minPadSize)
    self.model.refeshData()

    #self.searchBtn.setText('Search')

  def _readSettings(self):
    self.restoreGeometry(Options.get("MainWindow-geometry", QtCore.QByteArray()))
    self.restoreState(Options.get("MainWindow-state", QtCore.QByteArray()))

  def closeEvent(self, event):
    Options.set("MainWindow-geometry", self.saveGeometry())
    Options.set("MainWindow-state", self.saveState())
    
  class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mw):
      super().__init__(parent)
      self.mw = mw

    def rowCount(self, parent):
      rows = len(self.mw.result)
      return rows

    def columnCount(self, parent):
      return 10

    def data(self, index, role):
      if not index.isValid():
        return None

      # roles:  http://doc.qt.io/qt-5/qt.html#ItemDataRole-enum

      if role == QtCore.Qt.BackgroundRole:
        section=index.column()
        if section in [1, 2, 6, 7]:
          return QtGui.QBrush(QtGui.QColor(255,255,230))
        if section in [9]:
          return QtGui.QBrush(QtGui.QColor(230,255,255))
        if section in [4]:
          return QtGui.QBrush(QtGui.QColor(255,230,255))




      if index.row() >= len(self.mw.result):
        return None

      data = self.mw.result[index.row()]

      if role == QtCore.Qt.ToolTipRole:
        section=index.column()
        if section == 0:
          if self.mw.currentSystem is None:
            return
          else:
            curname=self.mw.currentSystem.getName()
            pos=self.mw.currentSystem.getPosition()
            dist=( (pos[0]-data["Ax"])**2 + (pos[1]-data["Ay"])**2 + (pos[2]-data["Az"])**2 ) ** 0.5
            return "Distance from "+curname+" (current system)\nto "+data["Asystemname"]+" (commodity seller) is "+("%.2f" % dist)+"ly"
        elif section in [1,2]:
          padsize={
            None:"unknown",
            0:'S',
            1:'M',
            2:'L'
          }
          returnstring=""
          returnstring+="System: "+data["Asystemname"]+"\n"
          returnstring+="Coordinates: "+str(data["Ax"])+", "+str(data["Ay"])+", "+str(data["Az"])+"\n"
          returnstring+="Station: "+data["Abasename"]+"\n"
          returnstring+="Distance to star: "+str(data["Adistance"])+"\n"
          returnstring+="Landing pad size: "+padsize[data["AlandingPadSize"]]
          return returnstring
        elif section == 3:
          return "Export sales price: "+str(data["AexportPrice"])+"\nSupply: "+str(data["Asupply"])
        elif section == 4:
          return "Commodity "+data["commodityname"]+ "\nGalactic average price: "+str(data["average"])
        elif section == 5:
          return "Import buy price: "+str(data["BimportPrice"])+"\nDemand: "+str(data["Bdemand"])
        elif section in [6,7]:
          padsize={
            None:"unknown",
            0:'S',
            1:'M',
            2:'L'
          }
          returnstring=""
          returnstring+="System: "+data["Bsystemname"]+"\n"
          returnstring+="Coordinates: "+str(data["Bx"])+", "+str(data["By"])+", "+str(data["Bz"])+"\n"
          returnstring+="Station: "+data["Bbasename"]+"\n"
          returnstring+="Distance to star: "+str(data["Bdistance"])+"\n"
          returnstring+="Landing pad size: "+padsize[data["BlandingPadSize"]]
          return returnstring
        elif section == 8:
          return "Travel distance "+str(data["DistanceSq"]**0.5)+"ly + "+str(data["Bdistance"])+"ls from star to station"
        elif section == 9:
          return "Buy for "+str(data["AexportPrice"])+"\nSell for "+str(data["BimportPrice"])+"\nProfit:  "+str(data["profit"])
        else:
          return None

      if role != QtCore.Qt.DisplayRole:
        return None

      # copypasteable column defs
      section=index.column()
      if section == 0:
        if self.mw.currentSystem is None:
          return '?'
        else:
          pos=self.mw.currentSystem.getPosition()
          dist=( (pos[0]-data["Ax"])**2 + (pos[1]-data["Ay"])**2 + (pos[2]-data["Az"])**2 ) ** 0.5
          return "%.2f" % dist # two decimals
      elif section == 1:
        field="Asystemname"
      elif section == 2:
        field="Abasename"
      elif section == 3:
        field="AexportPrice"
      elif section == 4:
        field="commodityname"
      elif section == 5:
        field="BimportPrice"
      elif section == 6:
        field="Bsystemname"
      elif section == 7:
        field="Bbasename"
      elif section == 8:
        return data["DistanceSq"] ** 0.5
      elif section == 9:
        field="profit"
      else:
        return None

      return data[field]

    def headerData(self, section, orientation, role):
      if role != QtCore.Qt.DisplayRole:
        return None
      
      if orientation != QtCore.Qt.Horizontal:
        return None
      
      # copypasteable column defs
      if section == 0:
        #field="Curr.Dist."
        if self.mw.currentSystem is None:
          sysname = 'here'
        else:
          sysname = self.mw.currentSystem.getName()
        field="Dist.from "+sysname

      elif section == 1:
        field="From System"
      elif section == 2:
        field="From Station"
      elif section == 3:
        field="Export Cr"
      elif section == 4:
        field="Commodity"
      elif section == 5:
        field="Import Cr"
      elif section == 6:
        field="To System"
      elif section == 7:
        field="To Station"
      elif section == 8:
        field="Distance"
      elif section == 9:
        field="Profit Cr"
      else:
        return None

      return field

    def refeshData(self):
      self.beginResetModel()
      self.endResetModel()
      self.dataChanged.emit(self.createIndex(0,0), self.createIndex(8, len(self.mw.result)), [])
