/**
 * Ep15 s24 - "The full code and the solution are in the lesson folder, linked
 * below. What would you guard with a light sensor? Tell me in the comments."
 * + 20 s silent pad: readable pages of the sketch (codeFull {pages: true}).
 * fit: true because the sketch's header comments run to ~115 characters.
 * (body: lib/codeFull.tsx, sketch: lessons/15-drawer-spy/.../drawer_spy.ino)
 */
import {makeScene2D} from '@motion-canvas/2d';
import {codeFullBody, Sketch} from '../lib/codeFull';
import {exact} from '../lib/ep10';
import {SKETCH15, timing15} from '../lib/ep15';

const T = timing15('code_full');

export default makeScene2D(
  exact(T.total, view => codeFullBody(view, T, SKETCH15 as Sketch, ['What would you guard?', '→ comments'], {pages: true, fit: true})),
);
