/**
 * Ep14 s07 - "When your finger touches the wire, your body makes the bucket
 * bigger. It fills slower, and the number drops."
 * Same rig as ep14_bucket: a finger lands on the wire, the bucket grows,
 * each fill takes longer and the readout falls 60 -> 25.
 */
import {Line, makeScene2D, Node, Rect} from '@motion-canvas/2d';
import {all, createRef, easeInOutCubic, easeOutBack, easeOutCubic, linear, useTime, Vector2} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {exact, Pill, popIn, until} from '../lib/ep10';
import {BucketRig, contact, Finger, timing14} from '../lib/ep14';
import {C} from '../style';

const T = timing14('bucket_finger');

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const rig = new BucketRig();
  const finger = createRef<Node>();
  const bodyPill = createRef<Rect>();
  const slowPill = createRef<Rect>();
  const arrow = createRef<Line>();
  const TOUCH = new Vector2(-520, BucketRig.PIN.y - 6);

  view.add(rig.node());
  view.add(<Finger refNode={finger} x={TOUCH.x} y={TOUCH.y - 360} rotation={-12} />);
  view.add(<Pill refNode={bodyPill} text={'+ your body'} color={C.amber} x={-480} y={-120} size={34} />);
  view.add(<Pill refNode={slowPill} text={'fills slower'} color={C.amber} x={-430} y={250} size={32} />);
  view.add(
    <Line
      ref={arrow}
      points={[[745, -60], [745, 90]]}
      stroke={C.red}
      lineWidth={12}
      lineCap={'round'}
      endArrow
      arrowSize={30}
      opacity={0}
    />,
  );

  const h1 = new Headline('Finger = *bigger* bucket');
  view.add(h1.node());

  // start where ep14_bucket ended: filling fast, readout 60
  rig.fillDur(0.32);
  rig.panel().opacity(1);
  yield rig.run();
  yield* h1.in();

  // your finger touches the wire
  yield* until(Math.max(useTime(), T.word('touches', 0.66) - 0.45));
  yield* finger().position(TOUCH, 0.45, easeOutCubic);
  yield contact(view, TOUCH, C.amber, 180);
  yield* rig.wire().stroke(C.amber, 0.2);

  // your body makes the bucket bigger
  yield* until(Math.max(useTime(), T.word('body', 2.26) - 0.2));
  yield* popIn(bodyPill(), 0.3);
  yield* until(Math.max(useTime(), T.word('bigger', 3.3) - 0.35));
  yield* all(rig.size(1.6, 0.7, easeInOutCubic), h1.pulse());

  // it fills slower
  yield* until(Math.max(useTime(), T.word('fills', 4.76) - 0.2));
  rig.fillDur(1.3);
  yield* popIn(slowPill(), 0.3);

  // ... and the number drops
  yield* until(Math.max(useTime(), T.word('number', 6.4) - 0.2));
  yield* all(
    rig.count(25, 0.8, easeOutCubic),
    rig.number().fill(C.red, 0.3),
    arrow().opacity(1, 0.25),
    arrow().position.y(30, 0.5, easeOutBack),
  );
  yield* rig.number().scale(1.15, 0.12).to(1, 0.3, easeOutBack);
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
