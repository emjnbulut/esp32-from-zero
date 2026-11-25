/**
 * Ep15 s08 - "Careful: many of these modules give a higher number in the
 * dark. One line in the code flips it, so for us zero always means dark."
 *   int readLight() { ... average 8 looks (Episode 7) ...
 *     return DARK_IS_HIGH ? 4095 - raw : raw; }
 * Glimpse -> the flip line (line 52: the sketch's two columns split readLight()); the module says 3900 in the dark (?!), the flip
 * turns it into 4095 - 3900 = 195; a dark..bright strip: 0 = dark.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt, Gradient} from '@motion-canvas/2d';
import {all, createRef, easeOutBack, easeOutCubic, linear, Reference, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {glimpse15, timing15} from '../lib/ep15';
import {C, FONT} from '../style';

const T = timing15('code_read');
const FLIP = 'return DARK_IS_HIGH ? 4095 - raw : raw;';
const CODE = [
  'int readLight() {',
  '  long sum = 0;',
  '  for (int i = 0; i < 8; i++) sum += analogRead(LDR_PIN);',
  '  int raw = sum / 8;',
  '  ' + FLIP,
  '}',
].join('\n');

const RAW = 3900;
const FLIPPED = 4095 - RAW;
const CARD_Y = 105;
const STRIP_Y = 300;
const SX0 = -520;
const SX1 = 520;

function Card(props: {refNode: Reference<Rect>; x: number; title: string; value: string; color: string; sub: string}) {
  return (
    <Rect
      ref={props.refNode}
      x={props.x}
      y={CARD_Y}
      width={400}
      height={220}
      radius={22}
      fill={'rgba(13,22,40,0.95)'}
      stroke={props.color}
      lineWidth={3}
      opacity={0}
      scale={0.6}
    >
      <Txt y={-70} text={props.title} fontFamily={FONT.ui} fontWeight={700} fontSize={32} fill={C.dim} />
      <Txt y={10} text={props.value} fontFamily={FONT.code} fontWeight={800} fontSize={96} fill={props.color} />
      <Txt y={80} text={props.sub} fontFamily={FONT.ui} fontWeight={700} fontSize={28} fill={props.color} />
    </Rect>
  );
}

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -222, size: 31, code: CODE});
  const avg = createRef<Rect>();
  const rawCard = createRef<Rect>();
  const flipCard = createRef<Rect>();
  const huh = createRef<Rect>();
  const arrow = createRef<Node>();
  const strip = createRef<Node>();
  const marker = createRef<Node>();
  const zeroTxt = createRef<Txt>();

  view.add(<Pill refNode={avg} text={'average of 8 looks (Episode 7)'} color={C.dim} x={0} y={-25} size={28} />);
  view.add(<Card refNode={rawCard} x={-470} title={'☾ dark: module says'} value={String(RAW)} color={C.red} sub={'higher?!'} />);
  view.add(<Card refNode={flipCard} x={470} title={'after the flip'} value={String(FLIPPED)} color={C.teal} sub={'low = dark ✓'} />);
  view.add(
    <Node ref={arrow} y={CARD_Y} opacity={0}>
      <Txt y={-46} text={`4095 − ${RAW}`} fontFamily={FONT.code} fontWeight={800} fontSize={40} fill={C.amber} />
      <Line points={[[-150, 20], [150, 20]]} stroke={C.amber} lineWidth={6} endArrow arrowSize={18} />
    </Node>,
  );
  view.add(<Pill refNode={huh} text={'flipped!'} color={C.amber} x={0} y={CARD_Y + 90} size={30} />);
  view.add(
    <Node ref={strip} y={STRIP_Y} opacity={0}>
      <Rect
        width={SX1 - SX0}
        height={40}
        radius={20}
        stroke={C.line}
        lineWidth={3}
        fill={
          new Gradient({
            type: 'linear',
            from: [SX0, 0],
            to: [SX1, 0],
            stops: [
              {offset: 0, color: '#03050a'},
              {offset: 0.5, color: '#6b5a2a'},
              {offset: 1, color: '#fff3c4'},
            ],
          })
        }
      />
      <Txt ref={zeroTxt} x={SX0 - 30} offsetX={1} text={'0 = dark'} fontFamily={FONT.ui} fontWeight={800} fontSize={36} fill={C.teal} />
      <Txt x={SX1 + 30} offsetX={-1} text={'4095 = bright'} fontFamily={FONT.ui} fontWeight={800} fontSize={36} fill={C.amber} />
      <Node ref={marker} x={SX0 + ((SX1 - SX0) * FLIPPED) / 4095}>
        <Line points={[[0, -36], [0, 36]]} stroke={C.teal} lineWidth={6} />
        <Circle y={-44} size={18} fill={C.teal} />
      </Node>
    </Node>,
  );
  view.add(code.node());

  const h1 = new Headline('Careful: *dark* can read *high*', {accent: C.red});
  view.add(h1.node());

  const lineCenter = () => {
    const c = code.code();
    const box = c.getSelectionBBox(c.findFirstRange(lit(FLIP)))[0];
    return toView(view, box.center.transformAsPoint(c.localToWorld()));
  };
  const ZOOM_AT = 1.1;
  yield glimpse15(view, {from: 52, to: 52, match: FLIP}, lineCenter, 31, ZOOM_AT);

  yield* h1.in();
  yield* until(ZOOM_AT + 0.3);
  yield* all(
    code.panel().opacity(1, 0.2),
    code.code().selection(code.code().findFirstRange(lit('for (int i = 0; i < 8; i++) sum += analogRead(LDR_PIN);')), 0.25),
    popIn(avg(), 0.3),
  );

  // many modules give a higher number in the dark
  yield* until(Math.max(useTime(), T.word('higher', 2.18) - 0.3));
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('int raw = sum / 8;')), 0.25),
    popIn(rawCard(), 0.35),
  );
  yield* until(Math.max(useTime(), T.word('dark', 3.1) - 0.1));
  yield* rawCard().scale(1.08, 0.12).to(1, 0.25, easeOutBack);

  // one line in the code flips it
  yield* until(Math.max(useTime(), T.word('line', 4.26) - 0.3));
  yield* code.code().selection(code.code().findFirstRange(lit(FLIP)), 0.25);
  yield* until(Math.max(useTime(), T.word('flips', 5.4) - 0.3));
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('4095 - raw')), 0.25),
    arrow().opacity(1, 0.25),
    arrow().x(-30).x(0, 0.35, easeOutCubic),
  );
  yield* all(popIn(flipCard(), 0.35), popIn(huh(), 0.3));

  // so for us zero always means dark
  yield* until(Math.max(useTime(), T.word('zero', 7.1) - 0.35));
  yield* all(
    code.code().selection(code.code().findFirstRange(lit(FLIP)), 0.25),
    strip().opacity(1, 0.3),
    strip().y(STRIP_Y + 30).y(STRIP_Y, 0.35, easeOutCubic),
  );
  yield* until(Math.max(useTime(), T.word('dark', 8.64, undefined, 1) - 0.3));
  yield* all(zeroTxt().scale(1.18, 0.12).to(1, 0.25, easeOutBack), marker().scale(1.3, 0.12).to(1, 0.25, easeOutBack));
  yield grid().opacity(0.6, 1.0, linear);
  yield* until(T.total);
}));
