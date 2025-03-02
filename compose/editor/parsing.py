# import json
import re #For Format

def format_notes(raw_treble, raw_bass):
    """
    Parse raw treble and bass notation into formatted note lists.
    
    Args:
        raw_treble (str): Raw treble clef notation (e.g. "c4q,d4q,g4h")
        raw_bass (str): Raw bass clef notation (e.g. "(c3w,e3w,g3w)")
    
    Returns:
        tuple: (treble_note_list, bass_note_list) with properly formatted notes
    """
    result = {}
    
    # Process both clefs using the same logic
    for clef, notes_str in [("treble", raw_treble), ("bass", raw_bass)]:
        note_list = []
        
        if notes_str:
            # Check if we're dealing with a chord (notes in parentheses)
            is_chord = notes_str.startswith('(') and notes_str.endswith(')')
            
            if is_chord:
                # Remove the outer parentheses
                notes_str = notes_str[1:-1]
                
                # Extract all notes in the chord
                parts = notes_str.split(',')
                pitches = []
                duration = None
                
                for part in parts:
                    match = re.match(r'([a-g][#b]?)(\d)([a-z]+)', part)
                    if match:
                        pitch, octave, dur = match.groups()
                        pitches.append(f"{pitch}/{octave}")
                        # All notes in a chord should have the same duration
                        duration = dur
                
                if pitches and duration:
                    chord_str = f'"{", ".join(pitches)}"'
                    note_list.append((chord_str, f'"{duration}"'))
            else:
                # These are sequential notes (separated by commas)
                sequential_notes = notes_str.split(',')
                
                for note in sequential_notes:
                    match = re.match(r'([a-g][#b]?)(\d)([a-z]+)', note)
                    if match:
                        pitch, octave, duration = match.groups()
                        note_list.append((f'"{pitch}/{octave}"', f'"{duration}"'))
        
        result[f"{clef}_note_list"] = note_list
    
    return result["treble_note_list"], result["bass_note_list"]


def count_beats(note_list):
    """
    Count the total beats in a measure based on the note list.
    
    Duration mapping:
    - 'w' (whole note) = 4 beats
    - 'h' (half note) = 2 beats
    - 'q' (quarter note) = 1 beat
    - 'e' (eighth note) = 0.5 beats
    - 's' (sixteenth note) = 0.25 beats (included for completeness)
    
    Args:
        note_list (list): List of tuples containing (pitch, duration)
                          Example: [('"c/4"', '"q"'), ('"d/4"', '"q"')]
    
    Returns:
        float: Total number of beats in the measure
    """
    # Define the beat value for each duration
    beat_values = {
        'w': 4.0,    # whole note
        'h': 2.0,    # half note
        'q': 1.0,    # quarter note
        'e': 0.5,    # eighth note
        's': 0.25,   # sixteenth note
        # Add other durations as needed
    }
    
    total_beats = 0.0
    
    for _, duration in note_list:
        # Remove quotes from the duration
        clean_duration = duration.strip('"')
        
        # Handle dot notation (e.g., "q." for dotted quarter)
        if '.' in clean_duration:
            base_duration = clean_duration[0]
            # A dot increases the duration by half its value
            if base_duration in beat_values:
                base_value = beat_values[base_duration]
                total_beats += base_value * 1.5
        # Handle triplet notation (e.g., "qt" for quarter triplet)
        elif 't' in clean_duration:
            base_duration = clean_duration[0]
            # A triplet decreases the duration to 2/3 of its value
            if base_duration in beat_values:
                base_value = beat_values[base_duration]
                total_beats += base_value * (2/3)
        # Standard duration
        elif clean_duration in beat_values:
            total_beats += beat_values[clean_duration]
        else:
            print(f"Warning: Unknown duration '{clean_duration}'")
    
    return total_beats
