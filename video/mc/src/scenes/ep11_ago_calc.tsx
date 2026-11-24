/**
 * Ep11 s24 - "Later, now minus last motion tells us how long ago it was.
 * Divide by sixty thousand, and you have minutes."
 *   now - lastMotion = 180 000 ms  ->  / 60 000  ->  3 min ago (on the OLED)
 */
import {makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  createSignal,
  delay,
  easeOutBack,
  easeOutCubic,
  linear,
  Reference,
  useTime,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Oled} from '../lib/oled';
import {burst, exact, popIn, until} from '../lib/ep10';
import {timing11} from '../lib/ep11';
import {C, FONT} from '../style';

const T = timing11('ago_calc');
const sp = (n: number) => Math.round(n).toLocaleString('en-US').replace(/,/g, ' ');

function Chip(props: {refNode: Reference<Rect>; name: string; value: () => string; color: string; x: number; y: number}) {
  return (
    <Rect
      ref={props.refNode}
      x={props.x}
      y={props.y}
      layout
      direction="column"
      alignItems="center"
      gap={4}
      padding={[12, 26]}
      radius={18}
      fill={'#101a2c'}
      stroke={props.color}
      lineWidth={4}
      opacity={0}
      scale={0.6}
    >
      <Txt text={props.name} fontFamily={FONT.code} fontWeight={700} fontSize={30} fill={props.color} />
      <Txt text={props.value} fontFamily={FONT.code} fontWeight={800} fontSize={56} fill={C.text} />
    </Rect>
  );
}

function Op(props: {refNode: Reference<Txt>; text: string; x: number; y: number; color?: string}) {
  return (
    <Txt ref={props.refNode} x={props.x} y={props.y} text={props.text} fontFamily={FONT.code} fontWeight={800} fontSize={72} fill={props.color ?? C.dim} opacity={0} />
  );
}

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const NOW = 934312;
  const LAST = 754312;
  const nowMs = createSignal(NOW - 2500);
  const result = createSignal(0);

  const cNow = createRef<Rect>();
  const cLast = createRef<Rect>();
  const cRes = createRef<Rect>();
  const cDiv = createRef<Rect>();
  const cMin = createRef<Rect>();
  const cRes2 = createRef<Rect>();
  const minus = createRef<Txt>();
  const eq1 = createRef<Txt>();
  const div = createRef<Txt>();
  const eq2 = createRef<Txt>();
  const row2 = createRef<Node>();
  const ago = createRef<Rect>();
  const oled = new Oled({x: 0, y: 270, scale: 0.46, label: 'seen 1x, last:', value: '', unit: ''});

  const Y1 = -190;
  const Y2 = 40;
  view.add(<Chip refNode={cNow} name={'now'} value={() => sp(nowMs())} color={C.amber} x={-590} y={Y1} />);
  view.add(<Op refNode={minus} text={'−'} x={-330} y={Y1} />);
  view.add(<Chip refNode={cLast} name={'lastMotion'} value={() => sp(LAST)} color={C.teal} x={-70} y={Y1} />);
  view.add(<Op refNode={eq1} text={'='} x={190} y={Y1} />);
  view.add(<Chip refNode={cRes} name={'ms ago'} value={() => sp(result())} color={C.text} x={470} y={Y1} />);
  view.add(
    <Node ref={row2}>
      <Chip refNode={cRes2} name={'ms ago'} value={() => sp(NOW - LAST)} color={C.teal} x={-560} y={Y2} />
      <Op refNode={div} text={'÷'} x={-300} y={Y2} />
      <Chip refNode={cDiv} name={'ms per minute'} value={() => '60 000'} color={C.amber} x={-30} y={Y2} />
      <Op refNode={eq2} text={'='} x={230} y={Y2} />
      <Chip refNode={cMin} name={'minutes'} value={() => '3'} color={C.teal} x={430} y={Y2} />
    </Node>,
  );
  view.add(
    <Rect ref={ago} x={470} y={Y1 + 100} layout padding={[10, 24]} radius={14} fill={'rgba(45,212,191,0.12)'} stroke={C.teal} lineWidth={3} opacity={0} scale={0.6}>
      <Txt text={'how long ago'} fontFamily={FONT.ui} fontWeight={800} fontSize={36} fill={C.teal} />
    </Rect>,
  );
  view.add(oled.node());
  oled.value().fontSize(104);
  oled.value().y(30);

  const h1 = new Headline('Now minus *then* = how long ago', {accent: C.teal});
  view.add(h1.node());

  // the "now" stopwatch keeps running until the subtraction freezes it
  const tick = nowMs(NOW, 1.8, linear);
  yield tick;
  oled.root().opacity(0);
  yield* delay(0.05, h1.in());

  // now ... minus ... last motion
  yield* until(Math.max(useTime(), T.word('now', 0.4) - 0.15));
  yield* all(cNow().opacity(1, 0.2), cNow().scale(1, 0.35, easeOutBack));
  yield* until(Math.max(useTime(), T.word('minus', 0.9) - 0.1));
  yield* all(minus().opacity(1, 0.2), minus().scale(1.3, 0.1).to(1, 0.2));
  yield* until(Math.max(useTime(), T.word('last', 1.4) - 0.1));
  yield* all(cLast().opacity(1, 0.2), cLast().scale(1, 0.35, easeOutBack));

  // = how long ago (the counter rolls up)
  yield* until(Math.max(useTime(), T.word('tells', 2.3) - 0.2));
  nowMs(NOW);
  yield* all(eq1().opacity(1, 0.2), cRes().opacity(1, 0.2), cRes().scale(1, 0.35, easeOutBack));
  yield* result(NOW - LAST, 0.9, easeOutCubic);
  yield* until(Math.max(useTime(), T.word('ago', 4.0) - 0.2));
  yield* all(popIn(ago(), 0.3), h1.pulse(), cRes().stroke(C.teal, 0.2));

  // divide by sixty thousand -> minutes
  yield* until(Math.max(useTime(), T.word('divide', 5.4) - 0.2));
  cRes2().position(cRes().position()).opacity(1).scale(1);
  yield* all(cRes2().position([-560, Y2], 0.45, easeOutCubic), ago().opacity(0, 0.2));
  yield* all(div().opacity(1, 0.2), cDiv().opacity(1, 0.2), cDiv().scale(1, 0.35, easeOutBack));
  yield* until(Math.max(useTime(), T.word('and', 7.3) - 0.1));
  yield* all(eq2().opacity(1, 0.2), cMin().opacity(1, 0.2), cMin().scale(1, 0.35, easeOutBack));

  // ... and you have minutes: the screen says "3 min ago"
  yield* until(Math.max(useTime(), Math.min(T.word('minutes', 8.6) - 0.3, T.total - 1.2)));
  oled.value().text('3 min ago');
  yield* all(oled.root().opacity(1, 0.2), oled.powerOn(), cMin().scale(1.15, 0.1).to(1, 0.3));
  yield* burst(view, oled.root().position(), [C.teal, C.amber, C.text], 170);
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));

