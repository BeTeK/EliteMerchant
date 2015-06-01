

class Base:
  def __init__(self, conn, id, name, blackMarket, landingPadSize, distance):
    self.conn = conn
    self.id = id
    self.name = name
    self.blackMarket = blackMarket
    self.landingPadSize = landingPadSize
    self.distance = distance

  def getName(self):
    return self.name

  def getId(self):
    return self.id

  def hasBlackMarket(self):
    if self.blackMarket is not None:
      return self.blackMarket != 0
    else:
      return None

  def getLandingPadSize(self):
    return landingPadSize

  def getDistance(self):
    return self.distance

  def getPrices(self):
    return self.conn.getPricesOfCommoditiesInBase(self.id)

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return "Base(id = {0}, name = \"{1}\", blackMarket = {2}, landingPadSize = {3}, distance = {4})" \
            .format(self.id, self.name, self.blackMarket, self.landingPadSize, self.distance)
