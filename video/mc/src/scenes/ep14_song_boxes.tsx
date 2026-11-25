/**
 * Ep14 s18 - "Every note you play goes into the next box of another array:
 * the song, eight boxes long."
 *   int song[8];          (song[songLength] = key; songLength++;)
 * Eight empty boxes song[0..7]; the played notes (do mi sol sol mi do mi sol,
 * the tune of s19) drop into the next box one by one, a "next" pointer
 * (songLength) walks along.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, createSignal, easeInCubic, easeInOutCubic, easeOutBack, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {Box, glimpse14, KEYS, timing14} from '../lib/ep14';
import {C, FONT} from '../style';

const T = timing14('song_boxes');
const LINE = 'int song[8];';
const TUNE = [0, 1, 2, 2, 1, 0, 1, 2];
const BW = 170;
const STEP = 190;
const X = (i: number) => -STEP * 3.5 + i * STEP;
const ROW_Y = 120;

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -300, size: 50, code: LINE});
  const boxes = TUNE.map((_, i) => new Box({x: X(i), y: ROW_Y, w: BW, h: 140, label: `song[${i}]`, value: '', labelSize: 22, valueSize: 44, opacity: 0}));
  const balls = TUNE.map(() => createRef<Node>());
  const pointer = createRef<Node>();
  const nextVal = createSignal(0);
  const bracket = createRef<Line>();
  const eight = createRef<Rect>();
  const another = createRef<Rect>();

  boxes.forEach(b => view.add(b.node()));
  view.add(
    <Node ref={pointer} x={X(0)} y={ROW_Y - 150} opacity={0}>
      <Rect y={-26} layout padding={[2, 12]} radius={10} fill={C.teal}>
        <Txt text={() => `next: ${nextVal()}`} fontFamily={FONT.code} fontWeight={800} fontSize={26} fill={C.bg} />
      </Rect>
      <Line points={[[0, -2], [0, 30]]} stroke={C.teal} lineWidth={7} endArrow arrowSize={16} />
    </Node>,
  );
  TUNE.forEach((k, i) => {
    view.add(
      <Node ref={balls[i]} x={X(i)} y={-160} opacity={0}>
        <Circle size={96} fill={KEYS[k].color} shadowColor={'rgba(0,0,0,0.4)'} shadowBlur={14} />
        <Txt text={KEYS[k].tag} fontFamily={FONT.ui} fontWeight={900} fontSize={36} fill={C.bg} />
      </Node>,
    );
  });
  view.add(
    <Line
      ref={bracket}
      points={[[X(0) - BW / 2, ROW_Y + 95], [X(0) - BW / 2, ROW_Y + 115], [X(7) + BW / 2, ROW_Y + 115], [X(7) + BW / 2, ROW_Y + 95]]}
      stroke={C.amber}
      lineWidth={5}
      end={0}
    />,
  );
  view.add(<Pill refNode={eight} text={'8 boxes: song[0] … song[7]'} color={C.amber} x={0} y={300} size={36} />);
  view.add(<Pill refNode={another} text={'another array'} color={C.teal} x={520} y={-300} size={32} />);
  view.add(code.node());

  const h1 = new Headline('Another array: the *song*', {accent: C.teal});
  view.add(h1.node());

  const ZOOM_AT = 1.1;
  yield glimpse14(view, {from: 29, to: 29, match: LINE}, () => toView(view, code.code().absolutePosition()), 50, ZOOM_AT);

  yield* h1.in();
  yield* until(ZOOM_AT + 0.3);
  yield* all(code.panel().opacity(1, 0.2), ...boxes.map((b, i) => b.root().opacity(1, 0.3)), pointer().opacity(1, 0.3));

  // each played note drops into the next box
  const tEnd = T.total - 0.9;
  const step = Math.max(0.5, (tEnd - useTime()) / TUNE.length);
  const tAnother = T.word('another', 2.7) - 0.2;
  const tEight = T.word('eight', 5.16) - 0.2;
  let shownAnother = false;
  let shownEight = false;
  for (let i = 0; i < TUNE.length; i++) {
    const t0 = useTime();
    const ball = balls[i]();
    const box = boxes[i];
    ball.opacity(1).scale(0.3);
    yield* ball.scale(1, 0.15, easeOutBack);
    yield* all(ball.position.y(ROW_Y + 10, 0.28, easeInCubic), ball.scale(0.7, 0.28));
    ball.opacity(0);
    box.value().text(KEYS[TUNE[i]].name).fill('#2a1a0a');
    box.body().fill(KEYS[TUNE[i]].color);
    yield box.root().scale([1.08, 0.92], 0.07).to(1, 0.2, easeOutBack);
    nextVal(i + 1);
    if (i < TUNE.length - 1) yield pointer().position.x(X(i + 1), 0.2, easeInOutCubic);
    else yield pointer().opacity(0, 0.2);
    if (!shownAnother && useTime() >= tAnother) {
      shownAnother = true;
      yield all(popIn(another(), 0.3), code.code().selection(code.code().findFirstRange(lit('song')), 0.25));
    }
    if (!shownEight && useTime() >= tEight) {
      shownEight = true;
      yield all(bracket().end(1, 0.3), popIn(eight(), 0.3), code.code().selection(code.code().findFirstRange(lit('[8]')), 0.25), h1.pulse());
    }
    yield* until(t0 + step);
  }
  if (!shownEight) yield* all(bracket().end(1, 0.3), popIn(eight(), 0.3));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
