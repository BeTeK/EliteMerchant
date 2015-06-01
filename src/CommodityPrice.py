import datetime

class CommodityPrice:
  def __init__(self, db, id, commodityId, importPrice, exportPrice, demand, lastUpdated, baseId, supply):
    self.db = db
    self.id = id
    self.commodityId = commodityId
    self.exportPrice = exportPrice
    self.importPrice = importPrice
    self.demand = demand
    self.lastUpdated = lastUpdated
    self.updated = False
    self.baseId = baseId
    self.supply = supply

  def getImportPrice(self):
    return self.importPrice
  
  def getExportPrice(self):
    return self.exportPrice

  def getDemand(self):
    return self.demand

  def getLastUpdated(self):
    return self.lastUpdated

  def getCommodity(self):
    return self.db.getCommodity(self.commodityId)

  def setImportPrice(self, price):
    self.importPrice = price
    self.updated = True

  def setExportPrice(self, price):
    self.exportPrice = price
    self.updated = True

  def setSupply(self, supply):
    self.supply = supply
    self.updated = True

  def setDemand(self, demand):
    self.demand = demand

  def touch(self):
    self.updated = True

  def commitChanges(self,):
    if self.updated:
      self.updated = False
      updateData = [{"commodityId" : self.commodityId,
                    "baseId" : self.baseId,
                    "importPrice" : self.importPrice,
                    "exportPrice" : self.exportPrice,
                    "lastUpdated" : int(datetime.datetime.now().timestamp()),
                    "demand" : self.demand,
                    "supply" : self.supply}]

      self.db.importCommodityPrices(updateData)

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return "CommodityPrice(id = {0}, name = \"{1}\", import = {2}, export = {3}, lastUpdated = {4})" \
        .format(self.id, self.getCommodity().getName(), self.importPrice, self.exportPrice, self.lastUpdated)

  
