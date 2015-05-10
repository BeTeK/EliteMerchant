from SQLiteDB import SQLiteDB

import os
import os.path
import json

def updatePrices(db):
  pass
  
def readJSON(filename):
  try:
    with open(filename, "r") as file:
      return json.loads(file.read())
  except Exception as ex:
    print(ex)
    return None

def importEDDB(db):
  if not os.path.exists('systems.json') or not os.path.exists('commodities.json') or not os.path.exists('stations.json'):
    print("eddb json files missing! - required: systems.json, commodities.json, stations.json")
    return False

  # -- commodities --

  print("improting eddb commodities")
  commoditiesdata = readJSON("commodities.json")
  if commoditiesdata is None:
    print("parsing commodities.json failed")
    return False

  # insert into db and retrieve new ids
  importedCommodities=db.importCommodities([[o["name"]] for o in commoditiesdata])

  # name to id map
  importedCommoditiesMap=dict( (y,x) for x,y in importedCommodities )

  # eddb to EliteDB id map
  commodities_importmap=dict( (o["id"],importedCommoditiesMap[o["name"]]) for o in commoditiesdata )

  # -- systems --

  print("improting eddb systems")
  systemsdata = readJSON("systems.json")
  if systemsdata is None:
    print("parsing systems.json failed")
    return False

  # insert into db and retrieve new ids
  importedSystems=db.importSystems([[o["name"],o["x"],o["y"],o["z"]] for o in systemsdata])

  # name to id map
  importedSystemsMap=dict( (y,x) for x,y in importedSystems )

  # eddb to EliteDB id map
  systems_importmap=dict( (o["id"],importedSystemsMap[o["name"]]) for o in systemsdata )

  # -- stations --

  print("improting eddb stations")
  stationsdata = readJSON("stations.json")
  if stationsdata is None:
    print("parsing stations.json failed")
    return False

  # remap database ids
  for station in stationsdata:
    station["system_id"]=systems_importmap[station["system_id"]]

  # insert into db and retrieve new ids
  importedStations=db.importBases([[o["name"],None,o["system_id"],o["distance_to_star"]] for o in stationsdata])

  # name to id map
  importedStationsMap=dict( (y,x) for x,y in importedStations )

  # eddb to EliteDB id map
  stations_importmap=dict( (o["id"],importedStationsMap[o["name"]]) for o in stationsdata )

  # -- station metadata --

  print("improting eddb station metadata")

  # remap database ids
  for station in stationsdata:
    station["id"]=stations_importmap[station["id"]]

  padsize={
    None:None,
    "S":0,
    "M":1,
    "L":2
  }
  db.importBaseInfos([[o["id"],o["has_blackmarket"],padsize[o["max_landing_pad_size"]]] for o in stationsdata])

  # -- station market data --

  print("improting eddb station market data")

  marketdata=[]
  # remap database ids
  for station in stationsdata:
    for commodity in station["listings"]:
      commodity["station_id"]=station["id"] # stationid already remapped
      commodity["commodity_id"]=commodities_importmap[commodity["commodity_id"]]
      marketdata.append(commodity)

  db.importCommodityPrices([[o["commodity_id"],o["station_id"],o["buy_price"],o["sell_price"],o["collected_at"],o["demand"],o["supply"]] for o in marketdata])

  print("eddb import complete")


def addSystem(db):
  db.addSystem("foobar2")

def fetchSystem(db):
  systems = db.getSystemByName("sol")
  systems[0].getStations()

def main():
  with SQLiteDB("main.sqlite") as db:
    #importEDDB(db)
    fetchSystem(db)





if __name__ == "__main__":
  main()
