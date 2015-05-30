from PyQt5 import QtCore, QtMultimedia

import Options
import SoundsAbstract

class SoundsQtMultimedia(SoundsAbstract.SoundsAbstract):
  def __init__(self):
    print("Using QtMultimedia for sound")
    self.sounds={
      "startup":None,
      "search":None,
      "error":None
    }
    self.sounds={
      "startup":QtMultimedia.QMediaPlayer(),
      "search":QtMultimedia.QMediaPlayer(),
      "error":QtMultimedia.QMediaPlayer()
    }
    self.refreshSounds()

  def setSoundFile(self, sound, file):
    try:
      self.sounds[sound].setMedia(QtMultimedia.QMediaContent( QtCore.QUrl( file )))
    except:
      print("Error loading sound file ["+file+"]!\nPlease check file path and format!")


  def refreshSounds(self):
    for soundname in self.sounds:
      self.setSoundFile(soundname,Options.get("sounds-"+soundname, "sounds/"+soundname+".wav"))

  def setVolume(self,volume):
    for s in self.sounds:
      if self.sounds[s] is not None:
        self.sounds[s].setVolume( volume )

  def play(self,sound):
    if sound not in self.sounds:
      print("[" + sound + "] is not a valid sound to play! call your local DJ and try again!")
      return
    if Options.get("sounds-enabled", "0")=="1":
      self.sounds[sound].play()
