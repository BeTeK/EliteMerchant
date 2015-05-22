import os
import os.path
import json
from urllib import request, parse
import time
import Options
import sys
import gzip
from io import BytesIO

eddbUrls={
  "commodities.json":"http://eddb.io/archive/v3/commodities.json",
  "systems.json":"http://eddb.io/archive/v3/systems.json",
  "stations.json":"http://eddb.io/archive/v3/stations.json"
}

def readJSON(filename):
  try:
    with open(filename, "r") as file:
      return json.loads(file.read())
  except Exception as ex:
    print(ex)
    return None

def downloadFile(url):

  # compression header:
  #Accept-Encoding: gzip, deflate, sdch

  file_name = url.split('/')[-1]
  header={
    #"Accept-Encoding": "gzip, deflate, sdch"
    "Accept-Encoding": "gzip"
  }
  lastupdate=0
  updateinterval=0.5

  def formatprogress(file_size_dl,file_size):
    if file_size is not None:
      return "\r%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    else:
      return "\r%10d" % file_size_dl

  rq=request.Request(url,None,header)
  with request.urlopen(rq) as req:
    meta = req.info()
    block_sz = 8192
    filebuffer=""
    file_size=None

    if meta.get('Content-Encoding') == 'gzip': # gunzip - download all in one go
      print("Downloading: %s" % file_name)
      filebuffer=req.read()
    else:
      if meta.get("Content-Length") is not None:  # if we known file length, have fancy progress indication
        file_size = int(meta.get("Content-Length"))
        print("Downloading: %s Bytes: %s" % (file_name, file_size))
      else:
        print("Downloading: %s" % file_name)

      while True:
        buffer = req.read(block_sz)
        if not buffer:
            break
        filebuffer+=buffer
        if time.time()-updateinterval > lastupdate: # console may slow us down so keep update intervals
          lastupdate=time.time()
          sys.stdout.write(formatprogress(len(filebuffer),file_size))

    with open(file_name, 'wb') as file:
      if meta.get('Content-Encoding') == 'gzip': # gunzip
        #buf = StringIO( filebuffer )
        buf = BytesIO( filebuffer )
        f = gzip.GzipFile(fileobj=buf)
        filebuffer = f.read()
      file.write(filebuffer)

    sys.stdout.write(formatprogress(len(filebuffer),file_size))
    print("  -  Done!")

    last_modified = meta.get('last-modified')
    #time_struct = time.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    #timestamp=time.mktime(time_struct)
    Options.set("EDDB-lastmodified-"+file_name,last_modified)


def update(db):
  print("Checking for updated EDDB database")
  anyUpdated=False
  for file in eddbUrls:
    if checkUpdated(file,eddbUrls[file]):
      anyUpdated=True
      downloadFile(eddbUrls[file])
  if anyUpdated:
    importDownloaded(db)

def checkUpdated(file,url):
  with request.urlopen(url, timeout=30) as conn:
    meta=conn.info()
    last_modified = meta.get('last-modified')
    #time_struct = time.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    #timestamp=time.mktime(time_struct)
    if last_modified != Options.get("EDDB-lastmodified-"+file,0):
      return True

  return False

def importDownloaded(db):
  if not os.path.exists('systems.json') or not os.path.exists('commodities.json') or not os.path.exists('stations.json'):
    print("eddb json files missing! - required: systems.json, commodities.json, stations.json")
    return False

  # -- commodities --

  print("improting eddb commodities")
  commoditiesdata = readJSON("commodities.json")
  if commoditiesdata is None:
    print("parsing commodities.json failed")
    return False

  # remap database columns
  for commodity in commoditiesdata:
    commodity['average']=commodity['average_price']

  # insert into db and retrieve new ids
  importedCommodities=db.importCommodities(commoditiesdata)

  # name to id map
  importedCommoditiesMap=dict( (o["name"].lower(),o["id"]) for o in importedCommodities )

  # eddb to EliteDB id map
  commodities_importmap=dict( (o["id"],importedCommoditiesMap[o["name"].lower()]) for o in commoditiesdata )

  # -- systems --

  print("               systems")
  systemsdata = readJSON("systems.json")
  if systemsdata is None:
    print("parsing systems.json failed")
    return False

  # insert into db and retrieve new ids
  importedSystems=db.importSystems(systemsdata)

  # name to id map
  importedSystemsMap=dict( (o["name"].lower(),o["id"]) for o in importedSystems )

  # eddb to EliteDB id map
  systems_importmap=dict( (o["id"],importedSystemsMap[o["name"].lower()]) for o in systemsdata )

  # -- stations --

  print("               stations")
  stationsdata = readJSON("stations.json")
  if stationsdata is None:
    print("parsing stations.json failed")
    return False

  # remap database
  for station in stationsdata:
    station["systemId"]=systems_importmap[station["system_id"]]
    station["distance"]=station["distance_to_star"]

  # insert into db and retrieve new ids
  importedStations=db.importBases(stationsdata)

  # name to id map
  importedStationsMap=dict( (o["name"].lower(),o["id"]) for o in importedStations )

  # eddb to EliteDB id map
  stations_importmap=dict( (o["id"],importedStationsMap[o["name"].lower()]) for o in stationsdata )

  # -- station metadata --

  print("               station metadata")

  padsize={
    None:None,
    "S":0,
    "M":1,
    "L":2
  }
  # remap database
  for station in stationsdata:
    station["id"]=stations_importmap[station["id"]]
    station["blackMarket"]=station["has_blackmarket"]
    station["landingPadSize"]=padsize[station["max_landing_pad_size"]]

  db.importBaseInfos(stationsdata)

  # -- station market data --

  print("               market data")

  marketdata=[]
  # remap database
  for station in stationsdata:
    for commodity in station["listings"]:
      commodity["baseId"]=station["id"] # stationid already remapped
      commodity["commodityId"]=commodities_importmap[commodity["commodity_id"]]
      commodity["importPrice"]=commodity["sell_price"] # note: eddb works from the perspective of the player - "sell" is import, "buy" is export
      commodity["exportPrice"]=commodity["buy_price"]
      commodity["lastUpdated"]=commodity["collected_at"]
      marketdata.append(commodity)

  db.importCommodityPrices(marketdata)

  db.vacuum()

  print("eddb import complete")
