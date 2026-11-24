/**
 * Ep11 s23 - "It's one line: last motion equals millis. Millis is the board's
 * stopwatch since power-on."   lastMotion = now;   (now = millis())
 * Full-code glimpse first; a stopwatch runs since power-on, its reading is
 * copied into the lastMotion box.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  createSignal,
  delay,
  easeOutBack,
  linear,
  useTime,
  Vector2,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, flyArc, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {glimpse11, timing11} from '../lib/ep11';
import {C, FONT} from '../style';

const T = timing11('code_last');
const fmt = (ms: number) => `${Math.floor(ms / 1000)} ${String(Math.floor(ms % 1000)).padStart(3, '0')}`;

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const ms = createSignal(754100);
  const saved = createSignal(0);
  const code = new CodePanel({y: -270, size: 72, code: 'lastMotion = now;'});
  const note = createRef<Rect>();
  const watch = createRef<Node>();
  const readout = createRef<Txt>();
  const box = createRef<Node>();
  const boxVal = createRef<Txt>();
  const fly = createRef<Txt>();
  const since = createRef<Rect>();

  const SW = new Vector2(-430, 70);
  view.add(
    <Node ref={watch} position={SW} opacity={0}>
      <Rect y={-168} width={46} height={30} radius={6} fill={C.metal} />
      <Circle size={300} fill={'#101a2c'} stroke={C.metal} lineWidth={10} />
      {Array.from({length: 12}, (_, i) => (
        <Line
          points={[Vector2.fromDegrees(i * 30).scale(112), Vector2.fromDegrees(i * 30).scale(128)]}
          stroke={C.dim}
          lineWidth={i % 3 ? 3 : 6}
        />
      ))}
      <Line
        points={() => [[0, 0], Vector2.fromDegrees(-90 + ((ms() % 1000) / 1000) * 360).scale(118)]}
        stroke={C.amber}
        lineWidth={7}
        lineCap={'round'}
      />
      <Circle size={22} fill={C.amber} />
      <Txt ref={readout} y={215} text={() => `${fmt(ms())} ms`} fontFamily={FONT.code} fontWeight={800} fontSize={48} fill={C.text} />
    </Node>,
  );
  view.add(
    <Node ref={box} x={430} y={70} opacity={0}>
      <Rect y={-98} x={-130} layout padding={[6, 18]} radius={[10, 10, 0, 0]} fill={C.teal}>
        <Txt text={'lastMotion'} fontFamily={FONT.code} fontWeight={800} fontSize={32} fill={C.bg} />
      </Rect>
      <Rect width={460} height={160} radius={18} fill={'#101a2c'} stroke={C.teal} lineWidth={4}>
        <Txt ref={boxVal} text={() => (saved() ? `${fmt(saved())} ms` : '0')} fontFamily={FONT.code} fontWeight={800} fontSize={52} fill={C.amber} />
      </Rect>
    </Node>,
  );
  view.add(<Pill refNode={note} text={'now = millis()'} color={C.amber} x={0} y={-150} size={36} />);
  view.add(<Pill refNode={since} text={'running since power-on'} color={C.teal} x={-430} y={-150} size={30} />);
  view.add(<Txt ref={fly} fontFamily={FONT.code} fontWeight={800} fontSize={48} fill={C.amber} opacity={0} />);
  view.add(code.node());

  const h1 = new Headline('Stamp it: *one* *line*');
  view.add(h1.node());

  const ZOOM_AT = 1.1;
  yield glimpse11(view, {from: 120, to: 122, match: 'lastMotion = now;'}, () => toView(view, code.code().absolutePosition()), 72, ZOOM_AT);

  // the stopwatch runs the whole time
  yield ms(ms() + T.total * 1000, T.total, linear);
  yield* all(delay(0.1, h1.in()), watch().opacity(1, 0.3), box().opacity(1, 0.3));
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);

  yield* until(Math.max(useTime(), T.word('last', 1.4) - 0.1));
  yield* code.code().selection(code.code().findFirstRange('lastMotion'), 0.25);
  // equals millis: the current reading is copied into the box
  yield* until(Math.max(useTime(), T.word('equals', 2.3) - 0.1));
  yield* all(code.code().selection(code.code().findFirstRange(lit('= now')), 0.25), popIn(note(), 0.3));
  const value = ms();
  fly().text(`${fmt(value)} ms`);
  const from = SW.add([0, 215]);
  fly().position(from).opacity(1).scale(1);
  yield* flyArc(fly(), from, new Vector2(430, 70), 160, 0.6);
  fly().opacity(0);
  saved(value);
  yield* all(boxVal().scale(1.2, 0.1).to(1, 0.3, easeOutBack), h1.pulse());

  // millis = the board's stopwatch since power-on
  yield* until(Math.max(useTime(), T.word('stopwatch', 5.0) - 0.3));
  yield* all(
    code.code().selection(code.code().findFirstRange('now'), 0.25),
    watch().scale(1.08, 0.15).to(1, 0.3, easeOutBack),
    popIn(since(), 0.3),
  );
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
