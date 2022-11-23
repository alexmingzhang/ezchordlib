# ezchordlib
Python library that can handle complex musical chords

Usage:
  >>> from ezchordlib import Chord
  >>> cool = Chord("Am7b5#11/E")
  >>> cool.get_midi()
  [4, 21, 24, 27, 31, 39]
  >>> cool.get_scale_degrees()
  {1: 0, 3: -1, 5: -1, 7: -1, 11: 1}
  >>> cool.get_notes()
  ['E', 'A', 'C', 'Eb', 'G', 'D#']
