import os
import os.path
import json
import urllib
import time

eddbUrls={
  "commodities":"http://eddb.io/archive/v3/commodities.json",
  "systems":"http://eddb.io/archive/v3/systems.json",
  "stations":"http://eddb.io/archive/v3/stations.json"
}

def readJSON(filename):
  try:
    with open(filename, "r") as file:
      return json.loads(file.read())
  except Exception as ex:
    print(ex)
    return None


def update(db):
  #if checkUpdated(db):
  #  download(db)
  importDownloaded(db)

def checkUpdated(db):

  with urllib.request.urlopen(eddbUrls['stations'], timeout=30) as conn:
    last_modified = conn.info().getdate('last-modified')
    time_struct = time.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
    # todo: this thing
    ## return conf["EDDBlastdownload"] < time_struct

  return False

def download(db):
  # compression header:
  #Accept-Encoding: gzip, deflate, sdch
  # todo: download
  pass

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



  print("eddb import complete")
