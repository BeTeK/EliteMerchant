import Options
from xml.dom.minidom import Node
from xml.dom import minidom
import os

class EliteLogAnalyzer:
    def __init__(self):
        self.path = None
        self.fixLog = True
        self.currentStatus = {
            "PlayerName" : "",
            "System" : "",
            "Near" : ""
        }
        self.dockPermissionGot = False

    def setFixLog(self, fixLog):
        self.fixLog = fixLog
        self.setPath(self.path)

    def hasDockPermissionGot(self):
        return self.dockPermissionGot

    def setPath(self, path):
        try:
            if path is None:
                return

            if self.fixLog:
                self._fixLoggingSetting(path)

            self.path = path
            return True

        except Exception as ex:
            return False

    def poll(self):
        try:
            ret = False

            if self.path is None:
                return

            logFileName = self._findNewestNetLog()

            if logFileName is None:
                return

            latestIsland = None
            permissionGot = False
            with open(os.path.join(self.path, "Logs", logFileName), "rb") as file:
                for lineNum, line in enumerate(file):
                    if line.find(b"IJoinSession:Island: ") >= 0 or \
                       line.find(b"^^^------------ ") >= 0:
                        latestIsland = None
                        permissionGot = False

                    if line.find(b"System:") >= 0:
                        latestIsland = line

                    if line.find(b"Dock Permission Received on pad") >= 0:
                        permissionGot = True


            if latestIsland is None:
                return

            latestIsland = latestIsland.decode("latin-1").replace("\n", "").replace("\r", "")

            if permissionGot != self.dockPermissionGot:
                self.dockPermissionGot = permissionGot
                ret = True

            if self.currentStatus != self._parseLatestIsland(latestIsland):
                self.currentStatus = self._parseLatestIsland(latestIsland)
                ret = True

            return ret

        except Exception as ex:
            return None

    def getCurrentStatus(self):
        return self.currentStatus

    def _findChild(self, cur, name):
        for node in cur.childNodes:
            if node.nodeType == Node.ELEMENT_NODE and node.nodeName == name:
                return node

        return None

    def _fixLoggingSetting(self, path):
        doc = minidom.parse(os.path.join(path, "AppConfig.xml"))
        appConfig = doc.childNodes[0]
        networkNode = self._findChild(appConfig, "Network")
        if networkNode is None:
            return

        if networkNode.hasAttribute("VerboseLogging") and networkNode.getAttribute("VerboseLogging") == "1":
            return

        networkNode.setAttribute("VerboseLogging", "1")
        with open(os.path.join(path, "AppConfig.xml"), "w+") as file:
            doc.writexml(file)

    def _findNewestNetLog(self):
        file = None
        latestDate = None

        for path in os.listdir(os.path.join(self.path, "Logs")):
            if not path.startswith("netLog."):
                continue

            date = path[len("netLog."):len("netLog.") + 10]
            if file is None or date > latestDate:
                latestDate = date
                file = path

        return file

    def _parseLatestIsland(self, latestIsland):
        startPos = latestIsland.index("(") + 1
        endPos = latestIsland.index(")", startPos)

        return {
            "PlayerName" : "",
            "System" : latestIsland[startPos:endPos],
            "Near" : ""
        }

