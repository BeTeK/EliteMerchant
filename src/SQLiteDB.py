import sqlite3
import EliteDB
import os.path
import os
import operator
import System
import Base
import time
import datetime
import CommonityPrice
import Commonity

class SQLiteDB(EliteDB.EliteDB):
  
  def __init__(self, filename, forceInit = False):
    super().__init__()
    print(filename)
    self.filename = filename
    self.forceInit = forceInit
    self.commonityCache = {}
  

  def __enter__(self):
    self._init()
    return self

  def _init(self):
    exists = os.path.exists(self.filename)
    if exists and self.forceInit:
      os.remove(self.filename)

    self.conn = sqlite3.connect(self.filename)

    # database settings
    cur=self.conn.cursor()
    cur.execute("""PRAGMA cache_size = 1000000""")

    self.conn.row_factory = sqlite3.Row
    if not exists or self.forceInit:
      self._createDB()

    
  def __exit__(self, type, value, traceback):
    if self.conn is not None:
      self.conn.close()

  def vacuum(self):
    print("vacuuming database...")
    cur=self.conn.cursor()
    cur.execute("VACUUM")
    return

  def getBasesOfSystem(self, id):
    cur = self.conn.cursor()

    cur.execute("SELECT bases.id, bases.name, bases.planetId, bases.distance, baseInfo.blackMarket, baseInfo.landingPadSize FROM bases, baseInfo WHERE bases.id = baseInfo.baseId AND bases.systemId = ?", (id, ))

    return [self._dictToBase(self._rowToDict(i)) for i in cur.fetchall()]

  def _dictToBase(self, info):
    return Base.Base(self, info["id"], info["name"], info["blackMarket"], info["landingPadSize"], info["distance"])

  def getSystemByWindow(self, pos, windowSize):
    cur = self.conn.cursor()
    params = {"x" : pos[0],
              "y" : pos[1],
              "z" : pos[2],
              "window" : windowSize}

    cur.execute("""SELECT id, name, x, y, z  FROM systems WHERE :x - :window < systems.x AND systems.x <= :x + :window AND
                                                                :y - :window < systems.y AND systems.y <= :y + :window AND
                                                                :z - :window < systems.z AND systems.z <= :z + :window""", params)

    return [self._dictToSystem(self._rowToDict(i)) for i in cur.fetchall()]

  def getSystemByName(self, name, limit = 20):
    cur = self.conn.cursor()
    cur.execute("SELECT id, name, x, y, z FROM systems WHERE systems.name LIKE ?", (name, ))

    return [self._dictToSystem(self._rowToDict(i)) for i in cur.fetchmany(limit)]

  def getSystemById(self, id):
    cur = self.conn.cursor()
    cur.execute("SELECT id, name, x, y, z FROM systems WHERE systems.id=?", (id, ))

    result = cur.fetch()
    if result is None:
      return None
    else:
      return self._dictToSystem(self._rowToDict(result))

  def getCommonity(self, id):
    if id not in self.commonityCache:
      cur = self.conn.cursor()

      cur.execute("SELECT id, name, average FROM commodities WHERE commodities.id = ?", (id, ))
      rows = cur.fetchall()
      if len(rows) != 1:
        return None
      
      data = self._rowToDict(rows[0])

      self.commonityCache[id] = self._dictToCommonity(data)

    return self.commonityCache[id]
  
  def _dictToCommonity(self, data):
    return Commonity.Commonity(self, data["id"], data["name"], data["average"])

  def getPricesOfCommonitiesInBase(self, baseId):
    cur = self.conn.cursor()
    cur.execute("SELECT id, baseId, supply, commodityId, demand, importPrice, exportPrice, lastUpdated FROM commodityPrices WHERE commodityPrices.baseId = ?", (baseId, ))

    return [self._dictToPriceData(self._rowToDict(i)) for i in cur.fetchall()]

  def _dictToPriceData(self, data):
    return CommonityPrice.CommonityPrice(self, data["id"], data["commodityId"], data["importPrice"], data["exportPrice"], data["demand"], datetime.date.fromtimestamp(data['lastUpdated']))
  
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
    "blackMarket" BIT,
    "landingPadSize" INTEGER
    )""")
    cur.execute("""CREATE INDEX "baseInfoIdIndex" on baseinfo (id ASC)""")
    cur.execute("""CREATE INDEX "baseInfoBaseIdIndex" on baseinfo (baseId ASC)""")
    cur.execute("""CREATE INDEX "baseInfoBlackMarketIndex" on baseinfo (blackMarket ASC)""")
    cur.execute("""CREATE INDEX "baseInfoLandingPadSize" on baseinfo (landingPadSize ASC)""")

    cur.execute("""CREATE TABLE "commodities" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT UNIQUE,
    "average" INTEGER
    )""")
    cur.execute("""CREATE INDEX "commoditiesIdIndex" on commodities (id ASC)""")
    cur.execute("""CREATE INDEX "commoditiesNameIndex" on commodities (name ASC)""")

    cur.execute("""CREATE TABLE "commodityPrices" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "commodityId" INTEGER NOT NULL,
    "baseId" INTEGER NOT NULL,
    "supply" INTEGER NOT NULL,
    "demand" INTEGER NOT NULL,
    "importPrice" INTEGER NOT NULL,
    "exportPrice" INTEGER NOT NULL,
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
    cur.executemany("INSERT OR IGNORE INTO commodities(name,average) VALUES(:name,:average)",commoditylist)

    self.conn.commit()

    cur.execute('SELECT id,name FROM commodities')
    return [self._rowToDict(o) for o in cur.fetchall()]

  def importSystems(self,systemlist):
    cur = self.conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO systems(name,x,y,z) VALUES(:name,:x,:y,:z)",systemlist)

    self.conn.commit()

    cur.execute('SELECT id,name FROM systems')
    return [self._rowToDict(o) for o in cur.fetchall()]

  def importBases(self,baselist):
    cur = self.conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO bases(name,systemId,distance) VALUES(:name,:systemId,:distance)",baselist)

    self.conn.commit()
    cur.execute('SELECT id,name FROM bases')
    return [self._rowToDict(o) for o in cur.fetchall()]

  def importBaseInfos(self,baselist):
    cur = self.conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO baseInfo(baseId,blackMarket,landingPadSize) VALUES(:id,:blackMarket,:landingPadSize)",baselist)

    self.conn.commit()

  def importCommodityPrices(self,marketlist):
    cur = self.conn.cursor()
    # insert if new, skip if old
    cur.executemany("INSERT OR IGNORE INTO commodityPrices( commodityId, baseId, importPrice, exportPrice, lastUpdated, demand, supply ) VALUES(:commodityId,:baseId,:importPrice,:exportPrice,:lastUpdated,:demand,:supply)",marketlist)

    # update value if newer than db
    cur.executemany("""
    UPDATE commodityPrices
    SET importPrice=:importPrice, exportPrice=exportPrice, lastUpdated=:lastUpdated, demand=:demand, supply=:supply
    WHERE baseId=:baseId AND commodityId=:commodityId AND lastUpdated<:lastUpdated
    """, marketlist)
    self.conn.commit()

  def getGalaxyExtents(self):
    cur = self.conn.cursor()

    cur.execute("""
    SELECT MAX(x) AS maxX, MIN(x) AS minX, MAX(y) AS maxY, MIN(y) AS minY, MAX(z) AS maxZ, MIN(z) AS minZ
    FROM
    systems,bases
    WHERE
    bases.systemId=systems.id --we only want systems with stations on them
    """)

    return self._rowToDict(cur.fetchone())

  def getWindowProfit(self,queryvals):
    cur = self.conn.cursor()

    queryvals['maxdistance'] = 'maxdistance' in queryvals and queryvals['maxdistance'] or 30
    queryvals['window'] = 'window' in queryvals and queryvals['window']/2 or 30
    queryvals['minprofit'] = 'minprofit' in queryvals and queryvals['minprofit'] or 1000
    queryvals['landingPadSize'] = 'landingPadSize' in queryvals and queryvals['landingPadSize'] or 0

    # TODO: distance from star limit

    # full querystring
    querystring="""
    WITH systemwindow AS (
      SELECT
        systems.name AS systemname, bases.name AS basename, commodityPrices.baseId, systemId, distance, landingPadSize, x, y, z,
        commodityId, exportPrice, supply, importPrice, demand, commodities.name AS commodityname, average
      FROM
        commodities,
        commodityPrices,
        bases,
        baseInfo,
        systems
      WHERE
        average>:minprofit*6
        AND
        commodityPrices.commodityId=commodities.id
        AND
        commodityPrices.baseId=bases.id
        AND
        bases.systemId=systems.id
        AND
        baseInfo.baseId=bases.id
        AND
        baseInfo.landingPadSize>=:landingPadSize
        AND
        :x-:window<x AND x<:x+:window AND :y-:window<y AND y<:y+:window AND :z-:window<z AND z<:z+:window
    )
    SELECT
        B.importPrice-A.exportPrice AS profit,
        (
            (A.x - B.x)*(A.x - B.x)
            +
            (A.y - B.y)*(A.y - B.y)
            +
            (A.z - B.z)*(A.z - B.z)
        ) AS DistanceSq,
        A.commodityname AS commodityname,
        A.commodityId AS commodityId,
        A.average AS average,
        A.systemname AS Asystemname, A.basename AS Abasename, A.baseId AS AbaseId, A.systemId AS AsystemId, A.distance AS Adistance, A.landingPadSize AS AlandingPadSize,
        A.exportPrice AS AexportPrice, A.supply AS Asupply,
        A.x AS Ax, A.y AS Ay, A.z AS Az,
        B.systemname AS Bsystemname, B.basename AS Bbasename, B.baseId AS BbaseId, B.systemId AS BsystemId, B.distance AS Bdistance, B.landingPadSize AS BlandingPadSize,
        B.importPrice AS BimportPrice, B.demand AS Bdemand,
        B.x AS Bx, B.y AS By, B.z AS Bz
      FROM
        systemwindow AS A,
        systemwindow AS B
    WHERE
        --B.importPrice > B.average
        --AND
        A.commodityId=B.commodityId
        AND
        distanceSQ < :maxdistance*:maxdistance
        AND
        A.exportPrice BETWEEN 1 AND A.average
        AND
        profit > :minprofit
    --ORDER BY profit DESC
    --LIMIT 0,10
    """

    if not queryvals['landingPadSize']>0: # query without landingpads
      querystring="""
      WITH systemwindow AS (
        SELECT
          systems.name AS systemname, bases.name AS basename, commodityPrices.baseId, systemId, distance, landingPadSize, x, y, z,
          commodityId, exportPrice, supply, importPrice, demand, commodities.name AS commodityname, average
        FROM
          commodities,
          commodityPrices,
          bases,
          baseInfo,
          systems
        WHERE
          average>:minprofit*6
          AND
          commodityPrices.commodityId=commodities.id
          AND
          commodityPrices.baseId=bases.id
          AND
          bases.systemId=systems.id
          AND
          :x-:window<x AND x<:x+:window AND :y-:window<y AND y<:y+:window AND :z-:window<z AND z<:z+:window
          AND
          baseInfo.baseId=bases.id
      )
      SELECT
          B.importPrice-A.exportPrice AS profit,
          (
              (A.x - B.x)*(A.x - B.x)
              +
              (A.y - B.y)*(A.y - B.y)
              +
              (A.z - B.z)*(A.z - B.z)
          ) AS DistanceSq,
          A.commodityname AS commodityname,
          A.commodityId AS commodityId,
          A.average AS average,
          A.systemname AS Asystemname, A.basename AS Abasename, A.baseId AS AbaseId, A.systemId AS AsystemId, A.distance AS Adistance, A.landingPadSize AS AlandingPadSize,
          A.exportPrice AS AexportPrice, A.supply AS Asupply,
          A.x AS Ax, A.y AS Ay, A.z AS Az,
          B.systemname AS Bsystemname, B.basename AS Bbasename, B.baseId AS BbaseId, B.systemId AS BsystemId, B.distance AS Bdistance, B.landingPadSize AS BlandingPadSize,
          B.importPrice AS BimportPrice, B.demand AS Bdemand,
          B.x AS Bx, B.y AS By, B.z AS Bz
        FROM
          systemwindow AS A,
          systemwindow AS B
      WHERE
          --B.importPrice > B.average
          --AND
          A.commodityId=B.commodityId
          AND
          distanceSQ < :maxdistance*:maxdistance
          AND
          A.exportPrice BETWEEN 1 AND A.average
          AND
          profit > :minprofit
      --ORDER BY profit DESC
      --LIMIT 0,10
      """


    querystart=time.time()
    result=cur.execute(querystring,queryvals).fetchall()
    querytime=time.time()-querystart

    print("queryProfitWindow, "+str(len(result))+" values, "+str("%.2f"%querytime)+" seconds")

    return [self._rowToDict(o) for o in result]
