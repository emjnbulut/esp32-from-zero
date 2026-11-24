/**
 * Shared bits for the Ep12 ("Control your ESP32 from your phone") scenes:
 * timing accessor, the full-code glimpse on phone_remote.ino, the phone with
 * the sketch's web page (5 buttons, same colours as PAGE), code labels, an
 * RGB LED and Wi-Fi waves.
 *
 * Re-time after a narration change:  node video/mc/tools/timing.mjs ep12
 */
import {Circle, Code, Line, Node, Rect, Txt, View2D} from '@motion-canvas/2d';
import {
  all,
  createRef,
  createSignal,
  easeOutCubic,
  Reference,
  SimpleSignal,
  ThreadGenerator,
  Vector2,
} from '@motion-canvas/core';
import data from '../timing/ep12.json';
import sketch from '../timing/ep12_sketch.json';
import {lit, makeTiming, toView} from './ep10';
import {SketchGlimpse} from './glimpse';
import {C, FONT} from '../style';

export const timing12 = makeTiming(data, 'ep12');
export const SKETCH12 = sketch as {file: string; folder: string; lines: string[]};

/** Full-code glimpse of phone_remote.ino (add on top, run as a background thread). */
export function glimpse12(
  view: View2D,
  o: {from: number; to: number; match: string},
  target: () => Vector2,
  targetFont: number,
  zoomAt = 1.1,
): ThreadGenerator {
  const g = new SketchGlimpse({...o, sketch: SKETCH12});
  view.add(g.node());
  return g.play(view, target, targetFont / g.font, zoomAt, 0.5);
}

/** The five links of the sketch's PAGE (labels + colours exactly as in the .ino). */
export const BUTTONS = [
  {label: 'RED', color: '#e5484d', link: '/color?c=red'},
  {label: 'GREEN', color: '#2fbf71', link: '/color?c=green'},
  {label: 'BLUE', color: '#3b82f6', link: '/color?c=blue'},
  {label: 'OFF', color: '#334155', link: '/color?c=off'},
  {label: 'RING', color: '#f59e0b', link: '/ring'},
];

/** A phone showing the board's page (http://192.168.4.1). */
export class Phone {
  public readonly root = createRef<Node>();
  public readonly screen = createRef<Rect>();
  public readonly page = createRef<Node>();
  public readonly buttons = BUTTONS.map(() => createRef<Rect>());
  public readonly labels = BUTTONS.map(() => createRef<Txt>());
  public readonly tags = BUTTONS.map(() => createRef<Rect>());
  public readonly tagTxt = BUTTONS.map(() => createRef<Txt>());
  public readonly address = createRef<Txt>();
  public static readonly BTN_Y = (i: number) => -120 + i * 84;

  public constructor(private readonly o: {x?: number; y?: number; scale?: number} = {}) {}

  public node() {
    return (
      <Node ref={this.root} x={this.o.x ?? 0} y={this.o.y ?? 0} scale={this.o.scale ?? 1}>
        <Rect width={330} height={660} radius={46} fill={'#0d1117'} stroke={'#3a4766'} lineWidth={6} shadowColor={'rgba(0,0,0,0.55)'} shadowBlur={36} shadowOffsetY={12} />
        <Rect ref={this.screen} width={298} height={610} radius={32} fill={'#0b1220'} clip>
          <Rect y={-282} width={90} height={22} radius={11} fill={'#05070c'} />
          <Rect y={-240} width={250} height={36} radius={18} fill={'#1e2a40'}>
            <Txt ref={this.address} text={'192.168.4.1'} fontFamily={FONT.ui} fontSize={19} fill={C.dim} />
          </Rect>
          <Node ref={this.page}>
            <Txt y={-186} text={'ESP32 remote'} fontFamily={FONT.ui} fontWeight={800} fontSize={28} fill={C.text} />
            {BUTTONS.map((b, i) => (
              <Rect ref={this.buttons[i]} y={Phone.BTN_Y(i)} width={244} height={66} radius={16} fill={b.color}>
                <Txt ref={this.labels[i]} text={b.label} fontFamily={FONT.ui} fontWeight={800} fontSize={27} fill={'#ffffff'} />
              </Rect>
            ))}
          </Node>
          {/* small tags on the buttons (numbers / links) - hidden by default */}
          {BUTTONS.map((_, i) => (
            <Rect
              ref={this.tags[i]}
              x={-96}
              y={Phone.BTN_Y(i)}
              layout
              padding={[2, 10]}
              radius={10}
              fill={'#0b1220'}
              opacity={0}
              scale={0.4}
            >
              <Txt ref={this.tagTxt[i]} text={String(i + 1)} fontFamily={FONT.code} fontWeight={800} fontSize={24} fill={C.amber} />
            </Rect>
          ))}
        </Rect>
      </Node>
    );
  }

  /** view-space centre of button i */
  public buttonPos(view: View2D, i: number) {
    return toView(view, this.buttons[i]().absolutePosition());
  }

  /** a finger tap on button i: ripple + squash */
  public *tap(i: number): ThreadGenerator {
    const ring = createRef<Circle>();
    this.buttons[i]().add(<Circle ref={ring} size={20} stroke={'#ffffff'} lineWidth={6} opacity={0.9} />);
    yield* all(
      this.buttons[i]().scale(0.92, 0.08).to(1, 0.2),
      ring().size(200, 0.45, easeOutCubic),
      ring().opacity(0, 0.45),
    );
    ring().remove();
  }
}

/** Bracket + label under a token of a Code node (like the Ep10 tone labels). */
export function addCodeLabel(
  view: View2D,
  code: Code,
  token: string | RegExp,
  text: string,
  color: string,
  dy = 0,
  size = 34,
): Reference<Node> {
  const box = code.getSelectionBBox(code.findFirstRange(typeof token === 'string' ? lit(token) : token))[0];
  const left = toView(view, box.topLeft.transformAsPoint(code.localToWorld()));
  const right = toView(view, box.bottomRight.transformAsPoint(code.localToWorld()));
  const y = right.y + 30; // below the code panel's padding
  const cx = (left.x + right.x) / 2;
  const ref = createRef<Node>();
  view.add(
    <Node ref={ref} opacity={0} y={16}>
      <Line points={[[left.x + 4, y], [left.x + 4, y + 14], [right.x - 4, y + 14], [right.x - 4, y]]} stroke={color} lineWidth={4} />
      <Line points={[[cx, y + 14], [cx, y + 34 + dy]]} stroke={color} lineWidth={4} />
      <Rect x={cx} y={y + 34 + dy + size * 0.8} layout padding={[4, 16]} radius={12} fill={'rgba(13,22,40,0.92)'} stroke={color} lineWidth={3}>
        <Txt text={text} fontFamily={FONT.ui} fontWeight={800} fontSize={size} fill={color} />
      </Rect>
    </Node>,
  );
  return ref;
}

export function* showLabel(ref: Reference<Node>): ThreadGenerator {
  yield* all(ref().opacity(1, 0.25), ref().y(0, 0.3, easeOutCubic));
}

/** RGB LED (top view): its colour is a signal so scenes can light it. */
export function Led(props: {refNode: Reference<Node>; color: SimpleSignal<string>; x?: number; y?: number; scale?: number}) {
  return (
    <Node ref={props.refNode} x={props.x ?? 0} y={props.y ?? 0} scale={props.scale ?? 1}>
      <Circle size={220} fill={() => props.color()} opacity={() => (props.color() === '#1a2233' ? 0 : 0.18)} />
      <Circle size={120} fill={() => props.color()} stroke={'#c9d1dc'} lineWidth={5} shadowColor={() => props.color()} shadowBlur={40} />
      <Circle x={-22} y={-22} size={28} fill={'rgba(255,255,255,0.35)'} />
      {[-30, -10, 10, 30].map(x => (
        <Line points={[[x, 60], [x, 130]]} stroke={C.metal} lineWidth={6} />
      ))}
    </Node>
  );
}
export const LED_OFF = '#1a2233';
export const ledSignal = () => createSignal(LED_OFF);

/** Wi-Fi arcs above a point (pulse them with `pulseWifi`). */
export function Wifi(props: {refs: Reference<Circle>[]; x?: number; y?: number; color?: string}) {
  return (
    <Node x={props.x ?? 0} y={props.y ?? 0}>
      {props.refs.map((r, i) => (
        <Circle ref={r} size={60 + i * 60} stroke={props.color ?? C.teal} lineWidth={9} startAngle={-135} endAngle={-45} opacity={0.25} />
      ))}
      <Circle y={0} size={18} fill={props.color ?? C.teal} />
    </Node>
  );
}

export function* pulseWifi(refs: Reference<Circle>[]): ThreadGenerator {
  for (const r of refs) {
    yield* r().opacity(1, 0.12);
  }
  yield* all(...refs.map(r => r().opacity(0.25, 0.3)));
}
