/**
 * Ep11 s35 - "The full code and the solution are in the lesson folder, linked
 * below. What would you guard with it? Tell me in the comments."
 * (body: lib/codeFull.tsx, sketch: lessons/11-motion-alarm/.../motion_alarm.ino)
 */
import {makeScene2D} from '@motion-canvas/2d';
import {codeFullBody, Sketch} from '../lib/codeFull';
import {exact, makeTiming} from '../lib/ep10';
import data from '../timing/ep11.json';
import sketch from '../timing/ep11_sketch.json';

const T = makeTiming(data, 'ep11')('code_full');

export default makeScene2D(
  exact(T.total, view => codeFullBody(view, T, sketch as Sketch, ['What would you guard?', '→ comments'])),
);
