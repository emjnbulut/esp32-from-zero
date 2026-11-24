/**
 * Shared bits for the Ep11 ("Motion Alarm") scenes: timing accessor, the
 * full-code glimpse on the Ep11 sketch, the PIR sensor, the thumbs up / down
 * answer (ANALOGIES: PIR output = thumb), a warm walking figure.
 *
 * Re-time after the narration exists:  node video/mc/tools/timing.mjs ep11
 */
import {Circle, Node, Rect, Txt, View2D} from '@motion-canvas/2d';
import {
  all,
  createRef,
  easeInOutCubic,
  easeOutBack,
  Reference,
  ThreadGenerator,
  Vector2,
} from '@motion-canvas/core';
import data from '../timing/ep11.json';
import sketch from '../timing/ep11_sketch.json';
import {makeTiming} from './ep10';
import {SketchGlimpse} from './glimpse';
import {C, FONT} from '../style';

export const timing11 = makeTiming(data, 'ep11');
export const SKETCH11 = sketch as {file: string; folder: string; lines: string[]};

/**
 * Full-code glimpse of motion_alarm.ino: add on top, run as a background
 * thread; `target()` = view centre of the scene's big code text.
 */
export function glimpse11(
  view: View2D,
  o: {from: number; to: number; match: string},
  target: () => Vector2,
  targetFont: number,
  zoomAt = 1.1,
): ThreadGenerator {
  const g = new SketchGlimpse({...o, sketch: SKETCH11});
  view.add(g.node());
  return g.play(view, target, targetFont / g.font, zoomAt, 0.5);
}

/** HC-SR501: green board + white Fresnel dome. */
export function Pir(props: {refNode: Reference<Node>; x?: number; y?: number; scale?: number}) {
  return (
    <Node ref={props.refNode} x={props.x ?? 0} y={props.y ?? 0} scale={props.scale ?? 1}>
      <Rect width={200} height={200} radius={14} fill={'#1f6b3a'} stroke={'#2f8f52'} lineWidth={4} />
      <Circle size={150} fill={'#eef1f4'} stroke={'#c9ced6'} lineWidth={4} />
      {[0, 1, 2].map(i => (
        <Circle size={110 - i * 32} stroke={'#d5dae2'} lineWidth={3} />
      ))}
      <Txt y={128} text={'PIR'} fontFamily={FONT.ui} fontWeight={800} fontSize={30} fill={C.dim} />
    </Node>
  );
}

/**
 * Thumb icon: up = HIGH ("yes, something warm moved"), down = LOW.
 * `root` rotates 0 (up) / 180 (down); `fill` colours the hand.
 */
export class Thumb {
  public readonly root = createRef<Node>();
  public readonly hand = createRef<Node>();
  public readonly fist = createRef<Rect>();
  public readonly finger = createRef<Rect>();

  public constructor(private readonly o: {x?: number; y?: number; scale?: number; up?: boolean} = {}) {}

  public node() {
    const col = this.o.up ? C.teal : '#6b7a90';
    return (
      <Node ref={this.root} x={this.o.x ?? 0} y={this.o.y ?? 0} scale={this.o.scale ?? 1} rotation={this.o.up ? 0 : 180}>
        <Node ref={this.hand}>
          <Rect ref={this.finger} x={-34} y={-62} width={44} height={96} radius={22} fill={col} />
          <Rect ref={this.fist} x={10} y={22} width={120} height={104} radius={28} fill={col} />
          {[0, 1, 2].map(i => (
            <Rect x={52} y={-6 + i * 28} width={36} height={4} radius={2} fill={'rgba(11,18,32,0.35)'} />
          ))}
        </Node>
      </Node>
    );
  }

  public *set(up: boolean, dur = 0.3): ThreadGenerator {
    const col = up ? C.teal : '#6b7a90';
    yield* all(
      this.root().rotation(up ? 0 : 180, dur, easeOutBack),
      this.fist().fill(col, dur * 0.6),
      this.finger().fill(col, dur * 0.6),
      this.root().scale(this.root().scale().x * 1.12, dur * 0.4).to(this.root().scale().x, dur * 0.6),
    );
  }
}

/** A warm walking figure (amber glow): head + body; walk it with position.x. */
export function Walker(props: {refNode: Reference<Node>; x?: number; y?: number; scale?: number}) {
  return (
    <Node ref={props.refNode} x={props.x ?? 0} y={props.y ?? 0} scale={props.scale ?? 1}>
      <Circle size={190} fill={'rgba(255,140,60,0.16)'} />
      <Circle y={-60} size={50} fill={C.amber} />
      <Rect y={10} width={56} height={90} radius={24} fill={C.amber} />
      <Rect x={-14} y={78} width={18} height={56} radius={9} fill={C.amber} />
      <Rect x={14} y={78} width={18} height={56} radius={9} fill={C.amber} />
    </Node>
  );
}

/** Walk a figure across: from x0 to x1 with a little bob. */
export function* walk(n: Node, x0: number, x1: number, dur: number): ThreadGenerator {
  n.position.x(x0);
  const y = n.position.y();
  yield* all(
    n.position.x(x1, dur, easeInOutCubic),
    n.position.y(y - 10, dur / 6).to(y, dur / 6).to(y - 10, dur / 6).to(y, dur / 6).to(y - 10, dur / 6).to(y, dur / 6),
  );
}
