from SQLiteDB import SQLiteDB
from EDDB import EDDB
import sys
from pprint import pprint # lets make debugging beautiful
from PyQt5 import QtCore, QtGui, QtWidgets
import ui.MainWindow
import time
import Options

def loadEDDB(db, options):
  EDDB().update(db)

def addSystem(db):
  db.addSystem("foobar2")

def fetchSystem(db):
  systems = db.getSystemByName("sol")
  systems[0].getStations()

def testfunction():
  with SQLiteDB("main.sqlite") as db:
    #updatePrices(db)
    querystart=time.time()
    queryresult=db.queryProfitWindow(0,0,0,30,30,1600)
    querytime=time.time()-querystart
    #pprint(queryresult)
    pprint(str(len(queryresult))+" values time="+str(querytime))
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
      elif sys.argv[index] in ["--load-eddb"]:
        options["operation"] = loadEDDB
      elif sys.argv[index] in ["--testfunction"]: # devhax
        return testfunction()
        
      index += 1
  except Exception as ex:
    pprint("Not known param")
  if options["operation"] is not None:
    with SQLiteDB(options["dbPath"], options["eraseDb"]) as db:
      options["operation"](db, options)

if __name__ == "__main__":
  main()
