/**
 * Shared bits for the Ep14 ("Fruit piano", DRAFT) scenes: timing accessor,
 * the full-code glimpse on fruit_piano.ino, the three fruit keys (pins and
 * notes exactly as in the sketch), the labelled moving box (Variable picture,
 * extended to arrays), a pointing finger and the touch-pin bucket rig
 * (ANALOGIES: touch pin = a tiny bucket the pin keeps filling).
 *
 * Re-time after a narration change:  node video/mc/tools/timing.mjs ep14
 */
import {Circle, Line, Node, Rect, Txt, View2D} from '@motion-canvas/2d';
import {
  all,
  createRef,
  createSignal,
  easeInCubic,
  easeOutCubic,
  linear,
  Reference,
  ThreadGenerator,
  Vector2,
} from '@motion-canvas/core';
import data from '../timing/ep14.json';
import sketch from '../timing/ep14_sketch.json';
import {makeTiming} from './ep10';
import {SketchGlimpse} from './glimpse';
import {C, FONT} from '../style';

export const timing14 = makeTiming(data, 'ep14');
export const SKETCH14 = sketch as {file: string; folder: string; lines: string[]};

/** Full-code glimpse of fruit_piano.ino (add on top, run as a background thread). */
export function glimpse14(
  view: View2D,
  o: {from: number; to: number; match: string},
  target: () => Vector2,
  targetFont: number,
  zoomAt = 1.1,
): ThreadGenerator {
  const g = new SketchGlimpse({...o, sketch: SKETCH14});
  view.add(g.node());
  return g.play(view, target, targetFont / g.font, zoomAt, 0.5);
}

/** The three keys: KEY_PIN / NOTE / NAME exactly as in fruit_piano.ino. */
export const KEYS = [
  {fruit: 'banana', pin: 14, note: 523, name: 'DO', tag: 'do', color: '#f5d142'},
  {fruit: 'apple', pin: 2, note: 659, name: 'MI', tag: 'mi', color: '#ff6b6b'},
  {fruit: 'orange', pin: 15, note: 784, name: 'SOL', tag: 'sol', color: '#ff9a3c'},
];

/** Stylised fruit icon (about 170 px wide at scale 1), centred on its origin. */
export function Fruit(props: {kind: number; refNode?: Reference<Node>; x?: number; y?: number; scale?: number; opacity?: number}) {
  const k = props.kind;
  let body;
  if (k === 0) {
    // banana: a thick smile-shaped curve with brown tips
    const pts: [number, number][] = [];
    for (let i = 0; i <= 16; i++) {
      const a = ((25 + (130 * i) / 16) * Math.PI) / 180;
      pts.push([Math.cos(a) * 95, Math.sin(a) * 95 - 70]);
    }
    body = (
      <Node>
        <Line points={pts} stroke={'#d9a91e'} lineWidth={50} lineCap={'round'} />
        <Line points={pts} stroke={'#f5d142'} lineWidth={40} lineCap={'round'} />
        <Line points={pts.slice(3, 13).map(([x, y]) => [x * 0.93, y - 8] as [number, number])} stroke={'#fbe78a'} lineWidth={8} lineCap={'round'} />
        <Circle position={pts[0]} size={18} fill={'#5a3d1a'} />
        <Circle position={pts[16]} size={16} fill={'#5a3d1a'} />
      </Node>
    );
  } else if (k === 1) {
    body = (
      <Node>
        <Line points={[[0, -62], [6, -95]]} stroke={'#6b4a2e'} lineWidth={9} lineCap={'round'} />
        <Rect x={28} y={-88} width={44} height={20} radius={[20, 2, 20, 2]} rotation={-20} fill={'#3fbf5f'} />
        <Circle size={150} fill={'#e5484d'} stroke={'#b8323a'} lineWidth={4} />
        <Circle x={-36} y={-28} size={34} fill={'rgba(255,255,255,0.35)'} />
      </Node>
    );
  } else {
    body = (
      <Node>
        <Circle size={150} fill={'#ff9a3c'} stroke={'#d9741c'} lineWidth={4} />
        {[[-30, 20], [25, 35], [40, -10], [-10, -40], [0, 5], [-45, -10], [20, -45], [-20, 48]].map(([x, y]) => (
          <Circle x={x} y={y} size={6} fill={'#e07a20'} />
        ))}
        <Circle x={-36} y={-30} size={30} fill={'rgba(255,255,255,0.3)'} />
        <Rect x={10} y={-78} width={36} height={16} radius={[16, 2, 16, 2]} rotation={-15} fill={'#3fbf5f'} />
      </Node>
    );
  }
  return (
    <Node ref={props.refNode} x={props.x ?? 0} y={props.y ?? 0} scale={props.scale ?? 1} opacity={props.opacity ?? 1}>
      {body}
    </Node>
  );
}

/** A small note tag ("do") in the fruit's colour. Starts hidden. */
export function NoteTag(props: {refNode: Reference<Rect>; kind: number; x?: number; y?: number; size?: number; text?: string}) {
  const key = KEYS[props.kind];
  return (
    <Rect
      ref={props.refNode}
      x={props.x ?? 0}
      y={props.y ?? 0}
      layout
      padding={[4, 18]}
      radius={30}
      fill={key.color}
      opacity={0}
      scale={0.5}
    >
      <Txt text={props.text ?? key.tag} fontFamily={FONT.ui} fontWeight={900} fontSize={props.size ?? 38} fill={C.bg} />
    </Rect>
  );
}

/**
 * The labelled moving box (Variable picture), extended for arrays: a sticker
 * with the name on top, the one value it holds big on the front.
 */
export class Box {
  public readonly root = createRef<Node>();
  public readonly body = createRef<Rect>();
  public readonly sticker = createRef<Rect>();
  public readonly label = createRef<Txt>();
  public readonly value = createRef<Txt>();

  public constructor(
    private readonly o: {x?: number; y?: number; w?: number; h?: number; label: string; value?: string; labelSize?: number; valueSize?: number; opacity?: number},
  ) {}

  public node() {
    const w = this.o.w ?? 230;
    const h = this.o.h ?? 170;
    return (
      <Node ref={this.root} x={this.o.x ?? 0} y={this.o.y ?? 0} opacity={this.o.opacity ?? 1}>
        <Rect
          ref={this.body}
          width={w}
          height={h}
          radius={10}
          fill={'#c8955c'}
          stroke={'#8f6234'}
          lineWidth={4}
          shadowColor={'rgba(0,0,0,0.45)'}
          shadowBlur={22}
          shadowOffsetY={8}
        >
          <Line points={[[-w / 2 + 4, -h / 2 + 30], [w / 2 - 4, -h / 2 + 30]]} stroke={'#a8763f'} lineWidth={3} />
          <Rect y={-h / 2 + 15} width={44} height={30} fill={'#dcae72'} />
          <Txt
            ref={this.value}
            y={h * 0.16}
            text={this.o.value ?? ''}
            fontFamily={FONT.code}
            fontWeight={800}
            fontSize={this.o.valueSize ?? 54}
            fill={'#2a1a0a'}
          />
        </Rect>
        <Rect
          ref={this.sticker}
          y={-h / 2 + 2}
          layout
          padding={[3, 14]}
          radius={6}
          fill={'#fbf8ef'}
          stroke={'#d6cdb6'}
          lineWidth={2}
        >
          <Txt ref={this.label} text={this.o.label} fontFamily={FONT.code} fontWeight={800} fontSize={this.o.labelSize ?? 28} fill={'#1b2a4a'} />
        </Rect>
      </Node>
    );
  }
}

/** A pointing finger whose tip is the node's origin (points down at rotation 0). */
export function Finger(props: {refNode: Reference<Node>; x?: number; y?: number; rotation?: number; opacity?: number}) {
  return (
    <Node ref={props.refNode} x={props.x ?? 0} y={props.y ?? 0} rotation={props.rotation ?? 0} opacity={props.opacity ?? 1}>
      <Rect y={-380} width={190} height={200} radius={60} fill={'#e8b98f'} stroke={'#c99872'} lineWidth={4} />
      <Rect y={-150} width={66} height={300} radius={33} fill={'#f0c9a0'} stroke={'#c99872'} lineWidth={4} />
      <Rect y={-34} width={44} height={44} radius={[18, 18, 14, 14]} fill={'#f8dfc8'} />
      <Line points={[[-20, -130], [20, -130]]} stroke={'#c99872'} lineWidth={3} />
      <Line points={[[-20, -210], [20, -210]]} stroke={'#c99872'} lineWidth={3} />
      <Rect y={-520} width={210} height={120} radius={20} fill={'#2c5aa0'} />
    </Node>
  );
}

/** Ring that grows and fades at `p` (view coords): a touch contact. */
export function* contact(view: View2D, p: Vector2, color: string = C.teal, size = 160): ThreadGenerator {
  const r = createRef<Circle>();
  view.add(<Circle ref={r} position={p} size={20} stroke={color} lineWidth={8} />);
  yield* all(r().size(size, 0.45, easeOutCubic), r().opacity(0, 0.45, easeInCubic));
  r().remove();
}

/** A "♪" that rises and fades from `p` (view coords). */
export function* noteFloat(view: View2D, p: Vector2, color: string, dx = 40): ThreadGenerator {
  const n = createRef<Txt>();
  view.add(<Txt ref={n} position={p} text={'♪'} fontFamily={FONT.ui} fontWeight={900} fontSize={70} fill={color} />);
  yield* all(n().position(p.add([dx, -120]), 0.8, easeOutCubic), n().opacity(0, 0.8, easeInCubic), n().scale(1.4, 0.8));
  n().remove();
}

/**
 * The touch pin as a bucket: an ESP32 pin (left) keeps pouring charge
 * through its wire into a bucket; the bucket drains when full and starts
 * again. `size` makes the bucket bigger (a finger adds capacity), `fillDur`
 * is the time for one fill, `count` is the readout on the right.
 */
export class BucketRig {
  public static readonly PIN = new Vector2(-760, -230);
  public static readonly NOZZLE = new Vector2(-60, -230);
  public static readonly BASE = 320; // bucket bottom (view y)
  public static readonly BW = 240;
  public static readonly BH = 260;

  public readonly root = createRef<Node>();
  public readonly wire = createRef<Line>();
  public readonly flow = createRef<Line>();
  public readonly bucket = createRef<Node>();
  public readonly bodyRect = createRef<Rect>();
  public readonly panel = createRef<Rect>();
  public readonly number = createRef<Txt>();
  public readonly panelLabel = createRef<Txt>();
  public readonly level = createSignal(0);
  public readonly size = createSignal(1);
  public readonly fillDur = createSignal(0.55);
  public readonly count = createSignal(60);
  public readonly pouring = createSignal(0);
  public readonly flowOffset = createSignal(0);

  public node() {
    const {PIN, NOZZLE, BASE, BW, BH} = BucketRig;
    const surfaceY = () => BASE - 8 * this.size() - this.level() * (BH - 30) * this.size();
    return (
      <Node ref={this.root}>
        {/* board edge with the touch pin */}
        <Rect x={PIN.x - 60} y={PIN.y} width={200} height={240} radius={16} fill={'#1b2233'} stroke={'#2e3a55'} lineWidth={4}>
          <Txt x={-20} y={-80} text={'ESP32'} fontFamily={FONT.ui} fontWeight={800} fontSize={30} fill={C.dim} />
          {[-60, 0, 60].map(y => (
            <Rect x={84} y={y + 20} width={18} height={18} radius={3} fill={'#8f7a45'} />
          ))}
          <Rect x={84} y={0} width={24} height={24} radius={4} fill={'#ffd36b'} shadowColor={C.amber} shadowBlur={16} />
        </Rect>
        <Rect x={PIN.x - 60} y={PIN.y + 160} layout padding={[4, 16]} radius={10} fill={'#101a2c'} stroke={C.amber} lineWidth={3}>
          <Txt text={'GPIO 14'} fontFamily={FONT.code} fontWeight={800} fontSize={30} fill={C.amber} />
        </Rect>
        {/* the wire + the charge flowing along it */}
        <Line ref={this.wire} points={[PIN.add([36, 0]), NOZZLE]} stroke={'#d0d6e0'} lineWidth={12} lineCap={'round'} />
        <Line
          ref={this.flow}
          points={[PIN.add([36, 0]), NOZZLE]}
          stroke={C.teal}
          lineWidth={6}
          lineCap={'round'}
          lineDash={[10, 26]}
          lineDashOffset={() => this.flowOffset()}
        />
        {/* nozzle + stream into the bucket */}
        <Rect x={NOZZLE.x} y={NOZZLE.y + 18} width={34} height={50} radius={6} fill={'#9aa8bd'} />
        <Rect
          x={NOZZLE.x}
          y={() => (NOZZLE.y + 43 + surfaceY()) / 2}
          width={12}
          height={() => Math.max(0, surfaceY() - (NOZZLE.y + 43))}
          fill={C.teal}
          opacity={() => this.pouring() * 0.85}
        />
        {/* the bucket (grows upwards from its bottom) */}
        <Node ref={this.bucket} x={NOZZLE.x} y={() => BASE - (BH / 2) * this.size()} scale={() => this.size()}>
          {/* the handle fades out when the bucket grows (it would cross the wire) */}
          <Circle y={-BH / 2} size={BW * 0.95} stroke={'#9aa8bd'} lineWidth={6} startAngle={190} endAngle={350} opacity={() => Math.max(0, Math.min(1, (1.3 - this.size()) / 0.25))} />
          <Rect ref={this.bodyRect} width={BW} height={BH} radius={[6, 6, 34, 34]} fill={'#22314d'} stroke={'#9aa8bd'} lineWidth={6} clip>
            <Rect
              y={() => BH / 2 - (this.level() * (BH - 30)) / 2}
              width={BW}
              height={() => this.level() * (BH - 30)}
              fill={'rgba(45,212,191,0.85)'}
            />
            <Rect y={() => BH / 2 - this.level() * (BH - 30)} width={BW} height={6} fill={'#9ff3e6'} opacity={() => (this.level() > 0.02 ? 1 : 0)} />
          </Rect>
          <Rect y={-BH / 2} width={BW + 22} height={18} radius={9} fill={'#9aa8bd'} />
        </Node>
        {/* the readout */}
        <Rect
          ref={this.panel}
          x={590}
          y={0}
          width={460}
          height={320}
          radius={24}
          fill={'rgba(13,22,40,0.95)'}
          stroke={C.line}
          lineWidth={3}
          opacity={0}
        >
          <Txt ref={this.panelLabel} y={-105} text={'fills per moment'} fontFamily={FONT.ui} fontWeight={700} fontSize={36} fill={C.dim} />
          <Txt ref={this.number} y={20} text={() => String(Math.round(this.count()))} fontFamily={FONT.code} fontWeight={800} fontSize={150} fill={C.text} />
          <Txt y={120} text={'touchRead()'} fontFamily={FONT.code} fontSize={28} fill={C.teal} />
        </Rect>
      </Node>
    );
  }

  /** Background thread: fill, drain, fill, drain ... (speed = fillDur). */
  public *run(): ThreadGenerator {
    while (true) {
      this.pouring(1);
      yield* all(this.level(1, this.fillDur(), linear), this.flowOffset(this.flowOffset() - 36 * this.fillDur() * 3, this.fillDur(), linear));
      this.pouring(0);
      yield* all(this.level(0, 0.16, easeInCubic), this.bodyRect().stroke('#e9edf2', 0.06).to('#9aa8bd', 0.12));
    }
  }
}
