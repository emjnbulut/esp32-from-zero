/**
 * Ep14 s15 - "Box zero holds do, box one holds mi, box two holds sol. The
 * pins get their own row, in the same order."
 *   const int KEY_PIN[3] = {14, 2, 15};
 *   const int NOTE[3] = {523, 659, 784};
 * Glimpse -> the two lines; the NOTE row of boxes lights box by box, then
 * the KEY_PIN row slides in under it and each column = one fruit.
 */
import {Circle, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, delay, easeOutBack, easeOutCubic, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {Box, Fruit, glimpse14, KEYS, NoteTag, timing14} from '../lib/ep14';
import {C, FONT} from '../style';

const T = timing14('code_array');
const CODE = 'const int KEY_PIN[3] = {14, 2, 15};\nconst int NOTE[3] = {523, 659, 784};';
const COLS = [-110, 150, 410];
const NOTE_Y = -45;
const PIN_Y = 145;
const BW = 220;
const BH = 140;

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -295, size: 40, code: CODE});
  const notes = KEYS.map((k, i) => new Box({x: COLS[i], y: NOTE_Y, w: BW, h: BH, label: `NOTE[${i}]`, value: String(k.note), labelSize: 24, valueSize: 50}));
  const pins = KEYS.map((k, i) => new Box({x: COLS[i], y: PIN_Y, w: BW, h: BH, label: `KEY_PIN[${i}]`, value: String(k.pin), labelSize: 24, valueSize: 50, opacity: 0}));
  const tags = KEYS.map(() => createRef<Rect>());
  const fruits = KEYS.map(() => createRef<Node>());
  const bands = KEYS.map(() => createRef<Rect>());
  const idx = KEYS.map(() => createRef<Node>());
  const rowNote = createRef<Txt>();
  const rowPin = createRef<Txt>();
  const order = createRef<Rect>();

  // column bands (behind the boxes): one column = one key
  KEYS.forEach((k, i) => {
    view.add(
      <Rect ref={bands[i]} x={COLS[i]} y={85} width={BW + 36} height={550} radius={18} fill={'rgba(255,255,255,0.05)'} stroke={k.color} lineWidth={3} opacity={0} />,
    );
  });
  view.add(<Txt ref={rowNote} x={-420} y={NOTE_Y} offsetX={1} text={'NOTE'} fontFamily={FONT.code} fontWeight={800} fontSize={40} fill={C.text} />);
  view.add(<Txt ref={rowPin} x={-420} y={PIN_Y} offsetX={1} text={'KEY_PIN'} fontFamily={FONT.code} fontWeight={800} fontSize={40} fill={C.text} opacity={0} />);
  KEYS.forEach((_, i) => {
    view.add(
      <Node ref={idx[i]} x={COLS[i]} y={NOTE_Y - 125}>
        <Circle size={48} fill={C.teal} />
        <Txt text={String(i)} fontFamily={FONT.code} fontWeight={800} fontSize={32} fill={C.bg} />
      </Node>,
    );
  });
  notes.forEach(b => view.add(b.node()));
  pins.forEach(b => view.add(b.node()));
  KEYS.forEach((k, i) => {
    view.add(<NoteTag refNode={tags[i]} kind={i} x={COLS[i] + BW / 2 - 14} y={NOTE_Y - BH / 2 + 8} size={32} />);
    view.add(<Fruit kind={i} refNode={fruits[i]} x={COLS[i]} y={318} scale={0.42} opacity={0} />);
  });
  view.add(<Pill refNode={order} text={'same box number = same key'} color={C.teal} x={-560} y={318} size={30} />);
  view.add(code.node());

  const h1 = new Headline('Numbered boxes: *0* *1* *2*', {accent: C.teal});
  view.add(h1.node());

  const lineCenter = () => {
    const c = code.code();
    const box = c.getSelectionBBox(c.findFirstRange(lit('const int NOTE[3] = {523, 659, 784};')))[0];
    return toView(view, box.center.transformAsPoint(c.localToWorld()));
  };
  const ZOOM_AT = 1.1;
  yield glimpse14(view, {from: 22, to: 23, match: 'const int NOTE[3] = {523, 659, 784};'}, lineCenter, 40, ZOOM_AT);

  yield* h1.in();
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);

  // box zero holds do, box one holds mi, box two holds sol
  const words = [
    {box: 'zero', note: 'do', at: [0.3, 1.5], val: '523'},
    {box: 'one', note: 'mi', at: [3.0, 4.1], val: '659'},
    {box: 'two', note: 'sol', at: [5.4, 5.9], val: '784'},
  ];
  for (let i = 0; i < 3; i++) {
    const w = words[i];
    yield* until(Math.max(useTime(), T.word(w.box, w.at[0]) - 0.25));
    yield* all(
      notes[i].root().position.y(NOTE_Y - 14, 0.2, easeOutCubic),
      notes[i].body().stroke(KEYS[i].color, 0.2),
      notes[i].body().lineWidth(7, 0.2),
      idx[i]().scale(1.25, 0.12).to(1, 0.25, easeOutBack),
      code.code().selection(code.code().findFirstRange(lit(w.val)), 0.25),
      ...(i > 0 ? [notes[i - 1].root().position.y(NOTE_Y, 0.2)] : []),
    );
    yield* until(Math.max(useTime(), T.word(w.note, w.at[1]) - 0.2));
    yield* popIn(tags[i](), 0.3);
  }
  yield notes[2].root().position.y(NOTE_Y, 0.25);

  // the pins get their own row ...
  yield* until(Math.max(useTime(), T.word('pins', 7.04) - 0.2));
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('{14, 2, 15}')), 0.25),
    rowPin().opacity(1, 0.3),
    ...pins.map((b, i) => {
      b.root().position.y(PIN_Y + 60);
      return delay(i * 0.1, all(b.root().opacity(1, 0.25), b.root().position.y(PIN_Y, 0.35, easeOutBack)));
    }),
  );

  // ... in the same order: one column = one fruit
  yield* until(Math.max(useTime(), T.word('same', 9.42) - 0.4));
  yield* all(
    code.code().selection([...code.code().findAllRanges(lit('{14, 2, 15}')), ...code.code().findAllRanges(lit('{523, 659, 784}'))], 0.25),
    ...bands.map((b, i) => delay(i * 0.1, b().opacity(1, 0.3))),
    ...fruits.map((f, i) => delay(i * 0.1, all(f().opacity(1, 0.25), f().scale(0.5, 0.15).to(0.42, 0.25)))),
    delay(0.2, popIn(order(), 0.3)),
    h1.pulse(),
  );
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
