
from PyQt5.QtCore import QSettings
import os
from os.path import expanduser


def getPath(file = None):
    global dirPath
    if file is None:
        return dirPath

    return os.path.join(dirPath, file)

def get(key, default, *formatStr):
    global settings
    val = settings.value(key, default)
    if len(formatStr) == 0:
        return val
    else:
        return val.format(*formatStr)
    
def set(key, value):
    global settings
    settings.setValue(key, value)
    settings.sync() # save the value

home = expanduser("~")
dirPath = os.path.join(home, "EliteMerchant")
if not os.path.exists(dirPath):
    os.makedirs(dirPath)


filePath = getPath("EliteMerchant.ini")
settings = QSettings(filePath, QSettings.IniFormat)
