from SQLiteDB import SQLiteDB
from EDDB import EDDB
import sys
from pprint import pprint # lets make debugging beautiful
from PyQt5 import QtCore, QtGui, QtWidgets
import ui.MainWindow

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
    pprint(db.queryProfitWindow(0,0,0,100,100,1600))
    #fetchSystem(db)

def showUI(db, options):
  app = QtWidgets.QApplication(sys.argv)
  ex = ui.MainWindow.MainWindow(db)
  ex.show()
  sys.exit(app.exec_())

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
      elif sys.argv[index] in ["--UI"]:
        options["operation"] = showUI
        
      index += 1
  except Exception as ex:
    pprint("Not known param")

  with SQLiteDB(options["dbPath"], options["eraseDb"]) as db:
    options["operation"](db, options)

if __name__ == "__main__":
  main()
