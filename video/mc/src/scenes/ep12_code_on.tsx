/**
 * Ep12 s11 - "And one line per link tells the board which helper answers it.
 * Server on: this link, this helper."
 *   server.on("/color", handleColor);
 *   server.on("/ring", handleRing);
 * Glimpse -> the lines; each link chip gets an arrow to its helper.
 */
import {Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, delay, easeInOutCubic, easeOutBack, easeOutCubic, linear, loop, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, toView, until} from '../lib/ep10';
import {glimpse12, timing12} from '../lib/ep12';
import {C, FONT} from '../style';

const T = timing12('code_on');
const L1 = 'server.on("/color", handleColor);';
const L2 = 'server.on("/ring", handleRing);';

function Row(props: {link: string; helper: string; color: string; y: number; refs: {row: any; link: any; helper: any; arrow: any; dot: any}}) {
  return (
    <Node ref={props.refs.row} y={props.y} opacity={0}>
      <Rect ref={props.refs.link} x={-470} layout padding={[10, 26]} radius={14} fill={'#101a2c'} stroke={props.color} lineWidth={4}>
        <Txt text={props.link} fontFamily={FONT.code} fontWeight={800} fontSize={44} fill={props.color} />
      </Rect>
      <Line ref={props.refs.arrow} points={[[-300, 0], [140, 0]]} stroke={C.dim} lineWidth={6} endArrow arrowSize={20} end={0} />
      <Rect ref={props.refs.dot} x={-300} width={22} height={22} radius={11} fill={props.color} opacity={0} />
      <Rect ref={props.refs.helper} x={400} layout direction="column" alignItems="center" padding={[12, 26]} radius={16} fill={'#15223a'} stroke={C.line} lineWidth={3}>
        <Txt text={'helper'} fontFamily={FONT.ui} fontSize={24} fill={C.dim} />
        <Txt text={props.helper} fontFamily={FONT.code} fontWeight={800} fontSize={40} fill={C.text} />
      </Rect>
    </Node>
  );
}

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -250, size: 50, code: `${L1}\n${L2}`});
  const mk = () => ({row: createRef<Node>(), link: createRef<Rect>(), helper: createRef<Rect>(), arrow: createRef<Line>(), dot: createRef<Rect>()});
  const r1 = mk();
  const r2 = mk();
  view.add(<Row link={'/color'} helper={'handleColor()'} color={C.teal} y={20} refs={r1} />);
  view.add(<Row link={'/ring'} helper={'handleRing()'} color={C.amber} y={200} refs={r2} />);
  view.add(code.node());

  const h1 = new Headline('One line per *link*', {accent: C.teal});
  view.add(h1.node());

  const line1Center = () => {
    const c = code.code();
    const box = c.getSelectionBBox(c.findFirstRange(lit(L1)))[0];
    return toView(view, box.center.transformAsPoint(c.localToWorld()));
  };
  const ZOOM_AT = 1.1;
  yield glimpse12(view, {from: 100, to: 103, match: L1}, line1Center, 50, ZOOM_AT);

  yield* delay(0.1, h1.in());
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);

  // links + helpers appear, arrows draw
  yield* until(Math.max(useTime(), T.word('helper', 2.3) - 0.5));
  for (const r of [r1, r2]) r.row().position.x(-40);
  yield* all(
    ...[r1, r2].map((r, i) => delay(i * 0.12, all(r.row().opacity(1, 0.25), r.row().position.x(0, 0.35, easeOutCubic)))),
  );
  yield* all(r1.arrow().end(1, 0.4, easeInOutCubic), delay(0.1, r2.arrow().end(1, 0.4, easeInOutCubic)), h1.pulse());

  // "Server on"
  yield* until(Math.max(useTime(), T.word('server', 3.6) - 0.15));
  yield* code.code().selection([code.code().findFirstRange(lit('server.on')), code.code().findLastRange(lit('server.on'))], 0.25);
  // "this link"
  yield* until(Math.max(useTime(), T.word('link', 4.9, undefined, 1) - 0.15));
  yield* all(
    code.code().selection([code.code().findFirstRange(lit('"/color"')), code.code().findFirstRange(lit('"/ring"'))], 0.25),
    r1.link().scale(1.12, 0.12).to(1, 0.25),
    r2.link().scale(1.12, 0.12).to(1, 0.25),
  );
  // "this helper": a dot travels each arrow, the helper lights up
  yield* until(Math.max(useTime(), T.word('helper', 5.6, undefined, 1) - 0.15));
  yield* all(
    code.code().selection([code.code().findFirstRange('handleColor'), code.code().findFirstRange('handleRing')], 0.25),
    ...[r1, r2].map(r =>
      all(
        r.dot().opacity(1, 0.1),
        r.dot().x(130, 0.45, easeInOutCubic),
        delay(0.4, all(r.helper().stroke(C.amber, 0.15), r.helper().scale(1.1, 0.12).to(1, 0.25, easeOutBack), r.dot().opacity(0, 0.1))),
      ),
    ),
  );
  // keep the requests flowing until the end
  yield loop(Infinity, function* () {
    for (const r of [r1, r2]) {
      r.dot().x(-300).opacity(1);
      yield* r.dot().x(130, 0.45, easeInOutCubic);
      r.dot().opacity(0);
    }
  });
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
