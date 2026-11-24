/**
 * Ep12 s24 - "The full code and the solution are in the lesson folder, linked
 * below. What would you control with your phone? Tell me in the comments."
 * (body: lib/codeFull.tsx, sketch: lessons/12-phone-control/.../phone_remote.ino)
 */
import {makeScene2D} from '@motion-canvas/2d';
import {codeFullBody, Sketch} from '../lib/codeFull';
import {exact, makeTiming} from '../lib/ep10';
import data from '../timing/ep12.json';
import sketch from '../timing/ep12_sketch.json';

const T = makeTiming(data, 'ep12')('code_full');

export default makeScene2D(
  exact(T.total, view => codeFullBody(view, T, sketch as Sketch, ['What would you control?', '→ comments'], {pages: true})),
);
