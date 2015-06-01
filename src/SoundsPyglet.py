import pyglet

import Options
import SoundsAbstract

class SoundsPyglet(SoundsAbstract.SoundsAbstract):
  def __init__(self):
    print("Using Pyglet for sound")
    self.sounds={
      "startup":None,
      "search":None,
      "error":None
    }
    self.refreshSounds()

  def setSoundFile(self, sound, file):
    try:
      self.sounds[sound]=pyglet.media.load( file )
    except:
      print("Error loading sound file ["+file+"]!\nPlease check file path and format!")


  def refreshSounds(self):
    for soundname in self.sounds:
      self.setSoundFile(soundname,Options.get("sounds-"+soundname, "sounds/"+soundname+".wav"))

  def setVolume(self,volume):
    self.refreshSounds()
    """
    for s in self.sounds:
      self.sounds[s].setVolume( int(Options.get("sounds-volume",100)) )
    """

  def play(self,sound):
    if sound not in self.sounds:
      print("[" + sound + "] is not a valid sound to play! call your local DJ and try again!")
      return
    if Options.get("sounds-enabled", "0")=="1":
      self.sounds[sound].play()
