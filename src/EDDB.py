import os
import os.path
import json
import csv
from urllib import request, parse
import time
import Options
import sys
import gzip
from io import BytesIO
import datetime
import Powers

eddbUrls={
  "commodities.json":"http://eddb.io/archive/v4/commodities.json",
  "systems.json":"http://eddb.io/archive/v4/systems.json",
  "stations.json":"http://eddb.io/archive/v4/stations.json",
  "listings.csv":"http://eddb.io/archive/v4/listings.csv"
}

def readJSON(filename):
  try:
    with open(Options.getPath(filename), "r") as file:
      return json.loads(file.read())
  except Exception as ex:
    print(ex)
    return None

def readCSV(filename):
  try:
    with open(Options.getPath(filename), "r") as file:
      fileDialect = csv.Sniffer().sniff(file.read(1024))
      file.seek(0)
      #fileDialect.quoting=csv.QUOTE_NONNUMERIC # can't use because header is unquoted - also python csv conf is shit
      reader = csv.DictReader(file, dialect=fileDialect) # read as dict
      parsedar=[]
      for row in reader: # read to array
        parsedar.append(row)
      return parsedar
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
        filebuffer+=str(buffer)
        if time.time()-updateinterval > lastupdate: # console may slow us down so keep update intervals
          lastupdate=time.time()
          sys.stdout.write(formatprogress(len(filebuffer),file_size))

    with open(Options.getPath(file_name), 'w') as file:
      if meta.get('Content-Encoding') == 'gzip': # gunzip
        #buf = StringIO( filebuffer )
        buf = BytesIO( filebuffer )
        f = gzip.GzipFile(fileobj=buf)
        filebuffer = f.read().decode("utf-8")
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

  powerstats=dict()

  # reformat faction allegiances, find power control systems
  for system in systemsdata:
    if system['allegiance'] in allegiance:
      system['allegiance']=allegiance[system['allegiance']]
    else:
      system['allegiance']=0

    # control systems
    system['controlled']=None
    system['exploited']=None
    if system['power_state']=='Expansion': # we don't care about expansion
      continue
    powerid=Powers.nameToVal(system['power'])
    if system['power_state']=='Exploited':
      system['exploited']=powerid
    if system['power_state']=='Control':
      system['controlled']=powerid
      system['exploited']=powerid
    if system['power_state']=='Contested':
      system['exploited']=-1

    if system['power'] is not None:
      if system['power'] not in powerstats:
        powerstats[system['power']]={
          'Control':0,
          'Exploited':0
        }
      powerstats[system['power']][system['power_state']]+=1

  for power in powerstats:
    print(power +" has "+ str(powerstats[power]['Control']) +" Control systems & "+ str(powerstats[power]['Exploited']) +" Exploited systems")

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

  # -- merge market data --

  print("reading eddb listings")

  listingsdata = readCSV("listings.csv")
  if listingsdata is None:
    print("parsing listings.csv failed")
    return False

  print("importing eddb market data")

  # limit data age - allow twice the age for desperate routes
  #validityhorizon=float( time.time() - (60*60*24* int(Options.get("Market-valid-days", 7) *2 ) ))
  validityhorizon=0 # do filtering in db - for more desperate routes

  marketdata=[]
  prohibiteddata=[]

  for listing in listingsdata:
    for col in listing:
      listing[col]=int(listing[col]) # python csv parsing is shit so we do it live
    listing["station_id"]=stations_importmap[listing["station_id"]]
    if validityhorizon < listing["collected_at"]: # no old data
      listing["baseId"]=listing["station_id"] # stationid already remapped
      listing["commodityId"]=commodities_importmap[listing["commodity_id"]]
      listing["importPrice"]=listing["sell_price"] # note: eddb works from the perspective of the player - "sell" is import, "buy" is export
      listing["exportPrice"]=listing["buy_price"]
      listing["lastUpdated"]=listing["collected_at"]
      marketdata.append(listing)
      # todo: remove legals
      #legalcommodities.append(commodities_importmap[commodity["commodity_id"]]) # keep track for black market

  # -- station market data --

  # remap database
  for station in stationsdata:
    legalcommodities=[]
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

  #db.vacuum() # todo: uncomment if skipping this causes slowdown

  print("eddb import complete")
