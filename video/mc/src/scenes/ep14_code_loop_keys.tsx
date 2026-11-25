/**
 * Ep14 s16 - "A tiny loop checks the three pads, one after another. The
 * first one that's touched plays its note."
 *   for (int i = 0; i < 3; i++) {
 *     if (touchRead(KEY_PIN[i]) < calm[i] - DROP) return i;
 *   }
 * Glimpse -> the loop; an "i = 0, 1, 2" pointer walks the three fruits;
 * second round a finger is on the orange: box 2 answers, SOL plays.
 */
import {Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, createSignal, delay, easeInOutCubic, easeOutBack, easeOutCubic, linear, useTime, Vector2} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {burst, CodePanel, exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {contact, Finger, Fruit, glimpse14, KEYS, NoteTag, noteFloat, timing14} from '../lib/ep14';
import {C, FONT} from '../style';

const T = timing14('code_loop_keys');
const CODE = 'for (int i = 0; i < 3; i++) {\n  if (touchRead(KEY_PIN[i]) < calm[i] - DROP) return i;\n}';
const FOR = 'for (int i = 0; i < 3; i++) {';
const XS = [-450, 0, 450];
const FY = 95;

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -265, size: 36, code: CODE});
  const fruits = KEYS.map(() => createRef<Node>());
  const marks = KEYS.map(() => createRef<Txt>());
  const chips = KEYS.map(() => createRef<Rect>());
  const pointer = createRef<Node>();
  const iVal = createSignal(0);
  const finger = createRef<Node>();
  const tag = createRef<Rect>();
  const plays = createRef<Rect>();
  const TOUCH = new Vector2(XS[2] + 66, FY + 10);

  KEYS.forEach((k, i) => {
    view.add(<Fruit kind={i} refNode={fruits[i]} x={XS[i]} y={FY} scale={0.75} />);
    view.add(<Txt ref={marks[i]} x={XS[i] - 95} y={FY - 60} text={'×'} fontFamily={FONT.ui} fontWeight={900} fontSize={70} fill={C.dim} opacity={0} />);
    view.add(
      <Rect ref={chips[i]} x={XS[i]} y={FY + 120} layout padding={[4, 16]} radius={10} fill={'#101a2c'} stroke={C.line} lineWidth={3}>
        <Txt text={`KEY_PIN[${i}] = ${k.pin}`} fontFamily={FONT.code} fontWeight={700} fontSize={28} fill={C.dim} />
      </Rect>,
    );
  });
  view.add(
    <Node ref={pointer} x={XS[0]} y={FY - 150} opacity={0}>
      <Rect y={-24} layout padding={[2, 14]} radius={10} fill={C.amber}>
        <Txt text={() => `i = ${iVal()}`} fontFamily={FONT.code} fontWeight={800} fontSize={34} fill={C.bg} />
      </Rect>
      <Line points={[[0, 2], [0, 36]]} stroke={C.amber} lineWidth={8} endArrow arrowSize={18} />
    </Node>,
  );
  view.add(<NoteTag refNode={tag} kind={2} x={XS[2]} y={FY - 150} size={40} text={'SOL'} />);
  view.add(<Pill refNode={plays} text={'NOTE[2] = 784 → buzzer'} color={C.amber} x={0} y={320} size={32} />);
  view.add(<Finger refNode={finger} x={TOUCH.x + 500} y={TOUCH.y} rotation={90} />);
  view.add(code.node());

  const h1 = new Headline('A tiny *loop* checks the pads', {accent: C.teal});
  view.add(h1.node());

  const forCenter = () => {
    const c = code.code();
    const box = c.getSelectionBBox(c.findFirstRange(lit(FOR)))[0];
    return toView(view, box.center.transformAsPoint(c.localToWorld()));
  };
  const ZOOM_AT = 1.1;
  yield glimpse14(view, {from: 51, to: 53, match: FOR}, forCenter, 36, ZOOM_AT);

  yield* h1.in();
  yield* until(ZOOM_AT + 0.3);
  yield* all(code.panel().opacity(1, 0.2), code.code().selection(code.code().findFirstRange(lit(FOR)), 0.25));

  // one check: pointer to pad i, the pad pulses, the answer shows
  function* check(i: number, touched: boolean, step: number) {
    yield* all(pointer().position.x(XS[i], Math.min(0.25, step * 0.5), easeInOutCubic), pointer().opacity(1, 0.15));
    iVal(i);
    yield fruits[i]().scale(0.85, 0.08).to(0.75, 0.15);
    const m = marks[i]();
    m.text(touched ? '✓' : '×').fill(touched ? C.teal : C.red);
    m.opacity(1).scale(0.4);
    yield* m.scale(1, 0.18, easeOutBack);
    if (!touched) yield m.opacity(0.85, 0.2).to(0, 0.3);
    yield* until(useTime() + Math.max(0, step - 0.43));
  }

  // checks the three pads, one after another
  yield* until(Math.max(useTime(), T.word('pads', 1.72) - 0.3));
  yield* code.code().selection(code.code().findFirstRange(lit('touchRead(KEY_PIN[i]) < calm[i] - DROP')), 0.2);
  const step1 = Math.max(0.45, (T.word('another', 3.3) + 0.3 - useTime()) / 3);
  for (let i = 0; i < 3; i++) yield* check(i, false, step1);
  yield pointer().opacity(0, 0.2);

  // the first one that's touched ...
  yield* until(Math.max(useTime(), T.word('first', 4.76) - 0.6));
  yield* finger().position(TOUCH, 0.35, easeOutCubic);
  yield contact(view, TOUCH.add([-40, 0]), KEYS[2].color, 200);
  pointer().position.x(XS[0]);
  iVal(0);
  for (let i = 0; i < 2; i++) yield* check(i, false, 0.4);
  yield* check(2, true, 0.3);
  yield* code.code().selection(code.code().findFirstRange(lit('return i;')), 0.2);

  // ... plays its note
  yield* until(Math.max(useTime(), T.word('plays', 5.86) - 0.15));
  yield* all(
    pointer().opacity(0, 0.15),
    popIn(tag(), 0.3),
    burst(view, new Vector2(XS[2], FY), [KEYS[2].color, C.amber, C.text], 160),
    noteFloat(view, new Vector2(XS[2] - 120, FY - 40), KEYS[2].color, -40),
    delay(0.15, popIn(plays(), 0.3)),
    h1.pulse(),
  );
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
