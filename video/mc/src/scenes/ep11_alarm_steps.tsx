/**
 * Ep11 s17 - the alarm's plan as the washing-machine dial (same look as Ep10
 * "steps"): OFF -> LEAVING -> ARMED -> ALARM, the OLED shows each screen of
 * motion_alarm.ino.
 */
import {Circle, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  delay,
  easeInOutCubic,
  easeOutBack,
  linear,
  loop,
  sequence,
  useTime,
  Vector2,
  waitFor,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Oled} from '../lib/oled';
import {exact, until} from '../lib/ep10';
import {timing11} from '../lib/ep11';
import {C, FONT, H, W} from '../style';

const T = timing11('alarm_steps');

const STATES = [
  {name: 'OFF', label: 'press to arm', value: 'OFF', color: C.dim},
  {name: 'LEAVING', label: 'leave the room!', value: '10 s', color: C.amber},
  {name: 'ARMED', label: 'guarding...', value: 'ARMED', color: C.teal},
  {name: 'ALARM', label: 'motion detected!', value: 'INTRUDER', color: C.red},
];

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const DX = -420;
  const DY = -20;
  const R = 190;
  const LR = 300;
  const dial = createRef<Node>();
  const knob = createRef<Node>();
  const ticks = STATES.map(() => createRef<Circle>());
  const labels = STATES.map(() => createRef<Txt>());
  const red = createRef<Rect>();
  const cycle = createRef<Circle>();

  const oled = new Oled({x: 480, y: -40, scale: 0.66, label: STATES[0].label, value: STATES[0].value, unit: ''});
  const pos = (i: number, r: number) => Vector2.fromDegrees(-90 + i * 90).scale(r);

  view.add(<Rect ref={red} width={W} height={H} fill={'rgba(255,40,60,0.0)'} />);
  view.add(
    <Node ref={dial} x={DX} y={DY}>
      <Circle size={R * 2 + 70} fill={'#101a2c'} stroke={C.line} lineWidth={4} />
      {/* the plan: one loop through the four steps */}
      <Circle
        ref={cycle}
        size={R * 2 + 130}
        stroke={C.amber}
        lineWidth={6}
        lineDash={[18, 14]}
        startAngle={-90}
        endAngle={-90}
        endArrow
        arrowSize={18}
        opacity={0.9}
      />
      <Circle size={R * 2} fill={'#15223a'} stroke={'#2e3f62'} lineWidth={6} />
      {STATES.flatMap((s, i) => [
        <Circle ref={ticks[i]} position={pos(i, R - 34)} size={28} fill={C.line} />,
        <Txt
          ref={labels[i]}
          position={pos(i, LR + (i % 2 ? 70 : 0))}
          text={s.name}
          fontFamily={FONT.ui}
          fontWeight={800}
          fontSize={44}
          fill={C.dim}
          opacity={0}
          scale={0.5}
        />,
      ])}
      <Node ref={knob}>
        <Circle size={210} fill={'#1e2a40'} stroke={C.metal} lineWidth={6} shadowColor={'rgba(0,0,0,0.5)'} shadowBlur={24} />
        <Rect y={-62} width={22} height={86} radius={11} fill={C.amber} />
        <Circle size={34} fill={C.metal} />
      </Node>
    </Node>,
  );
  view.add(oled.node());
  // the sketch's show() uses text size 2 for the big line: smaller than Ep10
  oled.value().fontSize(104);
  oled.value().y(30);

  const h1 = new Headline('An alarm needs a *plan*', {accent: C.teal});
  const h2 = new Headline('Steps, like a *washing* *machine*');
  view.add(h1.node());
  view.add(h2.node());

  let cur = -1;
  function* goState(i: number, turn = 0.3) {
    const prev = cur;
    cur = i;
    const s = STATES[i];
    let target = i * 90;
    while (target < knob().rotation() - 1) target += 360;
    yield* all(
      knob().rotation(target, turn, easeOutBack),
      prev >= 0 ? ticks[prev]().fill(C.line, 0.2) : waitFor(0),
      prev >= 0 ? labels[prev]().fill(C.dim, 0.2) : waitFor(0),
      prev >= 0 ? labels[prev]().scale(1, 0.2) : waitFor(0),
      ticks[i]().fill(s.color === C.dim ? C.text : s.color, 0.15),
      labels[i]().fill(s.color === C.dim ? C.text : s.color, 0.15),
      labels[i]().scale(1.2, 0.2, easeOutBack),
      delay(turn * 0.3, oled.powerOff()),
    );
    oled.label().text(s.label);
    oled.value().text(s.value);
    yield* oled.powerOn();
  }

  // ------------------------------------------------------------ beats
  dial().scale(0.7).opacity(0);
  oled.root().scale(0.4).opacity(0);
  yield* all(
    dial().scale(1, 0.45, easeOutBack),
    dial().opacity(1, 0.3),
    oled.root().scale(0.66, 0.45, easeOutBack),
    oled.root().opacity(1, 0.3),
    delay(0.1, h1.in()),
    delay(0.3, sequence(0.12, ...labels.map(l => all(l().opacity(1, 0.2), l().scale(1, 0.3, easeOutBack))))),
  );
  yield* until(Math.max(useTime(), T.word('plan', 2.0) - 0.1));
  yield* all(h1.pulse(), cycle().endAngle(262, 1.2, easeInOutCubic));
  // the loop keeps flowing while we talk
  yield loop(Infinity, () => cycle().lineDashOffset(-64, 0.8, linear).to(0, 0));
  yield all(cycle().opacity(0.35, 0.6));

  // "steps": the four labels light up one after another
  yield* until(Math.max(useTime(), T.word('steps', 4.0) - 0.2));
  yield* all(
    h1.out(),
    delay(0.25, h2.in()),
    sequence(0.15, ...STATES.map((_, i) => all(labels[i]().fill(C.amber, 0.12).to(C.dim, 0.3), ticks[i]().fill(C.amber, 0.12).to(C.line, 0.3)))),
  );
  yield* until(Math.max(useTime(), T.word('washing', 5.5) - 0.1));
  yield* all(h2.pulse(), dial().rotation(-6, 0.12).to(6, 0.12).to(0, 0.12));

  const words = ['off', 'leaving', 'armed', 'alarm'];
  const fb = [0.72, 0.77, 0.82, 0.9].map(f => f * T.total);
  for (let i = 0; i < 4; i++) {
    // "alarm" is said twice ("an alarm needs a plan" ... "and alarm"): take the last one
    const w = i === 3 ? T.word('alarm', fb[i], undefined, 1) : T.word(words[i], fb[i]);
    yield* until(Math.max(useTime(), Math.min(w - 0.15, T.total - (4 - i) * 0.45)));
    yield* goState(i, 0.3);
  }
  // ALARM: the room flashes red
  yield loop(Infinity, () => red().fill('rgba(255,40,60,0.14)', 0.12).to('rgba(255,40,60,0)', 0.25));
  yield loop(Infinity, () => oled.board().scale(1.04, 0.12).to(1, 0.25));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));

