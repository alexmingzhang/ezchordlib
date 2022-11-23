import math
from .constants import *
from .parse import parse
from .utils import text_to_pitch, scale_degree_to_note

class Chord:
    def __init__(self, chord: str, key='c'):
        self._chord: str = chord
        
        root, quality, bass_note, extensions = parse(chord)
        self._root: str = root
        self._quality: Quality = quality
        self._bass_note: str = bass_note
        self._extensions: dict = extensions
        
    def __unicode__(self):
        return self._chord

    def __str__(self):
        return self._chord

    def __repr__(self):
        return f"<Chord: {self._chord}>"

    def __eq__(self, other):
        return self.get_midi() == other.get_midi()

    def get_scale_degrees(self):
        degrees = {}
        degrees[1] = 0
        degrees[3] = QUALITY_TO_SHIFT[self._quality][3]
        degrees[5] = QUALITY_TO_SHIFT[self._quality][5]

        for ext, ext_shift in self._extensions.items():
            if ext_shift == None and ext in degrees:
                del degrees[ext]
            else:
                degrees[ext] = ext_shift

        return dict(sorted(degrees.items()))
    
    def get_midi(self):
        pitches = []
        
        if self._bass_note != None:
            pitches.append(text_to_pitch(self._bass_note) - 12)

        root_pitch = text_to_pitch(self._root)
        
        for degree, shift in self.get_scale_degrees().items():
            octave = math.floor(degree / 8)
            scale_degree = (degree - 1) % 7 + 1

            pitches.append(root_pitch + SCALE_DEGREE_TO_SHIFT[scale_degree] + shift + octave * 12)
        
        while (pitches[0] < 0):
            for i in range(len(pitches)):
                pitches[i] = pitches[i] + 12

        return pitches

    def get_notes(self):
        notes = []

        if self._bass_note != None:
            notes.append(self._bass_note)

        for degree, shift in self.get_scale_degrees().items():
            notes.append(scale_degree_to_note(degree, self._root, shift))
        
        return notes