import os
import os.path
import json

class EDDB:

  def __init__(self):
    pass

  def update(self,db):
    # todo: download
    self.importDownloaded(db)

  def importDownloaded(self,db):
    if not os.path.exists('systems.json') or not os.path.exists('commodities.json') or not os.path.exists('stations.json'):
      print("eddb json files missing! - required: systems.json, commodities.json, stations.json")
      return False

    # -- commodities --

    print("improting eddb commodities")
    json_data=open("commodities.json").read()
    try:
      commoditiesdata = json.loads(json_data)
    except:
      print("parsing commodities.json failed")
      return False

    # insert into db and retrieve new ids
    importedCommodities=db.importCommodities([[o["name"],o["average_price"]] for o in commoditiesdata])

    # name to id map
    importedCommoditiesMap=dict( (y,x) for x,y in importedCommodities )

    # eddb to EliteDB id map
    commodities_importmap=dict( (o["id"],importedCommoditiesMap[o["name"]]) for o in commoditiesdata )

    # -- systems --

    print("               systems")
    json_data=open("systems.json").read()
    try:
      systemsdata = json.loads(json_data)
    except:
      print("parsing systems.json failed")
      return False

    # insert into db and retrieve new ids
    importedSystems=db.importSystems([[o["name"],o["x"],o["y"],o["z"]] for o in systemsdata])

    # name to id map
    importedSystemsMap=dict( (y,x) for x,y in importedSystems )

    # eddb to EliteDB id map
    systems_importmap=dict( (o["id"],importedSystemsMap[o["name"]]) for o in systemsdata )

    # -- stations --

    print("               stations")
    json_data=open("stations.json").read()
    try:
      stationsdata = json.loads(json_data)
    except:
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

    print("               station metadata")

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

    print("               market data")

    marketdata=[]
    # remap database ids
    for station in stationsdata:
      for commodity in station["listings"]:
        commodity["station_id"]=station["id"] # stationid already remapped
        commodity["commodity_id"]=commodities_importmap[commodity["commodity_id"]]
        marketdata.append(commodity)

    # note: eddb works from the perspective of the player - "sell" is import, "buy" is export
    db.importCommodityPrices([[o["commodity_id"],o["station_id"],o["sell_price"],o["buy_price"],o["collected_at"],o["demand"],o["supply"]] for o in marketdata])

    print("eddb import complete")
