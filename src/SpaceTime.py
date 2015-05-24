from math import *

# calculating spacetime relations - namely how long it takes to travel across sytems and within a system

def BaseToBase(ly,shiprange=16.5,stops=1):

  # calculated magic values:   see traveltimes.ods for source data

  time_hop=13 # single hop takes 13 seconds
  time_fsdrecharge=31.4 # time between fsd jumps in multi-hop travel
  time_stationdock=69.1 # time after dropping out of supercruise, entering station
  time_stationbusiness=49.6 # time spent trading in station
  time_stationleave=54.7 # time between leaving and fsd

  # todo: hopsPerLy ship range multiplier
  hopsPerLy=1.464/shiprange

  #empty hauler
  #hopsPerLy=0.055 # multiplier for ly to get number of hops
  #empty t7 23.28
  #hopsPerLy=0.061 # multiplier for ly to get number of hops
  #full t7 16.53
  #hopsPerLy=0.088 # multiplier for ly to get number of hops

  #hops=ceil(ly*hopsPerLy)
  hops=ly*hopsPerLy

  time_in_fsd=( hops * time_hop ) + ( max(0,(hops-1)) * time_fsdrecharge )

  time_in_stations=time_stationleave*stops + (stops-1)*time_stationbusiness + time_stationdock*stops

  return time_in_fsd+time_in_stations

def StarToBase(ls):
  if ls is None:
    #ls=16701.7188122397 # average base dest
    ls=291.0  # median base dist
  """
  values result of sagemath fit:
  reference=[
    ... ls,seconds tuples from traveltimes.ods
  ]

  var('a, b, c, d, x')
  def curvef(x,a,b,c,d):
    return (log(x+b)*(c+(a/10)))-d-a
  fit=find_fit(reference, curvef, parameters = [a, b, c, d], variables = [x], solution_dict = True)
  print(fit)

  refplot=list_plot( [[ls,sec] for ls,sec in reference] , color="red")
  logrefplot=list_plot( [[log(ls),sec] for ls,sec in reference] , color="red")
  def retfit(x):
    return curvef(x,fit[a],fit[b],fit[c],fit[d])
  fitplot=plot(retfit,1,221000)
  logfitplot=list_plot([[log(ls),retfit(ls)] for ls in range(1,221000,50)])
  show(fitplot+refplot)
  show(logfitplot+logrefplot)
  """
  a=745.359463485
  b=6614.34380137
  c=125.12281681
  d=922.259103446
  time_in_supercruise=(log(ls+b)*(c+(a/10)))-d-a
  return time_in_supercruise