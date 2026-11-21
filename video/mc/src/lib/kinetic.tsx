import {Layout, Node, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  easeInCubic,
  easeOutCubic,
  Reference,
  sequence,
  ThreadGenerator,
} from '@motion-canvas/core';
import {C, FONT} from '../style';

/**
 * Kinetic headline: each word slides up out of its own mask.
 * Words wrapped in *asterisks* get the accent colour.
 */
export class Headline {
  public readonly root = createRef<Layout>();
  private words: {
    mask: Reference<Rect>;
    txt: Reference<Txt>;
    accent: boolean;
  }[] = [];

  public constructor(
    private readonly text: string,
    private readonly opts: {
      y?: number;
      size?: number;
      accent?: string;
    } = {},
  ) {}

  public node(): Node {
    const size = this.opts.size ?? 64;
    const lineH = Math.round(size * 1.3);
    const accent = this.opts.accent ?? C.amber;
    this.words = this.text.split(' ').map(raw => ({
      mask: createRef<Rect>(),
      txt: createRef<Txt>(),
      accent: raw.startsWith('*') && raw.endsWith('*'),
    }));
    return (
      <Layout
        ref={this.root}
        layout
        direction="row"
        gap={size * 0.28}
        alignItems="center"
        y={this.opts.y ?? -440}
      >
        {this.text.split(' ').map((raw, i) => {
          const isAccent = raw.startsWith('*') && raw.endsWith('*');
          const word = raw.replace(/\*/g, '');
          return (
            <Rect
              ref={this.words[i].mask}
              layout
              clip
              direction="column"
              height={lineH}
            >
              <Txt
                ref={this.words[i].txt}
                text={word}
                fontFamily={FONT.ui}
                fontWeight={isAccent ? 800 : 700}
                fontSize={size}
                lineHeight={lineH}
                fill={isAccent ? accent : C.text}
                marginTop={lineH}
              />
            </Rect>
          );
        })}
      </Layout>
    ) as Node;
  }

  public *in(stagger = 0.07, duration = 0.38): ThreadGenerator {
    yield* sequence(
      stagger,
      ...this.words.map(w => w.txt().margin.top(0, duration, easeOutCubic)),
    );
  }

  public *out(stagger = 0.04, duration = 0.28): ThreadGenerator {
    const lineH = this.words[0]?.mask().height() ?? 80;
    yield* sequence(
      stagger,
      ...this.words.map(w =>
        w.txt().margin.top(-lineH * 1.6, duration, easeInCubic),
      ),
    );
  }

  /** Quick attention pulse on the accent words. */
  public *pulse(): ThreadGenerator {
    yield* all(
      ...this.words.map(w =>
        w.accent
          ? w.txt().scale(1.12, 0.15).to(1, 0.25)
          : w.txt().scale(1, 0),
      ),
    );
  }
}
