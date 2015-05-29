import ui.SearchTabUI
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

class SearchTab(QtWidgets.QWidget, ui.SearchTabUI.Ui_Dialog, ui.TabAbstract.TabAbstract):
    def __init__(self, db, analyzer, tabName, mainwindow):
        super(QtWidgets.QWidget, self).__init__()
        self.setupUi(self)
        self.tabName = tabName
        self.db = db
        self.mainwindow = mainwindow
        self.result = []
        self.currentSystem = None
        self.searchType=1
        self.searchBtn.clicked.connect(self.searchBtnPressed)
        self.model = SearchTab.TableModel(None, self)
        self.SearchResultTable.setModel(self.model)
        self.getCurrentBtn.clicked.connect(self._setCurrentSystemByname)
        self.analyzer = analyzer

        self._restoreSearchStatus()

    def setTabName(self, name):
        self.tabName = name

    def getTabName(self):
        return "Search {0}".format(self.tabName)

    def getType(self):
        return "search"

    def dispose(self):
        self._saveSearchStatus()

    def _optName(self, name):
        return "search_tab__{0}_{1}".format(name, self.tabName)

    def _restoreSearchStatus(self):
        self.currentSystemTxt.setText(Options.get(self._optName("current_system"), "Sol"))
        self.maxDistanceTxt.setText(Options.get(self._optName("maximum_distance"), "30"))
        self.minProfitTxt.setText(Options.get(self._optName("minimum_profit"), "1000"))
        self.searchTypeCombo.setCurrentIndex(int(Options.get(self._optName("search_type"), "0")))
        self.searchType=int(Options.get(self._optName("search_type"), "0"))
        self.graphDepthSpin.setValue(int(Options.get(self._optName("search_max_depth"), "3")))
        self.graphMinDepthSpin.setValue(int(Options.get(self._optName("search_min_depth"), "1")))
        self.windowSizeTxt.setText(Options.get(self._optName("search_window_size"), "100"))
        self.windowCountTxt.setText(Options.get(self._optName("search_window_count"), "1"))
        self.profitPhChk.setChecked(Options.get(self._optName("search_profitPh"),"1")=="1")

    def _saveSearchStatus(self):
        Options.set(self._optName("current_system"), self.currentSystemTxt.text())
        Options.set(self._optName("maximum_distance"), self.maxDistanceTxt.text())
        Options.set(self._optName("minimum_profit"), self.minProfitTxt.text())
        Options.set(self._optName("search_window_size"), self.windowSizeTxt.text())
        Options.set(self._optName("search_window_count"), self.windowCountTxt.text())
        Options.set(self._optName("search_type"), self.searchTypeCombo.currentIndex())
        Options.set(self._optName("search_max_depth"), self.graphDepthSpin.value())
        Options.set(self._optName("search_min_depth"), self.graphMinDepthSpin.value())
        Options.set(self._optName("search_profitPh"), self.profitPhChk.isChecked() and "1" or "0")

    def _setCurrentSystemByname(self):
        systemName = self.analyzer.getCurrentStatus()["System"]
        self.currentSystemTxt.setText(systemName)
        systems = self.db.getSystemByName(systemName)
        if len(systems) == 0:
            return
        self.currentSystem = systems[0]
        self.model.refeshData()


    def searchBtnPressed(self):
        #print ("searchBtnPressed")
        #self.searchBtn.setText('- - - - S e a r c h i n g - - - -') # unfortunately these never show with synchronous ui

        currentSystem = self.currentSystemTxt.text()
        windowSize = float(self.windowSizeTxt.text())
        windows = int(self.windowCountTxt.text())
        maxDistance = float(self.maxDistanceTxt.text())
        jumprange = float(self.mainwindow.jumpRangeTxt.text())
        minProfit =None
        minProfitPh =None
        if bool(self.profitPhChk.isChecked()):
            minProfitPh = int(self.minProfitTxt.text())
        else:
            minProfit = int(self.minProfitTxt.text())
        minPadSize = int(self.mainwindow.minPadSizeCombo.currentIndex())
        searchType = int(self.searchTypeCombo.currentIndex())
        graphDepth = int(self.graphMinDepthSpin.value())
        graphDepthmax = int(self.graphDepthSpin.value())
        #twoway = bool(self.twoWayBool.isChecked())

        if (graphDepth>graphDepthmax):
          print("min hops have to be less than max hops!")
          return

        systems = self.db.getSystemByName(currentSystem)
        if len(systems) == 0:
          print("system not found!")
          return
        self.currentSystem = systems[0]
        pos = self.currentSystem.getPosition()

        self.searchType=searchType
        #self.twowaySearch=twoway

        print("Querying database...")
        if searchType==4:
            print("queryProfit")
            self.result = Queries.queryProfit(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize,jumprange )
            #self.result = self.db.queryProfit(pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minPadSize)
        elif searchType==2:
            print("queryProfitGraphLoops")
            self.result = Queries.queryProfitGraphLoops(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize,jumprange ,graphDepth,graphDepthmax)
        elif searchType==3:
            print("queryProfitGraphDeadends")
            self.result = Queries.queryProfitGraphDeadends(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize,jumprange ,graphDepth,graphDepthmax)
        elif searchType==0 or searchType==1:
            currentBase=None
            if self.analyzer.getCurrentStatus()['System'] == self.currentSystem:
              #if self.analyzer.hasDockPermissionGot():
              currentBase=self.analyzer.getCurrentStatus()["Near"]

            print("queryProfitGraphDeadends from current")
            self.result = Queries.queryProfitGraphDeadends(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize,jumprange ,graphDepth,graphDepthmax,currentSystem,currentBase)
        else:
            print("unknown search type - we should not be here")
        #elif searchType==1:
        #    print("queryProfitRoundtrip")
        #    self.result = Queries.queryProfitRoundtrip(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize)
        #    #self.result = self.db.queryProfitRoundtrip(pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minPadSize)

        self.model.refeshData()
        print("Done!")

            #self.searchBtn.setText('Search')

    class TableModel(QtCore.QAbstractTableModel):
        def __init__(self, parent, mw):
            super().__init__(parent)
            self.mw = mw
            basictradetable=[
                    "_curdist",
                    "Asystemname",
                    "Abasename",
                    "AexportPrice",
                    "commodityname",
                    "BimportPrice",
                    "Bsystemname",
                    "Bbasename",
                    #"DistanceSq",
                    "SystemDistance",
                    "profit",
                    "profitPh"
                ]
            twowaytradetable=[
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
                    #"DistanceSq",
                    "SystemDistance",
                    "totalprofit",
                    "profitPh"
                ]
            self.columnorder=[
                basictradetable,
                basictradetable,
                basictradetable,
                basictradetable,
                basictradetable
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
                if columnorder[section] in ["Asystemname","Abasename","Bsystemname","Bbasename"]:
                    return QtGui.QBrush(QtGui.QColor(255,255,230))
                if columnorder[section] in ["commodityname","Ccommodityname"]:
                    return QtGui.QBrush(QtGui.QColor(230,255,255))
                if columnorder[section] in ["profit","Cprofit","totalprofit"]:
                    return QtGui.QBrush(QtGui.QColor(255,230,255))

            if role == QtCore.Qt.ToolTipRole: # tooltips

                if "averageprofit" in data: # this is a graph search
                    if columnorder[section] == "profit":
                        ret="Loop average profit: "+str(data["averageprofit"])\
                            +"\nLoop max profit: "+str(data["loopmaxprofit"])\
                            +"\nLoop min profit: "+str(data["loopmaxprofit"])
                        if "celltype" not in data:
                            ret+= "\nBuy for "+str(data["AexportPrice"])\
                                +"\nSell for "+str(data["BimportPrice"])\
                                +"\nProfit:    "+str(data["profit"])
                        return ret
                    if columnorder[section] == "profitPh":
                        ret="Loop average profit: "+str(data["averageprofit"])\
                            +"\nLoop max profit: "+str(data["loopmaxprofit"])\
                            +"\nLoop min profit: "+str(data["loopmaxprofit"])
                        if "celltype" not in data:
                            ret+= "\nBuy for "+str(data["AexportPrice"])\
                                  +"\nSell for "+str(data["BimportPrice"])\
                                  +"\nProfit:    "+str(data["profit"])\
                                  +"\nProfit/h:"+str(int(data["profit"]/data["hours"]))
                        return ret
                    else:
                        if "celltype" in data:
                            return None

                if columnorder[section] == "_curdist":
                    if self.mw.currentSystem is None:
                        return
                    else:
                        curname=self.mw.currentSystem.getName() # todo: ship range
                        pos=self.mw.currentSystem.getPosition()
                        dist=( (pos[0]-data["Ax"])**2 + (pos[1]-data["Ay"])**2 + (pos[2]-data["Az"])**2 ) ** 0.5
                        return "Distance from "+curname+" (current system)\n" \
                            "to "+data["Asystemname"]+" (commodity seller) is "+("%.2f" % dist)+"ly " \
                            "("+str("%.2f" % (SpaceTime.BaseToBase(dist)/60))+"min)"
                elif columnorder[section] == "_Bcurdist":
                    if self.mw.currentSystem is None:
                        return
                    else:
                        curname=self.mw.currentSystem.getName() # todo: ship range
                        pos=self.mw.currentSystem.getPosition()
                        dist=( (pos[0]-data["Bx"])**2 + (pos[1]-data["By"])**2 + (pos[2]-data["Bz"])**2 ) ** 0.5
                        return "Distance from "+curname+" (current system)\n" \
                            "to "+data["Bsystemname"]+" (commodity seller) is "+("%.2f" % dist)+"ly " \
                            "("+str("%.2f" % (SpaceTime.BaseToBase(dist)/60))+"min)"
                elif columnorder[section] in ["Asystemname","Abasename"]:
                    padsize={
                        None:"unknown",
                        0:'S',
                        1:'M',
                        2:'L'
                    }
                    returnstring=""
                    returnstring+="System: "+data["Asystemname"]+"\n"
                    returnstring+="Station: "+data["Abasename"]+"\n"
                    returnstring+="Distance to star: "+str(data["Adistance"] is not None and (str(data["Adistance"])
                    +" ("+str("%.2f" % (SpaceTime.StarToBase(data["Adistance"])/60))+"min)") or "unknown")+"\n"
                    returnstring+="Landing pad size: "+padsize[data["AlandingPadSize"]]
                    return returnstring
                elif columnorder[section] == "AexportPrice":
                    return "Export sales price: "+str(data["AexportPrice"])+"\nSupply: "+str(data["Asupply"])
                elif columnorder[section] == "BexportPrice":
                    return "Export sales price: "+str(data["BexportPrice"])+"\nSupply: "+str(data["Bsupply"])
                elif columnorder[section] == "commodityname":
                    return "Commodity "+data["commodityname"]+ "\nBuy for "+str(data["AexportPrice"])+"\nSell for "+str(data["BimportPrice"])+"\nProfit:    "+str(data["profit"])+"\nGalactic average price: "+str(data["average"])
                elif columnorder[section] == "Ccommodityname":
                    return "Commodity "+data["Ccommodityname"]+ "\nBuy for "+str(data["BexportPrice"])+"\nSell for "+str(data["CimportPrice"])+"\nProfit:    "+str(data["Cprofit"])+"\nGalactic average price: "+str(data["Caverage"])
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
                    returnstring+="Station: "+data["Bbasename"]+"\n"
                    returnstring+="Distance to star: "+str(data["Bdistance"] is not None and (str(data["Bdistance"])
                    + " ("+str("%.2f" %(SpaceTime.StarToBase(data["Bdistance"])/60))+"min)") or "unknown")+"\n"
                    returnstring+="Landing pad size: "+padsize[data["BlandingPadSize"]]
                    return returnstring
                elif columnorder[section] == "DistanceSq":
                    return "Travel distance "+str(data["DistanceSq"]**0.5)+"ly + "+\
                                str(data["Bdistance"] is not None and data["Bdistance"] or "unknown")+"ls from star to station"
                elif columnorder[section] == "SystemDistance":
                    return "Travel distance "+str(data["SystemDistance"])+"ly + "+\
                                str(data["Bdistance"] is not None and data["Bdistance"] or "unknown")+"ls from star to station\n"+\
                                str(data["Bdistance"] is not None and str("%.2f" % (SpaceTime.StarToBase(data["Bdistance"])/60))+"min" or "")
                elif columnorder[section] == "profit":
                    return "Buy for "+str(data["AexportPrice"])\
                                 +"\nSell for "+str(data["BimportPrice"])\
                                 +"\nProfit:    "+str(data["profit"])
                elif columnorder[section] == "Cprofit":
                    return "Buy for "+str(data["BexportPrice"])\
                                 +"\nSell for "+str(data["CimportPrice"])\
                                 +"\nProfit:    "+str(data["Cprofit"])
                elif columnorder[section] == "profitPh":
                    returnstring="Profit:"+str(data["profit"])+"\n"
                    returnstring+="System: "+data["Bsystemname"]+"\n"
                    returnstring+=str(data["SystemDistance"])+"ly\n"
                    returnstring+="Station: "+data["Bbasename"]+"\n"
                    returnstring+=str(data["Bdistance"] is not None and str(data["Bdistance"])+"ls\n" or "")
                    returnstring+=str(data["Bdistance"] is not None and str("%.2f" % (SpaceTime.StarToBase(data["Bdistance"])/60))+"min" or "")
                    return returnstring
                elif columnorder[section] == "CprofitPh":
                    returnstring="Profit:"+str(data["Cprofit"])+"\n"
                    returnstring+="System: "+data["Csystemname"]+"\n"
                    returnstring+=str(data["CSystemDistance"])+"ly\n"
                    returnstring+="Station: "+data["Cbasename"]+"\n"
                    returnstring+=str(data["Cdistance"] is not None and str(data["Cdistance"])+"ls\n" or "")
                    returnstring+=str(data["Cdistance"] is not None and str("%.2f" % (SpaceTime.StarToBase(data["Cdistance"])/60))+"min" or "")
                    return returnstring
                else:
                    return None

            if role == QtCore.Qt.DisplayRole: # visible text data
                if section >=len(columnorder):
                        return None

                if "celltype" in data:
                    if data["celltype"] in ['separatorrow']:
                        if columnorder[section]=='profit':
                            return "Average: "+str(data["averageprofit"])+"cr"
                        elif columnorder[section]=='profitPh':
                            return str(data["totalprofitPh"])+"cr/h"
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
                elif columnorder[section] == "SystemDistance":
                    return data["SystemDistance"]
                elif columnorder[section] == "profitPh":
                    return str(int(data["profit"]/data["hours"]))
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
                elif columnorder[section] == "SystemDistance":
                    field="Distance"
                elif columnorder[section] == "profit":
                    field="Profit Cr"
                elif columnorder[section] == "Cprofit":
                    field="Return Profit Cr"
                elif columnorder[section] == "totalprofit":
                    field="Total Profit Cr"
                elif columnorder[section] == "profitPh":
                    field="Profit Cr/h"
                else:
                    return None

                return field

            return None # default when nothing matches


        def refeshData(self):
            self.beginResetModel()
            self.endResetModel()
            #self.dataChanged.emit(self.createIndex(0,0), self.createIndex(self.columnCount(1), len(self.mw.result)), [])
            self.dataChanged.emit(self.createIndex(0,0), self.createIndex(8, len(self.mw.result)), [])
