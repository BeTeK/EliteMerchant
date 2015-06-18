import time, Options

class TabAbstract:
    def setTabName(self, name):
        raise NotImplemented()

    def getTabName(self):
        raise NotImplemented()

    def getType(self):
        raise NotImplemented()

    def dispose(self):
        raise NotImplemented()

    def AgeToColor(self,timestamp):
        def clamp(minv,maxv,v):
          return max(minv,min(maxv,v))

        age= ( (time.time() -  timestamp  )/(60.0*60.0*24.0) ) / float(Options.get("Market-valid-days", 7))

        colorblind=False # todo: add an option
        # colorblind mode
        if (colorblind):
          print(age)
          i=clamp(64,255,255-age*128)

          return i,i,i

        # if data is older than market validity horizon, have it show
        desat=1
        if age>1.0:
          desat=0

        age*=2

        r=255*clamp(0.2*desat,1.0,(age-1)+0.5)
        g=255*clamp(0.4*desat,1.0,(1-age)+0.5)
        b=255*clamp(0.5*desat,1.0,(abs(age-1)*-1)+1)
        return r,g,b