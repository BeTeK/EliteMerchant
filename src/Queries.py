
import operator
import time
import Options
import sys
from functools import reduce

# as a rule, functions starting with 'query..' need db as first param - others are standalone

def queryGenerateWindows(db,x,y,z,windowsize=60,distance=30,windows=1):
  if distance>=windowsize:
    print("Distance cannot be larger then window size!\nSearch windows are created to overlap by the amount of 'distance'")
    return []
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
  if windows > 0:
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

def ProfitArrayToHierarchy_flat(oneway,prune=None): # add old hierarchy as second parameter to add to it
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
      prune[way["AbaseId"]][way["BbaseId"]]=True

  return prune

def ProfitArrayToHierarchy_flat_profitPh(oneway,prune=None): # add old hierarchy as second parameter to add to it
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
      prune[way["AbaseId"]][way["BbaseId"]]=way['profitPh']
    else:
      prune[way["AbaseId"]][way["BbaseId"]]=max(way['profitPh'],prune[way["AbaseId"]][way["BbaseId"]])

  return prune

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

def ProfitArrayToHierarchyReverse(oneway,prune=None): # add old hierarchy as second parameter to add to it
  # hierarchy follows this simple structure:
  """
  toId
    fromId
      commodId=traderow
    fromId
      commodId=traderow
  toId
    fromId
      commodId=traderow
    fromId
      commodId=traderow
  """
  if prune is None:
    prune=dict()
  for way in oneway:
    if way["AbaseId"] == way["BbaseId"]: # anomalous data discard
      continue
    if not way["BbaseId"] in prune:
      prune[way["BbaseId"]]=dict()
    if not way["AbaseId"] in prune[way["BbaseId"]]:
      prune[way["BbaseId"]][way["AbaseId"]]=dict()
    if not way["commodityId"] in prune[way["BbaseId"]][way["AbaseId"]]:
      prune[way["BbaseId"]][way["AbaseId"]][way["commodityId"]]=way
  return prune

def queryProfitRoundtrip(db,x,y,z,windowsize,windows,maxdistance,minprofit,minprofitPh,landingPadSize):
  oneway=queryProfit(db,x,y,z,windowsize,windows,maxdistance,minprofit,minprofitPh,landingPadSize)
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
              twowayroute["CprofitPh"]=yaw["profitPh"]
              twowayroute["totalprofit"]=way["profit"]+yaw["profit"]
              twowayroute["totalprofitPh"]=way["profitPh"]+yaw["profitPh"]/2
              twowayroute["CSystemDistance"]=yaw["SystemDistance"]
              twoway.append(twowayroute)

  print("Found "+str(len(twoway))+" roundtrip trade routes in "+str("%.2f"%(time.time()-querystart))+" seconds")
  return sorted(twoway,key=operator.itemgetter("totalprofitPh"), reverse=True)

def queryProfit(db,x,y,z,windowsize,windows,maxdistance,minprofit,minprofitPh,landingPadSize):
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
    queryparams['minprofitPh']=minprofitPh
    queryparams['landingPadSize']=landingPadSize
    queryparams['lastUpdated']=int(Options.get('Market-valid-days',7))
    results=db.getWindowProfit(queryparams)
    #results=db.queryProfitWindow(w[0],w[1],w[2],windowsize,maxdistance,minprofit,landingPadSize)
    combined=ProfitArrayToHierarchy(results,combined)
    print("Window " + str(wi+1) + " of " + str(len(windows)) + " (" + str("%.2f"%( (wi+1)/len(windows) *100 )) + "%)")
  combinedAr=ProfitHierarchyToArray(combined)
  return sorted(combinedAr,key=operator.itemgetter("profitPh"),reverse=True)

def queryProfitGraphLoops(db,x,y,z,windowsize,windows,maxdistance,minprofit,minprofitPh,landingPadSize,routelength,maxdepth):
  oneway = queryProfit(db,x,y,z,windowsize,windows,maxdistance,minprofit,minprofitPh,landingPadSize)

  """
  # list of unique baseIds
  #bases=list(set([way["AbaseId"] for way in oneway]+[way["BbaseId"] for way in oneway]))
  bases_from=set([way["AbaseId"] for way in oneway])
  bases_to=set([way["BbaseId"] for way in oneway])
  bases_deadends=list(bases_to-bases_from)
  onewayviable=[]
  for way in oneway:
    if way["BbaseId"] not in bases_deadends:
      onewayviable.append(way)

  print("discarded "+str(len(bases_deadends))+" confirmed deadends")
  """

  startingroutecount=len(oneway)
  iteration=0
  routecount=0
  print("pruning deadends...")
  while routecount!=len(oneway):
    prune=ProfitArrayToHierarchy(oneway)
    pruneR=ProfitArrayToHierarchyReverse(oneway)
    iteration+=1
    print("iteration "+str(iteration))
    routecount=len(oneway)
    oneway=[way for way in oneway if way["BbaseId"] in prune]
    oneway=[way for way in oneway if way["AbaseId"] in pruneR]
  print("discarded "+str(startingroutecount-len(oneway)))


  prune=ProfitArrayToHierarchy_flat_profitPh(oneway)

  #bases=list(set([way["AbaseId"] for way in onewayviable]))
  bases=list(set([way["AbaseId"] for way in oneway]))


  print("walking galaxy-graph for loops")

  querystart=time.time()

  #loopgraph=dict()

  #loops=set()
  loops=[]

  routed=[]
  def walk(fromid,start,history,depth,profitPh):
    if maxdepth<depth:
      return False
    #graph=dict()
    for toid in prune[fromid]:
      if toid==start: # found loop
        #print('----------------------------- loop '+str(start)+" - "+str(toid))
        if routelength<=depth:
          loops.append([start]+history+[toid])
        #loops.add(tuple([start]+history+[toid]))
        #graph[toid]=True
      elif toid in history: # avoid internal loops on the way
        #print("internal loop at "+str(toid))
        continue
      elif toid in routed: # avoid multiple entries
        continue
      elif toid in prune: # new target - walk it
        walk(toid,start,history+[toid],depth,profitPh+prune[fromid][toid])
        #graph[toid]=walk(toid,start,history+[toid])
      else: # deadend
        #print('deadend '+str(start)+" - "+str(toid)+"  history depth "+str(len(history)))
        #graph[toid]=False
        pass
    #return graph


  lastupdate=0
  updateinterval=1

  for bi in range(len(bases)):
    fromid=bases[bi]
    if time.time()-updateinterval > lastupdate: # console may slow us down so keep update intervals
      lastupdate=time.time()
      sys.stdout.write("\r"+str("%.2f"%(bi/len(bases)*100))+"%  "+str(len(loops))+" routes")
      #print(str("%.2f"%(bi/len(bases)*100))+"%")
    for toid in prune[fromid]:
      if toid in prune:
        walk(toid,fromid,[toid],1,prune[fromid][toid])
        #loopgraph[fromid]=walk(toid,fromid,[toid])
    routed.append(fromid)

  print("")

  print("Found "+str(len(loops))+" loop trade routes in "+str("%.2f"%(time.time()-querystart))+" seconds")

  prune=ProfitArrayToHierarchy(oneway)
  print("Gathering hops...")
  traderoutes=[]
  for loop in loops:
    route=dict()
    route["loopminprofit"]=0
    route["loopmaxprofit"]=0
    route["totalprofitPh"]=0
    route["hops"]=[]
    prev=loop[0]
    for ni in range(1,len(loop)): # by hop
      next=loop[ni]
      hoptrades = prune[prev][next].values() # all possible commodities on this route
      hoptrades = sorted(hoptrades,key=operator.itemgetter("profitPh"),reverse=True) # sort by profit
      route["loopminprofit"]+=hoptrades[-1]["profit"]
      route["loopmaxprofit"]+=hoptrades[0]["profit"]
      route["totalprofitPh"]+=hoptrades[0]["profitPh"] #todo: confirm the math here
      prev=next
      route["hops"].append(hoptrades) # store hops
    route["averageprofit"]=int(route["loopmaxprofit"]/len(route["hops"]))
    route["totalprofitPh"]=int(route["totalprofitPh"]/len(route["hops"]))
    traderoutes.append(route)

  traderoutes = sorted(traderoutes,key=operator.itemgetter("totalprofitPh"),reverse=True) # sort by profit

  traderoutes=traderoutes[:5000] # don't overload the window

  returnarray=[]
  for loop in traderoutes:
    for hop in loop["hops"]:
      returnarray.append(dict({
        "celltype":'emptyrow',
        "averageprofit":loop["averageprofit"],
        "loopminprofit":loop["loopminprofit"],
        "loopmaxprofit":loop["loopmaxprofit"]
      }))
      for commodity in hop:
        commodity["averageprofit"]=loop["averageprofit"]
        commodity["loopminprofit"]=loop["loopminprofit"]
        commodity["loopmaxprofit"]=loop["loopmaxprofit"]
        returnarray.append(commodity)
    returnarray.append(dict({
      "celltype":'separatorrow',
      "averageprofit":loop["averageprofit"],
      "loopminprofit":loop["loopminprofit"],
      "loopmaxprofit":loop["loopmaxprofit"],
      "totalprofitPh":loop["totalprofitPh"]
    }))
    #returnarray.append('separatorrow')
  return returnarray



def queryProfitGraphDeadends(db,x,y,z,windowsize,windows,maxdistance,minprofit,minprofitPh,landingPadSize,routelength,maxdepth):
  oneway = queryProfit(db,x,y,z,windowsize,windows,maxdistance,minprofit,minprofitPh,landingPadSize)

  prune=ProfitArrayToHierarchy_flat_profitPh(oneway)

  #bases=list(set([way["AbaseId"] for way in onewayviable]))
  bases=list(set([way["AbaseId"] for way in oneway]))
  profitpotential=0
  for way in oneway:
    profitpotential=max(profitpotential,way["profitPh"])

  print("walking galaxy-graph for loops")

  querystart=time.time()

  #loopgraph=dict()
  #routelength=10
  #loops=set()
  loops=[]

  allowedprofitloss=10 # pct
  minprofit=(1-1/allowedprofitloss)*profitpotential

  routed=[]
  def walk(fromid,start,history,depth,profitPh):
    for toid in prune[fromid]:
      if depth>maxdepth:
        loops.append([start]+history)
      elif toid==start: # found loop
        if depth>=routelength:
          loops.append([start]+history+[toid])
        #print('----------------------------- loop '+str(start)+" - "+str(toid))
        #loops.add(tuple([start]+history+[toid]))
        #graph[toid]=True
      elif toid in history: # avoid internal loops on the way
        #print("internal loop at "+str(toid))
        continue
      #elif toid in routed: # avoid multiple entries
      #  continue
      elif toid in prune: # new target - walk it
        walk(toid,start,history+[toid],depth+1,profitPh+prune[fromid][toid])
        #graph[toid]=walk(toid,start,history+[toid])
      else: # deadend
        if depth>=routelength:
          loops.append([start]+history+[toid])
        #print('deadend '+str(start)+" - "+str(toid)+"  history depth "+str(len(history)))
        #graph[toid]=False
        #pass
    #return graph


  lastupdate=0
  updateinterval=1

  for bi in range(len(bases)):
    fromid=bases[bi]
    if time.time()-updateinterval > lastupdate: # console may slow us down so keep update intervals
      lastupdate=time.time()
      sys.stdout.write("\r"+str("%.2f"%(bi/len(bases)*100))+"%  "+str(len(loops))+" routes")
      #print(str("%.2f"%(bi/len(bases)*100))+"%")
    for toid in prune[fromid]:
      if toid in prune:
        walk(toid,fromid,[toid],1,prune[fromid][toid])
        #loopgraph[fromid]=walk(toid,fromid,[toid])
    routed.append(fromid)

  print("")

  print("Found "+str(len(loops))+" loop trade routes in "+str("%.2f"%(time.time()-querystart))+" seconds")

  prune=ProfitArrayToHierarchy(oneway)

  print("Gathering hops...")
  traderoutes=[]
  for loop in loops:
    route=dict()
    route["loopminprofit"]=0
    route["loopmaxprofit"]=0
    route["totalprofitPh"]=0
    route["hops"]=[]
    prev=loop[0]
    for ni in range(1,len(loop)): # by hop
      next=loop[ni]
      hoptrades = prune[prev][next].values() # all possible commodities on this route
      hoptrades = sorted(hoptrades,key=operator.itemgetter("profitPh"),reverse=True) # sort by profit
      route["loopminprofit"]+=hoptrades[-1]["profit"]
      route["loopmaxprofit"]+=hoptrades[0]["profit"]
      route["totalprofitPh"]+=hoptrades[0]["profitPh"] #todo: confirm the math here
      prev=next
      route["hops"].append(hoptrades) # store hops
    route["averageprofit"]=int(route["loopmaxprofit"]/len(route["hops"]))
    route["totalprofitPh"]=int(route["totalprofitPh"]/len(route["hops"]))
    traderoutes.append(route)

  traderoutes = sorted(traderoutes,key=operator.itemgetter("totalprofitPh"),reverse=True) # sort by profit

  traderoutes=traderoutes[:5000] # don't overload the window

  returnarray=[]
  for loop in traderoutes:
    for hop in loop["hops"]:
      returnarray.append(dict({
        "celltype":'emptyrow',
        "averageprofit":loop["averageprofit"],
        "loopminprofit":loop["loopminprofit"],
        "loopmaxprofit":loop["loopmaxprofit"]
      }))
      for commodity in hop:
        commodity["averageprofit"]=loop["averageprofit"]
        commodity["loopminprofit"]=loop["loopminprofit"]
        commodity["loopmaxprofit"]=loop["loopmaxprofit"]
        returnarray.append(commodity)
    returnarray.append(dict({
      "celltype":'separatorrow',
      "averageprofit":loop["averageprofit"],
      "loopminprofit":loop["loopminprofit"],
      "loopmaxprofit":loop["loopmaxprofit"],
      "totalprofitPh":loop["totalprofitPh"]
    }))
    #returnarray.append('separatorrow')
  return returnarray




