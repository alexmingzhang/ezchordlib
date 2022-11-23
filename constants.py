from enum import Enum, auto

NOTES = ("a", "b", "c", "d", "e", "f", "g")
ROMAN_NUMERALS = ("i", "ii", "iii", "iv", "v", "vi", "vii")
ROMAN_NUMERAL_LETTERS = ("i", "v")
ACCIDENTALS = ("#", "b")

NOTE_TO_PITCH = {
    "a": 9,
    "b": 11,
    "c": 0,
    "d": 2,
    "e": 4,
    "f": 5,
    "g": 7
}

PITCH_TO_NOTE = {}

for note, pitch in NOTE_TO_PITCH.items():
    PITCH_TO_NOTE[pitch] = note

ROMAN_NUMERAL_TO_PITCH = {
    "i": 0,
    "ii": 2,
    "iii": 4,
    "iv": 5,
    "v": 7,
    "vi": 9,
    "vii": 11
}

ACCIDENTAL_TO_SHIFT = {
    "b": -1,
    "#": 1
}

SCALE_DEGREE_TO_SHIFT = {
    1: 0,
    2: 2,
    3: 4,
    4: 5,
    5: 7,
    6: 9,
    7: 11
}

class Quality(Enum):
    MAJ = auto()
    MIN = auto()
    AUG = auto()
    DIM = auto()
    DOM = auto()
    FIVE = auto()

# Ordered from most to least lexicographically unique (important for searching)
TEXT_TO_QUALITY = {
    "dim":  Quality.DIM,
    "o":    Quality.DIM,
    "min":  Quality.MIN,
    "-":    Quality.MIN,
    "aug":  Quality.AUG,
    "+":    Quality.AUG,
    "5":    Quality.FIVE,
    "five": Quality.FIVE,
    "maj":  Quality.MAJ,
    "m":    Quality.MIN

}

QUALITY_TO_SHIFT = {
    Quality.MAJ:   {3:0, 5:0},
    Quality.DOM:   {3:0, 5:0},
    Quality.DIM:   {3:-1, 5:-1},
    Quality.MIN:   {3:-1, 5:0},
    Quality.AUG:   {3:0, 5:1},
    Quality.FIVE:  {3:3, 5:0},
}

CIRCLE_OF_FIFTHS = ["f", "c", "g", "d", "a", "e", "b"]