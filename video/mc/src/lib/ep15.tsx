/**
 * Shared bits for the Ep15 ("Drawer spy", DRAFT) scenes: timing accessor,
 * the full-code glimpse on drawer_spy.ino and the light-number graph used by
 * one_line (one threshold) and two_lines (OPEN_AT 1800 / CLOSED_AT 1200,
 * hysteresis). The graph's OPEN / CLOSED badge is computed from the trace
 * with the sketch's own rule, so what it shows is what the board would do.
 *
 * Re-time after a narration change:  node video/mc/tools/timing.mjs ep15
 */
import {Circle, Line, Node, Rect, Txt, View2D} from '@motion-canvas/2d';
import {createRef, createSignal, easeOutBack, linear, Reference, ThreadGenerator, Vector2} from '@motion-canvas/core';
import data from '../timing/ep15.json';
import sketch from '../timing/ep15_sketch.json';
import {makeTiming} from './ep10';
import {SketchGlimpse} from './glimpse';
import {C, FONT} from '../style';

export const timing15 = makeTiming(data, 'ep15');
export const SKETCH15 = sketch as {file: string; folder: string; lines: string[]};

/** Full-code glimpse of drawer_spy.ino (add on top, run as a background thread). */
export function glimpse15(
  view: View2D,
  o: {from: number; to: number; match: string},
  target: () => Vector2,
  targetFont: number,
  zoomAt = 1.1,
): ThreadGenerator {
  const g = new SketchGlimpse({...o, sketch: SKETCH15});
  view.add(g.node());
  return g.play(view, target, targetFont / g.font, zoomAt, 0.5);
}

/** OPEN_AT / CLOSED_AT exactly as in drawer_spy.ino. */
export const OPEN_AT = 1800;
export const CLOSED_AT = 1200;

/** Light value at scene time t (a piecewise-linear path + optional wobble). */
export type Path = (t: number) => number;

/** Piecewise-linear helper: keys = [[t, v], ...] (sorted by t). */
export function keyed(keys: [number, number][]): Path {
  return t => {
    if (t <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) {
      const [t1, v1] = keys[i];
      if (t <= t1) {
        const [t0, v0] = keys[i - 1];
        const k = (t - t0) / (t1 - t0);
        const s = k * k * (3 - 2 * k); // smoothstep
        return v0 + (v1 - v0) * s;
      }
    }
    return keys[keys.length - 1][1];
  };
}

/**
 * Number-over-time graph: y = light number 0..4095, x = scene time.
 * The trace draws itself in real time (run `drive()` as a background thread).
 * `hi` / `lo` are the switching lines (equal = one line); the badge follows
 * the sketch's rule: open when > hi, closed again only when < lo.
 */
export class LightGraph {
  public static readonly X0 = -720;
  public static readonly X1 = 760;
  public static readonly YT = -290; // y of 4095
  public static readonly YB = 290; // y of 0

  public readonly root = createRef<Node>();
  public readonly trace = createRef<Line>();
  public readonly head = createRef<Circle>();
  public readonly badge = createRef<Rect>();
  public readonly badgeTxt = createRef<Txt>();
  public readonly now = createSignal(0);
  private readonly samples: {t: number; v: number}[] = [];

  public constructor(
    private readonly o: {path: Path; t0: number; t1: number; hi: number; lo: number; badgeX?: number; badgeY?: number},
  ) {
    for (let t = o.t0; t <= o.t1 + 1e-6; t += 0.04) this.samples.push({t, v: o.path(t)});
  }

  public static vy(v: number) {
    return LightGraph.YB - ((LightGraph.YB - LightGraph.YT) * v) / 4095;
  }

  public tx(t: number) {
    const {X0, X1} = LightGraph;
    return X0 + 30 + ((X1 - 330 - X0 - 30) * (t - this.o.t0)) / (this.o.t1 - this.o.t0); // right column stays free for tags
  }

  /** open / closed after everything drawn so far (the sketch's two ifs). */
  public isOpen(): boolean {
    let open = false;
    const n = this.now();
    for (const s of this.samples) {
      if (s.t > n) break;
      if (!open && s.v > this.o.hi) open = true;
      else if (open && s.v < this.o.lo) open = false;
    }
    return open;
  }

  public value(): number {
    return this.o.path(Math.max(this.o.t0, Math.min(this.o.t1, this.now())));
  }

  public node() {
    const {X0, X1, YT, YB} = LightGraph;
    const vy = LightGraph.vy;
    const pts = () => {
      const n = this.now();
      const out: [number, number][] = [];
      for (const s of this.samples) {
        if (s.t > n) break;
        out.push([this.tx(s.t), vy(s.v)]);
      }
      if (out.length === 0) out.push([this.tx(this.o.t0), vy(this.o.path(this.o.t0))]);
      if (out.length === 1) out.push([out[0][0] + 0.1, out[0][1]]);
      return out;
    };
    return (
      <Node ref={this.root}>
        {/* y axis + grid */}
        <Line points={[[X0, YT - 10], [X0, YB]]} stroke={C.dim} lineWidth={4} />
        <Line points={[[X0, YB], [X1, YB]]} stroke={C.dim} lineWidth={4} />
        {[0, 1000, 2000, 3000, 4095].flatMap(v => [
          <Line points={[[X0 - 12, vy(v)], [X0, vy(v)]]} stroke={C.dim} lineWidth={4} />,
          ...(v > 0 ? [<Line points={[[X0, vy(v)], [X1, vy(v)]]} stroke={C.line} lineWidth={2} />] : []),
          <Txt x={X0 - 24} y={vy(v)} offsetX={1} text={String(v)} fontFamily={FONT.code} fontSize={26} fill={C.dim} />,
        ])}
        <Txt x={X1} y={YB + 32} offsetX={1} text={'time →'} fontFamily={FONT.ui} fontWeight={700} fontSize={28} fill={C.dim} />
        <Txt x={X0 + 16} y={YT - 28} offsetX={-1} text={'light number'} fontFamily={FONT.ui} fontWeight={700} fontSize={28} fill={C.dim} />
        {/* the trace */}
        <Line ref={this.trace} points={pts} stroke={C.text} lineWidth={7} lineCap={'round'} lineJoin={'round'} />
        <Circle
          ref={this.head}
          position={() => {
            const p = pts();
            return p[p.length - 1];
          }}
          size={24}
          fill={() => (this.isOpen() ? C.amber : C.teal)}
          stroke={C.bg}
          lineWidth={4}
        />
        {/* OPEN / CLOSED badge */}
        <Rect
          ref={this.badge}
          x={this.o.badgeX ?? 560}
          y={this.o.badgeY ?? -240}
          width={250}
          height={70}
          radius={35}
          fill={() => (this.isOpen() ? 'rgba(255,181,71,0.18)' : 'rgba(45,212,191,0.14)')}
          stroke={() => (this.isOpen() ? C.amber : C.teal)}
          lineWidth={4}
          opacity={0}
        >
          <Txt
            ref={this.badgeTxt}
            text={() => (this.isOpen() ? 'OPEN' : 'CLOSED')}
            fontFamily={FONT.ui}
            fontWeight={900}
            fontSize={38}
            fill={() => (this.isOpen() ? C.amber : C.teal)}
          />
        </Rect>
      </Node>
    );
  }

  /** Background thread: advance the trace in real time from t0 to t1. */
  public *drive(): ThreadGenerator {
    this.now(this.o.t0);
    yield* this.now(this.o.t1, this.o.t1 - this.o.t0, linear);
  }

  /** Background thread: pop the badge every time the state flips. */
  public *watch(): ThreadGenerator {
    let prev = this.isOpen();
    while (true) {
      const s = this.isOpen();
      if (s !== prev) {
        prev = s;
        yield this.badge().scale(1.22, 0.1).to(1, 0.25, easeOutBack);
      }
      yield;
    }
  }
}

/** A horizontal switching line across the graph, with a tag on the right. */
export function ThresholdLine(props: {refNode: Reference<Node>; v: number; text: string; color: string; dashed?: boolean}) {
  const {X0, X1} = LightGraph;
  const y = LightGraph.vy(props.v);
  return (
    <Node ref={props.refNode} opacity={0}>
      <Line points={[[X0, y], [X1, y]]} stroke={props.color} lineWidth={5} lineDash={props.dashed ? [16, 10] : undefined} />
      <Rect x={X1 - 10} y={y} offsetX={1} layout padding={[2, 14]} radius={10} fill={'rgba(13,22,40,0.95)'} stroke={props.color} lineWidth={3}>
        <Txt text={props.text} fontFamily={FONT.code} fontWeight={800} fontSize={28} fill={props.color} />
      </Rect>
    </Node>
  );
}
