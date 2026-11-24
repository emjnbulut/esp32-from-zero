/**
 * Shared helpers for the Ep10 ("Reflex Game 2.0") Motion Canvas scenes.
 *
 * Timing comes from src/timing/ep10.json (written by tools/ep10_timing.mjs from
 * video/ep10/build/schedule.json). Scenes pace their beats by segment starts and
 * spoken-word times, and end exactly at `total`.
 */
import {Circle, Code, Line, Node, Rect, Txt, View2D} from '@motion-canvas/2d';
import {
  all,
  createRef,
  easeInCubic,
  easeInOutCubic,
  easeOutBack,
  easeOutCubic,
  Reference,
  ThreadGenerator,
  tween,
  useTime,
  Vector2,
  waitFor,
} from '@motion-canvas/core';
import timingData from '../timing/ep10.json';
import {arduino} from './arduinoHighlighter';
import {C, FONT} from '../style';

interface Word {
  w: string;
  t: number;
}
interface Seg {
  id: string;
  start: number;
  dur: number;
  words: Word[];
}
interface SceneTiming {
  total: number;
  estimated: boolean;
  segments: Seg[];
}

const norm = (s: string) => s.toLowerCase().replace(/[^a-z0-9]/g, '');

/** Timing accessor for one scene id. */
/** Ep10 timing accessor (src/timing/ep10.json). */
export function timing(scene: string) {
  return makeTiming(timingData, 'ep10')(scene);
}

/**
 * Timing accessor for any episode's src/timing/<ep>.json (from
 * tools/timing.mjs <ep>):  const T = makeTiming(ep11, 'ep11')('code_read');
 */
export const makeTiming = (data: unknown, ep: string) => (scene: string) => {
  const t = (data as Record<string, SceneTiming>)[scene];
  if (!t) throw new Error(`no timing for scene ${scene} - run node video/mc/tools/timing.mjs ${ep}`);
  const seg = (id?: string) => {
    const s = id ? t.segments.find(x => x.id === id) : t.segments[0];
    if (!s) throw new Error(`${scene}: no segment ${id}`);
    return {start: s.start, dur: s.dur, end: s.start + s.dur, words: s.words};
  };
  /**
   * Scene time of the nth spoken word starting with `word` (inside segment
   * `segId`, or anywhere). Falls back to `fallback` (scene seconds) if missing.
   */
  const word = (w: string, fallback: number, segId?: string, nth = 0) => {
    const want = norm(w);
    let k = 0;
    for (const s of t.segments) {
      if (segId && s.id !== segId) continue;
      for (const x of s.words) {
        if (norm(x.w).startsWith(want)) {
          if (k === nth) return s.start + x.t;
          k++;
        }
      }
    }
    return fallback;
  };
  return {total: t.total, segments: t.segments, seg, word};
};

/**
 * Wrap a scene body so the scene lasts exactly `total` seconds: the body runs
 * as a child thread and is cut off at `total` even if a beat ran late.
 *   export default makeScene2D(exact(T.total, function* (view) { ... }));
 */
export function exact(total: number, body: (view: View2D) => ThreadGenerator) {
  return function* (view: View2D): ThreadGenerator {
    yield body(view);
    yield* waitFor(total);
  };
}

/** Wait until scene time `t` (no-op if already past). */
export function* until(t: number): ThreadGenerator {
  const d = t - useTime();
  if (d > 0) yield* waitFor(d);
}

/** Exact-text pattern for Code.findFirstRange (strings are treated as RegExp). */
export const lit = (s: string) =>
  new RegExp(s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');

/** World (canvas px) -> view-local coordinates. */
export const toView = (view: View2D, p: Vector2) =>
  p.transformAsPoint(view.worldToLocal());

/** Big code line inside a dark rounded panel with a coloured chip. */
export class CodePanel {
  public readonly panel = createRef<Rect>();
  public readonly code = createRef<Code>();
  public readonly chip = createRef<Rect>();
  public readonly chipTxt = createRef<Txt>();

  public constructor(
    private readonly o: {
      y?: number;
      x?: number;
      chip?: string;
      chipColor?: string;
      size?: number;
      code?: string;
    } = {},
  ) {}

  public node() {
    return (
      <Rect
        ref={this.panel}
        x={this.o.x ?? 0}
        y={this.o.y ?? 300}
        layout
        direction="row"
        alignItems="center"
        gap={30}
        padding={[24, 40]}
        radius={22}
        fill={'rgba(13,22,40,0.95)'}
        stroke={C.line}
        lineWidth={3}
        opacity={0}
      >
        {this.o.chip ? (
          <Rect
            ref={this.chip}
            padding={[8, 18]}
            radius={10}
            fill={this.o.chipColor ?? C.amber}
          >
            <Txt
              ref={this.chipTxt}
              text={this.o.chip}
              fontFamily={FONT.ui}
              fontWeight={800}
              fontSize={30}
              fill={C.bg}
            />
          </Rect>
        ) : null}
        <Code
          ref={this.code}
          highlighter={arduino}
          fontFamily={FONT.code}
          fontSize={this.o.size ?? 52}
          code={this.o.code ?? ''}
        />
      </Rect>
    );
  }

  public *show(dur = 0.35): ThreadGenerator {
    const y = this.panel().y();
    this.panel().y(y + 40);
    yield* all(
      this.panel().opacity(1, dur * 0.8),
      this.panel().y(y, dur, easeOutCubic),
    );
  }

  public *hide(dur = 0.3): ThreadGenerator {
    yield* this.panel().opacity(0, dur);
  }
}

/** Rounded pill label ("saved ✓"). Starts hidden; use popIn(). */
export function Pill(props: {
  refNode: Reference<Rect>;
  text: string;
  color?: string;
  x?: number;
  y?: number;
  size?: number;
}) {
  const col = props.color ?? C.teal;
  return (
    <Rect
      ref={props.refNode}
      x={props.x ?? 0}
      y={props.y ?? 0}
      layout
      padding={[8, 24]}
      radius={40}
      fill={col === C.red ? 'rgba(255,93,108,0.16)' : col === C.amber ? 'rgba(255,181,71,0.16)' : col === C.teal ? 'rgba(45,212,191,0.16)' : 'rgba(138,151,171,0.14)'}
      stroke={col}
      lineWidth={3}
      opacity={0}
      scale={0.5}
    >
      <Txt
        text={props.text}
        fontFamily={FONT.ui}
        fontWeight={700}
        fontSize={props.size ?? 36}
        fill={col}
      />
    </Rect>
  );
}

export function* popIn(n: Node, dur = 0.35, to = 1): ThreadGenerator {
  yield* all(n.opacity(1, dur * 0.6), n.scale(to, dur, easeOutBack));
}

export function* popOut(n: Node, dur = 0.25): ThreadGenerator {
  yield* all(n.opacity(0, dur), n.scale(0.6, dur, easeInCubic));
}

/** Particle burst + ring at `center` (view coordinates). */
export function* burst(
  view: View2D,
  center: Vector2,
  colors: string[] = [C.amber, C.teal, C.text],
  radius = 200,
): ThreadGenerator {
  const host = createRef<Node>();
  view.add(<Node ref={host} />);
  const parts = Array.from({length: 14}, (_, i) => {
    const ref = createRef<Circle>();
    host().add(
      <Circle ref={ref} position={center} size={i % 3 === 0 ? 18 : 12} fill={colors[i % colors.length]} />,
    );
    return {ref, angle: (i / 14) * Math.PI * 2 + (i % 2) * 0.2, dist: radius * (0.8 + (i % 4) * 0.15)};
  });
  const ring = createRef<Circle>();
  host().add(<Circle ref={ring} position={center} size={40} stroke={colors[0]} lineWidth={8} />);
  yield* all(
    ring().size(radius * 2.3, 0.55, easeOutCubic),
    ring().opacity(0, 0.55, easeInCubic),
    ...parts.map(p =>
      all(
        p.ref().position(center.add(Vector2.fromRadians(p.angle).scale(p.dist)), 0.6, easeOutCubic),
        p.ref().opacity(0, 0.6, easeInCubic),
      ),
    ),
  );
  host().remove();
}

/** Stylised ESP32 dev board (top view), centred on its origin. */
export function Esp32Board(props: {
  refNode: Reference<Node>;
  x?: number;
  y?: number;
  scale?: number;
  led?: Reference<Circle>;
}) {
  const pins = Array.from({length: 12}, (_, i) => -165 + i * 30);
  return (
    <Node ref={props.refNode} x={props.x ?? 0} y={props.y ?? 0} scale={props.scale ?? 1}>
      <Rect
        width={420}
        height={240}
        radius={18}
        fill={'#1b2233'}
        stroke={'#2e3a55'}
        lineWidth={4}
        shadowColor={'rgba(0,0,0,0.5)'}
        shadowBlur={30}
        shadowOffsetY={10}
      />
      {/* (no fragments inside .map: nested fragments are not rendered) */}
      {pins.flatMap(x => [
        <Rect x={x} y={-104} width={14} height={14} radius={3} fill={'#d8b45a'} />,
        <Rect x={x} y={104} width={14} height={14} radius={3} fill={'#d8b45a'} />,
      ])}
      {/* metal RF shield */}
      <Rect x={-30} width={220} height={150} radius={10} fill={'#aab4c3'} stroke={'#cfd7e2'} lineWidth={3}>
        <Txt text={'ESP32'} fontFamily={FONT.ui} fontWeight={800} fontSize={44} fill={'#2a3242'} />
      </Rect>
      {/* antenna */}
      <Line
        points={[
          [110, -50],
          [150, -50],
          [150, -20],
          [170, -20],
          [170, 20],
          [150, 20],
          [150, 50],
          [110, 50],
        ]}
        stroke={'#d8b45a'}
        lineWidth={6}
      />
      {/* USB */}
      <Rect x={-212} width={40} height={64} radius={6} fill={C.metal} />
      <Circle ref={props.led} x={186} y={-80} size={18} fill={C.red} shadowColor={C.red} shadowBlur={14} />
    </Node>
  );
}

/**
 * The "Preferences" drawer: a small cabinet whose drawer slides out to the
 * right. `card` sits in the drawer tray; `value`/`label` are its texts.
 */
export class Drawer {
  public readonly root = createRef<Node>();
  public readonly body = createRef<Rect>();
  public readonly drawer = createRef<Node>();
  public readonly card = createRef<Rect>();
  public readonly cardLabel = createRef<Txt>();
  public readonly cardValue = createRef<Txt>();
  public readonly title = createRef<Txt>();
  public readonly sub = createRef<Txt>();
  public readonly glow = createRef<Rect>();

  public constructor(
    private readonly o: {x?: number; y?: number; scale?: number; label?: string; value?: string; title?: string; sub?: string} = {},
  ) {}

  public node() {
    return (
      <Node ref={this.root} x={this.o.x ?? 0} y={this.o.y ?? 0} scale={this.o.scale ?? 1}>
        <Node ref={this.drawer} x={0}>
          <Rect width={380} height={150} fill={'#0f1a2e'} stroke={C.teal} lineWidth={4} radius={[0, 0, 12, 12]} />
          <Rect x={190} width={30} height={190} radius={8} fill={C.teal} />
          <Rect x={218} width={26} height={70} radius={8} fill={'#1aa391'} />
          <Rect
            ref={this.card}
            x={40}
            y={-26}
            layout
            direction="row"
            alignItems="center"
            gap={16}
            padding={[12, 22, 12, 16]}
            radius={14}
            fill={'#1e2a40'}
            stroke={C.amber}
            lineWidth={4}
            opacity={0}
          >
            <Rect padding={[4, 10]} radius={8} fill={'rgba(45,212,191,0.16)'}>
              <Txt ref={this.cardLabel} text={this.o.label ?? '"best"'} fontFamily={FONT.code} fontSize={28} fill={C.teal} />
            </Rect>
            <Txt ref={this.cardValue} text={this.o.value ?? '214'} fontFamily={FONT.code} fontWeight={700} fontSize={52} fill={C.amber} />
          </Rect>
        </Node>
        <Rect
          ref={this.body}
          width={430}
          height={330}
          radius={28}
          fill={'#132036'}
          stroke={C.teal}
          lineWidth={4}
          shadowColor={'rgba(0,0,0,0.5)'}
          shadowBlur={36}
          shadowOffsetY={12}
        >
          <Rect y={-84} width={84} height={64} radius={8} fill={'#0b1220'} stroke={C.teal} lineWidth={3}>
            {[-27, -9, 9, 27].flatMap(x => [
              <Rect x={x} y={-42} width={8} height={14} fill={C.teal} />,
              <Rect x={x} y={42} width={8} height={14} fill={C.teal} />,
            ])}
            <Txt text={'FLASH'} fontFamily={FONT.code} fontWeight={700} fontSize={18} fill={C.teal} />
          </Rect>
          <Txt ref={this.title} y={20} text={this.o.title ?? 'Preferences'} fontFamily={FONT.ui} fontWeight={800} fontSize={52} fill={C.text} />
          <Txt ref={this.sub} y={80} text={this.o.sub ?? '(flash memory)'} fontFamily={FONT.ui} fontSize={32} fill={C.teal} />
          <Rect x={213} width={8} height={160} radius={4} fill={'#07101e'} />
        </Rect>
      </Node>
    );
  }

  public *open(dist = 320, dur = 0.4): ThreadGenerator {
    yield* this.drawer().x(dist, dur, easeOutCubic);
  }

  public *close(dur = 0.4): ThreadGenerator {
    yield* this.drawer().x(0, dur, easeInCubic);
  }
}

/** Key/value card that flies between places ("best" 214). */
export function ValueCard(props: {
  refNode: Reference<Rect>;
  label?: string;
  value?: string;
  valueRef?: Reference<Txt>;
  opacity?: number;
  x?: number;
  y?: number;
  color?: string;
}) {
  return (
    <Rect
      ref={props.refNode}
      x={props.x ?? 0}
      y={props.y ?? 0}
      opacity={props.opacity ?? 0}
      layout
      direction="row"
      alignItems="center"
      gap={16}
      padding={[12, 22, 12, 16]}
      radius={14}
      fill={'#1e2a40'}
      stroke={props.color ?? C.amber}
      lineWidth={4}
    >
      <Rect padding={[4, 10]} radius={8} fill={'rgba(45,212,191,0.16)'}>
        <Txt text={props.label ?? '"best"'} fontFamily={FONT.code} fontSize={28} fill={C.teal} />
      </Rect>
      <Txt ref={props.valueRef} text={props.value ?? '214'} fontFamily={FONT.code} fontWeight={700} fontSize={52} fill={props.color ?? C.amber} />
    </Rect>
  );
}

/** Arc flight for a node between two view points. */
export function* flyArc(n: Node, from: Vector2, to: Vector2, lift: number, dur: number): ThreadGenerator {
  yield* tween(dur, (v: number) => {
    const t = easeInOutCubic(v);
    const p = Vector2.lerp(from, to, t);
    n.position(p.add([0, -Math.sin(Math.PI * t) * lift]));
    n.rotation(Math.sin(Math.PI * t) * -8);
  });
}
