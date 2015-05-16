

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

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return "System(id = {0}, name = \"{1}\", pos = {2})".format(self.id, self.name, self.pos)

  
