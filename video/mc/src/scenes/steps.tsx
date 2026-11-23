/**
 * Ep10 s25+s26 - the game loop as a washing-machine dial.
 * s25: READY -> WAIT -> GO -> RESULT, the OLED shows each screen.
 * s26: on a press we pick a random wait between 1.5 and 4 s (the marker
 *      spins on a range bar), nobody can guess it, then GO.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
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
  sequence,
  useTime,
  Vector2,
  waitFor,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Oled} from '../lib/oled';
import {burst, CodePanel, lit, popIn, timing, until, exact} from '../lib/ep10';
import {C, FONT} from '../style';

const T = timing('steps');

const STATES = [
  {name: 'READY', label: 'REFLEX 2.0 best:', value: '214', unit: 'ms'},
  {name: 'WAIT', label: 'get ready...', value: 'WAIT', unit: ''},
  {name: 'GO!', label: '', value: ' GO!', unit: ''},
  {name: 'RESULT', label: 'your time', value: '287', unit: 'ms'},
];

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);
  const S26 = T.seg('s26').start;

  const DX = -420;
  const DY = -40;
  const R = 190;
  const LR = 262;
  const dial = createRef<Node>();
  const knob = createRef<Node>();
  const ticks = STATES.map(() => createRef<Circle>());
  const labels = STATES.map(() => createRef<Txt>());
  const arc = createRef<Circle>();
  const qs = [createRef<Txt>(), createRef<Txt>(), createRef<Txt>()];

  const oled = new Oled({x: 480, y: -90, scale: 0.62, label: STATES[0].label, value: STATES[0].value, unit: STATES[0].unit});

  // range bar 1.5 .. 4 s
  const BX0 = 250;
  const BX1 = 710;
  const BY = 150;
  const msToX = (ms: number) => BX0 + ((ms - 1500) / 2500) * (BX1 - BX0);
  const range = createRef<Node>();
  const marker = createRef<Node>();
  const markerTxt = createRef<Txt>();
  const ms = createSignal(2600);

  const pos = (i: number, r: number) => Vector2.fromDegrees(-90 + i * 90).scale(r);

  view.add(
    <Node ref={dial} x={DX} y={DY}>
      <Circle size={R * 2 + 70} fill={'#101a2c'} stroke={C.line} lineWidth={4} />
      <Circle
        ref={arc}
        size={R * 2 + 70}
        stroke={C.amber}
        lineWidth={14}
        startAngle={0}
        endAngle={0}
        opacity={0}
      />
      <Circle size={R * 2} fill={'#15223a'} stroke={'#2e3f62'} lineWidth={6} />
      {STATES.flatMap((s, i) => [
        <Circle ref={ticks[i]} position={pos(i, R - 34)} size={28} fill={C.line} />,
        <Txt
          ref={labels[i]}
          position={pos(i, LR + (i % 2 ? 40 : 0))}
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
  view.add(
    <Node ref={range} opacity={0}>
      <Rect x={(BX0 + BX1) / 2} y={BY} width={BX1 - BX0} height={16} radius={8} fill={'#1e2a40'} />
      <Rect x={(BX0 + BX1) / 2} y={BY} width={BX1 - BX0} height={16} radius={8} stroke={C.teal} lineWidth={3} />
      <Txt x={BX0} y={BY + 48} text={'1.5 s'} fontFamily={FONT.ui} fontWeight={700} fontSize={34} fill={C.teal} />
      <Txt x={BX1} y={BY + 48} text={'4 s'} fontFamily={FONT.ui} fontWeight={700} fontSize={34} fill={C.teal} />
      <Node ref={marker} x={() => msToX(ms())} y={BY}>
        <Circle size={38} fill={C.amber} stroke={C.bg} lineWidth={5} />
        <Rect y={-56} layout padding={[4, 14]} radius={10} fill={C.amber}>
          <Txt
            ref={markerTxt}
            text={() => `${(ms() / 1000).toFixed(1)} s`}
            fontFamily={FONT.code}
            fontWeight={800}
            fontSize={34}
            fill={C.bg}
          />
        </Rect>
      </Node>
    </Node>,
  );
  [
    [-190, -120],
    [170, -170],
    [200, 120],
  ].forEach(([x, y], i) =>
    view.add(
      <Txt ref={qs[i]} x={DX + x} y={DY + y} text={'?'} fontFamily={FONT.ui} fontWeight={900} fontSize={84} fill={C.teal} opacity={0} scale={0.4} />,
    ),
  );

  const code = new CodePanel({y: 335, size: 50, code: 'waitTime = random(1500, 4000);'});
  view.add(code.node());

  const h1 = new Headline('Four steps, like a *washing* *machine*');
  const h2 = new Headline('A *random* wait, every time', {accent: C.teal});
  view.add(h1.node());
  view.add(h2.node());

  // set the dial + OLED to state i
  let cur = -1;
  function* goState(i: number, turn = 0.35) {
    const prev = cur;
    cur = i;
    const s = STATES[i];
    // always turn clockwise
    let target = i * 90;
    while (target < knob().rotation() - 1) target += 360;
    yield* all(
      knob().rotation(target, turn, easeOutBack),
      prev >= 0 ? ticks[prev]().fill(C.line, 0.2) : waitFor(0),
      prev >= 0 ? labels[prev]().fill(C.dim, 0.2) : waitFor(0),
      prev >= 0 ? labels[prev]().scale(1, 0.2) : waitFor(0),
      ticks[i]().fill(C.amber, 0.15),
      labels[i]().fill(i === 2 ? C.teal : C.amber, 0.15),
      labels[i]().scale(1.2, 0.2, easeOutBack),
      delay(turn * 0.3, oled.powerOff()),
    );
    oled.label().text(s.label);
    oled.value().text(s.value);
    oled.unit().text(s.unit);
    yield* oled.powerOn();
  }

  // ------------------------------------------------------------ s25
  dial().scale(0.7).opacity(0);
  oled.root().scale(0.4).opacity(0);
  yield* all(
    dial().scale(1, 0.45, easeOutBack),
    dial().opacity(1, 0.3),
    oled.root().scale(0.62, 0.45, easeOutBack),
    oled.root().opacity(1, 0.3),
    delay(0.1, h1.in()),
    delay(0.3, sequence(0.12, ...labels.map(l => all(l().opacity(1, 0.2), l().scale(1, 0.3, easeOutBack))))),
  );
  // "four steps": the four labels light up one after another
  yield* until(Math.max(useTime(), T.word('four', 1.2) - 0.1));
  yield* sequence(
    0.15,
    ...STATES.map((_, i) => all(labels[i]().fill(C.amber, 0.12).to(C.dim, 0.3), ticks[i]().fill(C.amber, 0.12).to(C.line, 0.3))),
  );
  yield* until(Math.max(useTime(), T.word('washing', 1.4) - 0.1));
  yield* all(h1.pulse(), dial().rotation(-6, 0.12).to(6, 0.12).to(0, 0.12));

  const segEnd = T.seg('s25').end;
  const fb = [0.55, 0.65, 0.75, 0.85].map(f => f * T.seg('s25').dur);
  const words = ['ready', 'wait', 'go', 'result'];
  for (let i = 0; i < 4; i++) {
    yield* until(Math.max(useTime(), Math.min(T.word(words[i], fb[i], 's25') - 0.15, segEnd - (4 - i) * 0.5)));
    yield* goState(i, 0.3);
  }

  // ------------------------------------------------------------ s26
  yield* until(Math.max(useTime(), S26 - 0.2));
  yield* all(h1.out(), delay(0.3, h2.in()), goState(0, 0.4));
  // "when you press": knob bump + go to WAIT
  yield* until(Math.max(useTime(), T.word('press', S26 + 0.8, 's26') - 0.1));
  yield* all(knob().scale(0.9, 0.08).to(1, 0.2), goState(1, 0.35));

  // random pick: marker spins along the range bar like a slot machine
  yield* until(Math.max(useTime(), T.word('random', S26 + 2, 's26') - 0.3));
  yield* all(range().opacity(1, 0.25), code.show(), h2.pulse());
  yield code.code().selection(code.code().findFirstRange(lit('random(1500, 4000)')), 0.3);
  const picks = [3700, 1700, 3200, 2100, 3900, 1600, 2900, 2300, 3400, 2800];
  // spin (slowing down) until the narration has said "... and four seconds"
  const spinEnd = Math.max(useTime() + 1.6, Math.min(T.word('seconds', S26 + 6, 's26'), T.total - 3.5));
  const weights = picks.map((_, k) => 1 + k * 0.3);
  const wsum = weights.reduce((a, b) => a + b, 0);
  const spin = spinEnd - useTime();
  for (let k = 0; k < picks.length; k++) {
    yield* ms(picks[k], (spin * weights[k]) / wsum, easeInOutCubic);
  }
  yield* marker().scale(1.3, 0.12).to(1, 0.25, easeOutBack);

  // nobody can guess: question marks pop around the dial while the wait runs
  const tGuess = Math.max(useTime(), T.word('guess', S26 + 6, 's26') - 0.6);
  yield* until(Math.max(useTime(), tGuess - 1.2));
  arc().opacity(1);
  arc().startAngle(-90);
  arc().endAngle(-90);
  const tGo = Math.max(useTime() + 1.6, Math.min(T.total - 1.4, T.word('moment', T.total - 1.6, 's26') + 0.1));
  yield all(
    arc().endAngle(270, tGo - useTime() - 0.05, linear),
    sequence(0.25, ...qs.map(q => all(q().opacity(1, 0.2), q().scale(1, 0.35, easeOutBack)))),
    loop(Infinity, () => all(...qs.map((q, i) => q().rotation(i % 2 ? 12 : -12, 0.35).to(0, 0.35)))),
  );
  yield* until(tGo);
  // GO!
  yield* all(
    ...qs.map(q => q().opacity(0, 0.2)),
    arc().opacity(0, 0.3),
    code.code().selection(code.code().findFirstRange(lit('waitTime')), 0.3),
    goState(2, 0.3),
  );
  yield* burst(view, new Vector2(480, -90), [C.teal, C.amber, C.text], 200);
  yield loop(Infinity, () => oled.board().scale(1.03, 0.3).to(1, 0.3));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
