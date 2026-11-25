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

export function* codeFullBody(
  view: View2D,
  T: Timing & {segments?: {start: number; words: {w: string; t: number}[]}[]},
  sk: Sketch,
  ask: [string, string],
  opts: {pages?: boolean; fit?: boolean} = {},
): ThreadGenerator {
  // with pages: the narrated part ends after the last spoken word, the silent pad pages through the sketch
  const lastSeg = T.segments?.[T.segments.length - 1];
  const lastWord = lastSeg?.words[lastSeg.words.length - 1];
  const narrEnd = opts.pages && lastSeg && lastWord ? Math.min(T.total - 4, lastSeg.start + lastWord.t + 1.0) : T.total;
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
  const scrollEnd = narrEnd - 0.6;
  yield scroller().y(scroller().y() - scrollMax, scrollEnd - useTime(), easeInOutSine);

  yield* until(Math.max(useTime(), T.word('solution', 1.0) - 0.2));
  yield* popIn(solution(), 0.3);
  yield* until(Math.max(useTime(), T.word('lesson', 2.1) - 0.2));
  yield* popIn(folder(), 0.35);
  yield* until(Math.max(useTime(), T.word('linked', 3.0) - 0.2));
  yield* arrow().opacity(1, 0.25);
  yield loop(Infinity, () => arrow().position.y(80, 0.35, easeInOutCubic).to(60, 0.35, easeInOutCubic));

  yield* until(Math.max(useTime(), T.word('comments', narrEnd - 1.4) - 0.2));
  yield* all(popIn(comments(), 0.35), h1.pulse());
  yield all(comments().rotation(-3, 0.25).to(3, 0.25).to(0, 0.2), grid().opacity(0.6, 1.2, linear));
  if (opts.pages && narrEnd < T.total) {
    yield* until(narrEnd);
    yield* all(
      card().opacity(0, 0.3),
      solution().opacity(0, 0.3),
      arrow().opacity(0, 0.3),
      comments().opacity(0, 0.3),
      folder().opacity(0, 0.3),
      h1.out(),
    );
    yield* pageThrough(view, sk, T.total, opts.fit);
  }
  yield* until(T.total);
}

/**
 * Split the sketch into the fewest pages of at most max lines, balanced in
 * size, preferring to break after a blank line (so a function's first line
 * stays with its body).
 */
export function splitPages(lines: string[], max = 24): [number, number][] {
  const n = lines.length;
  const count = Math.ceil(n / max);
  const pages: [number, number][] = [];
  let start = 0;
  for (let p = 0; p < count; p++) {
    const left = count - p - 1; // pages after this one
    if (left === 0) {
      pages.push([start, n]);
      break;
    }
    const target = Math.ceil((n - start) / (left + 1));
    let end = Math.min(n, start + max);
    for (let i = Math.min(n, start + max) - 1; i >= start + target - 6; i--) {
      if (lines[i].trim() === '' && n - (i + 1) <= left * max) {
        end = i + 1;
        break;
      }
    }
    if (n - end > left * max) end = n - left * max;
    pages.push([start, end]);
    start = end;
  }
  return pages;
}

/**
 * Readable paging through the whole sketch until scene time `t1`: ~24 lines
 * per page, 30 px monospace, line numbers, file tab, "n/N" page indicator and
 * a thin progress bar per page, 0.3 s slide between pages, equal hold times.
 * fit = true shrinks the font when the longest sketch line would be cut off.
 * Fits between y = -500 and y = 378 (subtitle zone stays free).
 */
export function* pageThrough(view: View2D, sk: Sketch, t1: number, fit = false): ThreadGenerator {
  const pages = splitPages(sk.lines, 24);
  const W = 1840;
  // fit: shrink the font so the longest line fits the card (Consolas advance = 0.55 em)
  const maxLen = Math.max(...sk.lines.map(l => l.replace(/	/g, '  ').length));
  const FS = fit ? Math.min(30, Math.floor((W - 112 - 24) / (maxLen * 0.55))) : 30;
  const LH = fit ? Math.round(FS * 1.1) : 33;
  const per = Math.max(...pages.map(([a, b]) => b - a));
  const TAB = 54;
  const H = per * LH + TAB + 30;
  const TOP = 378 - H; // card bottom sits on the subtitle line
  const card = createRef<Rect>();
  const host = createRef<Node>();
  const pageTxt = createRef<Txt>();
  const prog = createRef<Rect>();
  const codeTop = TOP + TAB + 16;

  view.add(
    <Rect ref={card} y={TOP + H / 2} width={W} height={H} radius={18} fill={'#0e1728'} stroke={'#2a3a5c'} lineWidth={3} opacity={0} clip>
      <Node ref={host} />
      <Rect y={-H / 2 + TAB / 2} width={W} height={TAB} fill={'#15223a'} />
      {[0, 1, 2].map(i => (
        <Circle x={-W / 2 + 28 + i * 26} y={-H / 2 + TAB / 2} size={14} fill={['#ff5f57', '#febc2e', '#28c840'][i]} />
      ))}
      <Rect x={-W / 2 + 112} y={-H / 2 + TAB / 2 + 4} offsetX={-1} height={TAB - 8} layout alignItems="center" gap={18} padding={[0, 22]} radius={[10, 10, 0, 0]} fill={'#0e1728'}>
        <Txt text={sk.file} fontFamily={FONT.code} fontWeight={700} fontSize={26} fill={C.amber} />
        <Txt text={sk.folder} fontFamily={FONT.code} fontSize={20} fill={C.dim} />
      </Rect>
      <Txt ref={pageTxt} x={W / 2 - 30} y={-H / 2 + TAB / 2} offsetX={1} text={''} fontFamily={FONT.code} fontWeight={800} fontSize={28} fill={C.text} />
      <Rect x={-W / 2} y={-H / 2 + TAB} offsetX={-1} width={W} height={4} fill={'#1e2a40'} />
      <Rect ref={prog} x={-W / 2} y={-H / 2 + TAB} offsetX={-1} width={0} height={4} fill={C.teal} />
    </Rect>,
  );

  const makePage = (i: number) => {
    const [a, b] = pages[i];
    const ref = createRef<Node>();
    host().add(
      <Node ref={ref} y={codeTop - (TOP + H / 2)}>
        <Txt
          x={-W / 2 + 84}
          offset={[1, -1]}
          text={Array.from({length: b - a}, (_, k) => String(a + k + 1)).join('\n')}
          fontFamily={FONT.code}
          fontSize={FS}
          lineHeight={LH}
          textAlign={'right'}
          fill={'#4a5878'}
        />
        <Code
          x={-W / 2 + 112}
          offset={[-1, -1]}
          highlighter={arduino}
          fontFamily={FONT.code}
          fontSize={FS}
          lineHeight={LH}
          code={sk.lines.slice(a, b).join('\n')}
        />
      </Node>,
    );
    return ref;
  };

  const t0 = useTime();
  const turn = 0.3;
  const hold = (t1 - t0 - 0.3) / pages.length; // includes the turn
  let cur = makePage(0);
  pageTxt().text(`1/${pages.length}`);
  yield* card().opacity(1, 0.3);
  for (let i = 0; i < pages.length; i++) {
    const pageStart = t0 + 0.3 + i * hold;
    if (i > 0) {
      const old = cur;
      cur = makePage(i);
      cur().x(W * 0.35).opacity(0);
      pageTxt().text(`${i + 1}/${pages.length}`);
      prog().width(0);
      yield* all(
        old().x(-W * 0.35, turn, easeInOutCubic),
        old().opacity(0, turn),
        cur().x(0, turn, easeInOutCubic),
        cur().opacity(1, turn),
        pageTxt().scale(1.25, 0.1).to(1, 0.2),
      );
      old().remove();
    }
    const end = pageStart + hold;
    yield* prog().width(W, Math.max(0.1, end - useTime()), linear);
  }
}
