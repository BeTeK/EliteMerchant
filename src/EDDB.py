import os
import os.path
import json
from urllib import request, parse
import time
import Options
import sys
import gzip
from io import BytesIO
import datetime
import Powers

eddbUrls={
  "commodities.json":"http://eddb.io/archive/v3/commodities.json",
  "systems.json":"http://eddb.io/archive/v3/systems.json",
  "stations.json":"http://eddb.io/archive/v3/stations.json"
}

def readJSON(filename):
  try:
    with open(Options.getPath(filename), "r") as file:
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

    with open(Options.getPath(file_name), 'wb') as file:
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


def update(db,force=False):
  print("Checking for EDDB database update")
  Options.set("EDDB-last-updated", int(datetime.datetime.now().timestamp()))
  anyUpdated=False
  for file in eddbUrls:
    if force or checkUpdated(file,eddbUrls[file]):
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
  if not os.path.exists(Options.getPath('systems.json')) or not os.path.exists(Options.getPath('commodities.json')) or not os.path.exists(Options.getPath('stations.json')):
    print("eddb json files missing! - required: systems.json, commodities.json, stations.json")
    return False

  # -- commodities --

  print("importing eddb commodities")
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

  # commodityname to EliteDB id map (for prohibited commodities later on)
  importedCommoditiesByName=dict( (o["name"],importedCommoditiesMap[o["name"].lower()]) for o in commoditiesdata )


  # -- systems --

  systemsdata = readJSON("systems.json")
  if systemsdata is None:
    print("parsing systems.json failed")
    return False

  print('resolving system allegiances')

  allegiance={
    None:None,
    "Empire":3,
    "Federation":2,
    "Alliance":1
  }

  def distance3d(x,y,z,i,j,k):
    return ((x-i)**2+(y-j)**2+(z-k)**2)**.5

  controlsystems=dict()

  # reformat faction allegiances, find power control systems
  for system in systemsdata:
    if system['allegiance'] in allegiance:
      system['allegiance']=allegiance[system['allegiance']]
    else:
      system['allegiance']=0

    # control systems
    powerid=Powers.nameToVal(system['power_control_faction'])
    system['controlled']=powerid
    system['exploited']=powerid
    if system['power_control_faction'] is not None:
      if powerid not in controlsystems:
        controlsystems[powerid]=[]
      controlsystems[powerid].append(system)

  print( 'The galaxy has' , str(len(list(controlsystems.keys()))) , 'powers' )

  # bake power exploited values
  for p in controlsystems:
    print(Powers.valToName(p), 'has', len(controlsystems[p]) , 'control systems')
    exploited=0
    for c in controlsystems[p]:
      powerid=c['controlled']
      x,y,z=c['x'],c['y'],c['z']
      for system in systemsdata:
        # if ours, contested or control system, ignore
        if system['exploited']==powerid or system['exploited']==-1 or system['controlled'] is not None:
          continue
        x2,y2,z2=system['x'],system['y'],system['z']
        if distance3d(x,y,z,x2,y2,z2) <= 15: # everything within 15ly is exploited
          if system['exploited'] is not None: # if some other power has it in range, it's contested
            system['exploited']=-1
          else:
            system['exploited']=powerid # else it's ours
            exploited+=1
    print(' has',str(exploited),'exploited systems')

  print("importing eddb systems")

  # insert into db and retrieve new ids
  importedSystems=db.importSystems(systemsdata)

  # name to id map
  importedSystemsMap=dict( (o["name"].lower(),o["id"]) for o in importedSystems )

  # eddb to EliteDB id map
  systems_importmap=dict( (o["id"],importedSystemsMap[o["name"].lower()]) for o in systemsdata )

  # id to row map
  systemRowById=dict( (o["id"],o) for o in importedSystems )


  # -- stations --

  print("importing eddb stations")
  stationsdata = readJSON("stations.json")
  if stationsdata is None:
    print("parsing stations.json failed")
    return False

  # remap database
  for station in stationsdata:
    station["systemId"]=systems_importmap[station["system_id"]]
    station["distance"]=station["distance_to_star"]
    system=systemRowById[station["systemId"]]
    Powers.applyPowerPolicy(system['controlled'],system['exploited'],[station])

  # insert into db and retrieve new ids
  importedStations=db.importBases(stationsdata)

  # name to id map
  importedStationsMap=dict( (o["name"].lower()+'~'+str(o["systemId"]),o["id"]) for o in importedStations )

  # eddb to EliteDB id map
  stations_importmap=dict( (o["id"],importedStationsMap[o["name"].lower()+'~'+str(o["systemId"])]) for o in stationsdata )

  # -- station metadata --

  print("importing eddb station metadata")

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

  print("importing eddb market data")

  # limit data age - allow twice the age for desperate routes
  #validityhorizon=float( time.time() - (60*60*24* int(Options.get("Market-valid-days", 7) *2 ) ))
  validityhorizon=0 # do filtering in db - for more desperate routes

  marketdata=[]
  prohibiteddata=[]
  # remap database
  for station in stationsdata:
    legalcommodities=[]
    for commodity in station["listings"]: # market listings
      if validityhorizon < commodity["collected_at"]: # no old data
        commodity["baseId"]=station["id"] # stationid already remapped
        commodity["commodityId"]=commodities_importmap[commodity["commodity_id"]]
        commodity["importPrice"]=commodity["sell_price"] # note: eddb works from the perspective of the player - "sell" is import, "buy" is export
        commodity["exportPrice"]=commodity["buy_price"]
        commodity["lastUpdated"]=commodity["collected_at"]
        marketdata.append(commodity)
        legalcommodities.append(commodities_importmap[commodity["commodity_id"]]) # keep track for black market

    if station['has_blackmarket']:
      for contraband in station['prohibited_commodities']: # black market listings
        if importedCommoditiesByName[contraband] not in legalcommodities: # only add if not in legal market
          item=dict()
          item['baseId']=station['id']
          item['commodityId']=importedCommoditiesByName[contraband]
          prohibiteddata.append(item)

  db.importCommodityPrices(marketdata)

  print("importing eddb black market data")

  db.deleteProhibitedCommodities() # these may change a lot if station changes owner - better to nuke on update

  db.importProhibitedCommodities(prohibiteddata)

  db.vacuum()

  print("eddb import complete")
