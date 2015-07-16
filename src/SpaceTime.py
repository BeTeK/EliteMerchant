from math import *

# calculating spacetime relations - namely how long it takes to travel between systems and within a system

def BaseToBase(ly,shiprange=16.5,stops=1):

  # calculated magic values:   see traveltimes.ods for source data

  time_hop=13 # single hop takes 13 seconds
  time_fsdrecharge=31.4 # time between fsd jumps in multi-hop travel
  time_stationdock=69.1 # time after dropping out of supercruise, entering station
  time_stationbusiness=49.6 # time spent trading in station
  time_stationleave=54.7 # time between leaving and fsd

  hops=0.2+(ly/shiprange)*1.35

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

  var('a, b, c, ls')
  def curvef(ls,a,b,c):
      return log(ls+a)*b-c
  fit=find_fit(reference, curvef, parameters = [a, b, c], variables = [ls], solution_dict = True)
  print(fit)

  refplot=list_plot( [[ls,sec] for ls,sec in reference] , color="red")
  logrefplot=list_plot( [[log(ls),sec] for ls,sec in reference] , color="red")
  def retfit(ls):
      return curvef(ls,fit[a],fit[b],fit[c])
  fitplot=plot(retfit,1,221000)
  logfitplot=list_plot([[log(ls),retfit(ls)] for ls in range(1,221000,50)])
  show(fitplot+refplot)
  show(logfitplot+logrefplot)
  """
  a= 6613.896196062265
  b= 199.65462707095878
  c= 1667.5696048367702
  time_in_supercruise= log(ls+a)*b-c
  return time_in_supercruise