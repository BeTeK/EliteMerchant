import os
import sys
import Options
import CommodityPrice
import threading
import time

class EdceWrapper:
    _commodityNameTranslationTable = {
        "Fruit And Vegetables" : "Fruit and Vegetables",
        "Atmospheric Extractors" : "Atmospheric Processors",
        "Marine Supplies" : "Marine Equipment",
        "Agricultural Medicines" : "Agri-Medicines",
        "Basic Narcotics" : "Narcotics",
        "Drones" : "Limpet",
        "Terrain Enrichment Systems" : "Land Enrichment Systems",
        "Non Lethal Weapons" : "Non-lethal Weapons",
        "Heliostatic Furnaces" : "Microbial Furnaces",
        "Bio Reducing Lichen" : "Bioreducing Lichen",
        "Hazardous Environment Suits" : "H.E. Suits",
        "Auto Fabricators" : "Auto-Fabricators"
    }

    def __init__(self, edcePath, db, postMarketData, verificationCodeInputFn):
        self.verificationFn = verificationCodeInputFn
        self.db = db
        self.lock = threading.RLock()
        self.disabled = None

        sys.path.insert(0, edcePath)
        sys.path.insert(0, os.path.join(edcePath, "edce"))

        import edce.query
        import edce.error
        import edce.util
        import edce.eddn
        import edce.config
        import edce.globals

        edce.eddn.testSchema = False
        edce.query.minimumDelay = 0
        print(Options.getPath())
        import configparser
        edce.config.setConfigFile(Options.getPath("edce.ini"))
        edce.config.writeConfig(Options.get("elite-username", ""), Options.get("elite-password", ""), True, Options.getPath(), Options.getPath(), Options.getPath())
        self.resultsUpdated = True
        self.resultsLastUpdated=0
        self.activeThreads = []
        self.result = None
        self.finishedListeners = []
        self.postMarkedData = postMarketData
        self.lastUpdatedInfo = {"starportName" : "",
                                "systemName" : "",
                                "docked" : False}

    def addFinishedListener(self, listener):
        self.finishedListeners.append(listener)

    def callFinishedListeners(self, data):
        for i in self.finishedListeners:
            i(data)

    def _updateResults(self):
        import edce.query
        import edce.error
        import edce.util
        import edce.eddn
        import edce.config
        import edce.globals

        try:
            if self.disabled is not None:
                return

            res = edce.query.performQuery(verificationCodeSupplyFn = self.verificationFn)
            result = edce.util.edict(res)
            if self.postMarkedData:
                if "docked" in result.commander and result.commander.docked:
                    edce.eddn.postMarketData(result)

            with self.lock:
                self.result = result

            print("New data fetched from edce")
        except Exception as ex:
            self.disabled = ex

    def isDisabled(self):
        return self.disabled

    def _cleanThreads(self):
        toBeRemoved = []
        for index, value in enumerate(self.activeThreads):
            if not value.is_alive():
                toBeRemoved.append(index)

        for i in toBeRemoved:
            del self.activeThreads[i]

    def fetchNewInfo(self):
        self._cleanThreads()
        thread = threading.Thread(target = self._updateResults)
        self.activeThreads.append(thread)
        thread.start()

    def isActive(self):
        for i in self.activeThreads:
            if i.is_alive():
                return True

        return False

    def join(self):
        self._cleanThreads()
        for i in self.activeThreads:
            i.join()

        self._cleanThreads()

    def updateResults(self):
        self._cleanThreads()
        result = None

        with self.lock:
            result = self.result
            if result is not None:
                self.result = None

        if result is not None:
            self._updateImpl(result)
            return True
        else:
            return False

    def _updateImpl(self, results):
        starportName = results.lastStarport.name
        systemName = results.lastSystem.name
        docked = results.commander.docked

        systems = self.db.getSystemByName(systemName)
        if len(systems) == 0:
            print("This is not known system")
            return

        if len(systems) > 1:
            print("More than one hit for {0} skipping".format(systemName))
            return

        system = systems[0]

        base = self.findBase(starportName, system)

        if base is None:
            system.addStation(starportName, None)
            base = self.findBase(starportName, system)

        pricesLst = base.getPrices()
        newPrices = []
        prices = dict(zip([i.getCommodity().getName() for i in pricesLst], pricesLst))

        print("Updating prices for base {0}({1}) at system {2}".format(starportName, base.getId(), systemName))

        for i in results.lastStarport.commodities:
            localName = self._getLocalCommodityName(i.name)
            if not localName in prices:
                print("Commity price '{0}' for base {1} is not in database... creating".format(localName, base.getName()))
                commodity = self.db.getCommodityByName(localName)
                if commodity is None:
                    print("Commity '{0}' for base {1} is not in database... skipping".format(localName, base.getName()))
                    continue
                priceData = CommodityPrice.CommodityPrice(self.db, None, commodity.getId(), i.sellPrice, i.buyPrice, i.demand, 0, base.getId(), i.stock)
                priceData.touch()
                newPrices.append(priceData)
            else:
                priceData = prices[localName]
                priceData.setImportPrice(i.sellPrice)
                priceData.setExportPrice(i.buyPrice)
                priceData.setSupply(i.stock)
                priceData.setDemand(i.demand)

        for i in pricesLst:
            i.commitChanges()

        for i in newPrices:
            i.commitChanges()

        print("prices updated from edce!")
        self.resultsLastUpdated=time.time()
        self.lastUpdatedInfo = {"starportName" : starportName,
                                "systemName" : systemName,
                                "docked" : docked}

        self.callFinishedListeners(dict(self.lastUpdatedInfo))

    def findBase(self, starportName, system):
        base = None
        for i in system.getStations():
            if i.getName() == starportName:
                base = i
                break
        return base

    def getLastUpdatedInfo(self):
        return self.lastUpdatedInfo

    def getResult(self):
        return self.result

    def _getLocalCommodityName(self, name):
        if name in EdceWrapper._commodityNameTranslationTable:
            return EdceWrapper._commodityNameTranslationTable[name]
        else:
            return name
