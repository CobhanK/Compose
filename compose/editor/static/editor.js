// import { Renderer, Stave, StaveNote, Voice, Formatter } from "https://unpkg.com/vexflow@4.0.0/build/esm/vexflow.js";

function drawGrandStaff(notesTreble = [], notesBass = []) {
    const { Renderer, Stave, StaveNote, Voice, Formatter } = Vex.Flow;
    // Create a canvas dynamically
    const container = document.getElementById("music-container");
    container.innerHTML = ""; // Clear previous content

    const canvas = document.createElement("canvas");
    container.appendChild(canvas);
    
    const width = 800;
    const height = 300;
    canvas.width = width;
    canvas.height = height;

    // Set up the renderer
    const renderer = new Renderer(canvas, Renderer.Backends.CANVAS);
    const context = renderer.getContext();
    context.setFont("Arial", 10);

    // Stave settings
    const marginLeft = 50;
    const staveWidth = width - 100;

    // Treble Clef Stave
    const stave_treble = new Stave(marginLeft, 40, staveWidth);
    stave_treble.addClef("treble").addTimeSignature("4/4");
    stave_treble.setContext(context).draw();

    // Bass Clef Stave
    const stave_bass = new Stave(marginLeft, 140, staveWidth);
    stave_bass.addClef("bass").addTimeSignature("4/4");
    stave_bass.setContext(context).draw();

    //Draw Treble Notes
    // Create a voice in 4/4 and add above notes
    const voice_treble = new Voice({ num_beats: 4, beat_value: 4 });
    voice_treble.addTickables(notesTreble);

    // Format and justify the notes to 400 pixels.
    new Formatter().joinVoices([voice_treble]).format([voice_treble], 350);

    // Render voice
    voice_treble.draw(context, stave_treble);
    
        //Draw Treble Notes
    // Create a voice in 4/4 and add above notes
    const voice_bass = new Voice({ num_beats: 4, beat_value: 4 });
    voice_bass.addTickables(notesBass);

    // Format and justify the notes to 400 pixels.
    new Formatter().joinVoices([voice_bass]).format([voice_bass], 350);

    // Render voice
    voice_bass.draw(context, stave_bass);
}
    // // Convert notes into VexFlow format
    // const formatNotes = (notes) => notes.map(n => {
    //     const [keys, duration] = n.split("/");
    //     return new StaveNote({ keys: [keys], duration });
    // });

    // const trebleNotes = formatNotes(notesTreble);
    // const bassNotes = formatNotes(notesBass);

    // // Create voices for both staves
    // const createVoice = (notes) => {
    //     const voice = new Voice({ num_beats: 4, beat_value: 4 });
    //     voice.addTickables(notes);
    //     return voice;
    // };

    // const voiceTreble = createVoice(trebleNotes);
    // const voiceBass = createVoice(bassNotes);

    // // Format and join the notes on the same line
    // new Formatter().joinVoices([voiceTreble]).format([voiceTreble], staveWidth - 50);
    // new Formatter().joinVoices([voiceBass]).format([voiceBass], staveWidth - 50);

    // // Render the notes
    // voiceTreble.draw(context, stave_treble);
    // voiceBass.draw(context, stave_bass);
// }