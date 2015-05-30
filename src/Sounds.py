import Options
from PyQt5 import QtCore, QtMultimedia

class Sounds:
  def __init__(self):
    self.sounds={
      "startup":QtMultimedia.QMediaPlayer(),
      "searched":QtMultimedia.QMediaPlayer(),
      "error":QtMultimedia.QMediaPlayer()
    }
    self.refreshSounds()

  def setSoundFile(self, sound, file):
    self.sounds[sound].setMedia(QtMultimedia.QMediaContent( QtCore.QUrl( file )))

  def refreshSounds(self):
    # invalid filenames are ok - they will fail silently
    self.sounds["startup"].setMedia( QtMultimedia.QMediaContent( QtCore.QUrl( Options.get("sounds-startup", "sounds/Windows Notify.wav") ) ) )
    self.sounds["searched"].setMedia( QtMultimedia.QMediaContent( QtCore.QUrl( Options.get("sounds-searched", "sounds/Windows Shutdown.wav") ) ) )
    self.sounds["error"].setMedia( QtMultimedia.QMediaContent( QtCore.QUrl( Options.get("sounds-error", "sounds/Windows Critical Stop.wav") ) ) )
    #print("updated sounds")

  def play(self,sound):
    if Options.get("sounds-enabled", "0")=="1":
      for s in self.sounds:
        self.sounds[s].setVolume( int(Options.get("sounds-volume",100)) )
        self.sounds[s].setVolume( int(Options.get("sounds-volume",100)) )
        self.sounds[s].setVolume( int(Options.get("sounds-volume",100)) )
      if sound not in self.sounds:
        print("[" + sound + "] is not a valid sound to play! call your local DJ and try again!")
      self.sounds[sound].play()