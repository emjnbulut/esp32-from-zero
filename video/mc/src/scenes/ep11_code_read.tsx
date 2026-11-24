/**
 * Ep11 s16 - reading the PIR is one line:
 *   bool motion = digitalRead(PIR_PIN) == HIGH;
 * Full-code glimpse first; then the sensor answers with a thumb:
 * up = HIGH = motion, down = LOW = nothing.
 */
import {Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, DEFAULT, delay, easeOutBack, linear, loop, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {glimpse11, Pir, Thumb, timing11, walk, Walker} from '../lib/ep11';
import {C, FONT} from '../style';

const T = timing11('code_read');

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -250, size: 54, code: 'bool motion = digitalRead(PIR_PIN) == HIGH;'});
  const pir = createRef<Node>();
  const walker = createRef<Node>();
  const wire = createRef<Line>();
  const thumb = new Thumb({x: 330, y: 90, scale: 1.1, up: false});
  const answer = createRef<Txt>();
  const pinTag = createRef<Rect>();

  view.add(
    <Line ref={wire} points={[[-330, 90], [180, 90]]} stroke={'#a061ff'} lineWidth={10} lineCap={'round'} lineDash={[24, 16]} opacity={0} />,
  );
  view.add(<Pir refNode={pir} x={-480} y={90} scale={0.9} />);
  view.add(<Walker refNode={walker} x={-1100} y={60} scale={0.9} />);
  view.add(thumb.node());
  view.add(
    <Txt ref={answer} x={600} y={90} offsetX={-1} text={'LOW'} fontFamily={FONT.code} fontWeight={800} fontSize={64} fill={'#6b7a90'} opacity={0} />,
  );
  view.add(<Pill refNode={pinTag} text={'pin 33'} color={C.amber} x={-480} y={-60} size={34} />);
  view.add(code.node());

  const h1 = new Headline('One line reads the *sensor*', {accent: C.teal});
  view.add(h1.node());

  // full-code glimpse -> the read line
  const ZOOM_AT = 1.1;
  yield glimpse11(view, {from: 87, to: 87, match: 'bool motion = digitalRead(PIR_PIN) == HIGH;'},
    () => toView(view, code.code().absolutePosition()), 54, ZOOM_AT);

  pir().scale(0.5).opacity(0);
  yield* all(pir().scale(0.9, 0.4, easeOutBack), pir().opacity(1, 0.3), delay(0.1, h1.in()));
  yield* until(ZOOM_AT + 0.3);
  yield* all(
    code.panel().opacity(1, 0.2),
    wire().opacity(1, 0.3),
    thumb.root().opacity(0).opacity(1, 0.3),
    answer().opacity(1, 0.3),
  );
  // the dashes flow towards the thumb: the answer travels along the wire
  yield loop(Infinity, () => wire().lineDashOffset(-40, 0.5, linear).to(0, 0));

  // digital read ...
  yield* until(Math.max(useTime(), T.word('digital', 2.3) - 0.2));
  yield* code.code().selection(code.code().findFirstRange('digitalRead'), 0.25);
  // ... on pin 33
  yield* until(Math.max(useTime(), T.word('pin', 3.6) - 0.2));
  yield* all(code.code().selection(code.code().findFirstRange('PIR_PIN'), 0.25), popIn(pinTag(), 0.3));

  // HIGH means motion: someone warm walks past -> thumb up
  yield* until(Math.max(useTime(), T.word('high', 4.5) - 1.3));
  yield walk(walker(), -1100, -700, 1.2);
  yield* until(Math.max(useTime(), T.word('high', 4.5) - 0.15));
  answer().text('HIGH');
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('== HIGH')), 0.25),
    thumb.set(true),
    answer().fill(C.teal, 0.2),
    answer().scale(1.25, 0.12).to(1, 0.25),
    h1.pulse(),
  );
  yield* until(Math.max(useTime(), T.word('motion', T.total - 1.2, 's16', 0) + 0.2));
  // the walker leaves, the thumb drops again: LOW = nothing
  const tLeave = Math.min(T.total - 1.0, useTime() + 0.4);
  yield* until(tLeave);
  yield all(walk(walker(), walker().position.x(), -1100, 1.0), code.code().selection(DEFAULT, 0.4));
  yield* until(Math.max(useTime(), T.total - 0.7));
  answer().text('LOW');
  yield* all(thumb.set(false, 0.25), answer().fill('#6b7a90', 0.2));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
