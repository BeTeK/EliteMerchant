import ui.CommodityTabUI
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

class CommodityTab(QtWidgets.QWidget, ui.CommodityTabUI.Ui_Dialog, ui.TabAbstract.TabAbstract):
    def __init__(self, db, analyzer, tabName, mainwindow):
        super(QtWidgets.QWidget, self).__init__()
        self.setupUi(self)
        self.tabName = tabName
        self.db = db
        self.mainwindow = mainwindow
        self.result = []
        self.currentSystem = None
        self.searchType=0
        self.searchBtn.clicked.connect(self.searchBtnPressed)
        self.model = CommodityTab.TableModel(None, self)
        self.SearchResultTable.setModel(self.model)
        self.getCurrentBtn.clicked.connect(self._setCurrentSystemByname)
        self.analyzer = analyzer
        commodities=db.getCommodities()
        if commodities is not None:
          self.commoditylist=list(db.getCommodities().values())
          self.commoditylist.sort(key=lambda x: x.name )
        else:
          self.commoditylist=[]
        self.commodityCombobox.clear()
        self.commodityCombobox.addItems( [c.getName() for c in self.commoditylist] )
        systemlist=self.db.getSystemNameList()
        self.currentSystemCombo.clear()
        self.currentSystemCombo.addItems( systemlist )
        self._restoreSearchStatus()

    def setTabName(self, name):
        self.tabName = name

    def getTabName(self):
        return "Commodities {0}".format(self.tabName)

    def getType(self):
        return "commodity"

    def dispose(self):
        self._saveSearchStatus()

    def _optName(self, name):
        return "search_tab__{0}_{1}".format(name, self.tabName)

    def _restoreSearchStatus(self):
        self.currentSystemCombo.setCurrentText(Options.get(self._optName("current_system"), "Sol"))
        self.maxDistanceSpinBox.setValue(int(Options.get(self._optName("maximum_distance"), "200")))
        self.importComboBox.setCurrentIndex(int(Options.get(self._optName("importexport"), "0")))
        self.commodityCombobox.setCurrentIndex(int(Options.get(self._optName("commodity"), "0")))

    def _saveSearchStatus(self):
        Options.set(self._optName("current_system"), self.currentSystemCombo.currentText())
        Options.set(self._optName("maximum_distance"), self.maxDistanceSpinBox.value())
        Options.set(self._optName("importexport"), self.importComboBox.currentIndex())
        Options.set(self._optName("commodity"), self.commodityCombobox.currentIndex())

    def _setCurrentSystemByname(self):
        systemName = self.analyzer.getCurrentStatus()["System"]
        self.currentSystemCombo.setCurrentText(systemName)
        systems = self.db.getSystemByName(systemName)
        if len(systems) == 0:
            return
        self.currentSystem = systems[0]
        self.model.refeshData()


    def searchBtnPressed(self):
        #print ("searchBtnPressed")
        #self.searchBtn.setText('- - - - S e a r c h i n g - - - -') # unfortunately these never show with synchronous ui

        currentSystem = self.currentSystemCombo.currentText()

        maxDistance = float(self.maxDistanceSpinBox.value())
        jumprange = float(self.mainwindow.jumpRangeSpinBox.value())
        minPadSize = int(self.mainwindow.minPadSizeCombo.currentIndex())
        importexport=int(self.importComboBox.currentIndex())
        commodityidx=int(self.commodityCombobox.currentIndex())
        if commodityidx==-1:
          return
        commodityid=self.commoditylist[commodityidx].getId()


        systems = self.db.getSystemByName(currentSystem)
        if len(systems) == 0:
          print("system not found!")
          return
        self.currentSystem = systems[0]
        pos = self.currentSystem.getPosition()


        print("Querying database...")

        self.result = Queries.queryCommodities(self.db, pos[0], pos[1], pos[2], maxDistance, minPadSize,jumprange ,importexport,commodityid)

        self.model.refeshData()

        print("Done!")

            #self.searchBtn.setText('Search')

    class TableModel(QtCore.QAbstractTableModel):
        def __init__(self, parent, mw):
            super().__init__(parent)
            self.mw = mw
            basictradetable=[
                    "SystemDistance",
                    "hours",
                    "systemname",
                    "basename",
                    "importPrice",
                    "importPavg",
                    "commodityname",
                    "exportPrice",
                    "exportPavg",
                    #"averagedeviation"
                ]
            self.columnorder=[
                basictradetable,
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

            # roles:    http://doc.qt.io/qt-5/qt.html#ItemDataRole-enum

            if role == QtCore.Qt.BackgroundRole: # background colors
                if "celltype" in data:
                    if data["celltype"]=='emptyrow':
                        return QtGui.QBrush(QtGui.QColor(255,255,255))
                    if data["celltype"]=='separatorrow':
                        return QtGui.QBrush(QtGui.QColor(200,200,200))
                if columnorder[section] in ["systemname","basename"]:
                    return QtGui.QBrush(QtGui.QColor(255,255,230))
                if columnorder[section] in ["commodityname"]:
                    r,g,b=self.mw.AgeToColor(data['lastUpdated'])
                    return QtGui.QBrush(QtGui.QColor(r,g,b))
                if columnorder[section] in ["profit","Cprofit","totalprofit"]:
                    return QtGui.QBrush(QtGui.QColor(255,230,255))

            if role == QtCore.Qt.ToolTipRole: # tooltips

                if columnorder[section] == "_curdist":
                    if self.mw.currentSystem is None:
                        return
                    else:
                        curname=self.mw.currentSystem.getName() # todo: ship range
                        pos=self.mw.currentSystem.getPosition()
                        dist=( (pos[0]-data["x"])**2 + (pos[1]-data["y"])**2 + (pos[2]-data["z"])**2 ) ** 0.5
                        return "Distance from "+curname+" (current system)\n" \
                            "to "+data["systemname"]+" (commodity seller) is "+("%.2f" % dist)+"ly " \
                            "("+str("%.2f" % (SpaceTime.BaseToBase(dist)/60))+"min)"
                elif columnorder[section] in ["systemname","basename"]:
                    padsize={
                        None:"unknown",
                        0:'S',
                        1:'M',
                        2:'L'
                    }
                    returnstring=""
                    returnstring+="System: "+data["systemname"]+"\n"
                    returnstring+="Station: "+data["basename"]+"\n"
                    returnstring+="Distance to star: "+str(data["distance"] is not None and (str(data["distance"])
                    +" ("+str("%.2f" % (SpaceTime.StarToBase(data["distance"])/60))+"min)") or "unknown")+"\n"
                    returnstring+="Landing pad size: "+padsize[data["landingPadSize"]]
                    return returnstring
                elif columnorder[section] == "exportPrice":
                    return "Export sales price: "+str(data["exportPrice"])+"\nSupply: "+str(data["supply"])
                elif columnorder[section] == "commodityname":
                    return "Commodity "+data["commodityname"]\
                           +"\nData "+str("%.2f" %((time.time()-data['lastUpdated'])/(60*60*24)))+" days old"\
                           +"\nBuy for "+str(data["exportPrice"])\
                           +"\nSell for "+str(data["importPrice"])\
                           +"\nGalactic average price: "+str(data["average"])
                elif columnorder[section] == "importPrice":
                    return "Import buy price: "+str(data["importPrice"])+"\nDemand: "+str(data["demand"])
                elif columnorder[section] == "DistanceSq":
                    return "Travel distance "+str(data["DistanceSq"]**0.5)+"ly + "+\
                                str(data["distance"] is not None and data["distance"] or "unknown")+"ls from star to station"
                elif columnorder[section] == "SystemDistance":
                    return "Travel distance "+str(data["SystemDistance"])+"ly + "+\
                                str(data["distance"] is not None and data["distance"] or "unknown")+"ls from star to station\n"+\
                                str(data["distance"] is not None and str("%.2f" % (SpaceTime.StarToBase(data["distance"])/60))+"min" or "")
                elif columnorder[section] == "profit":
                    return "Buy for "+str(data["exportPrice"])\
                                 +"\nSell for "+str(data["importPrice"])
                elif columnorder[section] == "Cprofit":
                    return "Buy for "+str(data["BexportPrice"])\
                                 +"\nSell for "+str(data["CimportPrice"])
                else:
                    return None

            if role == QtCore.Qt.DisplayRole: # visible text data
                if section >=len(columnorder):
                        return None

                if columnorder[section] == "_curdist":
                    if self.mw.currentSystem is None:
                        return '?'
                    else:
                        pos=self.mw.currentSystem.getPosition()
                        dist=( (pos[0]-data["x"])**2 + (pos[1]-data["y"])**2 + (pos[2]-data["z"])**2 ) ** 0.5
                        return "%.2f" % dist # two decimals
                elif columnorder[section] == "hours":
                    return str(int(data["hours"]*60*10)/10)
                else:
                    return data[columnorder[section]]

            return None # default when nothing matches

        def headerData(self, section, orientation, role):
            if role == QtCore.Qt.DisplayRole: # visible text data

                if orientation != QtCore.Qt.Horizontal:
                    return None

                columnorder=self.columnorder[self.mw.searchType]

                if columnorder[section] in ["SystemDistance"]:
                    #field="Curr.Dist."
                    if self.mw.currentSystem is None:
                        sysname = 'here'
                    else:
                        sysname = self.mw.currentSystem.getName()
                    field="Dist.from "+sysname
                elif columnorder[section] == "systemname":
                    field="System"
                elif columnorder[section] == "basename":
                    field="Station"
                elif columnorder[section] == "exportPrice":
                    field="Export Cr"
                elif columnorder[section] in ["commodityname","Ccommodityname"]:
                    field="Commodity"
                elif columnorder[section] == "importPrice":
                    field="Import Cr"
                elif columnorder[section] == "hours":
                    field="Minutes travel"
                elif columnorder[section] in [ "exportPavg","importPavg"]:
                    field="% of average"
                else:
                    return columnorder[section]

                return field

            return None # default when nothing matches


        def refeshData(self):
            self.beginResetModel()
            self.endResetModel()
            #self.dataChanged.emit(self.createIndex(0,0), self.createIndex(self.columnCount(1), len(self.mw.result)), [])
            self.dataChanged.emit(self.createIndex(0,0), self.createIndex(8, len(self.mw.result)), [])
            # reset scroll
            self.mw.SearchResultTable.verticalScrollBar().setSliderPosition(0)
