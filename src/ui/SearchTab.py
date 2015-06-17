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
import ThreadWorker

class SearchTab(QtWidgets.QWidget, ui.SearchTabUI.Ui_Dialog, ui.TabAbstract.TabAbstract):

    _resultsUpdated = QtCore.pyqtSignal([list])

    def __init__(self, db, analyzer, tabName, mainwindow):
        super(QtWidgets.QWidget, self).__init__()
        self.setupUi(self)
        self.tabName = tabName
        self.db = db
        self.mainwindow = mainwindow
        self.result = []
        self.currentSystem = None
        self.currentBase = None
        self.targetSystem = None
        self.targetBase = None
        self.searchType=1
        self.searchBtn.clicked.connect(self.searchBtnPressed)
        self.model = SearchTab.TableModel(None, self)
        self.SearchResultTable.setModel(self.model)
        self.getCurrentBtn.clicked.connect(self._setCurrentSystemToTab)
        self.targetGetCurrentBtn.clicked.connect(self._setCurrentSystemToTabTarget)
        self.searchTypeCombo.currentIndexChanged.connect(self._searchtypeChanged)
        self.analyzer = analyzer

        self.currentSystemCombo.currentIndexChanged.connect(self._refreshCurrentStationlist)
        self.targetSystemCombo.currentIndexChanged.connect(self._refreshTargetStationlist)
        self.minProfitSpinBox.valueChanged.connect(self._minProfitChanged)
        self.graphDepthSpin.valueChanged.connect(self._graphDepthChanged)
        self.graphMinDepthSpin.valueChanged.connect(self._graphDepthChanged)
        self.windowSizeSpinBox.valueChanged.connect(self._distanceWindowChanged)
        self.maxDistanceSpinBox.valueChanged.connect(self._distanceWindowChanged)

        systemlist=self.db.getSystemNameList()
        self.currentSystemCombo.clear()
        self.currentSystemCombo.addItems( systemlist )
        self.targetSystemCombo.clear()
        self.targetSystemCombo.addItems( systemlist )
        self._restoreSearchStatus()
        self._resultsUpdated.connect(self._updateResults)
        self.currentWorker = None

    def _setSearchProgress(self, status):
        if status:
            self.searchBtn.setText("Stop search")
        else:
            self.searchBtn.setText("Search")

    def _minProfitChanged(self):
      maxval=750
      minval=100
      value=int(self.minProfitSpinBox.value())
      value=(value-minval)/(maxval-minval)
      redness=max(0.0,min(1.0,value))
      self.minProfitSpinBox.setStyleSheet("background:rgb(255,"+str(255*redness)+","+str(255*redness)+")")

    def _graphDepthChanged(self):
      if self.graphDepthSpin.value()<self.graphMinDepthSpin.value():
        self.graphDepthSpin.setStyleSheet("background:rgb(255,0,0)")
        self.graphMinDepthSpin.setStyleSheet("background:rgb(255,0,0)")
      else:
        self.graphDepthSpin.setStyleSheet("background:rgb(255,255,255)")
        self.graphMinDepthSpin.setStyleSheet("background:rgb(255,255,255)")

    def _distanceWindowChanged(self):
      value=(self.windowSizeSpinBox.value()-self.maxDistanceSpinBox.value())/(self.windowSizeSpinBox.value()/1.5)
      redness=max(0.0,min(1.0,value))
      self.windowSizeSpinBox.setStyleSheet("background:rgb(255,"+str(255*redness)+","+str(255*redness)+")")
      self.maxDistanceSpinBox.setStyleSheet("background:rgb(255,"+str(255*redness)+","+str(255*redness)+")")

    def _updateResults(self, data):
        self.result = data
        self.model.refeshData()
        self._setSearchProgress(False)
        self.currentWorker = None
        print("Search done!")
        if len(data)==0:
          print("Search resulted in 0 matches. Keep min hops low and try lower minimum profits to widen the search (note: this also takes longer)")

    def _searchtypeChanged(self,idx):
        #searchtype=self.searchTypeCombo.currentIndex()
        searchtype=idx
        if searchtype in [5,6]:
          self.targetSystemCombo.setEnabled(True)
          self.targetStationCombo.setEnabled(True)
        else:
          self.targetSystemCombo.setEnabled(False)
          self.targetStationCombo.setEnabled(False)
        if searchtype in [4,6]:
          self.graphDepthSpin.setEnabled(False)
          self.graphMinDepthSpin.setEnabled(False)
        else:
          self.graphDepthSpin.setEnabled(True)
          self.graphMinDepthSpin.setEnabled(True)
        if searchtype in [1,2,3,4]:
          self.currentStationCombo.setEnabled(False)
        else:
          self.currentStationCombo.setEnabled(True)
        if searchtype in [6]:
          self.maxDistanceSpinBox.setEnabled(False)
          self.windowSizeSpinBox.setEnabled(False)
          self.windowCountSpinBox.setEnabled(False)
          self.minProfitSpinBox.setEnabled(False)
        else:
          self.maxDistanceSpinBox.setEnabled(True)
          self.windowSizeSpinBox.setEnabled(True)
          self.windowCountSpinBox.setEnabled(True)
          self.minProfitSpinBox.setEnabled(True)


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

    def refreshData(self):
        self.model.refeshData()

    def _refreshCurrentStationlist(self):
        if self.currentSystem is None or self.currentSystem.getName()!=self.currentSystemCombo.currentText():
          self.setCurrentSystem(self.currentSystemCombo.currentText(),refreshstations=False)
        if self.currentSystem is None:
          print('Current system not set')
          return
        currentSystemStations=[o.getName() for o in self.currentSystem.getStations()]
        self.currentStationCombo.clear()
        self.currentStationCombo.addItems( ['ANY'] )
        self.currentStationCombo.addItems( currentSystemStations )

    def setCurrentSystem(self, system, refreshstations=True):
        systems = self.db.getSystemByName(system)
        if len(systems)==0:
          print('System not in db')
          return
        system=systems[0]
        self.currentSystem = system
        self.currentSystemCombo.setEditText(self.currentSystem.getName())
        if refreshstations:
          self._refreshCurrentStationlist()
        self.model.refeshData()

    def setCurrentBase(self, base):
        if self.currentSystem is None:
          print('Current system not set')
          return
        bases=self.currentSystem.getStations()
        baseo=None
        for bo in bases:
          if bo.getName()==base:
            baseo=bo
            break
        if baseo is None:
          print('Station not in db')
          self.currentBase = None
          self.currentStationCombo.setEditText('ANY')
          return
        self.currentBase = baseo
        self.currentStationCombo.setEditText(self.currentBase.getName())

    def _refreshTargetStationlist(self):
        if self.targetSystem is None or self.targetSystem.getName()!=self.targetSystemCombo.currentText():
          self.setTargetSystem(self.targetSystemCombo.currentText(),refreshstations=False)
        if self.targetSystem is None:
          print('Target system not set')
          return
        targetSystemStations=[o.getName() for o in self.targetSystem.getStations()]
        self.targetStationCombo.clear()
        self.targetStationCombo.addItems( ['ANY'] )
        self.targetStationCombo.addItems( targetSystemStations )

    def setTargetSystem(self, system, refreshstations=True):
        systems = self.db.getSystemByName(system)
        if len(systems)==0:
          print('System not in db')
          return
        system=systems[0]
        self.targetSystem = system
        self.targetSystemCombo.setEditText(self.targetSystem.getName())
        if refreshstations:
          self._refreshTargetStationlist()
        self.model.refeshData()

    def setTargetBase(self, base):
        if self.targetSystem is None:
          print('Target system not set')
          return
        bases=self.targetSystem.getStations()
        baseo=None
        for bo in bases:
          if bo.getName()==base:
            baseo=bo
            break
        if baseo is None:
          print('Station not in db')
          self.targetBase = None
          self.targetStationCombo.setEditText('ANY')
          return
        self.targetBase = baseo
        self.targetStationCombo.setEditText(self.targetBase.getName())

    def _setCurrentSystemToTab(self):
        self.setCurrentSystem(self.mainwindow.currentStatus['System'])
        self.setCurrentBase(self.mainwindow.currentStatus['Base'])

    def _setCurrentSystemToTabTarget(self):
        self.setTargetSystem(self.mainwindow.currentStatus['System'])
        self.setTargetBase(self.mainwindow.currentStatus['Base'])

    def _restoreSearchStatus(self):
        self.currentSystemCombo.setCurrentText(Options.get(self._optName("current_system"), "Sol"))
        self.targetSystemCombo.setCurrentText(Options.get(self._optName("target_system"), "Lave"))
        self.maxDistanceSpinBox.setValue(int(Options.get(self._optName("maximum_distance"), "50")))
        self.minProfitSpinBox.setValue(int(Options.get(self._optName("minimum_profit"), "1000")))
        self.searchTypeCombo.setCurrentIndex(int(Options.get(self._optName("search_type"), "0")))
        self.searchType=int(Options.get(self._optName("search_type"), "0"))
        self.graphDepthSpin.setValue(int(Options.get(self._optName("search_max_depth"), "5")))
        self.graphMinDepthSpin.setValue(int(Options.get(self._optName("search_min_depth"), "1")))
        self.windowSizeSpinBox.setValue(int(Options.get(self._optName("search_window_size"), "200")))
        self.windowCountSpinBox.setValue(int(Options.get(self._optName("search_window_count"), "7")))
        #self.profitPhChk.setChecked(Options.get(self._optName("search_profitPh"),"0")=="1")

        self._refreshCurrentStationlist() # populate station lists
        self._refreshTargetStationlist()

        self.currentStationCombo.setCurrentText(Options.get(self._optName("current_station"), "Abraham Lincoln"))
        self.targetStationCombo.setCurrentText(Options.get(self._optName("target_station"), "Lave Station"))

        self._searchtypeChanged(int(Options.get(self._optName("search_type"), "0")))

    def _saveSearchStatus(self):
        Options.set(self._optName("current_system"), self.currentSystemCombo.currentText())
        Options.set(self._optName("target_system"), self.targetSystemCombo.currentText())
        Options.set(self._optName("maximum_distance"), self.maxDistanceSpinBox.value())
        Options.set(self._optName("minimum_profit"), self.minProfitSpinBox.value())
        Options.set(self._optName("search_window_size"), self.windowSizeSpinBox.value())
        Options.set(self._optName("search_window_count"), self.windowCountSpinBox.value())
        Options.set(self._optName("search_type"), self.searchTypeCombo.currentIndex())
        Options.set(self._optName("search_max_depth"), self.graphDepthSpin.value())
        Options.set(self._optName("search_min_depth"), self.graphMinDepthSpin.value())
        Options.set(self._optName("current_station"), self.currentStationCombo.currentText())
        Options.set(self._optName("target_station"), self.targetStationCombo.currentText())
        #Options.set(self._optName("search_profitPh"), self.profitPhChk.isChecked() and "1" or "0")

    def _cancelSearch(self):
        self.currentWorker.terminate()
        self.currentWorker = None
        self.model.refeshData()
        self._setSearchProgress(False)

    def searchBtnPressed(self):
        if self.currentWorker is not None:
            print('Cancelled search!')
            self._cancelSearch()
            return

        #print ("searchBtnPressed")
        #self.searchBtn.setText('- - - - S e a r c h i n g - - - -') # unfortunately these never show with synchronous ui

        currentSystem = self.currentSystemCombo.currentText()
        currentBase = self.currentStationCombo.currentText()
        targetSystem = self.targetSystemCombo.currentText()
        targetBase = self.targetStationCombo.currentText()
        windowSize = float(self.windowSizeSpinBox.value())
        windows = int(self.windowCountSpinBox.value())
        maxDistance = float(self.maxDistanceSpinBox.value())
        jumprange = float(self.mainwindow.jumpRangeSpinBox.value())
        minProfit = int(self.minProfitSpinBox.value())
        #minProfit =None
        minProfitPh =None
        #if bool(self.profitPhChk.isChecked()):
        #    minProfitPh = int(self.minProfitSpinBox.value())
        #else:
        #    minProfit = int(self.minProfitSpinBox.value())
        minPadSize = int(self.mainwindow.minPadSizeCombo.currentIndex())
        searchType = int(self.searchTypeCombo.currentIndex())
        graphDepth = int(self.graphMinDepthSpin.value())
        graphDepthmax = int(self.graphDepthSpin.value())
        #twoway = bool(self.twoWayBool.isChecked())

        if graphDepth>graphDepthmax:
          print("min hops have to be less than max hops!")
          self.mainwindow.sounds.play('error')
          return

        pos = self.currentSystem.getPosition()

        self.searchType=searchType

        print("Querying database...")
        searchFn = None
        if searchType==4:
            print("queryProfit")
            searchFn = lambda : Queries.queryProfit(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize,jumprange )

            #self.result = self.db.queryProfit(pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minPadSize)
        elif searchType==2:
            print("queryProfitGraphLoops")
            searchFn = lambda : Queries.queryProfitGraphLoops(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize,jumprange ,graphDepth,graphDepthmax)
        elif searchType==3:
            print("queryProfitGraphDeadends")
            searchFn = lambda : Queries.queryProfitGraphDeadends(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize,jumprange ,graphDepth,graphDepthmax)
        elif searchType==5:
            print("queryProfitGraphTarget")
            if currentBase == 'ANY':
              currentBase=None
            if targetBase == 'ANY':
              targetBase=None

            tpos=self.targetSystem.getPosition()
            directionality=0.0
            searchFn = lambda : Queries.queryProfitGraphTarget(self.db, pos[0], pos[1], pos[2], tpos[0], tpos[1], tpos[2], directionality, windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize,jumprange ,graphDepth,graphDepthmax,currentSystem,currentBase,targetSystem,targetBase)
        elif searchType==6:
            print("queryDirectTrades")
            if currentBase == 'ANY':
              currentBase=None
            if targetBase == 'ANY':
              targetBase=None

            tpos=self.targetSystem.getPosition()
            directionality=0.0
            searchFn = lambda : Queries.queryDirectTrades(self.db, pos[0], pos[1], pos[2], tpos[0], tpos[1], tpos[2], directionality, windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize,jumprange ,graphDepth,graphDepthmax,currentSystem,currentBase,targetSystem,targetBase)
        elif searchType==0 or searchType==1:
            if currentBase == 'ANY':
              currentBase=None

            print("queryProfitGraphDeadends from current")
            searchFn = lambda : Queries.queryProfitGraphDeadends(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize,jumprange ,graphDepth,graphDepthmax,currentSystem,currentBase)
        else:
            print("unknown search type - we should not be here")
        #elif searchType==1:
        #    print("queryProfitRoundtrip")
        #    self.result = Queries.queryProfitRoundtrip(self.db, pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minProfitPh,minPadSize)
        #    #self.result = self.db.queryProfitRoundtrip(pos[0], pos[1], pos[2], windowSize, windows, maxDistance, minProfit,minPadSize)

        if searchFn is not None:
            self.currentWorker = ThreadWorker.ThreadWorker(searchFn, lambda result: self._resultsUpdated.emit(result))
            self.currentWorker.start()
            self._setSearchProgress(True)

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
                    "hours",
                    "profit",
                    "profitPh"
                ]
            basictradetable_target=[
                    "Asystemname",
                    "Abasename",
                    "AexportPrice",
                    "commodityname",
                    "BimportPrice",
                    "Bsystemname",
                    "Bbasename",
                    #"DistanceSq",
                    "SystemDistance",
                    "hours",
                    "profit",
                    "profitPh",
                    "_targetdist"
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
                basictradetable,
                basictradetable_target,
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

            if role == QtCore.Qt.TextColorRole: # text color
                if "celltype" not in data:
                  if columnorder[section] in ["AexportPrice"]:
                    if int(data['AlastUpdated'])<time.time()-60*60*24*int(Options.get('Market-valid-days',7)):
                      return QtGui.QBrush(QtGui.QColor(255,255,0))
                  if columnorder[section] in ["BimportPrice"]:
                    if int(data['BlastUpdated'])<time.time()-60*60*24*int(Options.get('Market-valid-days',7)):
                      return QtGui.QBrush(QtGui.QColor(255,255,0))

            if role == QtCore.Qt.BackgroundRole: # background colors
                if "celltype" in data:
                    if data["celltype"]=='emptyrow':
                        return QtGui.QBrush(QtGui.QColor(255,255,255))
                    if data["celltype"]=='separatorrow':
                        return QtGui.QBrush(QtGui.QColor(200,200,200))
                if columnorder[section] in ["Asystemname","Abasename","Bsystemname","Bbasename"]:
                    return QtGui.QBrush(QtGui.QColor(255,255,230))
                if columnorder[section] in ["AexportPrice"]:
                    r,g,b=self.mw.AgeToColor(data['AlastUpdated'])
                    return QtGui.QBrush(QtGui.QColor(r,g,b))
                if columnorder[section] in ["BimportPrice"]:
                    r,g,b=self.mw.AgeToColor(data['BlastUpdated'])
                    return QtGui.QBrush(QtGui.QColor(r,g,b))
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
                    return "Data "+str("%.2f" %((time.time()-data['AlastUpdated'])/(60*60*24)))+" days old"\
                          +"\nExport sales price: "+str(data["AexportPrice"])+"\nSupply: "+str(data["Asupply"])
                elif columnorder[section] == "BexportPrice":
                    return "Export sales price: "+str(data["BexportPrice"])+"\nSupply: "+str(data["Bsupply"])
                elif columnorder[section] == "commodityname":
                    return "Commodity "+data["commodityname"]\
                           +"\nData "+str("%.2f" %((time.time()-min(data['AlastUpdated'],data['BlastUpdated']))/(60*60*24)))+" days old"\
                           +"\nBuy for "+str(data["AexportPrice"])\
                           +"\nSell for "+str(data["BimportPrice"])\
                           +"\nProfit:    "+str(data["profit"])\
                           +"\nGalactic average price: "+str(data["average"])
                elif columnorder[section] == "Ccommodityname":
                    return "Commodity "+data["Ccommodityname"]\
                           +"\nBuy for "+str(data["BexportPrice"])\
                           +"\nSell for "+str(data["CimportPrice"])\
                           +"\nProfit:    "+str(data["Cprofit"])\
                           +"\nGalactic average price: "+str(data["Caverage"])
                elif columnorder[section] == "BimportPrice":
                    return "Data "+str("%.2f" %((time.time()-data['BlastUpdated'])/(60*60*24)))+" days old"\
                          +"\nImport buy price: "+str(data["BimportPrice"])+"\nDemand: "+str(data["Bdemand"])
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
                        elif columnorder[section] == "hours":
                          return str(int(data["totalhours"]*60*10)/10)
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
                elif columnorder[section] == "_targetdist":
                    if self.mw.targetSystemCombo.currentText() is None:
                        return '?'
                    else:
                        pos=self.mw.targetSystem.getPosition()
                        dist=( (pos[0]-data["Bx"])**2 + (pos[1]-data["By"])**2 + (pos[2]-data["Bz"])**2 ) ** 0.5
                        return "%.2f" % dist # two decimals
                elif columnorder[section] == "DistanceSq":
                    return data["DistanceSq"] ** 0.5
                elif columnorder[section] == "SystemDistance":
                    return data["SystemDistance"]
                elif columnorder[section] == "profitPh":
                    return str(int(data["profit"]/data["hours"]))
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
                if section>=len(columnorder):
                  return

                if columnorder[section] in ["_curdist","_Bcurdist"]:
                    #field="Curr.Dist."
                    if self.mw.currentSystem is None:
                        sysname = 'here'
                    else:
                        sysname = self.mw.currentSystem.getName()
                    field="Ly from "+sysname
                elif columnorder[section] in ["_targetdist"]:
                    #field="Curr.Dist."
                    if self.mw.targetSystem is None:
                        sysname = 'target'
                    else:
                        sysname = self.mw.targetSystem.getName()
                    field="Ly to "+sysname
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
                elif columnorder[section] == "hours":
                    field="Minutes travel"
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
            # reset scroll
            self.mw.SearchResultTable.verticalScrollBar().setSliderPosition(0)
