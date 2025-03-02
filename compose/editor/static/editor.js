function renderScore() {
    const { Renderer, Stave, StaveNote, Voice, Formatter } = Vex.Flow;

    // Create an SVG renderer and attach it to the DIV element named "output".
    const div = document.getElementById("output");
    const renderer = new Renderer(div, Renderer.Backends.SVG);

    // Configure the rendering context.
    renderer.resize(500, 500);
    const context = renderer.getContext();

    // Create a stave of width 400 at position 10, 40 on the canvas.
    const stave = new Stave(10, 40, 400);

    // Add a clef and time signature.
    stave.addClef("treble").addTimeSignature("4/4");

    // Connect it to the rendering context and draw!
    stave.setContext(context).draw();
}

// function renderScore() {
//     // Create an SVG renderer and attach it to the DIV element named "boo".
//     const { Renderer, Stave, StaveNote, Voice, Formatter } = Vex.Flow;

// // Create an SVG renderer and attach it to the DIV element named "output".
// const div = document.getElementById("output");
// const renderer = new Renderer(div, Renderer.Backends.SVG);

// // Configure the rendering context.
// renderer.resize(500, 500);
// const context = renderer.getContext();

//     system.addStave({
//         voices: [
//           score.voice(score.notes('C#5/q, B4, A4, G#4', {stem: 'up'})),
//           score.voice(score.notes('C#4/h, C#4', {stem: 'down'}))
//         ]
//       }).addClef('treble').addTimeSignature('4/4');
      
//       system.addStave({
//         voices: [
//           score.voice(score.notes('C#3/q, B2, A2/8, B2, C#3, D3', {clef: 'bass', stem: 'up'})),
//           score.voice(score.notes('C#2/h, C#2', {clef: 'bass', stem: 'down'}))
//         ]
//       }).addClef('bass').addTimeSignature('4/4');
      
//       system.addConnector();
//       vf.draw();
// }


// function renderScore() {
//     import { Renderer, Stave } from "https://unpkg.com/vexflow@4.0.0/build/esm/vexflow.js";
    
//     // Set up the canvas
//     const canvas = document.getElementById("scoreCanvas");
//     const width = 800;
//     const height = 1100;
//     canvas.width = width;
//     canvas.height = height;

//     // Create a renderer
//     const renderer = new Renderer(canvas, Renderer.Backends.CANVAS);
//     const context = renderer.getContext();
//     context.setFont("Arial", 10);

//     // Define number of staves and spacing
//     const numStaves = 5;
//     const staveSpacing = 100;
//     const marginLeft = 50;
//     let y = 50;
//     const timeSignature ='4/4'

//     // Draw multiple staves
//     let stave_treb = new Stave(marginLeft, y, width - 100).addClef('treble').addTimeSignature(timeSignature);
//     stave_treb.setContext(context).draw();
//     y += staveSpacing;

//     let stave_bass = new Stave(marginLeft, y, width - 100).addClef('bass').addTimeSignature(timeSignature);
//     stave_bass.setContext(context).draw();
//     y += staveSpacing;

        

// }