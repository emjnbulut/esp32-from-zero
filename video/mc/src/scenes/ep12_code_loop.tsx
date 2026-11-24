/**
 * Ep12 s12 - "The loop has one job now: like our night guard doing rounds,
 * it checks again and again whether a phone is knocking."
 *   void loop() { server.handleClient(); }
 * Glimpse -> loop(); a night guard circles past the door, faster and faster,
 * until a phone knocks.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, createSignal, delay, easeOutBack, easeOutCubic, linear, loop, useTime, Vector2} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {glimpse12, timing12} from '../lib/ep12';
import {C, FONT} from '../style';

const T = timing12('code_loop');
const CODE = 'void loop() {\n  server.handleClient();\n}';

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({x: -480, y: 0, size: 46, code: CODE});
  const CEN = new Vector2(470, 60);
  const R = 230;
  const ang = createSignal(0); // 0 = at the door (top)
  const rounds = createSignal(0);
  const yard = createRef<Node>();
  const guard = createRef<Node>();
  const door = createRef<Rect>();
  const phone = createRef<Node>();
  const knocks = [createRef<Circle>(), createRef<Circle>()];
  const alert = createRef<Txt>();
  const rTxt = createRef<Txt>();
  const jobPill = createRef<Rect>();

  const posAt = (a: number) => CEN.add(Vector2.fromDegrees(a - 90).scale(R));

  view.add(
    <Node ref={yard} opacity={0}>
      <Circle position={CEN} size={R * 2} stroke={C.line} lineWidth={6} lineDash={[18, 14]} />
      <Txt ref={rTxt} position={CEN.add([0, -10])} text={() => `${rounds()}`} fontFamily={FONT.code} fontWeight={800} fontSize={90} fill={C.text} />
      <Txt position={CEN.add([0, 60])} text={'rounds'} fontFamily={FONT.ui} fontWeight={700} fontSize={30} fill={C.dim} />
      {/* the door (port 80) at the top of the round */}
      <Rect ref={door} position={CEN.add([0, -R])} width={74} height={104} radius={[10, 10, 2, 2]} fill={'#6b4a2e'} stroke={'#8a6440'} lineWidth={4}>
        <Circle x={22} size={12} fill={C.amber} />
      </Rect>
    </Node>,
  );
  // the guard with a flashlight
  view.add(
    <Node ref={guard} position={() => posAt(ang())} opacity={0}>
      <Line
        points={[[0, 0], [150, -50], [150, 50]]}
        closed
        fill={'rgba(255,230,150,0.28)'}
        rotation={() => ang()}
      />
      <Circle size={74} fill={'#1e3a6b'} stroke={C.text} lineWidth={4} />
      <Rect y={-14} width={56} height={18} radius={6} fill={'#0f1d36'} />
      <Circle y={10} size={30} fill={'#f0c9a0'} />
    </Node>,
  );
  view.add(
    <Node ref={phone} position={CEN.add([0, -R - 130])} opacity={0}>
      {knocks.map(k => (
        <Circle ref={k} size={60} stroke={C.amber} lineWidth={5} opacity={0} />
      ))}
      <Rect width={56} height={100} radius={12} fill={'#0d1117'} stroke={C.amber} lineWidth={4} />
    </Node>,
  );
  view.add(<Txt ref={alert} position={CEN.add([90, -R - 40])} text={'!'} fontFamily={FONT.ui} fontWeight={900} fontSize={90} fill={C.amber} opacity={0} scale={0.3} />);
  view.add(<Pill refNode={jobPill} text={'its one job'} color={C.amber} x={-480} y={150} size={34} />);
  view.add(code.node());

  const h1 = new Headline('loop() = the *night* *guard*', {accent: C.teal});
  view.add(h1.node());

  const lineCenter = () => {
    const c = code.code();
    const box = c.getSelectionBBox(c.findFirstRange(lit('server.handleClient();')))[0];
    return toView(view, box.center.transformAsPoint(c.localToWorld()));
  };
  const ZOOM_AT = 1.1;
  yield glimpse12(view, {from: 106, to: 108, match: 'server.handleClient();'}, lineCenter, 46, ZOOM_AT);

  yield* delay(0.1, h1.in());
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);
  yield* until(Math.max(useTime(), T.word('job', 1.2) - 0.1));
  yield* all(code.code().selection(code.code().findFirstRange(lit('server.handleClient();')), 0.25), popIn(jobPill(), 0.3));

  // the night guard doing rounds
  yield* until(Math.max(useTime(), T.word('night', 2.9) - 0.3));
  yield* all(yard().opacity(1, 0.3), guard().opacity(1, 0.3), h1.pulse());
  const tFast = T.word('checks', 5.1) - 0.1;
  const tKnock = Math.min(T.word('phone', 6.9) - 0.3, T.total - 1.4);
  function* round(dur: number) {
    yield* ang(ang() + 360, dur, linear);
    rounds(rounds() + 1);
    yield door().scale(1.08, 0.06).to(1, 0.12);
  }
  while (useTime() + 1.1 <= tFast) yield* round(1.1);
  // ... again and again: faster and faster
  while (useTime() + 0.45 <= tKnock) yield* round(0.45);
  // a phone is knocking: the guard is at the door and notices it
  yield* all(phone().opacity(1, 0.2), phone().position.y(phone().position.y() + 20, 0.3, easeOutCubic));
  yield loop(Infinity, () =>
    all(...knocks.map((k, i) => delay(i * 0.15, all(k().size(60, 0).to(200, 0.5, easeOutCubic), k().opacity(1, 0.05).to(0, 0.45))))),
  );
  yield* all(alert().opacity(1, 0.15), alert().scale(1, 0.3, easeOutBack), door().stroke(C.amber, 0.2), rTxt().fill(C.amber, 0.2));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
