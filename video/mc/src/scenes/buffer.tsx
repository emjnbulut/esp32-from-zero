/**
 * Ep10 s21+s22 - the screen buffer.
 * s21: print() draws on a whiteboard behind a curtain; the OLED stays dark.
 * s22: display() opens the curtain; the whole picture appears at once.
 */
import {Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
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
  tween,
  useTime,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Oled} from '../lib/oled';
import {CodePanel, Pill, popIn, popOut, timing, until, exact} from '../lib/ep10';
import {C, FONT} from '../style';

const T = timing('buffer');
const INK = '#1b2a4a';

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);
  const S22 = T.seg('s22').start;

  const SX = -430; // stage centre
  const SY = -70;
  const stage = createRef<Node>();
  const small = createSignal('');
  const big = createSignal('');
  const pen = createRef<Node>();
  const curtL = createRef<Rect>();
  const curtR = createRef<Rect>();
  const boardLbl = createRef<Rect>();
  const beam = createRef<Rect>();
  const nothing = createRef<Rect>();
  const ok1 = createRef<Rect>();
  const ok2 = createRef<Rect>();

  const oled = new Oled({x: 470, y: SY, scale: 0.8, label: 'READY', value: 'GO!', unit: ''});

  const folds = (w: number) =>
    [0.2, 0.4, 0.6, 0.8].map(f => (
      <Line points={[[-w / 2 + f * w, -150], [-w / 2 + f * w, 160]]} stroke={'rgba(0,0,0,0.28)'} lineWidth={10} />
    ));

  view.add(
    <Node ref={stage} x={SX} y={SY}>
      {/* frame + whiteboard */}
      <Rect width={660} height={380} radius={18} fill={'#2a3550'} stroke={'#3a4766'} lineWidth={4} shadowColor={'rgba(0,0,0,0.5)'} shadowBlur={30} shadowOffsetY={10} />
      <Rect width={600} height={300} radius={8} fill={'#eef2f7'} y={10}>
        <Txt x={-270} y={-100} offsetX={-1} text={small} fontFamily={FONT.code} fontWeight={700} fontSize={50} fill={INK} />
        <Txt x={-276} y={30} offsetX={-1} text={big} fontFamily={FONT.code} fontWeight={800} fontSize={150} fill={INK} />
        <Node ref={pen} x={-250} y={-60} rotation={28} opacity={0}>
          <Rect y={-50} width={26} height={110} radius={6} fill={C.teal} />
          <Rect y={8} width={16} height={18} radius={3} fill={INK} />
        </Node>
      </Rect>
      {/* curtains */}
      <Rect ref={curtL} x={-300} y={10} offsetX={-1} width={302} height={320} fill={'#a3263b'} clip>
        {folds(302)}
      </Rect>
      <Rect ref={curtR} x={300} y={10} offsetX={1} width={302} height={320} fill={'#a3263b'} clip>
        {folds(302)}
      </Rect>
      <Rect y={-160} width={660} height={44} radius={[18, 18, 6, 6]} fill={'#7d1a2c'} />
      <Rect ref={boardLbl} y={225} layout gap={12} padding={[6, 20]} radius={12} fill={'rgba(45,212,191,0.12)'} opacity={0}>
        <Txt text={'whiteboard'} fontFamily={FONT.ui} fontWeight={800} fontSize={32} fill={C.teal} />
        <Txt text={'= the board’s memory'} fontFamily={FONT.ui} fontSize={32} fill={C.text} />
      </Rect>
    </Node>,
  );
  view.add(oled.node());
  oled.content().opacity(0);
  view.add(
    <Rect
      ref={beam}
      x={20}
      y={SY + 10}
      width={0}
      height={240}
      fill={'rgba(255,240,200,0.0)'}
      radius={20}
    />,
  );
  view.add(<Pill refNode={nothing} text={'screen: still dark'} color={C.dim} x={470} y={SY + 220} size={34} />);
  view.add(<Pill refNode={ok1} text={'no flicker ✓'} color={C.teal} x={470} y={SY + 215} size={34} />);
  view.add(<Pill refNode={ok2} text={'no half-drawn words ✓'} color={C.teal} x={470} y={SY + 290} size={34} />);

  const code = new CodePanel({x: SX, y: 270, size: 52});
  view.add(code.node());

  const h1 = new Headline('Drawn *behind* a *curtain*');
  const h2 = new Headline('display() → the *curtain* *opens*', {accent: C.teal});
  view.add(h1.node());
  view.add(h2.node());

  // ------------------------------------------------------------ s21
  stage().scale(0.9).opacity(0);
  oled.root().scale(0.7).opacity(0);
  yield* all(
    stage().scale(1, 0.4, easeOutBack),
    stage().opacity(1, 0.25),
    oled.root().scale(0.8, 0.4, easeOutBack),
    oled.root().opacity(1, 0.25),
    delay(0.1, h1.in()),
  );
  // curtains sway gently all the time while closed
  const sway = loop(Infinity, () =>
    all(curtL().skew.y(1.5, 0.7, easeInOutCubic).to(-1.5, 0.7, easeInOutCubic), curtR().skew.y(-1.5, 0.7, easeInOutCubic).to(1.5, 0.7, easeInOutCubic)),
  );
  yield sway;

  yield* until(Math.max(0.9, T.word('print', 2.6, 's21') - 0.7));
  yield* code.show();
  // curtain turns see-through so we can peek: the pen draws, the OLED stays dark
  yield* all(
    code.code().code('screen.print("GO!");', 0.5),
    delay(0.2, all(curtL().opacity(0.55, 0.3), curtR().opacity(0.55, 0.3), pen().opacity(1, 0.2))),
  );
  yield tween(0.5, v => small('READY'.slice(0, Math.round(v * 5))));
  yield* tween(0.5, v => pen().position([-250 + v * 170, -110 + Math.sin(v * 18) * 6]));
  yield* code.code().selection(code.code().findFirstRange('print'), 0.25);
  yield tween(0.6, v => big('GO!'.slice(0, Math.round(v * 3))));
  yield* tween(0.6, v => pen().position([-200 + v * 260, 40 + Math.sin(v * 14) * 18]));
  yield* all(pen().opacity(0, 0.2), popIn(nothing(), 0.3), oled.root().rotation(2, 0.06).to(-2, 0.08).to(0, 0.06));

  yield* until(Math.max(useTime(), T.word('whiteboard', S22 - 2.4, 's21') - 0.2));
  yield* all(popIn(boardLbl(), 0.3, 1));
  yield* until(Math.max(useTime(), T.word('curtain', S22 - 1, 's21') - 0.1));
  yield* all(h1.pulse(), curtL().opacity(1, 0.3), curtR().opacity(1, 0.3));

  // ------------------------------------------------------------ s22
  yield* until(S22 - 0.2);
  yield* all(
    h1.out(),
    delay(0.3, h2.in()),
    code.code().selection(DEFAULT, 0.2),
    code.code().code('screen.display();', 0.5),
    boardLbl().opacity(0, 0.3),
  );
  yield* until(Math.max(useTime(), T.word('display', S22 + 1.2, 's22') - 0.2));
  yield* all(
    code.code().selection(code.code().findFirstRange('display'), 0.25),
    code.panel().scale(1.08, 0.15).to(1, 0.3, easeOutBack),
    code.panel().stroke(C.teal, 0.2),
  );
  // the curtain opens on "the curtain opens"
  yield* until(Math.max(useTime(), T.word('curtain', S22 + 3, 's22') - 0.15));
  yield* all(
    curtL().scale.x(0.1, 0.45, easeInOutCubic),
    curtR().scale.x(0.1, 0.45, easeInOutCubic),
    h2.pulse(),
  );
  // the whole picture jumps to the OLED at once
  yield* all(
    popOut(nothing(), 0.15),
    beam().width(560, 0.18, easeOutCubic),
    beam().fill('rgba(255,240,200,0.25)', 0.18),
  );
  oled.content().opacity(1);
  oled.content().scale(1);
  yield* all(
    beam().fill('rgba(255,240,200,0)', 0.3),
    beam().x(300, 0.3),
    beam().width(0, 0.3),
    oled.board().scale(1.06, 0.1).to(1, 0.3, easeOutBack),
    oled.screen().fill('#1c2433', 0.04).to(C.oledBlack, 0.25),
  );
  yield* until(Math.max(useTime(), T.word('flicker', S22 + 4.5, 's22') - 0.2));
  yield* popIn(ok1(), 0.3);
  yield* until(Math.max(useTime(), T.word('half', S22 + 5.5, 's22') - 0.2));
  yield* popIn(ok2(), 0.3);

  // hold: OLED glow breathes
  const glow = createSignal(0);
  oled.value().shadowBlur(() => 18 + glow() * 18);
  yield loop(Infinity, () => glow(1, 0.6).to(0, 0.6));
  yield all(grid().opacity(0.6, 1.2, linear), sequence(0.1, ok1().scale(1.05, 0.3).to(1, 0.3), ok2().scale(1.05, 0.3).to(1, 0.3)));
  yield* until(T.total);
}));
