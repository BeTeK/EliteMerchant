
import Base

class System:
  def __init__(self, conn, id, name, pos):
    self.conn = conn
    self.name = name
    self.pos = pos
    self.id = id
 
  def getPosition(self):
    return self.pos

  def getName(self):
    return self.name

  def getId(self):
    return self.id

  def getStations(self):
    return self.conn.getBasesOfSystem(self.id)

  def addStation(self, name, distance):
    baseData = [{"name" : name,
                "distance" : distance,
                "systemId" : self.id}]

    self.conn.importBases(baseData)
    base = [i for i in self.getStations() if i.getName() == name][0]

    baseInfo = [{
      "id" : base.getId(),
      "blackMarket" : False,
      "landingPadSize" : 2
    }]
    self.conn.importBaseInfos(baseInfo)

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return "System(id = {0}, name = \"{1}\", pos = {2})".format(self.id, self.name, self.pos)

  
