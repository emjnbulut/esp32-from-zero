/**
 * Full-code glimpse for the Ep10 code scenes: the WHOLE real sketch
 * (src/timing/ep10_sketch.json, written by tools/ep10_timing.mjs from
 * lessons/10-reflex-oled/code/reflex_oled/reflex_oled.ino) in two small
 * syntax-coloured columns, the lines this scene is about highlighted, then a
 * quick zoom into one exact piece of code that lands on the scene's own big
 * code line. Draw it on top of the scene and run it as a background thread:
 *
 *   const g = new SketchGlimpse({from: 91, to: 97, match: 'prefs.putULong("best", best);'});
 *   view.add(g.node());
 *   yield g.play(view, () => targetCenter, 54 / SketchGlimpse.FONT, 1.1);
 */
import {Code, lines, Node, Rect, Txt, View2D} from '@motion-canvas/2d';
import {
  all,
  createRef,
  delay,
  easeInCubic,
  easeInOutCubic,
  easeOutCubic,
  ThreadGenerator,
  useTime,
  Vector2,
  waitFor,
} from '@motion-canvas/core';
import sketch from '../timing/ep10_sketch.json';
import {arduino} from './arduinoHighlighter';
import {C, FONT, H, W} from '../style';

const lit = (s: string) => new RegExp(s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');

export const SKETCH_LINES: string[] = (sketch as {lines: string[]}).lines;
export const SKETCH_FILE: string = (sketch as {file: string}).file;

export class SketchGlimpse {
  public static readonly FONT = 13;
  public static readonly LINE_H = 15;
  public readonly root = createRef<Node>();
  public readonly bg = createRef<Rect>();
  public readonly content = createRef<Node>();
  public readonly tab = createRef<Rect>();
  private readonly cols = [createRef<Code>(), createRef<Code>()];
  private readonly bar = createRef<Rect>();
  private readonly split: number;
  private readonly lines: string[];
  private readonly file: string;
  /** font size / line height of the sketch (two columns fit ~825 px of height) */
  public readonly font: number;
  public readonly lineH: number;

  /**
   * from/to are 1-based line numbers of the sketch (as in an editor).
   * sketch defaults to Ep10's; pass another src/timing/<ep>_sketch.json.
   */
  public constructor(
    private readonly o: {from: number; to: number; match: string; sketch?: {file: string; lines: string[]}},
  ) {
    this.lines = o.sketch?.lines ?? SKETCH_LINES;
    this.file = o.sketch?.file ?? SKETCH_FILE;
    this.split = Math.ceil(this.lines.length / 2);
    this.lineH = Math.min(SketchGlimpse.LINE_H, 825 / this.split);
    this.font = Math.round(this.lineH * 0.867 * 10) / 10;
  }

  public node() {
    const maxLen = Math.max(...this.lines.map(l => l.length));
    const colW = Math.min(840, Math.max(400, maxLen * this.font * 0.55 + 16));
    const gap = 70;
    const left = -(colW * 2 + gap) / 2;
    const top = this.lineH < SketchGlimpse.LINE_H ? -425 : -410;
    const texts = [this.lines.slice(0, this.split), this.lines.slice(this.split)];
    return (
      <Node ref={this.root}>
        <Rect ref={this.bg} width={W} height={H} fill={C.bg} />
        <Node ref={this.content}>
          <Rect
            ref={this.tab}
            x={left}
            y={top - 34}
            offsetX={-1}
            layout
            gap={14}
            alignItems="center"
            padding={[6, 18]}
            radius={[10, 10, 0, 0]}
            fill={'#15223a'}
          >
            <Txt text={this.file} fontFamily={FONT.code} fontWeight={700} fontSize={22} fill={C.amber} />
            <Txt text={`${this.lines.length} lines`} fontFamily={FONT.ui} fontSize={20} fill={C.dim} />
          </Rect>
          <Rect ref={this.bar} fill={'rgba(255,181,71,0.16)'} radius={6} opacity={0} />
          {texts.map((t, i) => (
            <Code
              ref={this.cols[i]}
              x={left + i * (colW + gap)}
              y={top}
              offset={[-1, -1]}
              highlighter={arduino}
              fontFamily={FONT.code}
              fontSize={this.font}
              lineHeight={this.lineH}
              code={t.join('\n')}
            />
          ))}
        </Node>
      </Node>
    );
  }

  /** column + 0-based local line of a 1-based sketch line */
  private where(line: number): [number, number] {
    const i = line - 1;
    return i < this.split ? [0, i] : [1, i - this.split];
  }

  private toContent(code: Code, p: Vector2) {
    return p.transformAsPoint(code.localToWorld()).transformAsPoint(this.content().worldToLocal());
  }

  /**
   * Runs the glimpse: shows the sketch, highlights the lines, holds until
   * scene time `zoomAt`, then zooms `match` onto `target()` (view coords,
   * evaluated at zoom start) at `scale`, fading the sketch away.
   */
  public *play(view: View2D, target: () => Vector2, scale: number, zoomAt = 1.1, zoomDur = 0.5): ThreadGenerator {
    const [ci, a] = this.where(this.o.from);
    const [, b] = this.where(this.o.to);
    const code = this.cols[ci]();
    const sel = lines(a, b);
    // highlight bar behind the lines
    const boxes = code.getSelectionBBox(sel);
    let minY = Infinity;
    let maxY = -Infinity;
    let minX = Infinity;
    let maxX = -Infinity;
    for (const r of boxes) {
      minY = Math.min(minY, r.top);
      maxY = Math.max(maxY, r.bottom);
      minX = Math.min(minX, r.left);
      maxX = Math.max(maxX, r.right);
    }
    const tl = this.toContent(code, new Vector2(minX - 8, minY - 3));
    const br = this.toContent(code, new Vector2(maxX + 8, maxY + 3));
    this.bar().position(tl.add(br).scale(0.5)).size([br.x - tl.x, br.y - tl.y]).scale([0, 1]);

    this.content().opacity(0).scale(1.04);
    code.selection(sel);
    const other = this.cols[1 - ci]();
    other.selection([]); // nothing selected -> the whole column dims
    yield* all(
      this.content().opacity(1, 0.18),
      this.content().scale(1, 0.3, easeOutCubic),
      delay(0.15, all(this.bar().opacity(1, 0.1), this.bar().scale([1, 1], 0.3, easeOutCubic))),
    );
    const wait = zoomAt - useTime();
    if (wait > 0) yield* waitFor(wait);

    // zoom: the exact piece of code flies onto the scene's own code line
    const range = code.findFirstRange(lit(this.o.match));
    const mb = code.getSelectionBBox(range)[0];
    const p = this.toContent(code, mb.center);
    const t = target();
    yield* all(
      this.content().scale(scale, zoomDur, easeInOutCubic),
      this.content().position(t.sub(p.scale(scale)), zoomDur, easeInOutCubic),
      code.selection(range, zoomDur * 0.5),
      this.bar().opacity(0, zoomDur * 0.4),
      this.tab().opacity(0, zoomDur * 0.4),
      this.bg().opacity(0, zoomDur, easeInCubic),
      delay(zoomDur * 0.6, this.content().opacity(0, zoomDur * 0.4)),
    );
    this.root().remove();
  }
}
