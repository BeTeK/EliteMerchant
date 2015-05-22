
import operator
import time

# as a rule, functions starting with 'query..' need db as first param - others are standalone

def queryGenerateWindows(db,x,y,z,windowsize=60,distance=30,windows=1):

  extents=db.getGalaxyExtents()

  windowlist=[]

  blocksize=windowsize-distance # overlap search windows by maxdistance

  # todo: this code is terrible - be ashamed and make everything about this smarter

  i,j,k=0,0,0

  # run to the min-edge
  while x+i*blocksize-windowsize/2 > extents["minX"]: # actual window will go +- window/2 from center coordinate
    i-=1
  while y+j*blocksize-windowsize/2 > extents["minY"]:
    j-=1
  while z+k*blocksize-windowsize/2 > extents["minZ"]:
    k-=1

  minI,minJ,minK=i,j,k
  i,j,k=0,0,0

  # run to the min-edge
  while x+i*blocksize+windowsize/2 < extents["maxX"]: # actual window will go +- window/2 from center coordinate
    i+=1
  while y+j*blocksize+windowsize/2 < extents["maxY"]:
    j+=1
  while z+k*blocksize+windowsize/2 < extents["maxZ"]:
    k+=1
  maxI,maxJ,maxK=i,j,k

  for i in range(minI,maxI):
    for j in range(minJ,maxJ):
      for k in range(minK,maxK):
        windowlist.append([i*blocksize,j*blocksize,k*blocksize])

  def sortdistance(a):
    return ( (x-a[0])**2 + (y-a[1])**2 + (z-a[2])**2 ) ** 0.5
  windowlist=sorted(windowlist,key=sortdistance)
  print("The scale of the inhabited galaxy is "+str(len(windowlist))+ " windows")
  windowlist=windowlist[:windows]
  return windowlist

def ProfitHierarchyToArray(prune=None):
  if prune is None:
    return []
  asarray=[]
  for AB in prune.values(): # walk the hierarchy
    for routes in AB.values():
      for way in routes.values():
        asarray.append(way)
  return asarray

def ProfitArrayToHierarchy(oneway,prune=None): # add old hierarchy as second parameter to add to it
  # hierarchy follows this simple structure:
  """
  fromId
    toId
      commodId=traderow
    toId
      commodId=traderow
  fromId
    toId
      commodId=traderow
    toId
      commodId=traderow
  """
  if prune is None:
    prune=dict()
  for way in oneway:
    if way["AbaseId"] == way["BbaseId"]: # anomalous data discard
      continue
    if not way["AbaseId"] in prune:
      prune[way["AbaseId"]]=dict()
    if not way["BbaseId"] in prune[way["AbaseId"]]:
      prune[way["AbaseId"]][way["BbaseId"]]=dict()
    if not way["commodityId"] in prune[way["AbaseId"]][way["BbaseId"]]:
      prune[way["AbaseId"]][way["BbaseId"]][way["commodityId"]]=way
  return prune

def queryProfitRoundtrip(db,x,y,z,windowsize=30,windows=1,maxdistance=30,minprofit=1000,landingPadSize=0):
  oneway=queryProfit(db,x,y,z,windowsize,windows,maxdistance,minprofit,landingPadSize)
  twoway=[]

  print("Finding two way routes...")

  querystart=time.time()

  prune=ProfitArrayToHierarchy(oneway)

  for AB in prune.values(): # walk the hierarchy
    for routes in AB.values():
      for way in routes.values():
        if way["BbaseId"] in prune: # look for reverse system
          if way["AbaseId"] in prune[way["BbaseId"]]:
            for yaw in prune[way["BbaseId"]][way["AbaseId"]].values(): # any commodity
              twowayroute=dict(way)
              twowayroute["BexportPrice"]=yaw["AexportPrice"] # for sake of simplicity we call A station C for return trip
              twowayroute["CimportPrice"]=yaw["BimportPrice"]
              twowayroute["Cdemand"]=yaw["Bdemand"]
              twowayroute["Bsupply"]=yaw["Asupply"]
              twowayroute["Ccommodityname"]=yaw["commodityname"]
              twowayroute["CcommodityId"]=yaw["commodityId"]
              twowayroute["Caverage"]=yaw["average"]
              twowayroute["Cprofit"]=yaw["profit"]
              twowayroute["totalprofit"]=way["profit"]+yaw["profit"]
              twoway.append(twowayroute)

  print("Found "+str(len(twoway))+" roundtrip trade routes in "+str("%.2f"%(time.time()-querystart))+" seconds")
  return sorted(twoway,key=operator.itemgetter("totalprofit"), reverse=True)

def queryProfit(db,x,y,z,windowsize=30,windows=1,maxdistance=30,minprofit=1000,landingPadSize=0):
  windows=queryGenerateWindows(db,x,y,z,windowsize,maxdistance,windows)
  combined=dict()
  for wi in range(len(windows)):
    w=windows[wi]
    queryparams=dict()
    queryparams['x']=w[0]
    queryparams['y']=w[1]
    queryparams['z']=w[2]
    queryparams['window']=windowsize
    queryparams['maxdistance']=maxdistance
    queryparams['minprofit']=minprofit
    queryparams['landingPadSize']=landingPadSize
    results=db.getWindowProfit(queryparams)
    #results=db.queryProfitWindow(w[0],w[1],w[2],windowsize,maxdistance,minprofit,landingPadSize)
    combined=ProfitArrayToHierarchy(results,combined)
    print("Window " + str(wi+1) + " of " + str(len(windows)) + " (" + str("%.2f"%( (wi+1)/len(windows) *100 )) + "%)")
  combinedAr=ProfitHierarchyToArray(combined)
  return sorted(combinedAr,key=operator.itemgetter("profit"),reverse=True)
