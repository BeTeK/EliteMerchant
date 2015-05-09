import sqlite3
import EliteDB
import os.path
import os

class SQLiteDB(EliteDB.EliteDB):
  
  def __init__(self, filename, forceInit = False):
    super().__init__()
    self.filename = filename
    self.forceInit = forceInit

  

  def __enter__(self):
    self._init()
    return self

  def _init(self):
    exists = os.path.exists(self.filename)
    if exists and self.forceInit:
      os.remove(self.filename)

    self.conn = sqlite3.connect(self.filename)
    if not exists or self.forceInit:
      self._createDB()

    
  def __exit__(self, type, value, traceback):
    if self.conn is not None:
      self.conn.close()

  def addSystem(self, name, pos = None):
    cur = self.conn.cursor()

    if pos is None:
      cur.execute('INSERT INTO systems (name, x, y, z) VALUES (?, NULL, NULL, NULL)', (name,))
    else:
      cur.execute('INSERT INTO systems (name, x, y, z) VALUES (?, ?, ?, ?)', (name, pos[0], pos[1], pos[2]))

    self.conn.commit()

  def _createDB(self):
    cur = self.conn.cursor()
    cur.execute("""CREATE TABLE "Planets" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "systemId" INTEGER NOT NULL,
    "distance" REAL,
    "name" TEXT NOT NULL
)""")
    cur.execute("""CREATE INDEX "planetIDIndex" on planets (id ASC)""")
    cur.execute("""CREATE INDEX "planetSystemIdIndex" on planets (systemId ASC)""")
    cur.execute("""CREATE TABLE systems (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL
, "x" REAL, "y" REAL, "z" REAL)""")
    cur.execute("""CREATE INDEX "systemsIdIndex" on systems (id ASC)""")
    cur.execute("""CREATE INDEX "systemsNameIndex" on systems (name ASC)""")
    cur.execute("""CREATE INDEX "systemsXIndex" on systems (x ASC)""")
    cur.execute("""CREATE INDEX "systemsYIndex" on systems (y ASC)""")
    cur.execute("""CREATE INDEX "systemsZIndex" on systems (z ASC)""")
    cur.execute("""CREATE TABLE "BaseInfo" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "baseId" INTEGER NOT NULL,
    "blackMarket" INTEGER,
    "landingPadSize" INTEGER
)""")
    cur.execute("""CREATE INDEX "baseInfoIdIndex" on baseinfo (id ASC)""")
    cur.execute("""CREATE INDEX "baseInfoBaseIdIndex" on baseinfo (baseId ASC)""")
    cur.execute("""CREATE INDEX "baseInfoBlackMarketIndex" on baseinfo (blackMarket ASC)""")
    cur.execute("""CREATE INDEX "baseInfoLandingPadSize" on baseinfo (landingPadSize ASC)""")
    cur.execute("""CREATE TABLE "Commonity" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT
)""")
    cur.execute("""CREATE INDEX "commonityIdIndex" on commonity (id ASC)""")
    cur.execute("""CREATE INDEX "commonityNameIndex" on commonity (name ASC)""")
    cur.execute("""CREATE TABLE "commonityPrices" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "commonityId" INTEGER NOT NULL,
    "baseId" INTEGER NOT NULL,
    "price" INTEGER NOT NULL,
    "lastUpdated" TEXT
)""")
    cur.execute("""CREATE INDEX "commonityPricesIdIndex" on commonityprices (id ASC)""")
    cur.execute("""CREATE INDEX "commonityPricesCommonitIdIndex" on commonityprices (commonityId ASC)""")
    cur.execute("""CREATE INDEX "commonityPricesBaseIdIndex" on commonityprices (baseId ASC)""")
    cur.execute("""CREATE TABLE bases (
    "id" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "planetId" INTEGER
, "systemId" INTEGER, "distance" REAL)""")
    cur.execute("""CREATE INDEX "basesIdIndex" on bases (id ASC)""")
    cur.execute("""CREATE INDEX "basesPlanetId" on bases (planetId ASC)""")
    cur.execute("""CREATE INDEX "basesNameIndex" on bases (name ASC)""")
    cur.execute("""CREATE INDEX "basesSystemIndex" on bases (systemId ASC)""")

    self.conn.commit()


