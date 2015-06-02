
import SoundsAbstract

def Sounds():

  # let's see what sound libraries the user has!

  # pygame is a general purpose game sound engine and maybe a bit overkill, but should work great on linux
  try:
    import SoundsPyGame
    return SoundsPyGame.SoundsPyGame()
  except:
    pass

   # QtMultimedia is great for windows but works only through gstreamer on linux
  try:
    import SoundsQtMultimedia
    return SoundsQtMultimedia.SoundsQtMultimedia()
  except:
    pass
  """
  # pyglet has easy syntax but is a fucking nazi with file formats and doesn't even follow standards
  try:
    import SoundsPyglet
    return SoundsPyglet.SoundsPyglet()
  except:
    pass
  """
  print("No soundsystem module loaded - sound functions disabled...")

  return SoundsAbstract.SoundsAbstract() # return dummy to eat calls
