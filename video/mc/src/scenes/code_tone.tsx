/**
 * Ep10 s28 - one line makes the beep: tone(BUZZER_PIN, 1500, 150);
 * The three arguments get labels (pin / how high / how long) and the sound
 * wave above reacts: higher pitch = tighter wave, shorter time = shorter wave.
 */
import {Circle, Code, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  createSignal,
  DEFAULT,
  delay,
  easeInOutCubic,
  easeOutBack,
  easeOutCubic,
  linear,
  loop,
  sequence,
  useTime,
  waitFor,
  cancel,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {arduino} from '../lib/arduinoHighlighter';
import {Headline} from '../lib/kinetic';
import {SketchGlimpse} from '../lib/glimpse';
import {lit, timing, toView, until, exact} from '../lib/ep10';
import {C, FONT} from '../style';

const T = timing('code_tone');
const PINK = '#ff7eb6';

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const buzzer = createRef<Node>();
  const ring = createRef<Circle>();
  const waves = [createRef<Circle>(), createRef<Circle>(), createRef<Circle>()];
  const wave = createRef<Line>();
  const code = createRef<Code>();
  const durBar = createRef<Node>();

  const WX0 = -480;
  const WX1 = 760;
  const WY = -180;
  const freq = createSignal(3); // cycles across the wave
  const amp = createSignal(0);
  const phase = createSignal(0);

  view.add(
    <Node ref={buzzer} x={-660} y={WY} scale={0}>
      <Circle size={190} fill={'#14161c'} stroke={'#3a3f4c'} lineWidth={6} shadowColor={'rgba(0,0,0,0.5)'} shadowBlur={24} />
      <Circle size={120} stroke={'#2a2e38'} lineWidth={4} />
      <Circle size={30} fill={'#05060a'} />
      <Txt x={-48} y={-44} text={'+'} fontFamily={FONT.ui} fontWeight={900} fontSize={40} fill={C.dim} />
      <Circle ref={ring} size={200} stroke={C.teal} lineWidth={8} opacity={0} />
      {waves.map(w => (
        <Circle ref={w} size={200} stroke={C.amber} lineWidth={8} startAngle={-40} endAngle={40} opacity={0} />
      ))}
    </Node>,
  );
  view.add(
    <Line
      ref={wave}
      opacity={0}
      stroke={C.amber}
      lineWidth={7}
      lineCap={'round'}
      points={() => {
        const pts: [number, number][] = [];
        const n = 260;
        for (let i = 0; i <= n; i++) {
          const u = i / n;
          const x = WX0 + u * (WX1 - WX0);
          // soft fade at both ends of the wave
          const env = Math.min(1, u * 8, (1 - u) * 8);
          pts.push([x, WY + Math.sin((u * freq() + phase()) * Math.PI * 2) * amp() * env]);
        }
        return pts;
      }}
    />,
  );
  view.add(
    <Node ref={durBar} opacity={0}>
      <Line points={[[WX0, WY + 95], [WX0 + 0.3 * (WX1 - WX0), WY + 95]]} stroke={PINK} lineWidth={5} startArrow endArrow arrowSize={14} />
      <Txt x={WX0 + 0.15 * (WX1 - WX0)} y={WY + 135} text={'150 ms'} fontFamily={FONT.code} fontWeight={700} fontSize={36} fill={PINK} />
    </Node>,
  );
  view.add(
    <Code ref={code} y={50} highlighter={arduino} fontFamily={FONT.code} fontSize={84} code={''} />,
  );

  const h1 = new Headline('One line = one *beep*');
  view.add(h1.node());

  // label under a code token (bracket + text)
  function addLabel(token: string | RegExp, text: string, color: string, dy = 0) {
    const box = code().getSelectionBBox(code().findFirstRange(typeof token === 'string' ? lit(token) : token))[0];
    const left = toView(view, box.topLeft.transformAsPoint(code().localToWorld()));
    const right = toView(view, box.bottomRight.transformAsPoint(code().localToWorld()));
    const y = right.y + 18;
    const cx = (left.x + right.x) / 2;
    const ref = createRef<Node>();
    view.add(
      <Node ref={ref} opacity={0} y={20}>
        <Line
          points={[[left.x + 4, y], [left.x + 4, y + 18], [right.x - 4, y + 18], [right.x - 4, y]]}
          stroke={color}
          lineWidth={5}
        />
        <Line points={[[cx, y + 18], [cx, y + 44 + dy]]} stroke={color} lineWidth={5} />
        <Rect x={cx} y={y + 82 + dy} layout padding={[6, 20]} radius={14} fill={'rgba(13,22,40,0.9)'} stroke={color} lineWidth={3}>
          <Txt text={text} fontFamily={FONT.ui} fontWeight={800} fontSize={44} fill={color} />
        </Rect>
      </Node>,
    );
    return ref;
  }

  function* beep(times = 1) {
    for (let k = 0; k < times; k++) {
      yield* all(
        buzzer().scale(1.08, 0.06).to(1, 0.18),
        sequence(
          0.1,
          ...waves.map(w =>
            all(w().size(200, 0).to(420, 0.5, easeOutCubic), w().opacity(1, 0.05).to(0, 0.45)),
          ),
        ),
      );
    }
  }

  // full-code glimpse on top: the whole sketch, the GO beep line flies into place
  const glimpse = new SketchGlimpse({from: 84, to: 84, match: 'tone(BUZZER_PIN, 1500, 150);'});
  view.add(glimpse.node());
  code().code('tone(BUZZER_PIN, 1500, 150);');
  code().opacity(0);
  const ZOOM_AT = Math.min(1.1, Math.max(0.9, T.word('line', 1.1) - 0.1));
  yield glimpse.play(view, () => code().position(), 84 / SketchGlimpse.FONT, ZOOM_AT, 0.5);

  // ------------------------------------------------------------ beats
  yield loop(Infinity, () => phase(phase() + 1, 0.5, linear));
  yield* all(buzzer().scale(1, 0.45, easeOutBack), delay(0.1, h1.in()));
  yield* until(ZOOM_AT + 0.3);
  yield* code().opacity(1, 0.2);
  // the beep: a calm wave appears and keeps pulsing until "pin"
  yield* all(code().selection(code().findFirstRange('tone'), 0.25), h1.pulse(), beep(), amp(28, 0.4), wave().opacity(1, 0.3));
  const idle = yield loop(Infinity, function* () {
    yield* waitFor(0.5);
    yield* beep();
  });
  yield* until(Math.max(useTime(), T.word('pin', 2.8) - 0.2));
  cancel(idle);
  waves.forEach(w => w().opacity(0));
  buzzer().scale(1);

  // pin
  yield* until(Math.max(useTime(), T.word('pin', 2.8) - 0.2));
  const lPin = addLabel('BUZZER_PIN', 'pin', C.teal);
  yield* all(
    code().selection(code().findFirstRange('BUZZER_PIN'), 0.25),
    lPin().opacity(1, 0.25),
    lPin().y(0, 0.3, easeOutCubic),
    ring().opacity(1, 0.1).to(0, 0.6),
  );

  // how high: the wave appears and tightens
  yield* until(Math.max(useTime(), T.word('high', 4.2) - 0.25));
  const lHigh = addLabel('1500', 'how high', C.amber);
  yield* all(
    code().selection(code().findFirstRange('1500'), 0.25),
    lHigh().opacity(1, 0.25),
    lHigh().y(0, 0.3, easeOutCubic),
    amp(60, 0.3),
    freq(4, 0).to(16, 0.9, easeInOutCubic),
    beep(2),
  );

  // how long: the wave shrinks to a short burst
  yield* until(Math.max(useTime(), T.word('long', 5.8) - 0.25));
  const lLong = addLabel(/\b150\b/g, 'how long', PINK, 80);
  yield* all(
    code().selection(code().findFirstRange(/\b150\b/g), 0.25),
    lLong().opacity(1, 0.25),
    lLong().y(0, 0.3, easeOutCubic),
    wave().end(0.3, 0.5, easeInOutCubic),
    wave().stroke(PINK, 0.4),
    delay(0.3, durBar().opacity(1, 0.3)),
  );

  // whole line, beep on a loop until the end
  yield* until(Math.max(useTime(), Math.min(T.total - 1.6, useTime() + 0.8)));
  yield* all(code().selection(DEFAULT, 0.3), wave().stroke(C.amber, 0.3));
  yield loop(Infinity, function* () {
    yield* all(beep(), wave().opacity(1, 0.05).to(0.35, 0.4));
    yield* wave().opacity(1, 0.3);
  });
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
