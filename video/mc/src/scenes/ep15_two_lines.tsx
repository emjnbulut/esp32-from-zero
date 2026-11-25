/**
 * Ep15 s15 - "So we use two lines. Open above eighteen hundred, closed again
 * only below twelve hundred. In between, nothing changes."
 * Same graph with OPEN_AT 1800 / CLOSED_AT 1200 (drawer_spy.ino). The trace
 * opens above 1800, wobbles in the gap while open (stays OPEN), closes below
 * 1200, then wobbles in the gap while closed (stays CLOSED). The badge runs
 * the sketch's two ifs on the trace.
 */
import {makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, easeOutBack, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {exact, popIn, until} from '../lib/ep10';
import {CLOSED_AT, keyed, LightGraph, OPEN_AT, ThresholdLine, timing15} from '../lib/ep15';
import {C, FONT} from '../style';

const T = timing15('two_lines');
const base = keyed([
  [0, 400], [1.6, 420], [2.9, 2500], [3.6, 2480], [4.6, 1500], [5.3, 1520], [5.95, 600],
  [6.8, 620], [7.4, 1500], [12, 1500],
]);
const wobbleAmp = (t: number) => (t > 4.5 && t < 5.4 ? 120 : t > 7.3 ? 165 : 30);
const path = (t: number) => base(t) + wobbleAmp(t) * (Math.sin(t * 9) * 0.65 + Math.sin(t * 23) * 0.35 + Math.sin(t * 4.1) * 0.5);

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const g = new LightGraph({path, t0: 0, t1: T.total, hi: OPEN_AT, lo: CLOSED_AT});
  const top = createRef<Node>();
  const bottom = createRef<Node>();
  const above = createRef<Rect>();
  const below = createRef<Rect>();
  const gap = createRef<Rect>();
  const aboveTxt = createRef<Txt>();
  const belowTxt = createRef<Txt>();
  const gapTxt = createRef<Txt>();
  const {X0, X1, YT, YB} = LightGraph;
  const yHi = LightGraph.vy(OPEN_AT);
  const yLo = LightGraph.vy(CLOSED_AT);

  view.add(<Rect ref={above} x={(X0 + X1) / 2} y={(YT + yHi) / 2} width={X1 - X0} height={yHi - YT} fill={'rgba(255,181,71,0.10)'} opacity={0} />);
  view.add(<Rect ref={below} x={(X0 + X1) / 2} y={(yLo + YB) / 2} width={X1 - X0} height={YB - yLo} fill={'rgba(45,212,191,0.08)'} opacity={0} />);
  view.add(<Rect ref={gap} x={(X0 + X1) / 2} y={(yHi + yLo) / 2} width={X1 - X0} height={yLo - yHi} fill={'rgba(138,151,171,0.12)'} opacity={0} />);
  view.add(g.node());
  view.add(<ThresholdLine refNode={top} v={OPEN_AT} text={'OPEN_AT 1800'} color={C.amber} />);
  view.add(<ThresholdLine refNode={bottom} v={CLOSED_AT} text={'CLOSED_AT 1200'} color={C.teal} />);
  view.add(<Txt ref={aboveTxt} x={600} y={yHi - 70} text={'above → open'} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={C.amber} opacity={0} />);
  view.add(<Txt ref={belowTxt} x={600} y={yLo + 70} text={'below → closed'} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={C.teal} opacity={0} />);
  view.add(<Txt ref={gapTxt} x={600} y={(yHi + yLo) / 2} text={'nothing changes'} fontFamily={FONT.ui} fontWeight={800} fontSize={32} fill={C.text} opacity={0} />);

  const h1 = new Headline('Two lines: *1800* and *1200*', {accent: C.amber});
  view.add(h1.node());

  yield g.drive();
  yield g.watch();
  yield* h1.in();

  // two lines
  yield* until(Math.max(useTime(), T.word('two', 0.8) - 0.2));
  top().y(-20);
  bottom().y(20);
  yield* all(top().opacity(1, 0.3), top().y(0, 0.35), bottom().opacity(1, 0.3), bottom().y(0, 0.35), g.badge().opacity(1, 0.3));

  // open above eighteen hundred
  yield* until(Math.max(useTime(), T.word('above', 2.44) - 0.3));
  yield* all(above().opacity(1, 0.3), popIn(aboveTxt(), 0.3));

  // closed again only below twelve hundred
  yield* until(Math.max(useTime(), T.word('closed', 3.92) - 0.2));
  yield* all(below().opacity(1, 0.3), popIn(belowTxt(), 0.3));
  yield* until(Math.max(useTime(), T.word('only', 4.72) - 0.1));
  yield* belowTxt().scale(1.15, 0.12).to(1, 0.25, easeOutBack);

  // in between, nothing changes
  yield* until(Math.max(useTime(), T.word('between', 7.38) - 0.3));
  yield* all(gap().opacity(1, 0.3), popIn(gapTxt(), 0.3));
  yield* until(Math.max(useTime(), T.word('nothing', 8.28) - 0.1));
  yield* all(gapTxt().scale(1.15, 0.12).to(1, 0.25, easeOutBack), g.badge().scale(1.12, 0.12).to(1, 0.25, easeOutBack));
  yield grid().opacity(0.6, 1.0, linear);
  yield* until(T.total);
}));
