/**
 * Ep10 s32 - normal variables live in RAM: sticky notes on a desk that get
 * swept off when the power goes (every night).
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  cancel,
  createRef,
  delay,
  easeInCubic,
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
import {timing, until, exact} from '../lib/ep10';
import {C, FONT, H, W} from '../style';

const T = timing('prefs_ram');

function Note(props: {refNode: Reference<Rect>; name: string; value: string; x: number; y: number; rot: number}) {
  return (
    <Rect
      ref={props.refNode}
      x={props.x}
      y={props.y}
      rotation={props.rot}
      width={260}
      height={230}
      radius={6}
      fill={'#ffd666'}
      shadowColor={'rgba(0,0,0,0.45)'}
      shadowBlur={18}
      shadowOffsetY={8}
      opacity={0}
      scale={1.6}
    >
      <Rect y={-100} width={260} height={30} fill={'rgba(0,0,0,0.08)'} />
      <Txt y={-40} text={props.name} fontFamily={FONT.code} fontWeight={700} fontSize={40} fill={'#5a4310'} />
      <Txt y={40} text={props.value} fontFamily={FONT.code} fontWeight={800} fontSize={76} fill={'#2a1f08'} />
    </Rect>
  );
}

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const desk = createRef<Node>();
  const notes = [createRef<Rect>(), createRef<Rect>(), createRef<Rect>()];
  const sw = createRef<Node>();
  const knob = createRef<Rect>();
  const led = createRef<Circle>();
  const moon = createRef<Node>();
  const dark = createRef<Rect>();
  const broom = createRef<Node>();
  const empty = createRef<Txt>();

  const DX = -130;
  const DY = 20;
  view.add(
    <Node ref={desk} x={DX} y={DY}>
      <Rect width={1100} height={470} radius={22} fill={'#4a3626'} stroke={'#5e4632'} lineWidth={5} shadowColor={'rgba(0,0,0,0.5)'} shadowBlur={36} shadowOffsetY={14} />
      {[-150, -60, 40, 140].map(y => (
        <Line points={[[-520, y], [-200, y + 6], [160, y - 4], [520, y + 4]]} stroke={'rgba(0,0,0,0.16)'} lineWidth={4} radius={80} />
      ))}
      <Rect x={-430} y={-195} layout padding={[6, 18]} radius={10} fill={'rgba(45,212,191,0.9)'}>
        <Txt text={'RAM'} fontFamily={FONT.ui} fontWeight={900} fontSize={36} fill={C.bg} />
      </Rect>
      <Txt ref={empty} y={10} text={'(empty)'} fontFamily={FONT.ui} fontStyle={'italic'} fontSize={52} fill={'rgba(255,255,255,0.45)'} opacity={0} />
    </Node>,
  );
  const data = [
    {name: 'best', value: '214', x: -310, y: 30, rot: -6},
    {name: 'state', value: '2', x: -10, y: -10, rot: 4},
    {name: 'waitTime', value: '2800', x: 290, y: 40, rot: -3},
  ];
  data.forEach((d, i) => view.add(<Note refNode={notes[i]} {...d} x={DX + d.x} y={DY + d.y} />));

  // power switch
  view.add(
    <Node ref={sw} x={720} y={DY} opacity={0}>
      <Rect width={150} height={250} radius={24} fill={'#1e2a40'} stroke={C.metal} lineWidth={4} />
      <Rect width={70} height={160} radius={35} fill={'#0b1220'} />
      <Rect ref={knob} y={-40} width={58} height={70} radius={29} fill={C.metal} />
      <Circle ref={led} y={-100} size={20} fill={'#3ddc84'} shadowColor={'#3ddc84'} shadowBlur={16} />
      <Txt y={160} text={'POWER'} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={C.dim} />
    </Node>,
  );
  view.add(<Rect ref={dark} width={W} height={H} fill={'#02040a'} opacity={0} />);
  // moon = "every night"
  view.add(
    <Node ref={moon} x={720} y={-250} opacity={0} scale={0.4}>
      <Circle size={110} fill={'#f2e6b8'} />
      <Circle x={30} y={-20} size={96} fill={'#0b1220'} />
    </Node>,
  );
  // broom
  view.add(
    <Node ref={broom} x={DX - 760} y={DY + 40} rotation={-20} opacity={0}>
      <Line points={[[0, -360], [0, 40]]} stroke={'#b48a5a'} lineWidth={22} lineCap={'round'} />
      <Line
        points={[[-30, 30], [30, 30], [90, 230], [-90, 230]]}
        closed
        fill={'#d9b25f'}
        stroke={'#9c7a35'}
        lineWidth={5}
      />
      {[-60, -30, 0, 30, 60].map(x => (
        <Line points={[[x * 0.4, 40], [x, 226]]} stroke={'#9c7a35'} lineWidth={4} />
      ))}
    </Node>,
  );

  const h1 = new Headline('Variables live in *RAM*', {accent: C.teal});
  const h2 = new Headline('Power off → *swept* *away*', {accent: C.red});
  view.add(h1.node());
  view.add(h2.node());

  // ------------------------------------------------------------ beats
  desk().scale(0.9).opacity(0);
  yield* all(
    desk().scale(1, 0.4, easeOutBack),
    desk().opacity(1, 0.3),
    sw().opacity(1, 0.4),
    delay(0.1, h1.in()),
  );
  // notes slap onto the desk
  const tNotes = Math.max(useTime(), Math.min(T.word('normally', 1.6), T.word('variable', 2.2) - 0.8));
  yield* until(tNotes);
  yield* sequence(
    0.28,
    ...notes.map(n => all(n().opacity(1, 0.12), n().scale(1, 0.3, easeOutBack))),
  );
  yield* h1.pulse();
  // notes breathe a little while we talk
  const breathe = yield loop(Infinity, () =>
    all(...notes.map((n, i) => n().position.y(n().position.y() + (i % 2 ? 6 : -6), 0.8, easeInOutCubic).back(0.8, easeInOutCubic))),
  );

  // power goes
  yield* until(Math.max(useTime(), T.word('power', T.total * 0.45) - 0.3));
  yield* all(knob().y(40, 0.18, easeInCubic), led().fill('#24303f', 0.1), led().shadowBlur(0, 0.1));
  yield* all(
    dark().opacity(0.55, 0.12).to(0.25, 0.08).to(0.6, 0.1),
    ...notes.map(n => n().opacity(0.6, 0.2)),
  );

  // "like sticky notes on a desk that get swept off every night"
  yield* until(Math.max(useTime(), T.word('like', T.total * 0.6) - 0.1));
  yield* all(h1.out(), delay(0.25, h2.in()), moon().opacity(1, 0.3), moon().scale(1, 0.4, easeOutBack));
  yield* until(Math.max(useTime(), T.word('swept', T.total * 0.8) - 0.4));
  cancel(breathe);
  broom().opacity(1);
  yield* all(
    broom().position.x(DX + 820, 0.9, easeInOutCubic),
    broom().rotation(25, 0.9, easeInOutCubic),
    ...notes.map((n, i) =>
      delay(
        0.18 + i * 0.16,
        all(
          n().position.x(n().position.x() + 1200, 0.55, easeInCubic),
          n().position.y(n().position.y() + (i - 1) * 140 - 40, 0.55, easeInCubic),
          n().rotation(60 + i * 25, 0.55, easeInCubic),
          n().opacity(0, 0.55, easeInCubic),
        ),
      ),
    ),
  );
  yield* all(
    broom().opacity(0, 0.2),
    dark().opacity(0, 0.4),
    knob().y(-40, 0.2, easeOutCubic),
    led().fill('#3ddc84', 0.2),
    led().shadowBlur(16, 0.2),
    delay(0.2, empty().opacity(1, 0.3)),
    h2.pulse(),
  );
  yield all(empty().scale(1.06, 0.6, easeInOutCubic).to(1, 0.6, easeInOutCubic), grid().opacity(0.6, 1.2, linear));
  yield* until(T.total);
}));
