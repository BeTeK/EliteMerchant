
powersbyname=dict({ # enum these by eddb ids, http://eddb.io/power
  'Edmund Mahon':1,
  'Felicia Winters':2,
  'Zachary Hudson':3,
  'Zemina Torval':4,
  'Arissa Lavigny-Duval':5,
  'Aisling Duval':6,
  'Denton Patreus':7,
  'Archon Delaine':8,
  'Li Yong-Rui':9,
  'Pranav Antal':10
})
powersbyval=dict()
for p in powersbyname.items():
  powersbyval[p[1]]=p[0]


def nameToVal(name):
  if name is None:
    return None
  if name not in powersbyname:
    print('Power name '+str(name)+' not in powers list!')
    return None
  return powersbyname[name]

def valToName(val):
  if val is None:
    return None
  if val is None or val<1 or val>10 or powersbyval[val] is None:
    print('Invalid power value '+str(val)+'!')
    return '?'
  return powersbyval[val]




def applyPowerPolicy(controlpowerid,exploitedpowerid,stationrow): #

  # Zemina Torval
  if controlpowerid==4:
    # CONTROL force imperial slaves legal
    stationrow[0]['prohibited_commodities']=[c for c in stationrow[0]['prohibited_commodities'] if c != 'Imperial Slaves']
  if exploitedpowerid==4:
    # exploited bonus is passive, requires pledge
    # PLEDGED ONLY
    # profit+   5    / 10  / 15  / 20
    # standing  base / 3   / 2   / 1
    return

  # Edmund Mahon
  if controlpowerid==1:
    # -
    pass
  if exploitedpowerid==1:
    # exploited bonus is passive, requires pledge
    # PLEDGED ONLY
    # profit+   5    / 10  / 15  / 20
    # standing  base / 3   / 2   / 1
    return

  # Pranav Antal
  if controlpowerid==10:
    # CONTROL force black markets closed
    stationrow[0]['has_blackmarket']=False
    pass
  if exploitedpowerid==10:
    # EXPLOITED black market bonus 10%
    return

  # Archon Delaine
  if controlpowerid==8:
    # CONTROL force black markets open
    stationrow[0]['has_blackmarket']=True
    # CONTROL nercotics, weapons legal
    allowlist=[
      'Battle Weapons',
      'Non-lethal Weapons',
      'Personal Weapons',
      'Reactive Armor',
      'Narcotics',
      'Tobacco'
    ]
    stationrow[0]['prohibited_commodities']=[c for c in stationrow[0]['prohibited_commodities'] if c not in allowlist ]
  if exploitedpowerid==8:
    # EXPLOITED black market bonus 10%
    return

  # Arissa Lavigny-Duval
  if controlpowerid==5:
    # CONTROL force black markets closed
    stationrow[0]['has_blackmarket']=False
  if exploitedpowerid==5:
    # EXPLOITED black market bonus 5%
    return

  # Zachary Hudson
  if controlpowerid==3:
    # CONTROL force imperial slaves illegal
    stationrow[0]['prohibited_commodities']=[c for c in stationrow[0]['prohibited_commodities'] if c != 'Imperial Slaves']
    stationrow[0]['prohibited_commodities'].append('Imperial Slaves')
  if exploitedpowerid==3:
    # -
    return

  # Aisling Duval
  if controlpowerid==6:
    # CONTROL/EXPLOITED force imperial slaves illegal
    pass
  if exploitedpowerid==6:
    # CONTROL/EXPLOITED force imperial slaves illegal
    stationrow[0]['prohibited_commodities']=[c for c in stationrow[0]['prohibited_commodities'] if c != 'Imperial Slaves']
    stationrow[0]['prohibited_commodities'].append('Imperial Slaves')
    return

  # Denton Patreus
  if controlpowerid==7:
    # CONTROL force imperial slaves legal
    stationrow[0]['prohibited_commodities']=[c for c in stationrow[0]['prohibited_commodities'] if c != 'Imperial Slaves']
  if exploitedpowerid==7:
    # -
    return

