import os
from SQLiteDB import SQLiteDB
import sys
from pprint import pprint # lets make debugging beautiful
from PyQt5 import QtCore, QtGui, QtWidgets
import ui.MainWindow
import EDDB
import EdceWrapper
import certifi
import Options


def loadEDDB(db, options):
  EDDB.update(db)

def addSystem(db):
  db.addSystem("foobar2")

def fetchSystem(db):
  systems = db.getSystemByName("sol")
  systems[0].getStations()

def testfn(db, options):
  #EDDB.update(db)
  #Queries.queryProfitGraph(db,0,0,0,60,1,30,500,0,2)
  #systems = db.getSystemByWindow((0, 0, 0), 10)
  #print(systems)
  edce = EdceWrapper.EdceWrapper("D:\\prog\\edce-client", db, verification)
  edce.fetchNewInfo()
  edce.join()
  edce.updateResults()

def verification():
    code = input("code: ")
    return code

def showUI(db, options):
  app = QtWidgets.QApplication(sys.argv)
  ex = ui.MainWindow.MainWindow(db)
  ex.show()
  sys.exit(app.exec_())

def main():

  index = 1
  options = {"dbPath" : Options.getPath("EliteMerchantList.sqlite"),
             "eraseDb" : False,
             "operation" : None,
             "redirectOutputToLog" : False}
  
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
      elif sys.argv[index] in ["--test"]: # devhax
        options["operation"] = testfn
      elif sys.argv[index] in ["--redirectOutput"]:
        stdOutFile = open(Options.getPath("eliteDb_stdout.log"), "w+")
        stdErrFile = open(Options.getPath("eliteDb_stderr.log"), "w+")

        sys.stdout = stdOutFile
        sys.stderr = stdErrFile
        
      index += 1
  except Exception as ex:
    pprint("Not known param")

  if options["operation"] is not None:
    with SQLiteDB(options["dbPath"], options["eraseDb"]) as db:
      options["operation"](db, options)

if __name__ == "__main__":
  main()
