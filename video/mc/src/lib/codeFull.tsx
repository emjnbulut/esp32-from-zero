/**
 * Shared "full code" closing scene body: the whole real sketch scrolls in an
 * editor card (file tab + line numbers); chips: code + solution, the lesson
 * folder, a bouncing "link below" arrow and a comments bubble timed to the
 * word "comments". Used by ep10 code_full and ep11_code_full:
 *
 *   export default makeScene2D(exact(T.total, view => codeFullBody(view, T, sketch, ['Your best time?', '→ comments'])));
 */
import {Circle, Code, Line, Node, Rect, Txt, View2D} from '@motion-canvas/2d';
import {
  all,
  createRef,
  delay,
  easeInOutCubic,
  easeInOutSine,
  easeOutBack,
  linear,
  loop,
  ThreadGenerator,
  useTime,
} from '@motion-canvas/core';
import {addBackdrop, drift} from './backdrop';
import {arduino} from './arduinoHighlighter';
import {Headline} from './kinetic';
import {Pill, popIn, until} from './ep10';
import {C, FONT} from '../style';

export interface Sketch {
  file: string;
  folder: string;
  lines: string[];
}
interface Timing {
  total: number;
  word: (w: string, fallback: number, segId?: string, nth?: number) => number;
}

export function* codeFullBody(view: View2D, T: Timing, sk: Sketch, ask: [string, string]): ThreadGenerator {
  const SKETCH_LINES = sk.lines;
  const SKETCH_FILE = sk.file;
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const CX = -180;
  const CY = 0;
  const CW = 1200;
  const CH = 700;
  const BAR = 56;
  const FS = 22;
  const LH = 30;
  const viewH = CH - BAR;
  const scrollMax = SKETCH_LINES.length * LH + 40 - viewH;

  const card = createRef<Rect>();
  const scroller = createRef<Node>();
  const solution = createRef<Rect>();
  const folder = createRef<Rect>();
  const arrow = createRef<Node>();
  const comments = createRef<Rect>();

  view.add(
    <Rect
      ref={card}
      x={CX}
      y={CY}
      width={CW}
      height={CH}
      radius={22}
      fill={'#0e1728'}
      stroke={'#2a3a5c'}
      lineWidth={3}
      shadowColor={'rgba(0,0,0,0.5)'}
      shadowBlur={36}
      shadowOffsetY={12}
      clip
    >
      {/* code area */}
      <Rect y={BAR / 2} width={CW} height={viewH} clip>
        <Node ref={scroller} y={-viewH / 2 + 20}>
          <Txt
            x={-CW / 2 + 70}
            offset={[1, -1]}
            text={SKETCH_LINES.map((_, i) => String(i + 1)).join('\n')}
            fontFamily={FONT.code}
            fontSize={FS}
            lineHeight={LH}
            textAlign={'right'}
            fill={'#3c4a66'}
          />
          <Code
            x={-CW / 2 + 96}
            offset={[-1, -1]}
            highlighter={arduino}
            fontFamily={FONT.code}
            fontSize={FS}
            lineHeight={LH}
            code={SKETCH_LINES.join('\n')}
          />
        </Node>
      </Rect>
      {/* title bar + tab */}
      <Rect y={-CH / 2 + BAR / 2} width={CW} height={BAR} fill={'#15223a'} />
      {[0, 1, 2].map(i => (
        <Circle x={-CW / 2 + 30 + i * 26} y={-CH / 2 + BAR / 2} size={14} fill={['#ff5f57', '#febc2e', '#28c840'][i]} />
      ))}
      <Rect
        x={-CW / 2 + 120}
        y={-CH / 2 + BAR / 2 + 4}
        offsetX={-1}
        height={BAR - 8}
        layout
        alignItems="center"
        padding={[0, 22]}
        radius={[10, 10, 0, 0]}
        fill={'#0e1728'}
      >
        <Txt text={SKETCH_FILE} fontFamily={FONT.code} fontWeight={700} fontSize={26} fill={C.amber} />
      </Rect>
      {/* fade at the bottom of the code area */}
      <Rect y={CH / 2 - 30} width={CW} height={60} fill={'rgba(14,23,40,0.85)'} />
    </Rect>,
  );

  const RX = 690;
  view.add(<Pill refNode={solution} text={'code + solution ✓'} color={C.teal} x={RX} y={-250} size={34} />);
  view.add(
    <Rect
      ref={folder}
      x={RX}
      y={-150}
      layout
      gap={14}
      alignItems="center"
      padding={[10, 22]}
      radius={16}
      fill={'#15223a'}
      stroke={C.amber}
      lineWidth={3}
      opacity={0}
      scale={0.5}
    >
      {/* folder icon */}
      <Rect width={40} height={32}>
        <Rect layout={false} x={-9} y={-12} width={20} height={8} radius={[3, 3, 0, 0]} fill={C.amber} />
        <Rect layout={false} y={3} width={40} height={26} radius={4} fill={C.amber} />
      </Rect>
      <Txt text={sk.folder} fontFamily={FONT.code} fontWeight={700} fontSize={28} fill={C.text} />
    </Rect>,
  );
  view.add(
    <Node ref={arrow} x={RX} y={60} opacity={0}>
      <Txt y={-80} text={'link below'} fontFamily={FONT.ui} fontWeight={800} fontSize={40} fill={C.text} />
      <Line points={[[0, -40], [0, 110]]} stroke={C.amber} lineWidth={12} lineCap={'round'} endArrow arrowSize={34} />
    </Node>,
  );
  view.add(
    <Rect
      ref={comments}
      x={RX}
      y={300}
      layout
      direction="column"
      gap={2}
      alignItems="center"
      padding={[12, 26]}
      radius={[24, 24, 24, 6]}
      fill={C.amber}
      opacity={0}
      scale={0.5}
    >
      <Txt text={ask[0]} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={C.bg} />
      <Txt text={ask[1]} fontFamily={FONT.ui} fontWeight={700} fontSize={34} fill={C.bg} />
    </Rect>,
  );

  const h1 = new Headline('The *full* *code*');
  view.add(h1.node());

  // ------------------------------------------------------------ beats
  card().scale(0.9).opacity(0);
  yield* all(card().scale(1, 0.4, easeOutBack), card().opacity(1, 0.25), delay(0.1, h1.in()));
  // the whole sketch scrolls by, top to bottom
  const scrollEnd = T.total - 0.6;
  yield scroller().y(scroller().y() - scrollMax, scrollEnd - useTime(), easeInOutSine);

  yield* until(Math.max(useTime(), T.word('solution', 1.0) - 0.2));
  yield* popIn(solution(), 0.3);
  yield* until(Math.max(useTime(), T.word('lesson', 2.1) - 0.2));
  yield* popIn(folder(), 0.35);
  yield* until(Math.max(useTime(), T.word('linked', 3.0) - 0.2));
  yield* arrow().opacity(1, 0.25);
  yield loop(Infinity, () => arrow().position.y(80, 0.35, easeInOutCubic).to(60, 0.35, easeInOutCubic));

  yield* until(Math.max(useTime(), T.word('comments', T.total - 1.4) - 0.2));
  yield* all(popIn(comments(), 0.35), h1.pulse());
  yield all(comments().rotation(-3, 0.25).to(3, 0.25).to(0, 0.2), grid().opacity(0.6, 1.2, linear));
  yield* until(T.total);
}
