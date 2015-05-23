
from PyQt5.QtCore import QSettings
import os
from os.path import expanduser

home = expanduser("~")
settings = QSettings(os.path.join(home, ".EliteDB.ini"), QSettings.IniFormat)

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
