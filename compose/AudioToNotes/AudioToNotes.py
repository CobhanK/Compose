import os
import json
import librosa
import numpy as np

filename = "/mnt/c/Users/owenf/Downloads/Hot_Cross_Buns_Instrumental.wav"

# Load the audio as a waveform `y` and sampling rate `sr`
y, sr = librosa.load(filename)

# Run the default beat tracker
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo[0]))

# Convert the frame indices of beat events into timestamps
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Estimate the pitch (f0) using the pyin algorithm
f0, voiced_flag, voiced_prob = librosa.pyin(
    y, 
    fmin=librosa.note_to_hz('C2'),  # Lower bound for pitch detection
    fmax=librosa.note_to_hz('C7')   # Upper bound for pitch detection
)

# Convert frequencies to MIDI note numbers
midi_notes = librosa.hz_to_midi(f0)

# Convert MIDI numbers to note names, handling non-voiced segments (NaN values)
# and replacing the Unicode symbols for sharps and flats.
notes = [
    (librosa.midi_to_note(int(round(m)))
     .replace('\u266f', 's')  # Replace sharp (♯) with 's'
     .replace('\u266d', 'f')) # Replace flat (♭) with 'f'
    if np.isfinite(m) else None
    for m in midi_notes
]

# Separate the notes into bass and treble.
bass_notes = []
treble_notes = []

# Using MIDI threshold: below C4 (MIDI < 60) is bass, C4 and above (MIDI >= 60) is treble.
for m, note in zip(midi_notes, notes):
    if note is None:
        continue  # Skip non-voiced frames
    if m < 60:
        bass_notes.append(note)
    else:
        treble_notes.append(note)

# Create a dictionary for JSON output with two fields: bass and treble.
result = {
    "bass": bass_notes,
    "treble": treble_notes
}

# Convert the result to a JSON formatted string and print it.
result_json = json.dumps(result, indent=2)
print("Notes in JSON format:")
print(result_json)

# Determine the directory of the current script.
# Note: __file__ is defined when running a script; if running interactively (e.g. in a notebook),
# this will fall back to the current working directory.
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    script_dir = os.getcwd()

# Create the full path to the JSON file in the same directory as the script.
json_path = os.path.join(script_dir, 'notes.json')

# Write the JSON data to the file.
with open(json_path, 'w') as f:
    json.dump(result, f, indent=2)

print("JSON file created at:", json_path)
