from SQLiteDB import SQLiteDB
from EDDB import EDDB

from pprint import pprint # lets make debugging beautiful

def updatePrices(db):
  EDDB().update(db)

def addSystem(db):
  db.addSystem("foobar2")

def fetchSystem(db):
  systems = db.getSystemByName("sol")
  systems[0].getStations()

def main():
  with SQLiteDB("main.sqlite") as db:
    #updatePrices(db)
    pprint(db.queryProfitWindow(0,0,0,30,30,1600))
    #fetchSystem(db)





if __name__ == "__main__":
  main()
