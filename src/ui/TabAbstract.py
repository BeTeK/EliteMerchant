
class TabAbstract:
    def setTabName(self, name):
        raise NotImplemented()

    def getTabName(self):
        raise NotImplemented()

    def getType(self):
        raise NotImplemented()

    def dispose(self):
        raise NotImplemented()
