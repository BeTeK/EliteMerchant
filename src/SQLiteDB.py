import threading
import sqlite3
import EliteDB
import os.path
import os
import operator
import System
import Base
import time
import datetime
import CommodityPrice
import Commodity
import SpaceTime
from math import *

class SQLiteDB(EliteDB.EliteDB):
  
  def __init__(self, filename, forceInit = False):
    super().__init__()
    print(filename)
    self.filename = filename
    self.forceInit = forceInit
    self.commodityCache = {}
    self.lock = threading.RLock()
    self.dbEmpty=False # set this to true if db load fails for whatever reason and we need to force download


  def __enter__(self):
    self._init()
    return self

  def _init(self):
    exists = os.path.exists(self.filename)
    if exists and self.forceInit:
      os.remove(self.filename)

    self.conn = sqlite3.connect(self.filename, check_same_thread = False)

    # custom db functions
    # https://docs.python.org/2/library/sqlite3.html#sqlite3.Connection.create_function
    self.conn.create_function("StarToBase", 1, SpaceTime.StarToBase)
    self.conn.create_function("BaseToBase", 2, SpaceTime.BaseToBase)
    def distance3d(x,y,z,i,j,k):
      return ((x-i)**2+(y-j)**2+(z-k)**2)**.5
    self.conn.create_function("Distance3D", 6, distance3d)

    # database settings
    cur=self.conn.cursor()
    cur.execute("""PRAGMA cache_size = 1000000""")

    self.conn.row_factory = sqlite3.Row
    if not exists or self.forceInit:
      self._createDB()
      self.dbEmpty=True

    
  def __exit__(self, type, value, traceback):
    if self.conn is not None:
      self.conn.close()

  def vacuum(self):
    with self.lock:
      print("vacuuming database...")
      cur=self.conn.cursor()
      cur.execute("VACUUM")
      return

  def getBasesOfSystem(self, id):
    with self.lock:
      cur = self.conn.cursor()

      cur.execute("SELECT bases.id, bases.name, bases.planetId, bases.distance, baseInfo.blackMarket, baseInfo.landingPadSize FROM  (bases LEFT JOIN baseInfo ON bases.id = baseInfo.baseId) WHERE bases.systemId = ?", (id, ))

      return [self._dictToBase(self._rowToDict(i)) for i in cur.fetchall()]

  def getBasesOfSystemByName(self, name):
    with self.lock:
      cur = self.conn.cursor()

      cur.execute("SELECT bases.id, bases.name, bases.planetId, bases.distance, baseInfo.blackMarket, baseInfo.landingPadSize FROM  (bases LEFT JOIN baseInfo ON bases.id = baseInfo.baseId), systems WHERE systems.id=bases.systemId AND systems.name LIKE ?", (name, ))

      return [self._dictToBase(self._rowToDict(i)) for i in cur.fetchall()]

  def _dictToBase(self, info):
    return Base.Base(self, info["id"], info["name"], info["blackMarket"], info["landingPadSize"], info["distance"])

  def getSystemByWindow(self, pos, windowSize):
    with self.lock:
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
    with self.lock:
      cur = self.conn.cursor()
      cur.execute("SELECT id, name, x, y, z FROM systems WHERE systems.name LIKE ?", (name, ))

      return [self._dictToSystem(self._rowToDict(i)) for i in cur.fetchmany(limit)]

  def getSystemById(self, id):
    with self.lock:
      cur = self.conn.cursor()
      cur.execute("SELECT id, name, x, y, z FROM systems WHERE systems.id=?", (id, ))

      result = cur.fetch()
      if result is None:
        return None
      else:
        return self._dictToSystem(self._rowToDict(result))

  def getCommodityByName(self, name):
    with self.lock:
      #if len(self.commodityCache) > 0:
      #  for i in self.commodityCache.values():
      #    if i.getName() == name:
      #      return i

        cur = self.conn.cursor()

        cur.execute("SELECT id, name, average FROM commodities WHERE commodities.name like ?", (name, ))
        rows = cur.fetchall()
        if len(rows) != 1:
          return None

        data = self._rowToDict(rows[0])
        ret = self._dictToCommodity(data)
        #self.commodityCache[ret.getId()] = ret

        return ret

  def getCommodities(self):
    with self.lock:

      cur = self.conn.cursor()

      cur.execute("SELECT id, name, average FROM commodities")
      rows = cur.fetchall()
      if len(rows) == 0:
        return None

      for row in rows:
        data = self._rowToDict(row)
        if data['id'] not in self.commodityCache:
          ret = self._dictToCommodity(data)
          self.commodityCache[ret.getId()] = ret

      return self.commodityCache


  def getCommodity(self, id):
    with self.lock:
      if id not in self.commodityCache:
        cur = self.conn.cursor()

        cur.execute("SELECT id, name, average FROM commodities WHERE commodities.id = ?", (id, ))
        rows = cur.fetchall()
        if len(rows) != 1:
          return None

        data = self._rowToDict(rows[0])

        self.commodityCache[id] = self._dictToCommodity(data)

      return self.commodityCache[id]
  
  def _dictToCommodity(self, data):
    return Commodity.Commodity(self, data["id"], data["name"], data["average"])

  def getPricesOfCommoditiesInBase(self, baseId):
    with self.lock:
      cur = self.conn.cursor()
      cur.execute("SELECT id, baseId, supply, commodityId, demand, importPrice, exportPrice, lastUpdated FROM commodityPrices WHERE commodityPrices.baseId = ?", (baseId, ))

      return [self._dictToPriceData(self._rowToDict(i)) for i in cur.fetchall()]

  def _dictToPriceData(self, data):
    return CommodityPrice.CommodityPrice(self, data["id"], data["commodityId"], data["importPrice"], data["exportPrice"], data["demand"], datetime.date.fromtimestamp(data['lastUpdated']), data["baseId"], data["supply"])
  
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
    with self.lock:
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
    cur.execute("""CREATE INDEX "commodityPricesCommoditIdIndex" on commodityPrices (commodityId ASC)""")
    cur.execute("""CREATE INDEX "commodityPricesBaseIdIndex" on commodityPrices (baseId ASC)""")

    cur.execute("""CREATE TABLE bases (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" TEXT NOT NULL,
    "planetId" INTEGER,
    "systemId" INTEGER,
    "distance" REAL,
    UNIQUE (name,systemId)
    )""")
    cur.execute("""CREATE INDEX "basesIdIndex" on bases (id ASC)""")
    cur.execute("""CREATE INDEX "basesPlanetId" on bases (planetId ASC)""")
    cur.execute("""CREATE INDEX "basesNameIndex" on bases (name ASC)""")
    cur.execute("""CREATE INDEX "basesSystemIndex" on bases (systemId ASC)""")

    self.conn.commit()


  def importCommodities(self,commoditylist):
    with self.lock:
      cur = self.conn.cursor()
      cur.executemany("INSERT OR IGNORE INTO commodities(name,average) VALUES(:name,:average)",commoditylist)

      self.conn.commit()

      cur.execute('SELECT id,name FROM commodities')
      return [self._rowToDict(o) for o in cur.fetchall()]

  def importSystems(self,systemlist):
    with self.lock:
      cur = self.conn.cursor()
      cur.executemany("INSERT OR IGNORE INTO systems(name,x,y,z) VALUES(:name,:x,:y,:z)",systemlist)

      self.conn.commit()

      cur.execute('SELECT id,name FROM systems')
      return [self._rowToDict(o) for o in cur.fetchall()]

  def importBases(self,baselist):
    with self.lock:
      cur = self.conn.cursor()
      cur.executemany("INSERT OR IGNORE INTO bases(name,systemId,distance) VALUES(:name,:systemId,:distance)",baselist)

      self.conn.commit()
      cur.execute('SELECT id,name,systemId FROM bases')
      return [self._rowToDict(o) for o in cur.fetchall()]

  def importBaseInfos(self,baselist):
    with self.lock:
      cur = self.conn.cursor()
      cur.executemany("INSERT OR IGNORE INTO baseInfo(baseId,blackMarket,landingPadSize) VALUES(:id,:blackMarket,:landingPadSize)",baselist)

      self.conn.commit()

  def importCommodityPrices(self,marketlist):
    with self.lock:
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
    with self.lock:
      cur = self.conn.cursor()

      cur.execute("""
      SELECT MAX(x) AS maxX, MIN(x) AS minX, MAX(y) AS maxY, MIN(y) AS minY, MAX(z) AS maxZ, MIN(z) AS minZ
      FROM
      systems,bases,commodityPrices
      WHERE
      bases.systemId=systems.id -- we only want systems with stations on them
      AND
      bases.id=commodityPrices.baseId -- we only want bases with commodities on them
      """)

      return self._rowToDict(cur.fetchone())

  def getSystemNameList(self):
    with self.lock:
      cur = self.conn.cursor()

      cur.execute("""
      SELECT DISTINCT systems.name
      FROM
      systems,bases,commodityPrices
      WHERE
      bases.systemId=systems.id -- we only want systems with stations on them
      AND
      bases.id=commodityPrices.baseId -- we only want bases with commodities on them
      """)
      result=cur.fetchall()

      result=[self._rowToDict(o) for o in result]
      result=[row["name"] for row in result] # names only

      return sorted(result)

  def getCommoditiesInRange(self,queryvals):
    with self.lock:
      cur = self.conn.cursor()

      queryvals['maxdistance'] = 'maxdistance' in queryvals and queryvals['maxdistance'] or 30
      queryvals['landingPadSize'] = 'landingPadSize' in queryvals and queryvals['landingPadSize'] or 0
      queryvals['lastUpdated'] = 'lastUpdated' in queryvals and queryvals['lastUpdated'] or 7 # max week old
      queryvals['lastUpdated'] = int( time.time() - (60*60*24* queryvals['lastUpdated'] ))
      queryvals['jumprange'] = 'jumprange' in queryvals and queryvals['jumprange'] or 16
      queryvals['importexport'] = 'importexport' in queryvals and queryvals['importexport'] or 0 # check if exists and set to 1 or 0
      if 'commodityId' not in queryvals:
        return []

      querystring="""
      SELECT *,
      systems.name AS systemname,
      bases.name AS basename,
      exportPrice,
      commodities.name AS commodityname,
      importPrice,
      Distance3D( :x, :y, :z, x, y, z) AS SystemDistance,
      (
        (
          StarToBase( distance )
          +
          BaseToBase( Distance3D( :x, :y, :z, x, y, z) ,:jumprange)
        )/60/60
      ) AS hours,
      (
        (:x - x)*(:x - x)
        +
        (:y - y)*(:y - y)
        +
        (:z - z)*(:z - z)
      ) AS DistanceSq,
      CASE
        WHEN :importexport=0 THEN (importPrice/average)
        ELSE (average/exportPrice)
      END AS potentialsort,
      CASE
        WHEN :importexport=0 THEN importPrice
        ELSE exportPrice
      END AS notzero,
      (100*exportPrice/average) AS exportPavg,
      (100*importPrice/average) AS importPavg
      FROM commodityPrices, bases, baseInfo, systems, commodities
      WHERE
      landingPadSize=:landingPadSize
      AND
      DistanceSQ<:maxdistance*:maxdistance
      AND
      commodityPrices.commodityId=:commodityId
      AND
      commodityPrices.baseId=bases.id
      AND
      bases.systemId=systems.id
      AND
      bases.id=baseInfo.baseId
      AND
      commodities.id=commodityPrices.commodityId
      AND
      notzero>0
      ORDER BY hours DESC
      --ORDER BY notzero DESC
      --LIMIT 0,50000
      """

      querystart=time.time()
      result=cur.execute(querystring,queryvals).fetchall()
      querytime=time.time()-querystart

      asdict=[self._rowToDict(o) for o in result]
      for ass in asdict:
        ass["potential"]=ass["potentialsort"]/(ass["hours"]/60)

      asdict.sort(key=operator.itemgetter("potential"),reverse=True) # sort by value deviation from avg per hours

      print("getCommoditiesInRange, "+str(len(result))+" values, "+str("%.2f"%querytime)+" seconds")
      return asdict

  def getWindowProfit(self,queryvals):
    with self.lock:
      cur = self.conn.cursor()

      queryvals['maxdistance'] = 'maxdistance' in queryvals and queryvals['maxdistance'] or 30
      queryvals['window'] = 'window' in queryvals and queryvals['window']/2 or 50
      queryvals['minprofit'] = 'minprofit' in queryvals and queryvals['minprofit'] or 0
      queryvals['minprofitPh'] = 'minprofitPh' in queryvals and queryvals['minprofitPh'] or 0
      queryvals['landingPadSize'] = 'landingPadSize' in queryvals and queryvals['landingPadSize'] or 0
      queryvals['lastUpdated'] = 'lastUpdated' in queryvals and queryvals['lastUpdated'] or 7 # max week old
      queryvals['lastUpdated'] = int( time.time() - (60*60*24* queryvals['lastUpdated'] ))
      queryvals['jumprange'] = 'jumprange' in queryvals and queryvals['jumprange'] or 16


      querystring="""
      WITH systemwindow AS (
      SELECT
        systems.name AS systemname, bases.name AS basename, commodityPrices.baseId, systemId, distance, landingPadSize, x, y, z,
        commodityId, exportPrice, supply, importPrice, demand, commodities.name AS commodityname, average, lastUpdated
      FROM
        commodities,
        commodityPrices,
        bases,
        baseInfo,
        systems
      WHERE
        average>:minprofit*6
        AND
        commodityPrices.lastUpdated>:lastUpdated
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
        Distance3D( A.x, A.y, A.z, B.x, B.y, B.z) AS SystemDistance,
        (
          (
            StarToBase( B.distance )
            +
            BaseToBase( Distance3D( A.x, A.y, A.z, B.x, B.y, B.z) ,:jumprange)
          )/60/60
        ) AS hours,
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
        A.exportPrice AS AexportPrice, A.supply AS Asupply, A.lastUpdated AS AlastUpdated,
        A.x AS Ax, A.y AS Ay, A.z AS Az,
        B.systemname AS Bsystemname, B.basename AS Bbasename, B.baseId AS BbaseId, B.systemId AS BsystemId, B.distance AS Bdistance, B.landingPadSize AS BlandingPadSize,
        B.importPrice AS BimportPrice, B.demand AS Bdemand, B.lastUpdated AS BlastUpdated,
        B.x AS Bx, B.y AS By, B.z AS Bz
      FROM
        systemwindow AS A,
        systemwindow AS B
      WHERE
        --B.importPrice > B.average
        --AND
        A.commodityId=B.commodityId
        AND
        --SystemDistance < :maxdistance
        DistanceSq < :maxdistance*:maxdistance
        AND
        A.exportPrice BETWEEN 1 AND A.average
        AND
        profit > :minprofit
        --AND
        --profit/hours > :minprofitPh
        --ORDER BY profit DESC
        --LIMIT 0,10
      """

      querystart=time.time()
      result=cur.execute(querystring,queryvals).fetchall()
      querytime=time.time()-querystart

      print("queryProfitWindow, "+str(len(result))+" values, "+str("%.2f"%querytime)+" seconds")
      rows=[self._rowToDict(o) for o in result]
      for row in rows:
        row['profitPh']=row['profit']/row['hours']
      return rows


  def getTradeFrom(self,queryvals):
    with self.lock:
      cur = self.conn.cursor()

      queryvals['maxdistance'] = 'maxdistance' in queryvals and queryvals['maxdistance'] or 30
      queryvals['window'] = queryvals['maxdistance'] # there's no slack with the windowing so keep it tight
      queryvals['minprofit'] = 0
      queryvals['minprofitPh'] = 0
      queryvals['landingPadSize'] = 'landingPadSize' in queryvals and queryvals['landingPadSize'] or 0
      queryvals['lastUpdated'] = 'lastUpdated' in queryvals and queryvals['lastUpdated'] or 7 # max week old
      queryvals['lastUpdated'] = int( time.time() - (60*60*24* queryvals['lastUpdated']*2 ))  # allow twice as old
      queryvals['jumprange'] = 'jumprange' in queryvals and queryvals['jumprange'] or 16
      queryvals['sourcesystem'] = 'sourcesystem' in queryvals and queryvals['sourcesystem'] or '%'
      queryvals['sourcebase'] = 'sourcebase' in queryvals and queryvals['sourcebase'] or '%'

      querystring="""
      WITH systemwindow AS (
      SELECT
        systems.name AS systemname, bases.name AS basename, commodityPrices.baseId, systemId, distance, landingPadSize, x, y, z,
        commodityId, exportPrice, supply, importPrice, demand, commodities.name AS commodityname, average, lastUpdated
      FROM
        commodities,
        commodityPrices,
        bases,
        baseInfo,
        systems
      WHERE
        --commodityPrices.lastUpdated>:lastUpdated
        --AND
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
        Distance3D( A.x, A.y, A.z, B.x, B.y, B.z) AS SystemDistance,
        (
          (
            StarToBase( B.distance )
            +
            BaseToBase( Distance3D( A.x, A.y, A.z, B.x, B.y, B.z) ,:jumprange)
          )/60/60
        ) AS hours,
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
        A.exportPrice AS AexportPrice, A.supply AS Asupply, A.lastUpdated AS AlastUpdated,
        A.x AS Ax, A.y AS Ay, A.z AS Az,
        B.systemname AS Bsystemname, B.basename AS Bbasename, B.baseId AS BbaseId, B.systemId AS BsystemId, B.distance AS Bdistance, B.landingPadSize AS BlandingPadSize,
        B.importPrice AS BimportPrice, B.demand AS Bdemand, B.lastUpdated AS BlastUpdated,
        B.x AS Bx, B.y AS By, B.z AS Bz
      FROM
        systemwindow AS A,
        systemwindow AS B
      WHERE
        A.systemname LIKE :sourcesystem
        AND
        A.basename LIKE :sourcebase
        AND
        A.commodityId=B.commodityId
        AND
        --DistanceSq < :maxdistance*:maxdistance*2
        --AND
        profit > 0
        AND
        A.exportPrice > 0
      """

      querystart=time.time()
      result=cur.execute(querystring,queryvals).fetchall()
      querytime=time.time()-querystart

      print("getTradeFrom, "+str(len(result))+" values, "+str("%.2f"%querytime)+" seconds")
      rows=[self._rowToDict(o) for o in result]
      for row in rows:
        row['profitPh']=row['profit']/row['hours']
      return rows

  def getTradeDirect(self,queryvals):
    with self.lock:
      cur = self.conn.cursor()

      queryvals['maxdistance'] = 'maxdistance' in queryvals and queryvals['maxdistance'] or 30
      queryvals['window'] = 'window' in queryvals and queryvals['window']/2 or 50
      queryvals['minprofit'] = 'minprofit' in queryvals and queryvals['minprofit'] or 0
      queryvals['minprofitPh'] = 'minprofitPh' in queryvals and queryvals['minprofitPh'] or 0
      queryvals['landingPadSize'] = 'landingPadSize' in queryvals and queryvals['landingPadSize'] or 0
      queryvals['lastUpdated'] = 'lastUpdated' in queryvals and queryvals['lastUpdated'] or 7 # max week old
      queryvals['lastUpdated'] = int( time.time() - (60*60*24* queryvals['lastUpdated'] ))*2  # allow twice as old
      queryvals['jumprange'] = 'jumprange' in queryvals and queryvals['jumprange'] or 16
      queryvals['sourcesystem'] = 'sourcesystem' in queryvals and queryvals['sourcesystem'] or '%'
      queryvals['sourcebase'] = 'sourcebase' in queryvals and queryvals['sourcebase'] or '%'
      queryvals['targetsystem'] = 'targetsystem' in queryvals and queryvals['targetsystem'] or '%'
      queryvals['targetbase'] = 'targetbase' in queryvals and queryvals['targetbase'] or '%'

      querystring="""
      WITH systemwindow AS (
      SELECT
        systems.name AS systemname, bases.name AS basename, commodityPrices.baseId, systemId, distance, landingPadSize, x, y, z,
        commodityId, exportPrice, supply, importPrice, demand, commodities.name AS commodityname, average, lastUpdated
      FROM
        commodities,
        commodityPrices,
        bases,
        baseInfo,
        systems
      WHERE
        (
          systems.name LIKE :sourcesystem
          OR
          systems.name LIKE :targetsystem
        )
        --AND
        --commodityPrices.lastUpdated>:lastUpdated
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
      )
      SELECT
        B.importPrice-A.exportPrice AS profit,
        Distance3D( A.x, A.y, A.z, B.x, B.y, B.z) AS SystemDistance,
        (
          (
            StarToBase( B.distance )
            +
            BaseToBase( Distance3D( A.x, A.y, A.z, B.x, B.y, B.z) ,:jumprange)
          )/60/60
        ) AS hours,
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
        A.exportPrice AS AexportPrice, A.supply AS Asupply, A.lastUpdated AS AlastUpdated,
        A.x AS Ax, A.y AS Ay, A.z AS Az,
        B.systemname AS Bsystemname, B.basename AS Bbasename, B.baseId AS BbaseId, B.systemId AS BsystemId, B.distance AS Bdistance, B.landingPadSize AS BlandingPadSize,
        B.importPrice AS BimportPrice, B.demand AS Bdemand, B.lastUpdated AS BlastUpdated,
        B.x AS Bx, B.y AS By, B.z AS Bz
      FROM
        systemwindow AS A,
        systemwindow AS B
      WHERE
        A.systemname LIKE :sourcesystem
        AND
        A.basename LIKE :sourcebase
        AND
        B.systemname LIKE :targetsystem
        AND
        B.basename LIKE :targetbase
        AND
        A.commodityId=B.commodityId
        AND
        profit > 0
        AND
        A.exportPrice > 0
      """

      querystart=time.time()
      result=cur.execute(querystring,queryvals).fetchall()
      querytime=time.time()-querystart

      print("getTradeDirect, "+str(len(result))+" values, "+str("%.2f"%querytime)+" seconds")
      rows=[self._rowToDict(o) for o in result]
      for row in rows:
        row['profitPh']=row['profit']/row['hours']
      return rows
