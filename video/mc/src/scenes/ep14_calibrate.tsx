/**
 * Ep14 s10 - "So at start-up, the board measures each fruit once while
 * nobody touches it, and remembers that calm number."
 *   for (int n = 0; n < 8; n++) sum += touchRead(KEY_PIN[i]);
 *   calm[i] = sum / 8;                      (average of 8 looks, Episode 7)
 * Each fruit gets 8 quick looks, their average becomes its calm number;
 * "hands off!" while it measures.
 */
import {Circle, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, createSignal, easeOutBack, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {Fruit, glimpse14, KEYS, timing14} from '../lib/ep14';
import {C, FONT} from '../style';

const T = timing14('calibrate');
const CODE = 'for (int n = 0; n < 8; n++) sum += touchRead(KEY_PIN[i]);\ncalm[i] = sum / 8;';
const XS = [-480, 0, 480];
// 8 looks per pad; calm = sum / 8 (integer division, as on the board)
const LOOKS = [
  [61, 59, 60, 62, 58, 60, 61, 59],
  [55, 57, 56, 58, 57, 56, 55, 58],
  [63, 64, 62, 65, 63, 64, 62, 65],
];
const CALM = LOOKS.map(l => Math.floor(l.reduce((a, b) => a + b, 0) / 8));

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -300, size: 34, code: CODE});
  const fruits = KEYS.map(() => createRef<Node>());
  const readTxt = KEYS.map(() => createRef<Txt>());
  const readVal = KEYS.map(() => createSignal(''));
  const dots = KEYS.map(() => Array.from({length: 8}, () => createRef<Circle>()));
  const calmCards = KEYS.map(() => createRef<Rect>());
  const hands = createRef<Rect>();
  const avg = createRef<Rect>();

  KEYS.forEach((k, i) => {
    view.add(<Fruit kind={i} refNode={fruits[i]} x={XS[i]} y={70} scale={0.8} opacity={0} />);
    view.add(
      <Txt ref={readTxt[i]} x={XS[i]} y={-125} text={() => readVal[i]()} fontFamily={FONT.code} fontWeight={800} fontSize={54} fill={C.text} />,
    );
    dots[i].forEach((d, n) => view.add(<Circle ref={d} x={XS[i] - 105 + n * 30} y={-70} size={16} fill={'#22324f'} />));
    view.add(
      <Rect ref={calmCards[i]} x={XS[i]} y={200} layout padding={[6, 22]} radius={14} fill={'#101a2c'} stroke={C.teal} lineWidth={3} opacity={0} scale={0.5}>
        <Txt text={`calm = ${CALM[i]}`} fontFamily={FONT.code} fontWeight={800} fontSize={40} fill={C.teal} />
      </Rect>,
    );
  });
  view.add(<Pill refNode={hands} text={'hands off!'} color={C.red} x={-120} y={310} size={40} />);
  view.add(<Pill refNode={avg} text={'average of 8 looks (Episode 7)'} color={C.dim} x={300} y={310} size={30} />);
  view.add(code.node());

  const h1 = new Headline('Start-up: learn the *calm* number', {accent: C.teal});
  view.add(h1.node());

  const lineCenter = () => {
    const c = code.code();
    const box = c.getSelectionBBox(c.findFirstRange(lit('calm[i] = sum / 8;')))[0];
    return toView(view, box.center.transformAsPoint(c.localToWorld()));
  };
  const ZOOM_AT = 1.1;
  yield glimpse14(view, {from: 73, to: 78, match: 'calm[i] = sum / 8;'}, lineCenter, 34, ZOOM_AT);

  yield* h1.in();
  yield* until(ZOOM_AT + 0.3);
  yield* all(code.panel().opacity(1, 0.2), ...fruits.map(f => f().opacity(1, 0.3)));

  // the board measures each fruit once ... while nobody touches it
  yield* until(Math.max(useTime(), T.word('measures', 1.8) - 0.1));
  yield* all(
    popIn(hands(), 0.3),
    code.code().selection(code.code().findFirstRange(lit('sum += touchRead(KEY_PIN[i])')), 0.25),
  );
  const tNobody = T.word('nobody', 4.08);
  for (let i = 0; i < 3; i++) {
    yield fruits[i]().scale(0.88, 0.1).to(0.8, 0.2);
    for (let n = 0; n < 8; n++) {
      readVal[i](String(LOOKS[i][n]));
      dots[i][n]().fill(KEYS[i].color);
      yield dots[i][n]().scale(1.5, 0.05).to(1, 0.08);
      yield* waitStep(0.11);
      if (i === 1 && n === 0) yield hands().scale(1.15, 0.12).to(1, 0.25, easeOutBack);
    }
    // the average becomes its calm number
    readVal[i](String(CALM[i]));
    readTxt[i]().fill(C.teal);
    yield popIn(calmCards[i](), 0.3);
    if (i === 0) yield popIn(avg(), 0.3);
    yield* waitStep(0.12);
  }
  if (useTime() < tNobody) yield* until(tNobody - 0.1);
  yield* hands().scale(1.15, 0.12).to(1, 0.25, easeOutBack);

  // ... and remembers that calm number
  yield* until(Math.max(useTime(), T.word('remembers', 5.78) - 0.2));
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('calm[i] = sum / 8;')), 0.25),
    ...calmCards.map(c => c().scale(1.12, 0.15).to(1, 0.3, easeOutBack)),
    ...calmCards.map(c => c().fill('rgba(45,212,191,0.18)', 0.3)),
  );
  yield* until(Math.max(useTime(), T.word('calm', 6.5) - 0.1));
  yield* h1.pulse();
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));

function* waitStep(s: number) {
  yield* until(useTime() + s);
}
