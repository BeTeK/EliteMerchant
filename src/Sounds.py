import Options
from PyQt5 import QtCore

# todo: remove extraneous soundsystems once consensus reached

soundsystem=None
if soundsystem is None:
  try:
    import pygame # general purpose game sound engine
    print("Using PyGame for sound")
    soundsystem="pygame"
  except:
    pass

if soundsystem is None:
  try:
    import pyglet # pyglet has easy syntax but is a fucking nazi with file formats and doesn't even follow standards
    print("Using Pyglet for sound")
    soundsystem="pyglet"
  except:
    pass

if soundsystem is None:
  try:
    from PyQt5 import QtMultimedia # QtMultimedia is great for windows but works only through gstreamer on linux
    print("Using QtMultimedia for sound")
    soundsystem="qt"
  except:
    pass


class Sounds:
  def __init__(self):
    self.sounds={
      "startup":None,
      "search":None,
      "error":None
    }
    if soundsystem is None:
      print("No soundsystem module loaded - sound functions disabled...")
      return
    if soundsystem=="pygame":
      pygame.init() # load soundsystem to avoid race conditions
    if soundsystem=='qt':
      self.sounds={
        "startup":QtMultimedia.QMediaPlayer(),
        "search":QtMultimedia.QMediaPlayer(),
        "error":QtMultimedia.QMediaPlayer()
      }
    self.refreshSounds()

  def setSoundFile(self, sound, file):
    if soundsystem is None:
      return
    try:
      if soundsystem=='qt':
        self.sounds[sound].setMedia(QtMultimedia.QMediaContent( QtCore.QUrl( file )))
      if soundsystem=='pygame':
          self.sounds[sound]=pygame.mixer.Sound( file )
      if soundsystem=='pyglet':
        self.sounds[sound]=pyglet.media.load( file )
    except:
      print("Error loading sound file ["+file+"]!\nPlease check file path and format!")


  def refreshSounds(self):
    if soundsystem is None:
      return
    for soundname in self.sounds:
      self.setSoundFile(soundname,Options.get("sounds-"+soundname, "sounds/"+soundname+".wav"))

  def setVolume(self,volume):
    if soundsystem is None:
        return
    if soundsystem=='pyglet':
      self.refreshSounds()
      """
      for s in self.sounds:
        self.sounds[s].setVolume( int(Options.get("sounds-volume",100)) )
      """
    if soundsystem=='qt':
      for s in self.sounds:
        if self.sounds[s] is not None:
          self.sounds[s].setVolume( volume )
    if soundsystem=='pygame':
      for s in self.sounds:
        if self.sounds[s] is not None:
          self.sounds[s].set_volume( float(volume)/100 )

  def play(self,sound):
    if soundsystem is None:
      return
    if sound not in self.sounds:
      print("[" + sound + "] is not a valid sound to play! call your local DJ and try again!")
      return
    if Options.get("sounds-enabled", "0")=="1":

      if soundsystem=='pyglet':
        self.sounds[sound].play()

      if soundsystem=='qt':
        self.sounds[sound].play()

      if soundsystem=='pygame':
        if self.sounds[sound] is not None:
          self.sounds[sound].play()
        else:
          print("[" + sound + "] is not loaded! check filename and format!")

  def quit(self):
    if soundsystem is None:
      return
    if soundsystem=="pygame":
      pygame.quit()