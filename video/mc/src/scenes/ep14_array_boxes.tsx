/**
 * Ep14 s14 - "Now the notes. Three keys, three notes. Instead of three
 * separate variables, we use one row of labelled boxes, all with the same
 * name and a number: an array."
 * The Variable picture (a labelled moving box) extended: three loose boxes
 * (noteDo / noteMi / noteSol) slide into one row and get ONE name with a
 * number: NOTE[0], NOTE[1], NOTE[2].
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, delay, easeInOutCubic, easeOutBack, linear, useTime, Vector2} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {exact, Pill, popIn, until} from '../lib/ep10';
import {Box, Fruit, KEYS, NoteTag, timing14} from '../lib/ep14';
import {C, FONT} from '../style';

const T = timing14('array_boxes');
const COLS = [-250, 0, 250];
const ROW_Y = 130;
const LOOSE = [
  {p: new Vector2(-560, 90), r: -8},
  {p: new Vector2(30, 210), r: 6},
  {p: new Vector2(560, 60), r: -5},
];
const OLD = ['noteDo', 'noteMi', 'noteSol'];

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const fruits = KEYS.map(() => createRef<Node>());
  const tags = KEYS.map(() => createRef<Rect>());
  const boxes = KEYS.map((k, i) => new Box({x: LOOSE[i].p.x, y: LOOSE[i].p.y, w: 240, h: 170, label: OLD[i], value: String(k.note), opacity: 0}));
  const idx = KEYS.map(() => createRef<Node>());
  const bracket = createRef<Line>();
  const arrayPill = createRef<Rect>();
  const sepPill = createRef<Rect>();

  KEYS.forEach((k, i) => {
    view.add(<Fruit kind={i} refNode={fruits[i]} x={COLS[i] * 1.8} y={-250} scale={0.6} opacity={0} />);
    view.add(<NoteTag refNode={tags[i]} kind={i} x={COLS[i] * 1.8 + 125} y={-280} size={34} />);
  });
  boxes.forEach((b, i) => {
    view.add(b.node());
    b.root().rotation(LOOSE[i].r);
  });
  KEYS.forEach((_, i) => {
    view.add(
      <Node ref={idx[i]} x={COLS[i]} y={ROW_Y - 150} opacity={0} scale={0.5}>
        <Circle size={56} fill={C.teal} />
        <Txt text={String(i)} fontFamily={FONT.code} fontWeight={800} fontSize={36} fill={C.bg} />
      </Node>,
    );
  });
  view.add(
    <Line
      ref={bracket}
      points={[[COLS[0] - 120, ROW_Y + 105], [COLS[0] - 120, ROW_Y + 125], [COLS[2] + 120, ROW_Y + 125], [COLS[2] + 120, ROW_Y + 105]]}
      stroke={C.amber}
      lineWidth={5}
      end={0}
    />,
  );
  view.add(<Pill refNode={arrayPill} text={'an array: NOTE[3]'} color={C.amber} x={0} y={300} size={40} />);
  view.add(<Pill refNode={sepPill} text={'3 separate variables'} color={C.dim} x={0} y={-60} size={32} />);

  const h1 = new Headline('Three notes, *one* *name*');
  view.add(h1.node());

  yield* h1.in();
  // three keys ...
  yield* until(Math.max(useTime(), T.word('keys', 1.8) - 0.4));
  for (let i = 0; i < 3; i++) yield delay(i * 0.12, all(fruits[i]().opacity(1, 0.3), fruits[i]().scale(0.7, 0.15).to(0.6, 0.25)));
  // ... three notes
  yield* until(Math.max(useTime(), T.word('notes', 2.76, undefined, 1) - 0.2));
  for (let i = 0; i < 3; i++) yield delay(i * 0.12, popIn(tags[i](), 0.3));

  // instead of three separate variables
  yield* until(Math.max(useTime(), T.word('separate', 4.54) - 0.3));
  for (let i = 0; i < 3; i++) {
    const r = boxes[i].root();
    r.scale(0.5);
    yield delay(i * 0.15, all(r.opacity(1, 0.25), r.scale(1, 0.35, easeOutBack)));
  }
  yield* delay(0.3, popIn(sepPill(), 0.3));

  // we use one row of labelled boxes
  yield* until(Math.max(useTime(), T.word('row', 6.8) - 0.4));
  yield sepPill().opacity(0, 0.2);
  yield* all(
    ...boxes.map((b, i) =>
      all(b.root().position([COLS[i], ROW_Y], 0.7, easeInOutCubic), b.root().rotation(0, 0.7, easeInOutCubic)),
    ),
    ...fruits.map((f, i) => f().position.x(COLS[i], 0.7, easeInOutCubic)),
    ...tags.map((t, i) => t().position.x(COLS[i] + 120, 0.7, easeInOutCubic)),
  );

  // all with the same name ...
  yield* until(Math.max(useTime(), T.word('same', 9.6) - 0.2));
  yield* all(...boxes.map(b => b.label().text('NOTE', 0.35)), h1.pulse());
  // ... and a number
  yield* until(Math.max(useTime(), T.word('number', 10.6) - 0.3));
  yield* all(
    ...boxes.map((b, i) => b.label().text(`NOTE[${i}]`, 0.3)),
    ...idx.map((n, i) => delay(i * 0.08, popIn(n(), 0.3))),
  );

  // an array
  yield* until(Math.max(useTime(), T.word('array', 11.3) - 0.35));
  yield* all(bracket().end(1, 0.3), delay(0.1, popIn(arrayPill(), 0.3)));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
