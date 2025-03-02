#editor/views.py
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
import json
import re #For Format

# Create your views here.
def editor(request):
    template = loader.get_template('editor.html')
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            trebleNotesRaw = data.get('treble', None)
            bassNotesRaw = data.get('bass', None)
            # len = data.get('beats', 4)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        treble_note_list, bass_note_list = format_notes(trebleNotesRaw, bassNotesRaw)
    else:
        treble_note_list = [('"c/4"', '"q"'), ('"d/4"', '"q"'), ('"g/4"', '"h"')]
        bass_note_list = [('"c/4", "e/4", "g/4"', '"w"')]

    context = {
            'treble_note_list' : treble_note_list,
            'bass_note_list' : bass_note_list
        }   
    return HttpResponse(template.render(context, request))
    
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