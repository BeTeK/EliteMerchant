import pygame

import Options
import SoundsAbstract

class SoundsPyGame(SoundsAbstract.SoundsAbstract):
  def __init__(self):
    print("Using PyGame for sound")
    self.sounds={
      "startup":None,
      "search":None,
      "error":None
    }
    pygame.init() # load soundsystem to avoid race conditions
    self.refreshSounds()

  def setSoundFile(self, sound, file):
    try:
        self.sounds[sound]=pygame.mixer.Sound( file )
    except:
      print("Error loading sound file ["+file+"]!\nPlease check file path and format!")


  def refreshSounds(self):
    for soundname in self.sounds:
      self.setSoundFile(soundname,Options.get("sounds-"+soundname, "sounds/"+soundname+".wav"))

  def setVolume(self,volume):
    for s in self.sounds:
      if self.sounds[s] is not None:
        self.sounds[s].set_volume( float(volume)/100 )

  def play(self,sound):
    if sound not in self.sounds:
      print("[" + sound + "] is not a valid sound to play! call your local DJ and try again!")
      return
    if Options.get("sounds-enabled", "0")=="1":
      if self.sounds[sound] is not None:
        self.sounds[sound].play()
      else:
        print("[" + sound + "] is not loaded! check filename and format!")

  def quit(self):
    pygame.quit()