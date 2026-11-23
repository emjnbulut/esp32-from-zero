/**
 * Ep10 s20 - a free library, installed once from the Library Manager.
 * Stylised Library Manager card: search types "SSD1306", the
 * "Adafruit SSD1306" row appears, INSTALL is clicked, progress, INSTALLED.
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
  tween,
  useTime,
  Vector2,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {burst, popIn, timing, until, exact} from '../lib/ep10';
import {C, FONT} from '../style';

const T = timing('code_screen');

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const card = createRef<Rect>();
  const query = createSignal('');
  const caret = createRef<Rect>();
  const row = createRef<Rect>();
  const btn = createRef<Rect>();
  const btnTxt = createRef<Txt>();
  const prog = createRef<Rect>();
  const progFill = createRef<Rect>();
  const cursor = createRef<Node>();
  const free = createRef<Rect>();
  const stamp = createRef<Rect>();
  const extras = createRef<Txt>();

  const CW = 1240;
  const CH = 470;
  const CY = -30;
  view.add(
    <Rect
      ref={card}
      y={CY}
      width={CW}
      height={CH}
      radius={24}
      fill={'#121c30'}
      stroke={'#2a3a5c'}
      lineWidth={3}
      shadowColor={'rgba(0,0,0,0.5)'}
      shadowBlur={40}
      shadowOffsetY={14}
      clip
    >
      {/* title bar */}
      <Rect y={-CH / 2 + 40} width={CW} height={80} fill={'#18243d'} />
      {[0, 1, 2].map(i => (
        <Circle x={-CW / 2 + 40 + i * 32} y={-CH / 2 + 40} size={18} fill={['#ff5f57', '#febc2e', '#28c840'][i]} />
      ))}
      <Txt
        x={-CW / 2 + 160}
        y={-CH / 2 + 40}
        offsetX={-1}
        text={'LIBRARY MANAGER'}
        fontFamily={FONT.ui}
        fontWeight={800}
        fontSize={34}
        letterSpacing={3}
        fill={C.text}
      />
      {/* search box */}
      <Rect
        x={0}
        y={-CH / 2 + 140}
        width={CW - 80}
        height={76}
        radius={14}
        fill={'#0b1322'}
        stroke={C.teal}
        lineWidth={3}
      >
        <Circle x={-(CW - 80) / 2 + 44} y={-4} size={30} stroke={C.dim} lineWidth={5} />
        <Line points={[[-(CW - 80) / 2 + 54, 8], [-(CW - 80) / 2 + 66, 20]]} stroke={C.dim} lineWidth={5} lineCap={'round'} />
        <Txt
          x={-(CW - 80) / 2 + 90}
          offsetX={-1}
          text={query}
          fontFamily={FONT.code}
          fontSize={44}
          fill={C.text}
        />
        <Rect
          ref={caret}
          x={() => -(CW - 80) / 2 + 96 + query().length * 24.2}
          width={4}
          height={46}
          fill={C.teal}
        />
      </Rect>
      {/* result row */}
      <Rect
        ref={row}
        y={60}
        width={CW - 80}
        height={210}
        radius={18}
        fill={'#18243d'}
        stroke={C.line}
        lineWidth={2}
        opacity={0}
      >
        <Txt
          x={-(CW - 80) / 2 + 40}
          y={-50}
          offsetX={-1}
          text={'Adafruit SSD1306'}
          fontFamily={FONT.ui}
          fontWeight={800}
          fontSize={56}
          fill={C.text}
        />
        <Txt
          x={-(CW - 80) / 2 + 40}
          y={20}
          offsetX={-1}
          text={'by Adafruit  ·  for small OLED screens'}
          fontFamily={FONT.ui}
          fontSize={34}
          fill={C.dim}
        />
        <Txt
          ref={extras}
          x={-(CW - 80) / 2 + 40}
          y={70}
          offsetX={-1}
          text={'+ Adafruit GFX, BusIO'}
          fontFamily={FONT.ui}
          fontSize={28}
          fill={C.teal}
          opacity={0}
        />
        <Rect
          ref={btn}
          x={(CW - 80) / 2 - 170}
          y={-10}
          width={270}
          height={84}
          radius={14}
          fill={C.teal}
        >
          <Txt ref={btnTxt} text={'INSTALL'} fontFamily={FONT.ui} fontWeight={800} fontSize={38} fill={C.bg} />
        </Rect>
        <Rect
          ref={prog}
          x={(CW - 80) / 2 - 170}
          y={62}
          width={270}
          height={14}
          radius={7}
          fill={'#0b1322'}
          opacity={0}
        >
          <Rect ref={progFill} x={-135} offsetX={-1} width={0} height={14} radius={7} fill={C.amber} />
        </Rect>
      </Rect>
    </Rect>,
  );
  view.add(
    <Rect
      ref={free}
      x={CW / 2 - 110}
      y={CY - CH / 2 + 40}
      layout
      padding={[6, 22]}
      radius={30}
      fill={C.amber}
      opacity={0}
      scale={0.4}
      rotation={6}
    >
      <Txt text={'FREE'} fontFamily={FONT.ui} fontWeight={900} fontSize={40} fill={C.bg} />
    </Rect>,
  );
  // mouse cursor
  view.add(
    <Node ref={cursor} position={[700, 420]} opacity={0}>
      <Line
        points={[[0, 0], [0, 56], [14, 42], [26, 68], [36, 63], [24, 38], [44, 38]]}
        closed
        fill={C.text}
        stroke={C.bg}
        lineWidth={3}
      />
    </Node>,
  );
  view.add(
    <Rect
      ref={stamp}
      x={0}
      y={292}
      layout
      direction="row"
      alignItems="center"
      gap={16}
      padding={[10, 30]}
      radius={18}
      stroke={C.amber}
      lineWidth={6}
      fill={'rgba(11,18,32,0.9)'}
      rotation={-4}
      opacity={0}
      scale={2}
    >
      <Txt text={'1×'} fontFamily={FONT.ui} fontWeight={900} fontSize={64} fill={C.amber} />
      <Txt text={'INSTALL ONCE'} fontFamily={FONT.ui} fontWeight={900} fontSize={46} fill={C.amber} />
    </Rect>,
  );

  const h1 = new Headline('A free *library* does the talking');
  view.add(h1.node());

  const btnAbs = () => new Vector2((CW - 80) / 2 - 170, CY + 60 - 10);

  // ------------------------------------------------------------ beats
  card().scale(0.9).opacity(0);
  yield all(loop(Infinity, () => caret().opacity(0, 0.25).to(1, 0.25)));
  yield* all(card().scale(1, 0.4, easeOutBack), card().opacity(1, 0.25), delay(0.1, h1.in()));

  // type the search
  const word = 'SSD1306';
  yield* tween(0.7, v => query(word.slice(0, Math.round(v * word.length))));
  yield* all(row().opacity(1, 0.25), row().position.y(60, 0.3, easeOutCubic));
  yield* until(Math.max(1.6, T.word('free', 1.8) - 0.1));
  yield* all(popIn(free(), 0.35), h1.pulse());

  // cursor moves to INSTALL and clicks
  const tClick = Math.max(2.5, Math.min(T.word('install', T.total * 0.5) - 0.2, T.total - 4));
  yield all(cursor().opacity(1, 0.2), cursor().position(btnAbs().add([20, 30]), 0.7, easeInOutCubic));
  yield* until(tClick);
  yield* all(
    btn().scale(0.9, 0.08).to(1, 0.15),
    btn().fill('#1aa391', 0.08),
    cursor().scale(0.85, 0.08).to(1, 0.12),
  );
  btnTxt().text('INSTALLING');
  btnTxt().fontSize(30);
  yield cursor().position(btnAbs().add([240, 170]), 0.6, easeInOutCubic);
  // "once" stamp lands on its spoken word, even while the install still runs
  const tOnce = Math.max(useTime() + 0.3, T.word('once', T.total - 2.5) + 0.1);
  yield delay(tOnce - useTime(), function* () {
    yield* all(stamp().opacity(1, 0.12), stamp().scale(1, 0.25, easeOutCubic));
    yield* card().position.x(-10, 0.04).to(10, 0.06).to(0, 0.05);
    yield* stamp().scale(1.04, 0.6, easeInOutCubic).to(1, 0.6, easeInOutCubic);
  }());
  yield* prog().opacity(1, 0.15);
  const fillDur = Math.max(0.7, Math.min(1.1, T.total - tClick - 2.4));
  yield* all(
    progFill().width(270, fillDur, easeInOutCubic),
    delay(fillDur * 0.4, extras().opacity(1, 0.3)),
    cursor().opacity(0, 0.4),
  );
  btnTxt().text('INSTALLED ✓');
  yield* all(
    prog().opacity(0, 0.2),
    btn().fill(C.amber, 0.2),
    btn().scale(1.12, 0.12).to(1, 0.25, easeOutBack),
    burst(view, btnAbs().add([0, 0]), [C.amber, C.teal, C.text], 160),
  );
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
