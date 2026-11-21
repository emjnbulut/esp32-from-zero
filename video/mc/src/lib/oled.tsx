import {Circle, Node, Pattern, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  easeInCubic,
  easeOutCubic,
  ThreadGenerator,
  waitFor,
} from '@motion-canvas/core';
import {C, FONT} from '../style';

/** 1-px dark grid every `cell` px -> makes plain text look like OLED pixels. */
function pixelGrid(cell = 6): Pattern {
  const canvas = document.createElement('canvas');
  canvas.width = cell;
  canvas.height = cell;
  const ctx = canvas.getContext('2d')!;
  ctx.fillStyle = 'rgba(0,0,0,0.6)';
  ctx.fillRect(cell - 1, 0, 1, cell);
  ctx.fillRect(0, cell - 1, cell, 1);
  return new Pattern({image: canvas, repetition: 'repeat'});
}

/**
 * Stylised 0.96" SSD1306 breakout: blue PCB, 4 header pins, 2:1 black glass.
 * Screen content: a small label line + one big value line.
 */
export class Oled {
  public readonly root = createRef<Node>();
  public readonly board = createRef<Rect>();
  public readonly screen = createRef<Rect>();
  public readonly content = createRef<Node>();
  public readonly label = createRef<Txt>();
  public readonly value = createRef<Txt>();
  public readonly unit = createRef<Txt>();
  public readonly glass = createRef<Rect>();

  public static readonly BOARD_W = 680;
  public static readonly BOARD_H = 420;
  public static readonly SCREEN_W = 600;
  public static readonly SCREEN_H = 300;

  public constructor(
    private readonly props: {
      x?: number;
      y?: number;
      scale?: number;
      label?: string;
      value?: string;
      unit?: string;
    } = {},
  ) {}

  public node(): Node {
    const {BOARD_W, BOARD_H, SCREEN_W, SCREEN_H} = Oled;
    const pins = ['GND', 'VCC', 'SCL', 'SDA'];
    return (
      <Node
        ref={this.root}
        x={this.props.x ?? 0}
        y={this.props.y ?? 0}
        scale={this.props.scale ?? 1}
      >
        <Rect
          ref={this.board}
          width={BOARD_W}
          height={BOARD_H}
          radius={26}
          fill={C.pcb}
          stroke={'#2b56b8'}
          lineWidth={4}
          shadowColor={'rgba(0,0,0,0.55)'}
          shadowBlur={40}
          shadowOffsetY={14}
        >
          {/* mounting holes */}
          {[
            [-1, -1],
            [1, -1],
            [-1, 1],
            [1, 1],
          ].map(([sx, sy]) => (
            <Circle
              x={sx * (BOARD_W / 2 - 26)}
              y={sy * (BOARD_H / 2 - 26)}
              size={22}
              fill={C.bg}
              stroke={'#d8b45a'}
              lineWidth={4}
            />
          ))}
          {/* header pins */}
          {pins.map((p, i) => (
            <Node x={(i - 1.5) * 58} y={-BOARD_H / 2 + 22}>
              <Rect width={22} height={22} radius={4} fill={'#d8b45a'} />
            </Node>
          ))}
          <Rect
            ref={this.screen}
            y={14}
            width={SCREEN_W}
            height={SCREEN_H}
            radius={10}
            fill={C.oledBlack}
            stroke={'#0a0f18'}
            lineWidth={6}
            clip
          >
            <Node ref={this.content}>
              <Txt
                ref={this.label}
                text={this.props.label ?? 'BEST'}
                x={-SCREEN_W / 2 + 40}
                y={-82}
                offsetX={-1}
                fontFamily={FONT.pixel}
                fontWeight={700}
                fontSize={52}
                letterSpacing={6}
                fill={C.oledOn}
                shadowColor={'rgba(190,220,255,0.8)'}
                shadowBlur={14}
              />
              <Txt
                ref={this.value}
                text={this.props.value ?? '214'}
                x={-SCREEN_W / 2 + 36}
                y={40}
                offsetX={-1}
                fontFamily={FONT.pixel}
                fontWeight={700}
                fontSize={150}
                letterSpacing={4}
                fill={C.oledOn}
                shadowColor={'rgba(190,220,255,0.85)'}
                shadowBlur={18}
              />
              <Txt
                ref={this.unit}
                text={this.props.unit ?? 'ms'}
                x={-SCREEN_W / 2 + 316}
                y={74}
                offsetX={-1}
                fontFamily={FONT.pixel}
                fontWeight={700}
                fontSize={60}
                fill={C.oledOn}
                shadowColor={'rgba(190,220,255,0.8)'}
                shadowBlur={14}
              />
            </Node>
            {/* pixel grid + glass reflection */}
            <Rect
              width={SCREEN_W}
              height={SCREEN_H}
              fill={pixelGrid(6)}
            />
            <Rect
              ref={this.glass}
              width={SCREEN_W}
              height={SCREEN_H}
              opacity={0.5}
              fill={'rgba(255,255,255,0.035)'}
            />
          </Rect>
        </Rect>
      </Node>
    );
  }

  /** CRT-style collapse: content squashes to a line, then disappears. */
  public *powerOff(): ThreadGenerator {
    yield* this.content().scale([1.04, 0.03], 0.16, easeInCubic);
    yield* all(
      this.content().scale([0, 0.03], 0.12, easeInCubic),
      this.content().opacity(0, 0.12),
    );
  }

  /** Reverse of powerOff: a line appears and opens up. */
  public *powerOn(): ThreadGenerator {
    this.content().scale([0, 0.03]);
    this.content().opacity(1);
    yield* this.content().scale([1.04, 0.03], 0.12, easeOutCubic);
    yield* this.content().scale([1, 1], 0.18, easeOutCubic);
    yield* waitFor(0);
  }

}
