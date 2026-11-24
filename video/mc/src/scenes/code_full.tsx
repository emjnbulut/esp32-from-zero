/**
 * Ep10 s39 - "The full code and the solution are in the lesson folder, linked
 * below. Post your best time in the comments."  (body: lib/codeFull.tsx)
 */
import {makeScene2D} from '@motion-canvas/2d';
import {codeFullBody, Sketch} from '../lib/codeFull';
import {exact, timing} from '../lib/ep10';
import sketch from '../timing/ep10_sketch.json';

const T = timing('code_full');

export default makeScene2D(
  exact(T.total, view => codeFullBody(view, T, sketch as Sketch, ['Your best time?', '→ comments'])),
);
