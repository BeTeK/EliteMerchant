
import ui.MainWindowUI
import ui.Options
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QVariant
import Options
import Queries
import datetime
import EDDB

class MainWindow(QtWidgets.QMainWindow, ui.MainWindowUI.Ui_MainWindow):
  def __init__(self, db):
    super(QtWidgets.QMainWindow, self).__init__()
    self.setupUi(self)
    self.retranslateUi(self)
    self.result = []
    self.currentSystem = None
    self.searchType=1
    self.searchBtn.clicked.connect(self.searchBtnPressed)
    self.optionsMenu.triggered.connect(self.optionsMenuSelected)
    self.db = db
    self.model = MainWindow.TableModel(None, self)
    self.SearchResultTable.setModel(self.model)
    self._readSettings()
    self.timer = QtCore.QTimer(self)

    self.timer.timeout.connect(self.onTimerEvent)
    self.timer.start(1000)

  def onTimerEvent(self):
    interval = int(Options.get("eddb-check-interval", 24))
    lastUpdated = int(Options.get("EDDB-last-updated", -1))
    now = datetime.datetime.now().timestamp()

    if interval <= 0:
      return

    if lastUpdated <= 0 or now - lastUpdated > interval * 60 * 60:
      EDDB.update(self.db)


  def optionsMenuSelected(self):
    options = ui.Options.Options(self.db)
    options.setModal(True)
    options.exec()

  def searchBtnPressed(self):

    #self.searchBtn.setText('- - - - S e a r c h i n g - - - -') # unfortunately these never show with synchronous ui

    currentSystem = self.currentSystemTxt.text()
    windowSize = float(self.windowSizeTxt.text())
    windows = int(self.windowCountTxt.text())
    maxDistance = float(self.maxDistanceTxt.text())
    minProfit = int(self.minProfitTxt.text())
    minPadSize = int(self.minPadSizeCombo.currentIndex())
    searchType = int(self.searchTypeCombo.currentIndex())
    graphDepth = int(self.graphDepthSpin.value())
    #twoway = bool(self.twoWayBool.isChecked())

    systems = self.db.getSystemByName(currentSystem)
    if len(systems) == 0:
      return
    system = systems[0]
    pos = system.getPosition()

    self.currentSystem=system
    self.searchType=searchType
    #self.twowaySearch=twoway

    print("Querying database...")
    if searchType==0:
      print("queryProfit")
      self.result = Queries.queryProfit(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minPadSize)
      #self.result = self.db.queryProfit(pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minPadSize)
    elif searchType==1:
      print("queryProfitRoundtrip")
      self.result = Queries.queryProfitRoundtrip(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minPadSize)
      #self.result = self.db.queryProfitRoundtrip(pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minPadSize)
    else:
      print("queryProfitGraph")
      self.result = Queries.queryProfitGraph(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minPadSize,graphDepth)

    self.model.refeshData()
    print("Done!")

    #self.searchBtn.setText('Search')

  def _readSettings(self):
    self.restoreGeometry(Options.get("MainWindow-geometry", QtCore.QByteArray()))
    self.restoreState(Options.get("MainWindow-state", QtCore.QByteArray()))

  def closeEvent(self, event):
    Options.set("MainWindow-geometry", self.saveGeometry())
    Options.set("MainWindow-state", self.saveState())
    self.timer.stop()

  class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mw):
      super().__init__(parent)
      self.mw = mw
      self.columnorder=[
        [
          "_curdist",
          "Asystemname",
          "Abasename",
          "AexportPrice",
          "commodityname",
          "BimportPrice",
          "Bsystemname",
          "Bbasename",
          "DistanceSq",
          "profit"
        ],
        [
          "_curdist",
          "Asystemname",
          "Abasename",
          "commodityname",
          "profit",
          "_Bcurdist",
          "Bsystemname",
          "Bbasename",
          "Ccommodityname",
          "Cprofit",
          "DistanceSq",
          "totalprofit"
        ],
        [
          "_curdist",
          "Asystemname",
          "Abasename",
          "AexportPrice",
          "commodityname",
          "BimportPrice",
          "Bsystemname",
          "Bbasename",
          "DistanceSq",
          "profit"
        ]
      ]


    def rowCount(self, parent):
      rows = len(self.mw.result)
      return rows

    def columnCount(self, parent):
      return len(self.columnorder[self.mw.searchType])


    def data(self, index, role):
      if not index.isValid():
        return None
      if index.row() >= len(self.mw.result):
        return None
      data = self.mw.result[index.row()]
      section=index.column()

      columnorder=self.columnorder[self.mw.searchType]

      if section >= len(columnorder):
        return None

      # roles:  http://doc.qt.io/qt-5/qt.html#ItemDataRole-enum

      if role == QtCore.Qt.BackgroundRole: # background colors
        if "celltype" in data:
          if data["celltype"]=='emptyrow':
            return QtGui.QBrush(QtGui.QColor(255,255,255))
          if data["celltype"]=='separatorrow':
            return QtGui.QBrush(QtGui.QColor(200,200,200))
        if columnorder[section] in ["Asystemname","Abasename","Bsystemname","Bbasename"]:
          return QtGui.QBrush(QtGui.QColor(255,255,230))
        if columnorder[section] in ["commodityname","Ccommodityname"]:
          return QtGui.QBrush(QtGui.QColor(230,255,255))
        if columnorder[section] in ["profit","Cprofit","totalprofit"]:
          return QtGui.QBrush(QtGui.QColor(255,230,255))

      if role == QtCore.Qt.ToolTipRole: # tooltips

        if self.mw.searchType==2:
          if columnorder[section] == "profit":
            """
            "averageprofit":loop["averageprofit"],
            "loopminprofit":loop["loopminprofit"],
            "loopmaxprofit":loop["loopmaxprofit"]
            """
            ret="Loop average profit: "+str(data["averageprofit"])+"\nLoop max profit: "+str(data["loopmaxprofit"])+"\nLoop min profit: "+str(data["loopmaxprofit"])
            if "celltype" not in data:
              ret+= "\nBuy for "+str(data["AexportPrice"])+"\nSell for "+str(data["BimportPrice"])+"\nProfit:  "+str(data["profit"])
            return ret
          else:
            if "celltype" in data:
              return None

        if columnorder[section] == "_curdist":
          if self.mw.currentSystem is None:
            return
          else:
            curname=self.mw.currentSystem.getName()
            pos=self.mw.currentSystem.getPosition()
            dist=( (pos[0]-data["Ax"])**2 + (pos[1]-data["Ay"])**2 + (pos[2]-data["Az"])**2 ) ** 0.5
            return "Distance from "+curname+" (current system)\nto "+data["Asystemname"]+" (commodity seller) is "+("%.2f" % dist)+"ly"
        elif columnorder[section] == "_Bcurdist":
          if self.mw.currentSystem is None:
            return
          else:
            curname=self.mw.currentSystem.getName()
            pos=self.mw.currentSystem.getPosition()
            dist=( (pos[0]-data["Bx"])**2 + (pos[1]-data["By"])**2 + (pos[2]-data["Bz"])**2 ) ** 0.5
            return "Distance from "+curname+" (current system)\nto "+data["Bsystemname"]+" (commodity seller) is "+("%.2f" % dist)+"ly"
        elif columnorder[section] in ["Asystemname","Abasename"]:
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
          returnstring+="Distance to star: "+str(data["Adistance"] is not None and data["Adistance"] or "unknown")+"\n"
          returnstring+="Landing pad size: "+padsize[data["AlandingPadSize"]]
          return returnstring
        elif columnorder[section] == "AexportPrice":
          return "Export sales price: "+str(data["AexportPrice"])+"\nSupply: "+str(data["Asupply"])
        elif columnorder[section] == "BexportPrice":
          return "Export sales price: "+str(data["BexportPrice"])+"\nSupply: "+str(data["Bsupply"])
        elif columnorder[section] == "commodityname":
          return "Commodity "+data["commodityname"]+ "\nBuy for "+str(data["AexportPrice"])+"\nSell for "+str(data["BimportPrice"])+"\nProfit:  "+str(data["profit"])+"\nGalactic average price: "+str(data["average"])
        elif columnorder[section] == "Ccommodityname":
          return "Commodity "+data["Ccommodityname"]+ "\nBuy for "+str(data["BexportPrice"])+"\nSell for "+str(data["CimportPrice"])+"\nProfit:  "+str(data["Cprofit"])+"\nGalactic average price: "+str(data["Caverage"])
        elif columnorder[section] == "BimportPrice":
          return "Import buy price: "+str(data["BimportPrice"])+"\nDemand: "+str(data["Bdemand"])
        elif columnorder[section] == "CimportPrice":
          return "Import buy price: "+str(data["CimportPrice"])+"\nDemand: "+str(data["Cdemand"])
        elif columnorder[section] in ["Bsystemname","Bbasename"]:
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
          returnstring+="Distance to star: "+str(data["Bdistance"] is not None and data["Bdistance"] or "unknown")+"\n"
          returnstring+="Landing pad size: "+padsize[data["BlandingPadSize"]]
          return returnstring
        elif columnorder[section] == "DistanceSq":
          return "Travel distance "+str(data["DistanceSq"]**0.5)+"ly + "+str(data["Bdistance"] is not None and data["Bdistance"] or "unknown")+"ls from star to station"
        elif columnorder[section] == "profit":
          return "Buy for "+str(data["AexportPrice"])+"\nSell for "+str(data["BimportPrice"])+"\nProfit:  "+str(data["profit"])
        elif columnorder[section] == "Cprofit":
          return "Buy for "+str(data["BexportPrice"])+"\nSell for "+str(data["CimportPrice"])+"\nProfit:  "+str(data["Cprofit"])
        else:
          return None

      if role == QtCore.Qt.DisplayRole: # visible text data
        if section >=len(columnorder):
            return None

        if "celltype" in data:
          if data["celltype"] in ['separatorrow']:
            if columnorder[section]=='profit':
              return "Average: "+str(data["averageprofit"])+"cr"
            else:
              return None
          else:
            return None

        if columnorder[section] == "_curdist":
          if self.mw.currentSystem is None:
            return '?'
          else:
            pos=self.mw.currentSystem.getPosition()
            dist=( (pos[0]-data["Ax"])**2 + (pos[1]-data["Ay"])**2 + (pos[2]-data["Az"])**2 ) ** 0.5
            return "%.2f" % dist # two decimals
        elif columnorder[section] == "_Bcurdist":
          if self.mw.currentSystem is None:
            return '?'
          else:
            pos=self.mw.currentSystem.getPosition()
            dist=( (pos[0]-data["Bx"])**2 + (pos[1]-data["By"])**2 + (pos[2]-data["Bz"])**2 ) ** 0.5
            return "%.2f" % dist # two decimals
        elif columnorder[section] == "DistanceSq":
          return data["DistanceSq"] ** 0.5
        else:
          return data[columnorder[section]]

      return None # default when nothing matches

    def headerData(self, section, orientation, role):
      if role == QtCore.Qt.DisplayRole: # visible text data

        if orientation != QtCore.Qt.Horizontal:
          return None

        columnorder=self.columnorder[self.mw.searchType]

        if columnorder[section] in ["_curdist","_Bcurdist"]:
          #field="Curr.Dist."
          if self.mw.currentSystem is None:
            sysname = 'here'
          else:
            sysname = self.mw.currentSystem.getName()
          field="Dist.from "+sysname
        elif columnorder[section] == "Asystemname":
          field="From System"
        elif columnorder[section] == "Abasename":
          field="From Station"
        elif columnorder[section] == "AexportPrice":
          field="Export Cr"
        elif columnorder[section] in ["commodityname","Ccommodityname"]:
          field="Commodity"
        elif columnorder[section] == "BimportPrice":
          field="Import Cr"
        elif columnorder[section] == "Bsystemname":
          field="To System"
        elif columnorder[section] == "Bbasename":
          field="To Station"
        elif columnorder[section] == "DistanceSq":
          field="Distance"
        elif columnorder[section] == "profit":
          field="Profit Cr"
        elif columnorder[section] == "Cprofit":
          field="Return Profit Cr"
        elif columnorder[section] == "totalprofit":
          field="Total Profit Cr"
        else:
          return None

        return field

      return None # default when nothing matches


    def refeshData(self):
      self.beginResetModel()
      self.endResetModel()
      #self.dataChanged.emit(self.createIndex(0,0), self.createIndex(self.columnCount(1), len(self.mw.result)), [])
      self.dataChanged.emit(self.createIndex(0,0), self.createIndex(8, len(self.mw.result)), [])
