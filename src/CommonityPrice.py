
class CommonityPrice:
  def __init__(self, conn, id, commonityId, importPrice, exportPrice, demand, lastUpdated):
    self.conn = conn
    self.id = id
    self.commonityId = commonityId
    self.exportPrice = exportPrice
    self.importPrice = importPrice
    self.demand = demand
    self.lastUpdated = lastUpdated
    

  def getImportPrice(self):
    return self.importPrice
  
  def getExportPrice(self):
    return self.exportPrice

  def getDemand(self):
    return self.demand

  def getLastUpdated(self):
    return self.lastUpdated

  def getCommonity(self):
    return self.conn.getCommonity(self.commonityId)

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return "CommonityPrice(id = {0}, name = \"{1}\", import = {2}, export = {3}, lastUpdated = {4})" \
        .format(self.id, self.getCommonity().getName(), self.importPrice, self.exportPrice, self.lastUpdated)

  
