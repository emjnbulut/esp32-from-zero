/**
 * Ep10 s23 - the show() helper: clear, small line on top, big line in the
 * middle, display. Then one call show("READY", "GO!") fills the OLED.
 */
import {Circle, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
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
  Reference,
  sequence,
  tween,
  useTime,
  Vector2,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Oled} from '../lib/oled';
import {burst, CodePanel, lit, timing, toView, until, exact} from '../lib/ep10';
import {SketchGlimpse} from '../lib/glimpse';
import {C, FONT} from '../style';

const T = timing('code_show');

function Step(props: {refNode: Reference<Rect>; n: number; text: string; code?: string; y: number}) {
  return (
    <Rect
      ref={props.refNode}
      x={-480}
      y={props.y}
      width={620}
      height={96}
      radius={18}
      fill={'#15223a'}
      stroke={C.line}
      lineWidth={3}
      opacity={0}
    >
      <Circle x={-262} size={60} fill={C.amber}>
        <Txt text={String(props.n)} fontFamily={FONT.ui} fontWeight={900} fontSize={36} fill={C.bg} />
      </Circle>
      <Txt x={-210} offsetX={-1} text={props.text} fontFamily={FONT.ui} fontWeight={700} fontSize={38} fill={C.text} />
      {props.code ? (
        <Txt x={290} offsetX={1} text={props.code} fontFamily={FONT.code} fontWeight={700} fontSize={32} fill={C.teal} />
      ) : null}
    </Rect>
  );
}

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const steps = [createRef<Rect>(), createRef<Rect>(), createRef<Rect>(), createRef<Rect>()];
  const wipe = createRef<Rect>();
  const oled = new Oled({x: 450, y: 40, scale: 0.78, label: 'best:', value: '214', unit: 'ms'});
  const code = new CodePanel({y: -285, size: 60, chip: 'HELPER', code: 'show(top, big)'});
  const topTxt = createSignal('');
  const bigTxt = createSignal('');

  const data = [
    {text: 'clear', code: 'clearDisplay()'},
    {text: 'small line on top', code: ''},
    {text: 'big line in the middle', code: ''},
    {text: 'open the curtain', code: 'display()'},
  ];
  view.add(
    <Node>
      {data.map((d, i) => (
        <Step refNode={steps[i]} n={i + 1} text={d.text} code={d.code} y={-150 + i * 120} />
      ))}
    </Node>,
  );
  view.add(oled.node());
  oled.screen().add(<Rect ref={wipe} x={-340} width={80} height={300} fill={'rgba(150,200,255,0.5)'} opacity={0} />);
  view.add(code.node());

  const h1 = new Headline('One helper: *show()*');
  view.add(h1.node());

  // dashed frame that "wraps" the four steps into one helper
  const wrap = createRef<Rect>();
  view.add(
    <Rect
      ref={wrap}
      x={-480}
      y={30}
      width={680}
      height={480}
      radius={26}
      stroke={C.amber}
      lineWidth={4}
      lineDash={[16, 12]}
      end={0}
    />,
  );

  // ------------------------------------------------------------ beats
  const fallbacks = [0.36, 0.52, 0.68, 0.85].map(f => f * T.total);
  const words = ['clears', 'small', 'big', 'opens'];
  const at = words.map((w, i) => Math.max(T.word(w, fallbacks[i]) - 0.15, 0));
  // step 4 doubles as the final call; it needs ~1.4 s before the scene ends
  at[3] = Math.min(at[3], T.total - 1.5);
  for (let i = 2; i >= 0; i--) at[i] = Math.min(at[i], at[i + 1] - 0.55);

  // full-code glimpse on top: the whole show() function, its header flies into the code panel
  const glimpse = new SketchGlimpse({from: 29, to: 40, match: 'show(const char* top, String big)'});
  view.add(glimpse.node());
  const ZOOM_AT = 1.1;
  yield glimpse.play(view, () => toView(view, code.code().absolutePosition()), 60 / SketchGlimpse.FONT, ZOOM_AT, 0.5);

  // intro: OLED + the four (dim) steps, then they get wrapped into show()
  oled.root().scale(0.6).opacity(0);
  steps.forEach(s => s().x(-520));
  yield all(loop(Infinity, () => oled.root().position.y(30, 1, easeInOutCubic).to(40, 1, easeInOutCubic)));
  yield* all(
    delay(0.05, h1.in()),
    oled.root().scale(0.78, 0.45, easeOutBack),
    oled.root().opacity(1, 0.3),
    sequence(0.1, ...steps.map(s => all(s().opacity(0.45, 0.25), s().x(-480, 0.3, easeOutCubic)))),
  );
  // the glimpse clears: the helper's code panel is already in place, then the wrap
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);
  yield* all(wrap().end(1, 0.5, easeInOutCubic), ...steps.map(s => s().scale(0.96, 0.5)));
  yield* until(Math.max(useTime(), T.word('helper', 1.6) - 0.2));
  yield* all(wrap().stroke(C.teal, 0.3), h1.pulse());
  yield* until(Math.max(useTime(), T.word('show', 2.6) - 0.1));
  yield* code.code().selection(code.code().findFirstRange('show'), 0.25);

  const stepIn = (i: number) =>
    all(
      steps[i]().opacity(1, 0.2),
      steps[i]().scale(1.02, 0.12).to(0.96, 0.2),
      steps[i]().stroke(C.amber, 0.15),
      steps[i]().x(-460, 0.12).to(-480, 0.2),
    );
  const stepDone = (i: number) => steps[i]().stroke(C.line, 0.3);

  // 1 clear: wipe the old screen
  yield* until(Math.max(useTime(), at[0]));
  yield* all(
    code.code().selection(DEFAULT, 0.2),
    stepIn(0),
    wipe().opacity(1, 0.05),
    wipe().x(340, 0.4, easeInOutCubic),
    delay(0.2, oled.content().opacity(0, 0.15)),
  );
  wipe().opacity(0);
  oled.label().text(topTxt);
  oled.value().text(bigTxt);
  oled.unit().text('');
  // drawn behind the curtain = ghost (dim) until display()
  oled.content().opacity(0.38);

  // 2 small line on top
  yield* until(Math.max(useTime(), at[1]));
  yield* all(stepDone(0), stepIn(1), tween(0.4, v => topTxt('top'.slice(0, Math.round(v * 3)))));
  // 3 big line in the middle
  yield* until(Math.max(useTime(), at[2]));
  yield* all(stepDone(1), stepIn(2), tween(0.4, v => bigTxt('big'.slice(0, Math.round(v * 3)))));

  // 4 open the curtain = the real call: show("READY", "GO!") lights the screen at once
  yield* until(Math.max(useTime(), at[3]));
  yield* all(
    stepDone(2),
    stepIn(3),
    code.chip().fill(C.teal, 0.25),
    code.chipTxt().text('CALL', 0.25),
    code.code().code('show("READY", "GO!");', 0.4),
  );
  topTxt('READY');
  bigTxt('GO!');
  const c = oled.root().position();
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('"READY", "GO!"')), 0.2),
    oled.content().opacity(1, 0.06),
    oled.screen().fill('#1c2433', 0.04).to(C.oledBlack, 0.3),
    oled.board().scale(1.05, 0.1).to(1, 0.3, easeOutBack),
    oled.value().scale(1.3, 0.1, easeOutCubic).to(1, 0.3, easeOutBack),
    burst(view, new Vector2(c.x - 60, c.y + 40), [C.amber, C.teal, C.text], 220),
  );

  const glow = createSignal(0);
  oled.value().shadowBlur(() => 18 + glow() * 18);
  yield loop(Infinity, () => glow(1, 0.55).to(0, 0.55));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
