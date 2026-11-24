/**
 * Ep12 s12b - "Some links carry a detail, like a note on an order slip. In
 * slash color question mark c equals red, the note says which color."
 * An order slip (dish = /color, note = c = red) builds the link
 * /color?c=red token by token on the spoken words.
 */
import {Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, delay, easeOutBack, linear, tween, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {exact, Pill, popIn, toView, until} from '../lib/ep10';
import {Led, ledSignal, timing12} from '../lib/ep12';
import {C, FONT} from '../style';

const T = timing12('order_slip');
const PEN = '#c0392b';
const TOKENS = [
  {t: '/color', c: C.teal, w: 'color'},
  {t: '?', c: C.dim, w: 'question'},
  {t: 'c', c: C.amber, w: 'c'},
  {t: '=', c: C.dim, w: 'equals'},
  {t: 'red', c: '#ff6b6b', w: 'red'},
];

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const slip = createRef<Node>();
  const note = createRef<Txt>();
  const noteLine = createRef<Line>();
  const noteText = 'c = red';
  const url = createRef<Rect>();
  const toks = TOKENS.map(() => createRef<Txt>());
  const detail = createRef<Rect>();
  const led = createRef<Node>();
  const ledColor = ledSignal();

  view.add(
    <Node ref={slip} x={-520} y={50} rotation={-3} opacity={0}>
      <Rect width={430} height={540} radius={8} fill={'#fbf8ef'} shadowColor={'rgba(0,0,0,0.5)'} shadowBlur={30} shadowOffsetY={10} />
      <Txt y={-215} text={'ORDER SLIP'} fontFamily={FONT.ui} fontWeight={900} fontSize={40} letterSpacing={6} fill={'#2a2418'} />
      <Line points={[[-170, -175], [170, -175]]} stroke={'#d6cdb6'} lineWidth={3} lineDash={[8, 6]} />
      <Txt x={-170} y={-120} offsetX={-1} text={'table 1'} fontFamily={FONT.ui} fontSize={28} fill={'#8a7f6a'} />
      <Txt x={-170} y={-50} offsetX={-1} text={'dish:'} fontFamily={FONT.ui} fontWeight={700} fontSize={32} fill={'#2a2418'} />
      <Txt x={-60} y={-50} offsetX={-1} text={'/color'} fontFamily={FONT.code} fontWeight={800} fontSize={40} fill={'#1b2a4a'} />
      <Txt x={-170} y={40} offsetX={-1} text={'note:'} fontFamily={FONT.ui} fontWeight={700} fontSize={32} fill={'#2a2418'} />
      <Txt ref={note} x={-60} y={40} offsetX={-1} text={''} fontFamily={'Segoe Print'} fontWeight={700} fontSize={46} fill={PEN} />
      <Line ref={noteLine} points={[[-64, 82], [130, 78]]} stroke={PEN} lineWidth={4} end={0} />
      {[140, 200].map(y => (
        <Line points={[[-170, y], [170, y]]} stroke={'#e6dfcc'} lineWidth={3} />
      ))}
    </Node>,
  );
  view.add(
    <Rect ref={url} x={380} y={-110} layout gap={6} alignItems="center" padding={[16, 30]} radius={18} fill={'#101a2c'} stroke={C.line} lineWidth={3} opacity={0}>
      {TOKENS.map((k, i) => (
        <Txt ref={toks[i]} text={k.t} fontFamily={FONT.code} fontWeight={800} fontSize={84} fill={k.c} opacity={i === 0 ? 1 : 0} />
      ))}
    </Rect>,
  );
  view.add(<Pill refNode={detail} text={'+ a detail'} color={C.amber} x={380} y={-250} size={34} />);
  view.add(<Led refNode={led} color={ledColor} x={380} y={230} scale={0.7} />);

  const h1 = new Headline('A link with a *note*');
  view.add(h1.node());

  // brackets + labels under parts of the link (built once the link is complete)
  const bracket = (from: number, to: number, text: string, color: string) => {
    const a = toView(view, toks[from]().absolutePosition()).sub([toks[from]().width() / 2, 0]);
    const b = toView(view, toks[to]().absolutePosition()).add([toks[to]().width() / 2, 0]);
    const y = a.y + 64;
    const ref = createRef<Node>();
    view.add(
      <Node ref={ref} opacity={0}>
        <Line points={[[a.x, y], [a.x, y + 16], [b.x, y + 16], [b.x, y]]} stroke={color} lineWidth={4} />
        <Txt x={(a.x + b.x) / 2} y={y + 52} text={text} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={color} />
      </Node>,
    );
    return ref;
  };

  // ------------------------------------------------------------ beats
  yield* delay(0.05, h1.in());
  // some links ... carry a detail
  yield* until(Math.max(useTime(), T.word('links', 0.3) - 0.1));
  yield* all(url().opacity(1, 0.3), url().position.y(-110, 0.3));
  yield* until(Math.max(useTime(), T.word('detail', 1.1) - 0.1));
  yield* popIn(detail(), 0.3);

  // like a note on an order slip
  yield* until(Math.max(useTime(), T.word('note', 2.4) - 0.3));
  slip().x(-700);
  yield* all(slip().opacity(1, 0.3), slip().x(-520, 0.5, easeOutBack), h1.pulse());
  yield* until(Math.max(useTime(), T.word('slip', 3.3) - 0.3));
  yield* tween(0.6, v => note().text(noteText.slice(0, Math.round(v * noteText.length))));
  yield* noteLine().end(1, 0.3);

  // In /color ? c = red : each token appears on its word
  yield* detail().opacity(0, 0.2);
  for (let i = 1; i < TOKENS.length; i++) {
    yield* until(Math.max(useTime(), T.word(TOKENS[i].w, 4.6 + i * 0.5, undefined, TOKENS[i].w === 'c' ? 2 : 0) - 0.12));
    const tk = toks[i]();
    tk.opacity(1).scale(0.3);
    yield* all(tk.scale(1.35, 0.1).to(1, 0.25, easeOutBack));
  }

  // the note says which color
  const lDish = bracket(0, 0, 'the dish', C.teal);
  const lNote = bracket(2, 4, 'the note', '#ff6b6b');
  yield* until(Math.max(useTime(), T.word('note', T.total - 2.6, undefined, 1) - 0.2));
  yield* all(lDish().opacity(1, 0.3), delay(0.15, lNote().opacity(1, 0.3)));
  yield* until(Math.max(useTime(), T.word('color', T.total - 1.4, undefined, 1) - 0.3));
  ledColor('#e5484d');
  yield* all(led().scale(0.85, 0.12).to(0.7, 0.3, easeOutBack), toks[4]().scale(1.2, 0.12).to(1, 0.25));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));

