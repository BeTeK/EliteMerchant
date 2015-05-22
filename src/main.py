from SQLiteDB import SQLiteDB
import sys
from pprint import pprint # lets make debugging beautiful
from PyQt5 import QtCore, QtGui, QtWidgets
import ui.MainWindow
import time
import Options
import Queries
import EDDB

def loadEDDB(db, options):
  EDDB.update(db)

def addSystem(db):
  db.addSystem("foobar2")

def fetchSystem(db):
  systems = db.getSystemByName("sol")
  systems[0].getStations()

def testfn(db, options):
  systems = db.getSystemByWindow((0, 0, 0), 10)
  print(systems)
  

def testfunction(db,options):
    #updatePrices(db)
    #querystart=time.time()
    queryresult=db.queryProfitWindow(0,0,0,30,30,1600)
    #querytime=time.time()-querystart
    #pprint(queryresult)
    #pprint(str(len(queryresult))+" values time="+str(querytime))
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
        options["operation"] = testfunction
      elif sys.argv[index] in ["--test"]: # devhax
        options["operation"] = testfn
        
      index += 1
  except Exception as ex:
    pprint("Not known param")
  if options["operation"] is not None:
    with SQLiteDB(options["dbPath"], options["eraseDb"]) as db:
      options["operation"](db, options)

if __name__ == "__main__":
  main()
