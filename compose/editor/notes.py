# from . import parsing

def equalize_counts(treble_note_list, bass_note_list, treble_counts, bass_counts):
    """
    Equalizes the beat counts between treble and bass staves by adding rests as needed
    in VexFlow format.
    
    Args:
        treble_note_list (list): List of tuples containing treble notes (pitch, duration)
        bass_note_list (list): List of tuples containing bass notes (pitch, duration)
        treble_counts (float): Total beats in treble staff
        bass_counts (float): Total beats in bass staff
    
    Returns:
        tuple: (updated_treble_list, updated_bass_list) with equalized beat counts
    """
    # Create copies to avoid modifying the originals
    # updated_treble = treble_note_list.copy()
    # updated_bass = bass_note_list.copy()
    
    # Calculate the difference in counts
    count_difference = abs(treble_counts - bass_counts)
    
    # If counts are already equal, return the lists as is
    if count_difference < 0.001:  # Use small epsilon for float comparison
        return treble_note_list, bass_note_list
    
    # Define the rest values to use based on the difference
    rest_values = [
        (4.0, 'w'),   # whole rest
        (2.0, 'h'),   # half rest
        (1.0, 'q'),   # quarter rest
        (0.5, 'e'),   # eighth rest
        (0.25, 's')   # sixteenth rest
    ]
    
    # Determine which staff needs to be padded with rests
    if treble_counts < bass_counts:
        staff_to_pad = "treble"
        remaining_beats = count_difference
    else:
        staff_to_pad = "bass"
        remaining_beats = count_difference
    
    # Generate the necessary rests in VexFlow format
    rests_to_add = []
    for beat_value, duration in rest_values:
        while remaining_beats >= beat_value - 0.001:  # Use epsilon for float comparison
            # In VexFlow, rests are represented as "b/4" for treble clef and "d/3" for bass clef
            if staff_to_pad == "treble":
                rest_pitch = '"b/4"'  # Standard treble clef rest position
            else:
                rest_pitch = '"d/3"'  # Standard bass clef rest position
                
            # Add the rest with a "r" suffix in the duration to indicate it's a rest
            rests_to_add.append((rest_pitch, f'"{duration}r"'))
            remaining_beats -= beat_value
    
    # Add the rests to the appropriate staff
    if staff_to_pad == "treble":
        treble_note_list.extend(rests_to_add)
    else:
        bass_note_list.extend(rests_to_add)
    
    return max(treble_counts, bass_counts)