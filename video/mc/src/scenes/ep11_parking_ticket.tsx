/**
 * Ep11 s22 - "At the moment of motion, we stamp the time, like the parking
 * ticket from episode nine." The board's stopwatch keeps running; when the
 * PIR's thumb goes up, the ticket machine prints a ticket with that moment
 * stamped on it (the number then stays frozen while the stopwatch runs on).
 */
import {Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  createSignal,
  delay,
  easeInCubic,
  easeOutBack,
  easeOutCubic,
  linear,
  useTime,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {exact, Pill, popIn, until} from '../lib/ep10';
import {Pir, Thumb, timing11, walk, Walker} from '../lib/ep11';
import {C, FONT} from '../style';

const T = timing11('parking_ticket');
const fmt = (ms: number) => `${Math.floor(ms / 1000).toLocaleString('en-US').replace(/,/g, ' ')} ${String(Math.floor(ms % 1000)).padStart(3, '0')}`;

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const clockMs = createSignal(751200);
  const stamped = createSignal(0);
  const watch = createRef<Rect>();
  const pir = createRef<Node>();
  const walker = createRef<Node>();
  const thumb = new Thumb({x: -380, y: 190, scale: 0.6, up: false});
  const machine = createRef<Node>();
  const pSign = createRef<Rect>();
  const ticket = createRef<Node>();
  const stamp = createRef<Rect>();
  const ep9 = createRef<Rect>();

  // the board's stopwatch (millis)
  view.add(
    <Rect ref={watch} x={-560} y={-170} width={520} height={190} radius={22} fill={'#101a2c'} stroke={C.line} lineWidth={3} opacity={0}>
      <Txt y={-55} text={'millis()  - the board’s stopwatch'} fontFamily={FONT.ui} fontWeight={700} fontSize={28} fill={C.dim} />
      <Txt y={20} text={() => fmt(clockMs())} fontFamily={FONT.code} fontWeight={800} fontSize={68} fill={C.text} />
      <Txt x={210} y={34} text={'ms'} fontFamily={FONT.code} fontSize={30} fill={C.dim} />
    </Rect>,
  );
  view.add(<Pir refNode={pir} x={-660} y={190} scale={0.55} />);
  view.add(<Walker refNode={walker} x={-1150} y={150} scale={0.75} />);
  view.add(thumb.node());

  // parking ticket machine
  view.add(
    <Node ref={machine} x={240} y={-40} opacity={0}>
      <Rect width={340} height={460} radius={26} fill={'#1c2a44'} stroke={'#2e4266'} lineWidth={4} shadowColor={'rgba(0,0,0,0.5)'} shadowBlur={30} shadowOffsetY={10} />
      <Rect ref={pSign} y={-150} width={110} height={110} radius={16} fill={'#2f6fe0'}>
        <Txt text={'P'} fontFamily={FONT.ui} fontWeight={900} fontSize={84} fill={'#ffffff'} />
      </Rect>
      <Rect y={-20} width={240} height={70} radius={10} fill={'#0b1220'}>
        <Txt text={() => fmt(clockMs())} fontFamily={FONT.code} fontWeight={700} fontSize={30} fill={C.teal} />
      </Rect>
      <Rect y={120} width={220} height={16} radius={8} fill={'#05080f'} />
    </Node>,
  );
  // the ticket (comes out of the slot, then grows to the right)
  view.add(
    <Node ref={ticket} x={240} y={80} opacity={0} scale={0.3}>
      <Rect width={540} height={290} radius={10} fill={'#f3efe3'} shadowColor={'rgba(0,0,0,0.45)'} shadowBlur={24} shadowOffsetY={8}>
        <Line points={[[-200, -70], [200, -70]]} stroke={'#c8bfa8'} lineWidth={3} lineDash={[10, 8]} />
        <Txt x={-60} y={-104} text={'ENTRY TICKET'} fontFamily={FONT.ui} fontWeight={900} fontSize={34} letterSpacing={4} fill={'#2a2418'} />
        <Txt y={-20} text={'motion seen at'} fontFamily={FONT.ui} fontSize={28} fill={'#6b6152'} />
        <Txt y={45} text={() => fmt(stamped())} fontFamily={FONT.code} fontWeight={800} fontSize={64} fill={'#1b2a4a'} />
        <Txt x={200} y={58} text={'ms'} fontFamily={FONT.code} fontSize={26} fill={'#6b6152'} />
        <Txt y={108} text={'lastMotion'} fontFamily={FONT.code} fontWeight={700} fontSize={26} fill={'#2a7f74'} />
      </Rect>
      <Rect ref={stamp} x={175} y={-100} rotation={-12} padding={[6, 16]} layout radius={10} stroke={C.red} lineWidth={6} opacity={0} scale={2}>
        <Txt text={'MOTION'} fontFamily={FONT.ui} fontWeight={900} fontSize={40} fill={C.red} />
      </Rect>
    </Node>,
  );
  view.add(<Pill refNode={ep9} text={'like the parking ticket, Ep 9'} color={C.amber} x={560} y={330} size={32} />);

  const h1 = new Headline('Now the *clever* part', {accent: C.teal});
  const h2 = new Headline('*Stamp* the moment');
  view.add(h1.node());
  view.add(h2.node());

  // ------------------------------------------------------------ beats
  machine().position.y(0);
  // the stopwatch runs for the whole scene (1000 ms per second)
  yield clockMs(clockMs() + T.total * 1000, T.total, linear);
  yield* all(
    delay(0.05, h1.in()),
    watch().opacity(1, 0.3),
    pir().opacity(0).opacity(1, 0.3),
    machine().opacity(1, 0.3),
    machine().position.y(-40, 0.4, easeOutCubic),
  );
  yield* until(Math.max(useTime(), T.word('clever', 0.9) - 0.1));
  yield* h1.pulse();

  // someone walks in front of the sensor -> thumb up at "motion"
  const tMotion = T.word('motion', 3.6);
  yield* until(Math.max(useTime(), tMotion - 1.4));
  yield walk(walker(), -1150, -560, 1.4);
  yield* until(Math.max(useTime(), tMotion - 0.1));
  yield* all(thumb.set(true), h1.out(), delay(0.25, h2.in()));

  // stamp: the machine prints a ticket with this exact moment
  yield* until(Math.max(useTime(), T.word('stamp', tMotion + 1) - 0.3));
  stamped(clockMs());
  yield* all(ticket().opacity(1, 0.15), ticket().position.y(200, 0.35, easeOutCubic), ticket().scale(0.5, 0.35));
  yield* all(
    ticket().position([570, 100], 0.5, easeOutBack),
    ticket().scale(1, 0.5, easeOutBack),
    ticket().rotation(-4, 0.5),
  );
  yield* all(stamp().opacity(1, 0.08), stamp().scale(1, 0.18, easeInCubic));
  yield* all(ticket().position.y(108, 0.05).to(100, 0.1), h2.pulse());
  yield walk(walker(), walker().position.x(), -1150, 1.3);
  yield thumb.set(false, 0.4);

  // like the parking ticket from episode 9
  yield* until(Math.max(useTime(), T.word('parking', T.total - 2.6) - 0.2));
  yield* all(popIn(ep9(), 0.35), pSign().scale(1.2, 0.15).to(1, 0.3, easeOutBack));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
