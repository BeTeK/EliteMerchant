from SQLiteDB import SQLiteDB



def updatePrices(db):
  pass

def main():
  with SQLiteDB("main.sqlite", True) as db:
    updatePrices(db)





if __name__ == "__main__":
  main()
