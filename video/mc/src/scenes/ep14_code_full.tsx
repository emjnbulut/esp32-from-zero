/**
 * Ep14 s24 - "The full code and the solution are in the lesson folder, linked
 * below. Which fruit would you use? Tell me in the comments."
 * + 20 s silent pad: readable pages of the sketch (codeFull {pages: true}).
 * fit: true because the sketch's header comments run to 120 characters.
 * (body: lib/codeFull.tsx, sketch: lessons/14-fruit-piano/.../fruit_piano.ino)
 */
import {makeScene2D} from '@motion-canvas/2d';
import {codeFullBody, Sketch} from '../lib/codeFull';
import {exact, makeTiming} from '../lib/ep10';
import data from '../timing/ep14.json';
import sketch from '../timing/ep14_sketch.json';

const T = makeTiming(data, 'ep14')('code_full');

export default makeScene2D(
  exact(T.total, view => codeFullBody(view, T, sketch as Sketch, ['Which fruit?', '→ comments'], {pages: true, fit: true})),
);
