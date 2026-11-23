/**
 * Ep10 s37 - tip: save only on a new record. Saving every round overwrites
 * the best with a slow time and wears the flash drawer out (wear meter).
 */
import {Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  createSignal,
  delay,
  easeInOutCubic,
  easeOutBack,
  easeOutCubic,
  linear,
  loop,
  Reference,
  sequence,
  useTime,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Drawer, flyArc, Pill, popIn, popOut, timing, toView, until, ValueCard, exact} from '../lib/ep10';
import {C, FONT} from '../style';

const T = timing('mistake');

function RoundChip(props: {refNode: Reference<Rect>; n: number; ms: number; record?: boolean; y: number}) {
  return (
    <Rect
      ref={props.refNode}
      x={-560}
      y={props.y}
      width={400}
      height={84}
      radius={16}
      fill={'#15223a'}
      stroke={props.record ? C.amber : C.line}
      lineWidth={props.record ? 4 : 3}
      opacity={0}
    >
      <Txt x={-176} offsetX={-1} text={`round ${props.n}`} fontFamily={FONT.ui} fontWeight={700} fontSize={34} fill={C.dim} />
      <Txt x={120} offsetX={1} text={`${props.ms}`} fontFamily={FONT.code} fontWeight={800} fontSize={46} fill={props.record ? C.amber : C.text} />
      <Txt x={130} offsetX={-1} text={'ms'} fontFamily={FONT.code} fontSize={28} fill={C.dim} />
      {props.record ? <Txt x={178} text={'★'} fontFamily={FONT.ui} fontSize={36} fill={C.amber} /> : null}
    </Rect>
  );
}

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const rounds = [
    {n: 1, ms: 231, record: false},
    {n: 2, ms: 214, record: true},
    {n: 3, ms: 350, record: false},
    {n: 4, ms: 402, record: false},
    {n: 5, ms: 297, record: false},
  ];
  const chips = rounds.map(() => createRef<Rect>());
  const drawer = new Drawer({x: 250, y: -70});
  const fly = createRef<Rect>();
  const flyVal = createRef<Txt>();
  const goodTag = createRef<Rect>();
  const badTag = createRef<Rect>();
  const slow = createRef<Rect>();
  const meter = createRef<Node>();
  const wear = createSignal(0.04);
  const cracks = createRef<Node>();

  rounds.forEach((r, i) => view.add(<RoundChip refNode={chips[i]} {...r} y={-215 + i * 106} />));
  view.add(drawer.node());
  view.add(<ValueCard refNode={fly} valueRef={flyVal} value={'214'} />);
  view.add(<Pill refNode={goodTag} text={'✓ only new records'} color={C.teal} x={430} y={-300} size={36} />);
  view.add(<Pill refNode={badTag} text={'✗ every round'} color={C.red} x={430} y={-300} size={36} />);
  view.add(<Pill refNode={slow} text={'best = a slow time ✗'} color={C.red} x={620} y={132} size={32} />);

  const MW = 520;
  view.add(
    <Node ref={meter} x={300} y={235} opacity={0}>
      <Txt x={-MW / 2} y={-42} offsetX={-1} text={'flash wear'} fontFamily={FONT.ui} fontWeight={700} fontSize={32} fill={C.dim} />
      <Rect width={MW} height={30} radius={15} fill={'#1e2a40'} stroke={C.line} lineWidth={3} />
      <Rect
        x={-MW / 2}
        offsetX={-1}
        width={() => MW * wear()}
        height={30}
        radius={15}
        fill={() => (wear() > 0.5 ? C.red : wear() > 0.25 ? C.amber : C.teal)}
      />
    </Node>,
  );
  view.add(
    <Node ref={cracks} x={250} y={-70} opacity={0}>
      <Line points={[[-150, -120], [-110, -60], [-130, -10], [-90, 40]]} stroke={'#ff9aa4'} lineWidth={5} />
      <Line points={[[140, -140], [100, -90], [120, -40]]} stroke={'#ff9aa4'} lineWidth={5} />
    </Node>,
  );

  const h1 = new Headline('Tip: save only on a *new* *record*', {accent: C.teal});
  const h2 = new Headline('Save every round? *Bad* *idea*', {accent: C.red});
  view.add(h1.node());
  view.add(h2.node());

  const tray = () => toView(view, drawer.card().absolutePosition());
  const chipPos = (i: number) => chips[i]().position().add([80, 0]);

  // fly round i into the drawer and overwrite the stored value
  function* save(i: number, bad: boolean, dur = 0.5) {
    flyVal().text(String(rounds[i].ms));
    fly().stroke(bad ? C.red : C.amber);
    flyVal().fill(bad ? C.red : C.amber);
    fly().position(chipPos(i)).scale(0.6).opacity(1).rotation(0);
    yield* all(flyArc(fly(), chipPos(i), tray(), 140, dur), fly().scale(1, dur));
    fly().opacity(0);
    drawer.card().opacity(1);
    drawer.cardValue().text(String(rounds[i].ms));
    drawer.cardValue().fill(bad ? C.red : C.amber);
    drawer.card().stroke(bad ? C.red : C.amber);
    yield* all(
      drawer.card().scale([1.12, 0.9], 0.08).to(1, 0.2),
      wear(Math.min(1, wear() + (bad ? 0.2 : 0.04)), 0.3, easeOutCubic),
      bad ? drawer.root().x(258, 0.04).to(242, 0.06).to(250, 0.04) : chips[i]().scale(1, 0),
    );
  }
  function* skip(i: number) {
    yield* all(
      chips[i]().x(-540, 0.06).to(-580, 0.08).to(-560, 0.06),
      chips[i]().opacity(0.45, 0.25),
    );
  }

  // ------------------------------------------------------------ the tip
  drawer.root().scale(0.5).opacity(0);
  chips.forEach(c => c().x(-600));
  yield* all(
    drawer.root().scale(1, 0.4, easeOutBack),
    drawer.root().opacity(1, 0.25),
    delay(0.1, h1.in()),
    delay(0.2, drawer.open(300, 0.4)),
    delay(0.3, sequence(0.08, ...chips.map(c => all(c().opacity(1, 0.2), c().x(-560, 0.3, easeOutCubic))))),
    delay(0.4, meter().opacity(1, 0.3)),
  );
  yield* popIn(goodTag(), 0.3);
  // round 1 -> first record, round 2 -> new record, the slow ones are skipped
  const S_BAD = Math.max(useTime() + 2.6, T.word('saving', T.total * 0.38) - 0.3);
  const goodStep = Math.max(0.35, Math.min(0.6, (S_BAD - useTime() - 0.6) / 5));
  yield* save(0, false, goodStep);
  yield* save(1, false, goodStep);
  yield* h1.pulse();
  for (const i of [2, 3, 4]) yield* skip(i);

  // ------------------------------------------------------------ every round
  yield* until(Math.max(useTime(), S_BAD));
  yield* all(
    h1.out(),
    delay(0.25, h2.in()),
    popOut(goodTag(), 0.2),
    delay(0.15, popIn(badTag(), 0.3)),
    ...[2, 3, 4].map(i => chips[i]().opacity(1, 0.25)),
    chips[2]().stroke(C.red, 0.25),
  );
  for (const i of [2, 3]) {
    chips[i]().stroke(C.red);
    yield* save(i, true, 0.45);
  }
  yield* popIn(slow(), 0.3);
  chips[4]().stroke(C.red);
  yield* save(4, true, 0.4);

  // ... and the drawer wears out faster
  yield* until(Math.max(useTime(), T.word('wear', T.total - 3) - 0.3));
  yield* all(
    wear(0.92, 0.8, easeInOutCubic),
    delay(0.3, cracks().opacity(1, 0.2)),
    delay(0.3, drawer.body().stroke(C.red, 0.2)),
    delay(0.3, drawer.root().rotation(1.5, 0.05).to(-1.5, 0.08).to(1, 0.08).to(0, 0.06)),
    h2.pulse(),
  );
  yield loop(Infinity, () => meter().scale(1.04, 0.3).to(1, 0.3));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
