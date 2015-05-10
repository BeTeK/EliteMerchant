from SQLiteDB import SQLiteDB
from EDDB import EDDB

def updatePrices(db):
  EDDB().update(db)

def addSystem(db):
  db.addSystem("foobar2")

def main():
  with SQLiteDB("main.sqlite") as db:
    updatePrices(db)
    #print(db.queryProfitWindow(0,0,0,30,30,1600))


if __name__ == "__main__":
  main()
