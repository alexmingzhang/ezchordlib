import math
from .constants import *

def text_to_pitch(text: str, key="c") -> int:
    text = text.lower()
    is_letter = text[0] in NOTE_TO_PITCH.keys()

    if is_letter:
        pitch = NOTE_TO_PITCH[text[0]]
    else:
        for rn in ROMAN_NUMERAL_TO_PITCH.keys():
            if rn in text:
                pitch = ROMAN_NUMERAL_TO_PITCH[rn] + NOTE_TO_PITCH[key]
                break

    for i in range(1 if is_letter else 0, len(text)):
        if text[i] in ACCIDENTAL_TO_SHIFT.keys():
            pitch += ACCIDENTAL_TO_SHIFT[text[i]]
    
    return pitch

def pitch_to_note(pitch: int) -> str:
    pitch = pitch % 12
    accidental = ""

    if not pitch in PITCH_TO_NOTE.keys():
        #print(pitch, "is not in keys")
        pitch = (pitch + 1) % 12
        accidental += "b"

    return PITCH_TO_NOTE[pitch].upper() + accidental

def scale_degree_to_note(scale_degree: int, key="c", shift=0) -> str:
    key = key.lower()
    index = 1
    
    if key in CIRCLE_OF_FIFTHS:
        search_direction = 1 if CIRCLE_OF_FIFTHS.index(key) > CIRCLE_OF_FIFTHS.index("c") else -1
    else:
        search_direction = 1 if "#" in key else -1
        
    accidental = ""

    while key != CIRCLE_OF_FIFTHS[index % 7] + accidental:
        #print(key, "not in", CIRCLE_OF_FIFTHS[index % 7] + accidental)
        index = index + search_direction

        if index < 0:
            accidental = "b" * (math.floor(abs(index) / 7))
        elif index > 6:
            accidental = "#" * (math.floor(index / 7))
        
    num_accidentals = index - 1

    if num_accidentals < 0:
        accidental_notes = CIRCLE_OF_FIFTHS[7 - abs(num_accidentals):7]
    else:
        accidental_notes = CIRCLE_OF_FIFTHS[:num_accidentals]
    
    note = CIRCLE_OF_FIFTHS[((scale_degree - 1) * 2 + CIRCLE_OF_FIFTHS.index(key[0])) % 7].upper()

    note_num_accidentals = shift

    if note.lower() in accidental_notes:
        note_num_accidentals += 1 if num_accidentals > 0 else -1

    if note_num_accidentals < 0:
        note += "b" * abs(note_num_accidentals)
    elif note_num_accidentals > 0:
        note += "#" * note_num_accidentals
    
    #index = ((scale_degree + 3) * 2) % 7

    #return note, accidental_notes, num_accidentals, note_num_accidentals

    return note