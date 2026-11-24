/**
 * Ep11 s20 - the siren: tone(BUZZER_PIN, (inState / 250) % 2 ? 2600 : 1800);
 * Full-code glimpse first, then two notes alternating on a scrolling timeline,
 * 250 ms each = four switches a second.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  createSignal,
  DEFAULT,
  delay,
  easeOutBack,
  easeOutCubic,
  linear,
  loop,
  useTime,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {glimpse11, timing11} from '../lib/ep11';
import {C, FONT, H, W} from '../style';

const T = timing11('code_siren');
const LINE = 'tone(BUZZER_PIN, (inState / 250) % 2 ? 2600 : 1800);';

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -260, size: 46, code: LINE});
  const track = createRef<Node>();
  const buzzer = createRef<Node>();
  const waves = [createRef<Circle>(), createRef<Circle>(), createRef<Circle>()];
  const note = createRef<Txt>();
  const bracket = createRef<Node>();
  const red = createRef<Rect>();
  const sirenTag = createRef<Rect>();

  const BW = 130; // one block = 250 ms
  const HI_Y = 40;
  const LO_Y = 150;
  const X0 = -560;
  const X1 = 820;
  const pos = createSignal(0); // scroll in px
  const nBlocks = 40;
  const P = BW * 1.5; // playhead, measured from the track start
  const idx = () => Math.floor((pos() + P) / BW); // block under the playhead
  const cur = () => idx() % 2;

  view.add(<Rect ref={red} width={W} height={H} fill={'rgba(255,40,60,0)'} />);
  // buzzer with sound arcs
  view.add(
    <Node ref={buzzer} x={-760} y={95}>
      <Circle size={150} fill={'#14161c'} stroke={'#3a3f4c'} lineWidth={6} />
      <Circle size={24} fill={'#05060a'} />
      {waves.map(w => (
        <Circle ref={w} size={160} stroke={C.amber} lineWidth={7} startAngle={-40} endAngle={40} opacity={0} />
      ))}
    </Node>,
  );
  // timeline: blocks alternate 2600 (high, amber) / 1800 (low, teal)
  view.add(
    <Node ref={track} opacity={0}>
      <Rect x={(X0 + X1) / 2} y={(HI_Y + LO_Y) / 2} width={X1 - X0} height={200} radius={16} fill={'#101a2c'} stroke={C.line} lineWidth={2} clip>
        <Node x={-(X1 - X0) / 2} y={-(HI_Y + LO_Y) / 2}>
          {Array.from({length: nBlocks}, (_, i) => (
            <Rect
              x={() => i * BW + BW / 2 - pos()}
              y={i % 2 ? HI_Y : LO_Y}
              width={BW - 10}
              height={56}
              radius={10}
              fill={i % 2 ? C.amber : C.teal}
              opacity={() => (idx() === i ? 1 : 0.45)}
            />
          ))}
        </Node>
      </Rect>
      <Txt x={X1 + 20} y={HI_Y} offsetX={-1} text={'2600'} fontFamily={FONT.code} fontWeight={800} fontSize={34} fill={C.amber} />
      <Txt x={X1 + 20} y={LO_Y} offsetX={-1} text={'1800'} fontFamily={FONT.code} fontWeight={800} fontSize={34} fill={C.teal} />
      {/* playhead */}
      <Line points={[[X0 + P, HI_Y - 70], [X0 + P, LO_Y + 60]]} stroke={C.text} lineWidth={4} />
    </Node>,
  );
  view.add(
    <Txt
      ref={note}
      x={-760}
      y={-30}
      text={() => (cur() ? '2600 Hz' : '1800 Hz')}
      fill={() => (cur() ? C.amber : C.teal)}
      fontFamily={FONT.code}
      fontWeight={800}
      fontSize={40}
      opacity={0}
    />,
  );
  // "250 ms each -> 4x a second" bracket over four blocks (one second)
  view.add(
    <Node ref={bracket} opacity={0}>
      <Line points={[[X0 + 10, LO_Y + 80], [X0 + 10, LO_Y + 96], [X0 + 4 * BW - 10, LO_Y + 96], [X0 + 4 * BW - 10, LO_Y + 80]]} stroke={C.text} lineWidth={4} />
      <Txt x={X0 + 2 * BW} y={LO_Y + 140} text={'1 second = 4 switches'} fontFamily={FONT.ui} fontWeight={800} fontSize={36} fill={C.text} />
    </Node>,
  );
  view.add(<Pill refNode={sirenTag} text={'250 ms each'} color={C.amber} x={300} y={-150} size={34} />);
  view.add(code.node());

  const h1 = new Headline('Two notes = a *siren*', {accent: C.red});
  view.add(h1.node());

  const ZOOM_AT = 1.1;
  yield glimpse11(view, {from: 129, to: 131, match: LINE}, () => toView(view, code.code().absolutePosition()), 46, ZOOM_AT);

  yield* all(delay(0.1, h1.in()));
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);

  // the siren starts
  yield* until(Math.max(useTime(), T.word('siren', 1.9) - 0.2));
  yield* all(track().opacity(1, 0.3), note().opacity(1, 0.3), h1.pulse());
  const scrollEnd = T.total;
  yield pos((scrollEnd - useTime()) * 4 * BW, scrollEnd - useTime(), linear);
  // arcs pulse in the current note's colour, faster for the high note
  yield loop(Infinity, function* () {
    const col = cur() ? C.amber : C.teal;
    yield* all(
      ...waves.map((w, i) =>
        delay(i * 0.06, all(w().stroke(col, 0), w().size(160, 0).to(cur() ? 300 : 260, 0.25, easeOutCubic), w().opacity(1, 0.03).to(0, 0.22))),
      ),
    );
  });

  // two notes
  yield* until(Math.max(useTime(), T.word('two', 2.8) - 0.1));
  yield* code.code().selection(code.code().findFirstRange(lit('2600 : 1800')), 0.25);
  // switching four times a second
  yield* until(Math.max(useTime(), T.word('switching', 3.7) - 0.1));
  yield* all(code.code().selection(code.code().findFirstRange(lit('(inState / 250) % 2')), 0.25), popIn(sirenTag(), 0.3));
  yield* until(Math.max(useTime(), T.word('four', 4.2) - 0.1));
  bracket().position.y(14);
  yield* all(bracket().opacity(1, 0.3), bracket().position.y(0, 0.3, easeOutBack));

  // ... so it really sounds like an alarm
  yield* until(Math.max(useTime(), T.word('alarm', T.total - 1.2) - 0.4));
  yield all(code.code().selection(DEFAULT, 0.3), h1.pulse());
  yield loop(Infinity, () => red().fill('rgba(255,40,60,0.13)', 0.125).to('rgba(255,40,60,0)', 0.125));
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
