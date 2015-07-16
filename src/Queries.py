
import operator
import time
import Options

# as a rule, functions starting with 'query..' need db as first param - others are standalone

def queryGenerateWindows(db,x,y,z,windowsize=60,distance=30,windows=1):

  if distance>=windowsize:
    print("Distance cannot be larger than window size!\nSearch windows are created to overlap by the amount of 'distance'")
    return []
  extents=db.getGalaxyExtents()

  windowlist=[]

  blocksize=float(windowsize-distance) # overlap search windows by maxdistance

  # centered around current system, snap min corner to nearest blocksize
  cornerX=x+ round( (extents["minX"]-x) /blocksize)*blocksize
  cornerY=y+ round( (extents["minY"]-y) /blocksize)*blocksize
  cornerZ=z+ round( (extents["minZ"]-z) /blocksize)*blocksize

  # size of galaxy from snapped min corner to max corner
  sizeX=extents["maxX"]-cornerX
  sizeY=extents["maxY"]-cornerY
  sizeZ=extents["maxZ"]-cornerZ

  # round max corner to nearest block size, as window-count
  windowsX=round( (sizeX / blocksize)+1 )
  windowsY=round( (sizeY / blocksize)+1 )
  windowsZ=round( (sizeZ / blocksize)+1 )

  # collect windows
  for wX in range(windowsX):
    for wY in range(windowsY):
      for wZ in range(windowsZ):
        windowlist.append([
          cornerX+(blocksize*wX),
          cornerY+(blocksize*wY),
          cornerZ+(blocksize*wZ)
        ])

  sizeX=extents["maxX"]-extents["minX"]
  sizeY=extents["maxY"]-extents["minY"]
  sizeZ=extents["maxZ"]-extents["minZ"]
  print("The scale of the inhabited galaxy is "+str(windowsX*windowsY*windowsZ)+ " windows, or "+"%.2f"%((sizeX*sizeY*sizeZ)/1000000)+"Mly cubed")
  """
  print()
  print('front corner',windowlist[0])
  print('min',extents["minX"],extents["minY"],extents["minZ"])
  if abs(windowlist[0][0]-extents["minX"])>windowsize/2:
    print('Xdiff outside window size ',str(windowlist[0][0]-extents["minX"]), windowsize/2)
  if abs(windowlist[0][1]-extents["minY"])>windowsize/2:
    print('Ydiff outside window size ',str(windowlist[0][1]-extents["minY"]), windowsize/2)
  if abs(windowlist[0][2]-extents["minZ"])>windowsize/2:
    print('Zdiff outside window size ',str(windowlist[0][2]-extents["minZ"]), windowsize/2)
  print()
  print('back corner',windowlist[-1])
  print('max',extents["maxX"],extents["maxY"],extents["maxZ"])
  if abs(windowlist[-1][0]-extents["maxX"])>windowsize/2:
    print('Xdiff outside window size ',str(windowlist[-1][0]-extents["maxX"]), windowsize/2)
  if abs(windowlist[-1][1]-extents["maxY"])>windowsize/2:
    print('Ydiff outside window size ',str(windowlist[-1][1]-extents["maxY"]), windowsize/2)
  if abs(windowlist[-1][2]-extents["maxZ"])>windowsize/2:
    print('Zdiff outside window size ',str(windowlist[-1][2]-extents["maxZ"]), windowsize/2)
  """
  def sortdistance(a):
    return ( (x-a[0])**2 + (y-a[1])**2 + (z-a[2])**2 ) ** 0.5
  windowlist=sorted(windowlist,key=sortdistance)
  if windows > 0:
    windowlist=windowlist[:windows]
  """
  print()
  print('current',x,y,z)
  print('closest',windowlist[0])
  print()
  """
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

def ProfitArrayToHierarchy_profitPh(oneway,prune=None): # add old hierarchy as second parameter to add to it
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
      prune[way["AbaseId"]][way["BbaseId"]]=way
    else:
      if prune[way["AbaseId"]][way["BbaseId"]]['profitPh']<way['profitPh']:
        prune[way["AbaseId"]][way["BbaseId"]]=way

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
      #way["profitPh"]=int(way["profit"]/way["hours"]) # bake me a cake  -----  profitPh = profit / hours - done on db side now
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

def queryProfitRoundtrip(db,queryparams): # deprecated
  oneway=queryProfit(db,dict(queryparams))
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


def queryDirectTrades(db,queryparams):
  queryparams['minprofit']=1
  queryparams['lastUpdated']=int(Options.get('Market-valid-days',7))
  results=db.getTradeDirect(dict(queryparams))
  if queryparams['blackmarket']:
    results+=db.getBlackmarketDirect(dict(queryparams))
  return sorted(results,key=operator.itemgetter("profitPh"),reverse=True)


def queryProfit(db,queryparams):
  #windows=queryGenerateWindows(db,x,y,z,windowsize,maxdistance,windows)
  combined=dict()

  #x,y,z=queryparams['x'],queryparams['y'],queryparams['z']
  x2,y2,z2=queryparams['x2'],queryparams['y2'],queryparams['z2']
  targetbase=queryparams['targetbase']
  targetsystem=queryparams['targetsystem']
  sourcebase=queryparams['sourcebase']
  sourcesystem=queryparams['sourcesystem']
  mindepth=queryparams['graphDepthMin']
  maxdepth=queryparams['graphDepthMax']

  # get exports if defined
  if sourcesystem is not None or sourcebase is not None:
    source_queryparams=dict(queryparams) # copy
    print("Fetching starting exports with loosened criteria ("+str(sourcesystem)+", "+str(sourcebase)+")")
    source_queryparams['minprofit']=0
    source_queryparams['lastUpdated']=int(Options.get('Market-valid-days',7))
    results=db.getTradeExports(source_queryparams)
    if len(results)==0:
      print('No exports found')
      return []

    # if exports contain any up to date data, discard old data
    markethorizon=int( time.time() - (60*60*24* int(Options.get('Market-valid-days',7)) ))
    uptodateresults=[o for o in results if markethorizon<o['AlastUpdated'] and markethorizon<o['BlastUpdated']]
    if len(uptodateresults)>0:
      results=uptodateresults
    else:
      print('No up-to-date data - allowing outdated data to appear')

    results=sorted(results,key=operator.itemgetter("profitPh"),reverse=True)[:50] # cap to 50 best deals
    combined=ProfitArrayToHierarchy(results,combined)

  # get imports if defined
  if targetsystem is not None or targetbase is not None:
    target_queryparams=dict(queryparams) # copy
    print("Fetching target imports with loosened criteria ("+str(targetsystem)+", "+str(targetbase)+")")
    target_queryparams['minprofit']=0
    target_queryparams['lastUpdated']=int(Options.get('Market-valid-days',7))
    results=db.getTradeImports(target_queryparams)
    if len(results)==0:
      print('No imports found')
      #return [] # but try to get as close as possible

    # if exports contain any up to date data, discard old data
    markethorizon=int( time.time() - (60*60*24* int(Options.get('Market-valid-days',7)) ))
    uptodateresults=[o for o in results if markethorizon<o['AlastUpdated'] and markethorizon<o['BlastUpdated']]
    if len(uptodateresults)>0:
      results=uptodateresults
    else:
      print('No up-to-date data - allowing outdated data to appear')

    results=sorted(results,key=operator.itemgetter("profitPh"),reverse=True)[:50] # cap to 50 best deals
    combined=ProfitArrayToHierarchy(results,combined)


  # get generic galaxy trade table
  print("Fetching galaxywide trades... (this may take a while)")
  queryparams['lastUpdated']=int(Options.get('Market-valid-days',7))
  results=db.getTradeProfits(queryparams)
  combined=ProfitArrayToHierarchy(results,combined)

  if queryparams['blackmarket']:
    print("Fetching blackmarket trades...")
    results=db.getBlackmarketProfits(queryparams)
    combined=ProfitArrayToHierarchy(results,combined)

  combinedAr=ProfitHierarchyToArray(combined)
  return sorted(combinedAr,key=operator.itemgetter("profitPh"),reverse=True)

def queryProfitGraphLoops(db,queryparams):
  oneway = queryProfit(db,dict(queryparams)) # query with copy to avoid poisoning future use of queryparams

  #x,y,z=queryparams['x'],queryparams['y'],queryparams['z']
  x2,y2,z2=queryparams['x2'],queryparams['y2'],queryparams['z2']
  targetbase=queryparams['targetbase']
  #targetsystem=queryparams['targetsystem']
  sourcebase=queryparams['sourcebase']
  sourcesystem=queryparams['sourcesystem']
  mindepth=queryparams['graphDepthMin']
  maxdepth=queryparams['graphDepthMax']

  mindepth=max(mindepth,2) # loops need two to tango
  maxdepth=max(maxdepth,2)

  minroutes=300 # first completed graph search try that finds this many routes is good enough
  maxroutes=5000 # no matter how much we find, only show this many to GUI
  profitmarginstep=0.1 # this is reduced from profit margin if number of found routes is <minroutes - this value is reduced if chocking on data
  profitmargin=0.99 # starting profit margin - start with 99% profit requirement
  walktimeout=5 # if search takes this long, it's too long and we're choking
  profitfailuredepth=1 # don't start evaluating profitability until this deep in the algo
  chokeforcelevel=3 # give up optimizing if we choke this many times

  ##  a deadend cannot be a loop - get rid of those
  iteration=0
  routecount=0
  startingroutecount=len(oneway)
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

  profitpotential=0 # calculate profit expectations to base profitmargin on
  for way in oneway:
    profitpotential=max(profitpotential,way["profitPh"])
  mintotalprofitPh=[profitpotential] # using array index to get around function scope issues

  prune=ProfitArrayToHierarchy_profitPh(oneway)
  bases=list(set([way["AbaseId"] for way in oneway])) #creating list of starting stations

  print(str(len(oneway))+" viable trade hops")
  if len(oneway)==0:
    return []
  print("walking galaxy-graph...")


  ############ recursive graph walking algo
  def walk(fromid,start,history,profit,hours):
    # bail if we're chocking on data
    if walkstart+walktimeout<time.time() and len(loops)>=minroutes and profitmargin<1.0 and chokelevel<chokeforcelevel:
      return False
    depth=len(history)+1
    if maxdepth<depth: # max depth reached
      return False
    if depth > profitfailuredepth and profit/hours < mintotalprofitPh[0] * profitmargin: # route is a profit failure
      return False
    for toid in prune[fromid]: # every outgoing trade
      if toid in history: # avoid internal loops on the way
        continue
      elif toid in routed: # avoid multiple entries
        continue
      elif toid==start: # found loop
        if mindepth<=depth:
          profit+=prune[fromid][toid]['profit']
          hours+=prune[fromid][toid]['hours']
          mintotalprofitPh[0]=max(mintotalprofitPh[0],profit/hours)
          loops.append([profit/hours,[start]+history+[toid]])
      else: # new target - walk it
        walk(toid,start,history+[toid],profit+prune[fromid][toid]['profit'],hours+prune[fromid][toid]['hours'])
  ############

  querystart=time.time()
  loops=[]
  chokelevel=0 # choking counter
  satisfiedwithresult=False
  while not satisfiedwithresult and profitmargin>=0:
    walkstart=time.time()
    loops=[]
    routed=dict() # blacklist of systems already explored
    lastupdate=0
    updateinterval=1
    for bi in range(len(bases)): # walk all starting systems
      fromid=bases[bi]
      if time.time()-updateinterval > lastupdate: # console may slow us down so keep update intervals
        lastupdate=time.time()
        print("   "+str("%.2f"%(bi/len(bases)*100))+"%  "+str(len(loops))+" routes")
      for toid in prune[fromid]:
        walk(toid,fromid,[toid],prune[fromid][toid]['profit'],prune[fromid][toid]['hours'])
      routed[fromid]=True
    if walkstart+walktimeout<time.time() and len(loops)>=minroutes and profitmargin<1.0 and chokelevel<chokeforcelevel:
      print('chocking in data - lowering profit allowance step')
      chokelevel+=1
      if chokelevel==chokeforcelevel:
        print("giving up on optimizing")
      profitmargin=profitmargin+profitmarginstep
      profitmarginstep/=10
      profitmargin-=profitmarginstep
      profitmargin=min(1.0,profitmargin)
      print("trying again with "+str(int((1-profitmargin)*100*100)/100)+"% profit allowance")
    elif len(loops)<minroutes and profitmargin<1.0 and chokelevel<chokeforcelevel:
      profitmargin-=profitmarginstep
      print("found "+str(len(loops))+" trade routes - trying again with "+str(int((1-profitmargin)*100*100)/100)+"% profit allowance")
    else:
      satisfiedwithresult=True


  print("Found "+str(len(loops))+" loop trade routes in "+str("%.2f"%(time.time()-querystart))+" seconds")

  loops = sorted(loops,key=lambda ar:ar[0],reverse=True) # sort by profit
  loops=loops[:10000] # don't overload the window
  loops=[i[1] for i in loops]

  prune=ProfitArrayToHierarchy(oneway)
  print("Gathering hops...")
  traderoutes=[]
  for loop in loops:
    route=dict()
    route["loopminprofit"]=0
    route["loopmaxprofit"]=0
    route["totalprofitPh"]=0
    route["totalhours"]=0
    route["hops"]=[]
    prev=loop[0]
    for ni in range(1,len(loop)): # by hop
      next=loop[ni]
      hoptrades = prune[prev][next].values() # all possible commodities on this route
      hoptrades = sorted(hoptrades,key=operator.itemgetter("profitPh"),reverse=True) # sort by profit
      route["loopminprofit"]+=hoptrades[-1]["profit"]
      route["loopmaxprofit"]+=hoptrades[0]["profit"]
      route["totalhours"]+=hoptrades[0]["hours"]
      prev=next
      route["hops"].append(hoptrades) # store hops
    route["averageprofit"]=int(route["loopmaxprofit"]/len(route["hops"]))
    route["totalprofitPh"]=int(route["loopmaxprofit"]/route["totalhours"])
    traderoutes.append(route)

  traderoutes = sorted(traderoutes,key=operator.itemgetter("totalprofitPh"),reverse=True) # sort by profit

  traderoutes=traderoutes[:maxroutes] # don't overload the window

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
      "totalprofitPh":loop["totalprofitPh"],
      "totalhours":loop["totalhours"]
    }))
    #returnarray.append('separatorrow')
  return returnarray

def queryProfitGraphDeadends(db,queryparams):
  oneway = queryProfit(db,dict(queryparams))

  prune=ProfitArrayToHierarchy_profitPh(oneway)

  minroutes=300 # first completed graph search try that finds this many routes is good enough
  maxroutes=5000 # no matter how much we find, only show this many to GUI
  profitmarginstep=0.1 # this is reduced from profit margin if number of found routes is <minroutes - this value is reduced if chocking on data
  profitmargin=0.99 # starting profit margin - start with 99% profit requirement
  walktimeout=5 # if search takes this long, it's too long and we're choking
  profitfailuredepth=1 # don't start evaluating profitability until this deep in the algo
  chokeforcelevel=3 # give up optimizing if we choke this many times

  #x,y,z=queryparams['x'],queryparams['y'],queryparams['z']
  #x2,y2,z2=queryparams['x2'],queryparams['y2'],queryparams['z2']
  #targetbase=queryparams['targetbase']
  #targetsystem=queryparams['targetsystem']
  sourcebase=queryparams['sourcebase']
  sourcesystem=queryparams['sourcesystem']
  mindepth=queryparams['graphDepthMin']
  maxdepth=queryparams['graphDepthMax']

  profitpotential=0 # calculate profit expectations to base profitmargin on
  for way in oneway:
    profitpotential=max(profitpotential,way["profitPh"])
  mintotalprofitPh=[profitpotential] # using array index to get around function scope issues

  #creating list of starting stations
  bases=list(set([way["AbaseId"] for way in oneway]))
  if sourcebase is not None:
    print("trying to select with station")
    bases=list(set([way["AbaseId"] for way in oneway if way["Abasename"].lower().strip()==sourcebase.lower().strip() and way["Asystemname"].lower().strip()==sourcesystem.lower().strip()]))
  if (sourcebase is None or len(bases)==0) and sourcesystem is not None:
    print("trying to select with system")
    bases=list(set([way["AbaseId"] for way in oneway if way["Asystemname"].lower().strip()==sourcesystem.lower().strip()]))

  print(str(len(oneway))+" viable trade hops")
  if len(oneway)==0:
    return []

  print("walking galaxy-graph...")

  ############ recursive graph walking algo
  def walk(fromid,start,history,profit,hours):
    # we're choking - bail out
    if walkstart+walktimeout<time.time() and len(loops)>=minroutes and profitmargin<1.0 and chokelevel<chokeforcelevel:
      return False
    depth=len(history)
    if depth > profitfailuredepth and profit/hours < mintotalprofitPh[0] * profitmargin: # route is a profit failure
      return False
    if mindepth<=depth:
      mintotalprofitPh[0]=max(mintotalprofitPh[0],profit/hours)
      loops.append([profit/hours,[start]+history])
    if maxdepth<depth:
      return False
    if fromid not in prune: #target doesn't exist
      return False
    for toid in prune[fromid]:
      if toid in history: # avoid internal loops on the way
        continue
      elif toid in routed: # avoid multiple entries
        continue
      elif toid==start: # found loop
        if mindepth<=depth:
          profit+=prune[fromid][toid]['profit']
          hours+=prune[fromid][toid]['hours']
          mintotalprofitPh[0]=max(mintotalprofitPh[0],profit/hours)
          loops.append([profit/hours,[start]+history+[toid]])
      else: # deadend
        walk(toid,start,history+[toid],profit+prune[fromid][toid]['profit'],hours+prune[fromid][toid]['hours'])
  ############

  querystart=time.time()
  chokelevel=0
  loops=[]
  satisfiedwithresult=False
  while not satisfiedwithresult and profitmargin>=0:
    walkstart=time.time()
    loops=[]
    routed=dict()
    lastupdate=0
    updateinterval=1
    for bi in range(len(bases)):
      fromid=bases[bi]
      if time.time()-updateinterval > lastupdate: # console may slow us down so keep update intervals
        lastupdate=time.time()
        print("   "+str("%.2f"%(bi/len(bases)*100))+"%  "+str(len(loops))+" routes")
      for toid in prune[fromid]:
        if sourcebase is not None or sourcesystem is not None: # forgive first step in export search
          walk(toid,fromid,[toid],mintotalprofitPh[0],1)
        else:
          walk(toid,fromid,[toid],prune[fromid][toid]['profit'],prune[fromid][toid]['hours'])
      routed[fromid]=True

    if walkstart+walktimeout<time.time() and len(loops)>=minroutes and profitmargin<1.0 and chokelevel<chokeforcelevel:
      print('chocking in data - lowering profit allowance step')
      chokelevel+=1
      if chokelevel==chokeforcelevel:
        print("giving up on optimizing")
      profitmargin=profitmargin+profitmarginstep
      profitmarginstep/=10
      profitmargin-=profitmarginstep
      profitmargin=min(1.0,profitmargin)
      print("let's try again with "+str(int((1-profitmargin)*100*100)/100)+"% profit allowance")
    elif len(loops)<minroutes and profitmargin<1.0 and chokelevel<chokeforcelevel:
      profitmargin-=profitmarginstep
      print("found "+str(len(loops))+" trade routes - trying again with "+str(int((1-profitmargin)*100*100)/100)+"% profit allowance")
    else:
      satisfiedwithresult=True

  print("Found "+str(len(loops))+" long trade routes in "+str("%.2f"%(time.time()-querystart))+" seconds")

  loops = sorted(loops,key=lambda ar:ar[0],reverse=True) # sort by profit
  loops=loops[:10000] # don't overload the window
  loops=[i[1] for i in loops]

  prune=ProfitArrayToHierarchy(oneway)

  print("Gathering hops...")
  traderoutes=[]
  for loop in loops:
    route=dict()
    route["loopminprofit"]=0
    route["loopmaxprofit"]=0
    route["totalprofitPh"]=0
    route["totalhours"]=0
    route["hops"]=[]
    prev=loop[0]
    for ni in range(1,len(loop)): # by hop
      next=loop[ni]
      hoptrades = prune[prev][next].values() # all possible commodities on this route
      hoptrades = sorted(hoptrades,key=operator.itemgetter("profitPh"),reverse=True) # sort by profit
      route["loopminprofit"]+=hoptrades[-1]["profit"]
      route["loopmaxprofit"]+=hoptrades[0]["profit"]
      route["totalhours"]+=hoptrades[0]["hours"]
      prev=next
      route["hops"].append(hoptrades) # store hops
    route["averageprofit"]=int(route["loopmaxprofit"]/len(route["hops"]))
    route["totalprofitPh"]=int(route["loopmaxprofit"]/route["totalhours"])
    traderoutes.append(route)

  traderoutes = sorted(traderoutes,key=operator.itemgetter("totalprofitPh"),reverse=True) # sort by profit

  traderoutes=traderoutes[:maxroutes] # don't overload the window

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
      "totalprofitPh":loop["totalprofitPh"],
      "totalhours":loop["totalhours"]
    }))
    #returnarray.append('separatorrow')
  return returnarray

def queryProfitGraphTarget(db,queryparams):
  oneway = queryProfit(db,dict(queryparams)) # copy


  def distance3d(x,y,z,i,j,k):
    return ((x-i)**2+(y-j)**2+(z-k)**2)**.5

  x,y,z=queryparams['x'],queryparams['y'],queryparams['z']
  x2,y2,z2=queryparams['x2'],queryparams['y2'],queryparams['z2']
  targetbase=queryparams['targetbase']
  #targetsystem=queryparams['targetsystem']
  sourcebase=queryparams['sourcebase']
  sourcesystem=queryparams['sourcesystem']
  mindepth=queryparams['graphDepthMin']
  maxdepth=queryparams['graphDepthMax']

  minroutes=300 # first completed graph search try that finds this many routes is good enough
  maxroutes=5000 # no matter how much we find, only show this many to GUI
  profitmarginstep=0.1 # this is reduced from profit margin if number of found routes is <minroutes - this value is reduced if chocking on data
  profitmargin=0.99 # starting profit margin - start with 99% profit requirement
  walktimeout=5 # if search takes this long, it's too long and we're choking
  profitfailuredepth=1 # don't start evaluating profitability until this deep in the algo
  chokeforcelevel=3 # give up optimizing if we choke this many times

  totaltargetdistance=distance3d(x,y,z,x2,y2,z2) # only systems closer than starting system allowed
  oneway=[way for way in oneway if way['targetdistance']<= totaltargetdistance]

  profitpotential=0 # calculate profit expectations to base profitmargin on
  for way in oneway:
    profitpotential=max(profitpotential,way["profitPh"])
    way["targetdistance"]=distance3d(x2,y2,z2,way["Bx"],way["By"],way["Bz"])
    if targetbase is not None and way["Bbasename"]==targetbase and way["targetdistance"]<1:
      way["targetdistance"]=-1000
  mintotalprofitPh=[profitpotential] # using array index to get around function scope issues

  #creating list of starting stations
  bases=list(set([way["AbaseId"] for way in oneway]))
  if sourcebase is not None:
    print("trying to select with station")
    bases=list(set([way["AbaseId"] for way in oneway if way["Abasename"].lower().strip()==sourcebase.lower().strip() and way["Asystemname"].lower().strip()==sourcesystem.lower().strip()]))
  if (sourcebase is None or len(bases)==0) and sourcesystem is not None:
    print("trying to select with system")
    bases=list(set([way["AbaseId"] for way in oneway if way["Asystemname"].lower().strip()==sourcesystem.lower().strip()]))

  print(str(len(oneway))+" viable trade hops")
  if len(oneway)==0:
    return []

  prune=ProfitArrayToHierarchy_profitPh(oneway)

  print("walking galaxy-graph...")

  ############ recursive graph walking algo
  def walk(fromid,start,history,profit,hours,lastdistance):
    #print('x')
    if walkstart+walktimeout<time.time() and len(loops)>=minroutes and profitmargin<1.0 and chokelevel<chokeforcelevel:
      return False
    depth=len(history)
    if depth > profitfailuredepth and profit/hours < mintotalprofitPh[0] * profitmargin: # route is a profit failure
      return False
    if mindepth<depth:
      mintotalprofitPh[0]=max(mintotalprofitPh[0],profit/hours)
      loops.append([profit/hours,[start]+history])
    if maxdepth<depth:
      return False
    if fromid not in prune:
      if mindepth<=depth:
        mintotalprofitPh[0]=max(mintotalprofitPh[0],profit/hours)
        loops.append([profit/hours,[start]+history])
      return False
    for toid in prune[fromid]:
      if lastdistance<prune[fromid][toid]["targetdistance"]: # only closer than previous allowed
        continue
      if prune[fromid][toid]["targetdistance"]<1: # we're really close to target
        profit+=prune[fromid][toid]['profit']
        hours+=prune[fromid][toid]['hours']
        mintotalprofitPh[0]=max(mintotalprofitPh[0],profit/hours)
        loops.append([profit/hours,[start]+history+[toid]])
      elif toid in history: # avoid internal loops on the way
        continue
      elif toid in routed: # avoid multiple entries
        continue
      elif toid==start: # found loop
        if mindepth<=depth:
          profit+=prune[fromid][toid]['profit']
          hours+=prune[fromid][toid]['hours']
          mintotalprofitPh[0]=max(mintotalprofitPh[0],profit/hours)
          loops.append([profit/hours,[start]+history+[toid]])
      else: # deadend
        walk(toid,start,history+[toid],profit+prune[fromid][toid]['profit'],hours+prune[fromid][toid]['hours'],prune[fromid][toid]["targetdistance"])
  ############

  querystart=time.time()
  chokelevel=0
  loops=[]
  satisfiedwithresult=False
  while not satisfiedwithresult and profitmargin>=0:
    walkstart=time.time()
    loops=[]
    routed=dict()

    lastupdate=0
    updateinterval=1

    for bi in range(len(bases)):
      fromid=bases[bi]
      if time.time()-updateinterval > lastupdate: # console may slow us down so keep update intervals
        lastupdate=time.time()
        print("   "+str("%.2f"%(bi/len(bases)*100))+"%  "+str(len(loops))+" routes")
      for toid in prune[fromid]:
        if sourcebase is not None or sourcesystem is not None: # forgive first step in export search
          walk(toid,fromid,[toid],mintotalprofitPh[0],1,prune[fromid][toid]['targetdistance'])
        else:
          walk(toid,fromid,[toid],prune[fromid][toid]['profit'],prune[fromid][toid]['hours'],prune[fromid][toid]['targetdistance'])
      routed[fromid]=True

    if walkstart+walktimeout<time.time() and len(loops)>=minroutes and profitmargin<1.0 and chokelevel<chokeforcelevel:
      print('chocking in data - lowering profit allowance step')
      chokelevel+=1
      if chokelevel==chokeforcelevel:
        print("giving up on optimizing")
      profitmargin=profitmargin+profitmarginstep
      profitmarginstep/=10
      profitmargin-=profitmarginstep
      profitmargin=min(1.0,profitmargin)
      print("let's try again with "+str(int((1-profitmargin)*100*100)/100)+"% profit allowance")
    elif len(loops)<minroutes and profitmargin<1.0 and chokelevel<chokeforcelevel:
      profitmargin-=profitmarginstep
      print("found "+str(len(loops))+" trade routes - trying again with "+str(int((1-profitmargin)*100*100)/100)+"% profit allowance")
    else:
      satisfiedwithresult=True



  print("Found "+str(len(loops))+" long trade routes in "+str("%.2f"%(time.time()-querystart))+" seconds")

  loops = sorted(loops,key=lambda ar:ar[0],reverse=True) # sort by profit
  loops=loops[:10000] # don't overload the window
  loops=[i[1] for i in loops]

  prune=ProfitArrayToHierarchy(oneway)

  print("Gathering hops...")
  traderoutes=[]
  for loop in loops:
    route=dict()
    route["loopminprofit"]=0
    route["loopmaxprofit"]=0
    route["totalprofitPh"]=0
    route["totalhours"]=0
    route["hops"]=[]
    route["distancefromlast"]=-1
    prev=loop[0]
    for ni in range(1,len(loop)): # by hop
      next=loop[ni]
      hoptrades = prune[prev][next].values() # all possible commodities on this route
      hoptrades = sorted(hoptrades,key=operator.itemgetter("profitPh"),reverse=True) # sort by profit
      route["loopminprofit"]+=hoptrades[-1]["profit"]
      route["loopmaxprofit"]+=hoptrades[0]["profit"]
      route["totalhours"]+=hoptrades[0]["hours"]
      route["distancefromlast"]=hoptrades[0]["targetdistance"]
      prev=next
      route["hops"].append(hoptrades) # store hops
    route["averageprofit"]=int(route["loopmaxprofit"]/len(route["hops"]))
    route["totalprofitPh"]=int(route["loopmaxprofit"]/route["totalhours"])
    traderoutes.append(route)

  traderoutes.sort(key=operator.itemgetter("totalprofitPh"),reverse=True) # sort by profit
  traderoutes.sort(key=lambda r:len(r["hops"])) # sort by hops
  traderoutes.sort(key=operator.itemgetter("distancefromlast")) # sort by distance

  traderoutes=traderoutes[:maxroutes] # don't overload the window

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
      "totalprofitPh":loop["totalprofitPh"],
      "totalhours":loop["totalhours"]
    }))
    #returnarray.append('separatorrow')
  return returnarray




def queryCommodities(db, x, y, z, maxDistance, minPadSize,jumprange ,importexport,commodityid):

  queryparams=dict()
  queryparams['x']=x
  queryparams['y']=y
  queryparams['z']=z
  queryparams['maxdistance']=maxDistance
  queryparams['landingPadSize']=minPadSize
  queryparams['jumprange']=jumprange
  queryparams['lastUpdated']=int(Options.get('Market-valid-days',7))
  queryparams['importexport']=importexport
  queryparams['commodityId']=commodityid


  results=db.getCommoditiesInRange(queryparams)

  #sort by time/value relation like usual
  for result in results:
    result['exportPh']=result['hours']/(result['exportPrice']+0.1) # can't be 0
    result['importPh']=result['importPrice']/result['hours']

  if importexport==0:
    results.sort(key=operator.itemgetter('importPh'),reverse=True)
  else:
    results.sort(key=operator.itemgetter('exportPh'))

  return results[:5000] # only winners go home