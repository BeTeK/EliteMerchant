import sqlite3
import EliteDB
import os.path
import os
import System
import Base

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
    self.conn.row_factory = sqlite3.Row
    if not exists or self.forceInit:
      self._createDB()

    
  def __exit__(self, type, value, traceback):
    if self.conn is not None:
      self.conn.close()

  def getBasesOfSystem(self, id):
    cur = self.conn.cursor()

    cur.execute("SELECT bases.id, bases.name, bases.planetId, bases.distance, baseInfo.blackMarket, baseInfo.landingPadSize FROM bases, baseInfo WHERE bases.id = baseInfo.baseId AND bases.systemId = ?", (id, ))

    print([self._dictToBase(self._rowToDict(i)) for i in cur.fetchall()])

  def _dictToBase(self, info):
    return Base.Base(self, info["id"], info["name"], info["blackMarket"], info["landingPadSize"], info["distance"])

  def getSystemByName(self, name, limit = 20):
    cur = self.conn.cursor()
    cur.execute("SELECT id, name, x, y, z FROM systems WHERE systems.name LIKE ?", (name, ))

    return [self._dictToSystem(self._rowToDict(i)) for i in cur.fetchmany(limit)]

  def _dictToSystem(self, info):
    if info["x"] is not None and info["y"] is not None and info["z"] is not None:
      pos = (info["x"], info["y"], info["z"])
    else:
      pos = None

    return System.System(self, info["id"], info["name"], pos)

  def _rowToDict(self, row):
    out = {}
    for index, value in enumerate(row.keys()):
      out[value] = row[index]

    return out

  def addSystem(self, name, pos = None):
    cur = self.conn.cursor()

    if pos is None:
      cur.execute('INSERT INTO systems (name, x, y, z) VALUES (?, NULL, NULL, NULL)', (name,))
    else:
      cur.execute('INSERT INTO systems (name, x, y, z) VALUES (?, ?, ?, ?)', (name, pos[0], pos[1], pos[2]))

    self.conn.commit()

  def _createDB(self):
    cur = self.conn.cursor()
    cur.execute("""CREATE TABLE "planets" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "systemId" INTEGER NOT NULL,
    "distance" REAL,
    "name" TEXT NOT NULL UNIQUE
    )""")
    cur.execute("""CREATE INDEX "planetIDIndex" on planets (id ASC)""")
    cur.execute("""CREATE INDEX "planetSystemIdIndex" on planets (systemId ASC)""")

    cur.execute("""CREATE TABLE systems (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL UNIQUE,
    "x" REAL, "y" REAL, "z" REAL
    )""")
    cur.execute("""CREATE INDEX "systemsIdIndex" on systems (id ASC)""")
    cur.execute("""CREATE INDEX "systemsNameIndex" on systems (name ASC)""")
    cur.execute("""CREATE INDEX "systemsXIndex" on systems (x ASC)""")
    cur.execute("""CREATE INDEX "systemsYIndex" on systems (y ASC)""")
    cur.execute("""CREATE INDEX "systemsZIndex" on systems (z ASC)""")

    cur.execute("""CREATE TABLE "baseInfo" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "baseId" INTEGER NOT NULL UNIQUE,
    "blackMarket" INTEGER,
    "landingPadSize" INTEGER
    )""")
    cur.execute("""CREATE INDEX "baseInfoIdIndex" on baseinfo (id ASC)""")
    cur.execute("""CREATE INDEX "baseInfoBaseIdIndex" on baseinfo (baseId ASC)""")
    cur.execute("""CREATE INDEX "baseInfoBlackMarketIndex" on baseinfo (blackMarket ASC)""")
    cur.execute("""CREATE INDEX "baseInfoLandingPadSize" on baseinfo (landingPadSize ASC)""")

    cur.execute("""CREATE TABLE "commodities" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT UNIQUE
    )""")
    cur.execute("""CREATE INDEX "commoditiesIdIndex" on commodities (id ASC)""")
    cur.execute("""CREATE INDEX "commoditiesNameIndex" on commodities (name ASC)""")

    cur.execute("""CREATE TABLE "commodityPrices" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "commodityId" INTEGER NOT NULL,
    "baseId" INTEGER NOT NULL,
    "supply" INTEGER NOT NULL,
    "demand" INTEGER NOT NULL,
    "import_price" INTEGER NOT NULL,
    "export_price" INTEGER NOT NULL,
    "lastUpdated" INTEGER,
    UNIQUE (baseId, commodityId)
    )""")
    cur.execute("""CREATE INDEX "commodityPricesIdIndex" on commodityPrices (id ASC)""")
    cur.execute("""CREATE INDEX "commodityPricesCommonitIdIndex" on commodityPrices (commodityId ASC)""")
    cur.execute("""CREATE INDEX "commodityPricesBaseIdIndex" on commodityPrices (baseId ASC)""")

    cur.execute("""CREATE TABLE bases (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT NOT NULL UNIQUE,
    "planetId" INTEGER,
    "systemId" INTEGER,
    "distance" REAL
    )""")
    cur.execute("""CREATE INDEX "basesIdIndex" on bases (id ASC)""")
    cur.execute("""CREATE INDEX "basesPlanetId" on bases (planetId ASC)""")
    cur.execute("""CREATE INDEX "basesNameIndex" on bases (name ASC)""")
    cur.execute("""CREATE INDEX "basesSystemIndex" on bases (systemId ASC)""")

    self.conn.commit()


  def importCommodities(self,commoditylist):
    cur = self.conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO commodities(name) VALUES(?)",commoditylist)

    self.conn.commit()

    return list(cur.execute('SELECT id,name FROM commodities'))

  def importSystems(self,systemlist):
    cur = self.conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO systems(name,x,y,z) VALUES(?,?,?,?)",systemlist)

    self.conn.commit()

    return list(cur.execute('SELECT id,name FROM systems'))

  def importBases(self,baselist):
    cur = self.conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO bases(name,planetId,systemId,distance) VALUES(?,?,?,?)",baselist)

    self.conn.commit()

    return list(cur.execute('SELECT id,name FROM bases'))

  def importBaseInfos(self,baselist):
    cur = self.conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO baseInfo(baseId,blackMarket,landingPadSize) VALUES(?,?,?)",baselist)

    self.conn.commit()
    #return cur.execute('SELECT id,name FROM baseInfo') # no need for ids here

  def importCommodityPrices(self,marketlist):
    cur = self.conn.cursor()
    cur.executemany("INSERT OR REPLACE INTO commodityPrices( commodityId, baseId, import_price, export_price, lastUpdated, demand, supply ) VALUES(?,?,?,?,?,?,?)",marketlist)
    # todo: timestamp comparison

    self.conn.commit()
