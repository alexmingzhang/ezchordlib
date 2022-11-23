# SPECIAL CASES
# todo:
# V/V in the five of the five chord in relative key, not the five chord over the relative fifth

from typing import List
from .constants import *

# Get string's digits and return it as int
def get_number(text: str) -> int:
    num_text = ""

    for char in text:
        if char.isdigit():
            num_text += char
    
    if num_text != "":
        return int(num_text)

    return None


def split(text: str) -> List[str]: 
    text += " "
    last_break = 0
    result = []

    # Find root
    note_found = False
    for i in range(1, len(text)):
        curr_char = text[i].lower()
        prev_char = text[i-1].lower()

        #print(i, curr_char, prev_char)

        if (not note_found) and (prev_char in NOTES+ROMAN_NUMERAL_LETTERS+ACCIDENTALS and not curr_char in ROMAN_NUMERAL_LETTERS+ACCIDENTALS):
            #print("FOUND NOTE!", text[last_break:i])
            note_found = True
        
        if note_found and (curr_char not in ACCIDENTALS):
            result.append(text[last_break:i])
            last_break = i
            break
        
    # Find quality, extensions, etc.
    if last_break + 1 < len(text):
        for i in range(last_break + 1, len(text)):
            curr_char = text[i].lower()
            prev_char = text[i-1].lower()
            
            if (
                (i == len(text) - 1)
                or (curr_char in ("/", "("))
                or (curr_char.isdigit() != prev_char.isdigit())
            ):
                result.append(int(text[last_break:i]) if prev_char.isdigit() else text[last_break:i])
                #result.append(text[last_break:i])
                last_break = i
    
    return result


def parse(chord: str, key="c"):
    root = None
    quality = Quality.MAJ
    quality_found = False
    quality_section_index = 0
    bass_note = None
    extensions = {}

    chord_split = split(chord)

    for i in range(len(chord_split)):
        curr_section = chord_split[i]
        prev_section = chord_split[i-1]

        if i == 0:
            root = curr_section
        elif type(curr_section) is int:
            prev_section_is_quality = i - 1 == quality_section_index

            if prev_section == root:
                quality = Quality.DOM
                quality_found = True
            
            if not prev_section_is_quality or curr_section % 2 == 0:
                if prev_section.lower() in ("no", "omit"):
                    shift = None
                else:
                    shift = 0
                    
                    if not prev_section_is_quality:
                        for char in prev_section:
                            if char in ACCIDENTALS:
                                shift += ACCIDENTAL_TO_SHIFT[char]
                    
                    if shift == 0 and curr_section == 7:
                        if "maj" in prev_section:
                            shift = 0
                        elif "dim" in prev_section:
                            shift = -2
                        else:
                            shift = -1
                        
                extensions[curr_section] = shift
            else:
                for i in range(7,curr_section+1):
                    if i == 7:
                        if "maj" in prev_section:
                            extensions[7] = 0
                        elif "dim" in prev_section:
                            extensions[7] = -2
                        else:
                            extensions[7] = -1
                    elif i % 2 != 0:
                        extensions[i] = 0
        elif curr_section[0] == "/":
            stuff_after_slash = curr_section[1:]
            
            if get_number(stuff_after_slash) != None:
                shift = 0

                for char in stuff_after_slash:
                    if char in ACCIDENTALS:
                        shift += ACCIDENTAL_TO_SHIFT[char]
                
                extensions[get_number(stuff_after_slash)] = shift
            else:
                bass_note = stuff_after_slash 
        elif curr_section == "sus":
            extensions[3] = None

            if i == len(chord_split) - 1 or chord_split[i+1] != 2:
                extensions[4] = 0

        elif not quality_found:
            for qual_text in TEXT_TO_QUALITY.keys():
                if qual_text.lower() == curr_section[0:len(qual_text)].lower():
                    quality = TEXT_TO_QUALITY[qual_text]
                    quality_found = True
                    quality_section_index = i
                    break
    
    return root, quality, bass_note, extensions