import os
import sys
import Options

from os.path import expanduser

home = expanduser("~")

class EdceWrapper:
    def __init__(self, edcePath, verificationCodeInputFn):
        global home

        sys.path.insert(0, edcePath)
        sys.path.insert(0, os.path.join(edcePath, "edce"))

        import configparser
        import edce.query
        import edce.error
        import edce.util
        import edce.eddn
        import edce.config
        import edce.globals
        edce.config.setConfigFile(os.path.join(home, "edce.ini"))
        edce.config.writeConfig(Options.get("elite-username", ""), Options.get("elite-password", ""), True, home, home)
        res = edce.query.performQuery(verificationCodeSupplyFn = verificationCodeInputFn)
        self.result = edce.util.edict(res)
        if edce.config.getString('preferences','enable_eddn').lower().find('y') >= 0:
            edce.eddn.postMarketData(self.result)

    def getResult(self):
        return self.result