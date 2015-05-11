from SQLiteDB import SQLiteDB
from EDDB import EDDB
import sys
from pprint import pprint # lets make debugging beautiful

def updatePrices(db):
  EDDB().update(db)

def addSystem(db):
  db.addSystem("foobar2")

def fetchSystem(db):
  systems = db.getSystemByName("sol")
  systems[0].getStations()

def main1():
  with SQLiteDB("main.sqlite") as db:
    #updatePrices(db)
    pprint(db.queryProfitWindow(0,0,0,30,30,1600))
    #fetchSystem(db)

def main():
  index = 1
  options = {"dbPath" : "main.sqlite",
             "eraseDb" : False,
             "operation" : None}
  
  try:
    while index < len(sys.argv):
      if sys.argv[index] in ["--databasepath", "-db"]:
        index += 1
        options["dbPath"] = sys.argv[index]
      elif sys.argv[index] in ["--erasedb", "-E"]:
        options["eraseDb"] = True
        
      index += 1
  except Exception as ex:
    pprint("Not known param")


if __name__ == "__main__":
  main()
