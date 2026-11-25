/**
 * Ep14 s06 - "Here's the trick. The pin keeps filling a tiny bucket of
 * charge, again and again, and counts how fast it fills."
 * GPIO 14 pours charge through its wire into a little bucket, the bucket
 * drains and fills again and again; the readout counts the fills (60).
 */
import {makeScene2D, Rect} from '@motion-canvas/2d';
import {all, createRef, easeOutBack, easeOutCubic, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {exact, Pill, popIn, until} from '../lib/ep10';
import {BucketRig, timing14} from '../lib/ep14';
import {C} from '../style';

const T = timing14('bucket');

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const rig = new BucketRig();
  const bucketPill = createRef<Rect>();
  const againPill = createRef<Rect>();
  view.add(rig.node());
  view.add(<Pill refNode={bucketPill} text={'a tiny bucket of charge'} color={C.teal} x={-430} y={250} size={32} />);
  view.add(<Pill refNode={againPill} text={'again and again'} color={C.amber} x={-400} y={-140} size={32} />);

  const h1 = new Headline('The pin fills a *bucket*', {accent: C.teal});
  view.add(h1.node());

  rig.root().opacity(0);
  rig.count(0);
  yield* all(rig.root().opacity(1, 0.35), h1.in());

  // the pin keeps filling a tiny bucket of charge
  yield* until(Math.max(useTime(), T.word('filling', 2.3) - 0.3));
  yield rig.run();
  yield* until(Math.max(useTime(), T.word('bucket', 3.5) - 0.2));
  yield* all(popIn(bucketPill(), 0.3), h1.pulse(), rig.bucket().rotation(-4, 0.12).to(4, 0.16).to(0, 0.12));

  // again and again: faster
  yield* until(Math.max(useTime(), T.word('again', 4.8) - 0.1));
  rig.fillDur(0.32);
  yield* popIn(againPill(), 0.3);

  // ... and counts how fast it fills
  yield* until(Math.max(useTime(), T.word('counts', 6.6) - 0.3));
  rig.panel().position.y(40);
  yield* all(rig.panel().opacity(1, 0.3), rig.panel().position.y(0, 0.35, easeOutCubic));
  yield* rig.count(60, Math.max(0.3, Math.min(1.2, T.word('fills', 7.6) - useTime())), easeOutCubic);
  yield* rig.number().scale(1.2, 0.12).to(1, 0.3, easeOutBack);
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
