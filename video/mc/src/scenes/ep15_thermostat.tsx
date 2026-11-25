/**
 * Ep15 s14 - "A thermostat has the same problem, and solves it by waiting a
 * little before switching back."
 * (ANALOGIES ep15: hysteresis = a thermostat that waits a little before
 * switching back.) The room sits right at 21°: a heater that switched at the
 * exact number would click on, off, on, off. The real one waits: it stays on
 * through the wobble and clicks off once, later.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, createSignal, easeOutBack, easeOutCubic, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {exact, Pill, popIn, popOut, until} from '../lib/ep10';
import {timing15} from '../lib/ep15';
import {C, FONT} from '../style';

const T = timing15('thermostat');
const TX = -420;
const HX = 380;
const OFF = '#34435e';
const ON = '#ff7a4a';

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const temp = createSignal(20.6);
  const heat = createSignal(1); // 0 off .. 1 on
  const stage = createRef<Node>();
  const clicks = createRef<Rect>();
  const wait = createRef<Rect>();
  const hourglass = createRef<Node>();
  const onTxt = createRef<Txt>();

  view.add(
    <Node ref={stage} opacity={0}>
      {/* wall thermostat */}
      <Rect x={TX} y={-10} width={360} height={360} radius={60} fill={'#e3e8ef'} stroke={'#aab4c3'} lineWidth={5} shadowColor={'rgba(0,0,0,0.5)'} shadowBlur={30} shadowOffsetY={10}>
        <Circle size={280} fill={'#0f1a2c'} stroke={'#2c3a55'} lineWidth={6} />
        <Circle size={250} stroke={C.amber} lineWidth={10} startAngle={140} endAngle={() => 140 + (temp() - 15) * 26} lineCap={'round'} />
        <Txt y={-10} text={() => `${temp().toFixed(1)}°`} fontFamily={FONT.ui} fontWeight={800} fontSize={84} fill={C.text} />
        <Txt y={70} text={'set 21°'} fontFamily={FONT.ui} fontWeight={700} fontSize={30} fill={C.dim} />
      </Rect>
      <Txt x={TX} y={215} text={'thermostat'} fontFamily={FONT.ui} fontWeight={700} fontSize={34} fill={C.dim} />
      {/* wire to the heater */}
      <Line points={[[TX + 185, -10], [HX - 230, -10]]} stroke={C.dim} lineWidth={5} lineDash={[14, 10]} />
      {/* heater (radiator fins) */}
      {[0, 1, 2, 3, 4, 5].map(i => (
        <Rect
          x={HX - 175 + i * 70}
          y={20}
          width={56}
          height={260}
          radius={22}
          fill={() => (heat() > 0.5 ? ON : OFF)}
          shadowColor={'#ff7a4a'}
          shadowBlur={() => heat() * 30}
          stroke={'#1c2638'}
          lineWidth={3}
        />
      ))}
      <Rect x={HX} y={-95} width={430} height={22} radius={11} fill={'#5a6884'} />
      <Rect x={HX} y={135} width={430} height={22} radius={11} fill={'#5a6884'} />
      {/* warm air */}
      {[-120, 0, 120].map(dx => (
        <Line
          points={[[HX + dx, -130], [HX + dx + 18, -160], [HX + dx - 18, -195], [HX + dx, -225]]}
          stroke={'#ff9a6b'}
          lineWidth={6}
          lineCap={'round'}
          radius={14}
          opacity={() => heat() * 0.8}
        />
      ))}
      <Txt ref={onTxt} x={HX} y={215} text={() => (heat() > 0.5 ? 'heater ON' : 'heater OFF')} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={() => (heat() > 0.5 ? ON : C.dim)} />
    </Node>,
  );
  view.add(<Pill refNode={clicks} text={'click, click, click…'} color={C.red} x={HX} y={300} size={34} />);
  view.add(<Pill refNode={wait} text={'waits a little before switching back'} color={C.teal} x={0} y={300} size={34} />);
  view.add(
    <Node ref={hourglass} x={-345} y={300} opacity={0} scale={0.5}>
      <Line points={[[-18, -26], [18, -26], [-18, 26], [18, 26], [-18, -26]]} stroke={C.teal} lineWidth={5} lineJoin={'round'} />
    </Node>,
  );

  const h1 = new Headline('Like a *thermostat*', {accent: C.teal});
  view.add(h1.node());

  yield* all(h1.in(), stage().opacity(1, 0.4));

  // the same problem: the room sits right at 21 and a naive heater flickers
  yield* until(Math.max(useTime(), T.word('same', 1.06) - 0.5));
  yield popIn(clicks(), 0.3);
  const seq = [21.1, 20.9, 21.1, 20.9, 21.1, 20.9, 21.1];
  for (const v of seq) {
    temp(v);
    heat(v < 21 ? 1 : 0);
    yield onTxt().scale(1.12, 0.06).to(1, 0.12);
    yield* waitStep(0.2);
  }

  // ... solves it by waiting a little before switching back
  yield* until(Math.max(useTime(), T.word('solves', 2.58) - 0.2));
  yield popOut(clicks(), 0.2);
  heat(1);
  yield (function* () {
    // the real one: stays on through the wobble ...
    for (const v of [20.9, 21.1, 20.95, 21.15, 21.05, 21.25, 21.4]) yield* temp(v, 0.22);
    // ... and clicks off once, a bit above the set number
    yield* temp(21.6, 0.3, easeOutCubic);
  })();
  yield* until(Math.max(useTime(), T.word('waiting', 3.6) - 0.25));
  yield* all(popIn(wait(), 0.3), popIn(hourglass(), 0.3));
  yield hourglass().rotation(180, 0.5, easeOutCubic);
  yield* until(Math.max(useTime(), T.word('back', 4.98) - 0.15));
  heat(0);
  yield* all(onTxt().scale(1.15, 0.1).to(1, 0.25, easeOutBack), wait().scale(1.06, 0.1).to(1, 0.25));
  yield grid().opacity(0.6, 1.0, linear);
  yield* until(T.total);
}));

function* waitStep(s: number) {
  yield* until(useTime() + s);
}
