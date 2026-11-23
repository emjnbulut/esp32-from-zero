/**
 * Ep10 s33 - the ESP32 has a small drawer that keeps things without power:
 * "Preferences". Zoom from the board into the drawer, cut the power, the
 * card in the drawer stays lit.
 */
import {Circle, Line, makeScene2D, Node, Rect} from '@motion-canvas/2d';
import {
  all,
  createRef,
  createSignal,
  delay,
  easeInBack,
  easeInOutCubic,
  easeOutBack,
  easeOutCubic,
  linear,
  loop,
  useTime,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Drawer, Esp32Board, Pill, popIn, timing, until, exact} from '../lib/ep10';
import {C} from '../style';

const T = timing('prefs_drawer');

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const BX = -500;
  const BY = 30;
  const BS = 0.95;
  const esp = createRef<Node>();
  const led = createRef<Circle>();
  const plug = createRef<Node>();
  const cable = createRef<Line>();
  const spot = createRef<Rect>();
  const callout = createRef<Node>();
  const kept = createRef<Rect>();
  const offTag = createRef<Rect>();

  const drawer = new Drawer({x: 250, y: 0, title: 'Preferences', sub: '(flash memory)'});

  view.add(
    <Node>
      <Line
        ref={cable}
        stroke={'#2a3550'}
        lineWidth={18}
        lineCap={'round'}
        points={() => {
          const p = plug().position();
          return [p.add([-40, 0]), p.add([-200, 0]), p.add([-260, 160]), p.add([-600, 180])];
        }}
      />
      <Node ref={plug} position={[BX - 212 * BS - 50, BY]}>
        <Rect width={80} height={56} radius={12} fill={'#3a4766'} stroke={'#56658a'} lineWidth={3} />
        <Rect x={44} width={30} height={30} radius={4} fill={C.metal} />
      </Node>
    </Node>,
  );
  view.add(<Esp32Board refNode={esp} x={BX} y={BY} scale={BS} led={led} />);
  // spot on the board where the flash drawer lives
  view.add(
    <Rect ref={spot} x={BX - 30 * BS} y={BY} width={230 * BS} height={160 * BS} radius={12} stroke={C.teal} lineWidth={5} opacity={0} />,
  );
  view.add(
    <Node ref={callout} opacity={0}>
      <Line points={[[BX + 85 * BS, BY - 76 * BS], [250 - 215, -165]]} stroke={C.teal} lineWidth={3} lineDash={[12, 10]} />
      <Line points={[[BX + 85 * BS, BY + 76 * BS], [250 - 215, 165]]} stroke={C.teal} lineWidth={3} lineDash={[12, 10]} />
    </Node>,
  );
  view.add(drawer.node());
  view.add(<Pill refNode={kept} text={'still here ✓'} color={C.teal} x={540} y={250} size={36} />);
  view.add(<Pill refNode={offTag} text={'power off'} color={C.red} x={BX} y={BY + 190} size={34} />);

  const h1 = new Headline('A small *drawer* inside', {accent: C.teal});
  const h2 = new Headline('It’s called *Preferences*', {accent: C.teal});
  view.add(h1.node());
  view.add(h2.node());

  // ------------------------------------------------------------ beats
  esp().scale(0.6).opacity(0);
  drawer.root().scale(0.3).opacity(0);
  drawer.title().opacity(0);
  drawer.sub().opacity(0);
  drawer.card().opacity(1);
  yield* all(esp().scale(BS, 0.4, easeOutBack), esp().opacity(1, 0.25), delay(0.1, h1.in()));

  yield* until(Math.max(useTime(), Math.min(T.word('also', 1.4), T.word('drawer', 1.6) - 0.9)));
  yield* all(spot().opacity(1, 0.2), spot().scale(1.1, 0.15).to(1, 0.2));
  yield* all(
    callout().opacity(1, 0.3),
    drawer.root().opacity(1, 0.25),
    drawer.root().scale(1, 0.45, easeOutBack),
    h1.pulse(),
  );
  yield* until(Math.max(useTime(), T.word('drawer', 2.4) - 0.3));
  yield* drawer.open(280, 0.4);

  // cut the power: board goes dark, the drawer keeps its card
  yield* until(Math.max(useTime(), T.word('without', T.total * 0.45) - 0.3));
  yield* plug().position.x(plug().position.x() - 220, 0.35, easeInBack);
  yield* all(
    led().fill('#2a2f3a', 0.1),
    led().shadowBlur(0, 0.1),
    esp().opacity(0.35, 0.3),
    spot().opacity(0.3, 0.3),
    callout().opacity(0.4, 0.3),
    plug().opacity(0, 0.3),
    cable().opacity(0, 0.3),
    popIn(offTag(), 0.3),
  );
  const glow = createSignal(0);
  drawer.card().shadowColor('rgba(255,181,71,0.7)');
  drawer.card().shadowBlur(() => 10 + glow() * 30);
  yield loop(Infinity, () => glow(1, 0.5).to(0, 0.5));
  yield* all(popIn(kept(), 0.3), drawer.card().scale(1.1, 0.15).to(1, 0.25));

  // name it
  yield* until(Math.max(useTime(), T.word('preferences', T.total - 1.8) - 0.3));
  yield* all(h1.out(), delay(0.25, h2.in()), drawer.close(0.35), kept().opacity(0, 0.25));
  drawer.title().scale(1.8);
  yield* all(
    drawer.title().opacity(1, 0.15),
    drawer.title().scale(1, 0.35, easeOutCubic),
    delay(0.2, drawer.sub().opacity(1, 0.3)),
    delay(0.1, drawer.body().stroke(C.amber, 0.15).to(C.teal, 0.4)),
  );
  yield* h2.pulse();
  yield all(drawer.root().position.y(-10, 0.9, easeInOutCubic).to(0, 0.9, easeInOutCubic), grid().opacity(0.6, 1.2, linear));
  yield* until(T.total);
}));
