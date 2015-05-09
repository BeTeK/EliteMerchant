from SQLiteDB import SQLiteDB



def updatePrices(db):
  pass

def addSystem(db):
  db.addSystem("foobar2")

def main():
  with SQLiteDB("main.sqlite") as db:
    addSystem(db)





if __name__ == "__main__":
  main()
