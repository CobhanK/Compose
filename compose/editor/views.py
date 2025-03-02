#editor/views.py
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from . import parsing
from . import notes
import json
# import re #For Format

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
        
        treble_note_list, bass_note_list = parsing.format_notes(trebleNotesRaw, bassNotesRaw)
        treble_counts = parsing.count_beats(treble_note_list)
        bass_counts = parsing.count_beats(bass_counts)
    
    else:
        treble_note_list = [('"c#/4"', '"q"'), ('"db/4"', '"q"'), ('"g/4"', '"h"')]
        bass_note_list = [('"c/4", "e/4", "g/4"', '"w"')]
        treble_counts = 4
        bass_counts = 4

    if treble_counts != bass_counts:
        counts = notes.equalize_counts(treble_note_list, bass_note_list, treble_counts, bass_counts)
    else:
        counts = treble_counts

    context = {
            'treble_note_list' : treble_note_list,
            'bass_note_list' : bass_note_list
        }   
    return HttpResponse(template.render(context, request))

    #     treble_note_list = [
    #     ("c/4", "q"),  # Example: (note, duration)
    #     ("d/4", "h"),
    # ]
    
    # bass_note_list = [
    #     ("f/3", "q"),
    #     ("g/3", "h"),
    # ]

    # context = {
    #     "treble_note_list": json.dumps(treble_note_list),  # Convert to JSON string
    #     "bass_note_list": json.dumps(bass_note_list),
    # }
    
    # return render(request, "editor.html", context)