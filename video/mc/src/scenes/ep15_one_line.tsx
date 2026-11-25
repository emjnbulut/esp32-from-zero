/**
 * Ep15 s12 - "First idea: one line. Above it, the drawer is open. Below it,
 * closed."
 * The light number drawn over time with one line at 1500: above = OPEN,
 * below = CLOSED (the badge follows the trace).
 */
import {makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {exact, popIn, until} from '../lib/ep10';
import {keyed, LightGraph, ThresholdLine, timing15} from '../lib/ep15';
import {C, FONT} from '../style';

const T = timing15('one_line');
const LINE = 1500;
const base = keyed([[0, 380], [2.0, 420], [2.75, 2700], [4.3, 2650], [5.0, 420], [9, 400]]);
const path = (t: number) => base(t) + 35 * Math.sin(t * 9) + 18 * Math.sin(t * 23);

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const g = new LightGraph({path, t0: 0, t1: T.total, hi: LINE, lo: LINE});
  const line = createRef<Node>();
  const above = createRef<Rect>();
  const below = createRef<Rect>();
  const aboveTxt = createRef<Txt>();
  const belowTxt = createRef<Txt>();
  const {X0, X1, YT, YB} = LightGraph;
  const ly = LightGraph.vy(LINE);

  view.add(<Rect ref={above} x={(X0 + X1) / 2} y={(YT + ly) / 2} width={X1 - X0} height={ly - YT} fill={'rgba(255,181,71,0.10)'} opacity={0} />);
  view.add(<Rect ref={below} x={(X0 + X1) / 2} y={(ly + YB) / 2} width={X1 - X0} height={YB - ly} fill={'rgba(45,212,191,0.08)'} opacity={0} />);
  view.add(g.node());
  view.add(<ThresholdLine refNode={line} v={LINE} text={'one line'} color={C.text} />);
  view.add(<Txt ref={aboveTxt} x={600} y={ly - 80} text={'above → open'} fontFamily={FONT.ui} fontWeight={800} fontSize={36} fill={C.amber} opacity={0} />);
  view.add(<Txt ref={belowTxt} x={600} y={ly + 80} text={'below → closed'} fontFamily={FONT.ui} fontWeight={800} fontSize={36} fill={C.teal} opacity={0} />);

  const h1 = new Headline('First idea: *one* line', {accent: C.amber});
  view.add(h1.node());

  yield g.drive();
  yield g.watch();
  yield* h1.in();

  // one line
  yield* until(Math.max(useTime(), T.word('line', 1.08) - 0.3));
  line().y(-20);
  yield* all(line().opacity(1, 0.3), line().y(0, 0.35), g.badge().opacity(1, 0.3));

  // above it, the drawer is open
  yield* until(Math.max(useTime(), T.word('above', 2.06) - 0.2));
  yield* all(above().opacity(1, 0.3), popIn(aboveTxt(), 0.3));

  // below it, closed
  yield* until(Math.max(useTime(), T.word('below', 4.4) - 0.2));
  yield* all(below().opacity(1, 0.3), popIn(belowTxt(), 0.3));
  yield grid().opacity(0.6, 1.0, linear);
  yield* until(T.total);
}));
