
class Commodity:
  def __init__(self, conn, id, name, average):
    self.conn = conn
    self.id = id
    self.name = name
    self.average = average

  def getName(self):
    return self.name

  def getId(self):
    return self.id

  def getAverage(self):
    return self.average

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return "Commodity(id = {0}, name = \"{1}\")" \
            .format(self.id, self.name)
