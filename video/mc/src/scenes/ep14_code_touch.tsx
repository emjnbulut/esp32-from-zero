/**
 * Ep14 s09 - "In code, one line reads it: touch read, on pin fourteen.
 * Touched means: the number fell well below its calm value."
 *   if (touchRead(KEY_PIN[i]) < calm[i] - DROP) return i;     (DROP = 20)
 * Glimpse -> the line; a number scale: calm 60, the line at calm - DROP = 40,
 * the reading falls 60 -> 25 past the line = touched.
 */
import {Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, createSignal, easeInOutCubic, easeOutBack, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {addCodeLabel, showLabel} from '../lib/ep12';
import {glimpse14, timing14} from '../lib/ep14';
import {C, FONT} from '../style';

const T = timing14('code_touch');
const LINE = 'if (touchRead(KEY_PIN[i]) < calm[i] - DROP) return i;';

// number scale 0..80
const X0 = -700;
const X1 = 700;
const vx = (v: number) => X0 + ((X1 - X0) * v) / 80;
const AXIS_Y = 160;
const BAR_Y = 95;

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -290, size: 44, code: LINE});
  const reading = createSignal(60);
  const scale = createRef<Node>();
  const bar = createRef<Rect>();
  const calmMark = createRef<Node>();
  const limitMark = createRef<Node>();
  const zone = createRef<Rect>();
  const touched = createRef<Rect>();
  const calmTxt = createRef<Txt>();
  const limitTxt = createRef<Txt>();

  view.add(
    <Node ref={scale} opacity={0}>
      {/* the "touched" zone: below calm - DROP */}
      <Rect ref={zone} x={(vx(0) + vx(40)) / 2} y={BAR_Y} width={vx(40) - vx(0)} height={110} radius={10} fill={'rgba(255,93,108,0.10)'} opacity={0} />
      <Line points={[[X0, AXIS_Y], [X1, AXIS_Y]]} stroke={C.dim} lineWidth={4} />
      {[0, 20, 40, 60, 80].flatMap(v => [
        <Line points={[[vx(v), AXIS_Y], [vx(v), AXIS_Y + 14]]} stroke={C.dim} lineWidth={4} />,
        <Txt x={vx(v)} y={AXIS_Y + 40} text={String(v)} fontFamily={FONT.code} fontSize={28} fill={C.dim} />,
      ])}
      {/* the reading */}
      <Rect
        ref={bar}
        x={X0}
        y={BAR_Y}
        offsetX={-1}
        width={() => vx(reading()) - X0}
        height={46}
        radius={[0, 12, 12, 0]}
        fill={C.teal}
      />
      {/* the value sits inside the bar, so it never collides with the calm / limit marks */}
      <Txt
        x={X0 + 18}
        y={BAR_Y + 2}
        offsetX={-1}
        text={() => String(Math.round(reading()))}
        fontFamily={FONT.code}
        fontWeight={800}
        fontSize={38}
        fill={C.bg}
      />
      <Node ref={calmMark}>
        <Line points={[[vx(60), BAR_Y - 60], [vx(60), AXIS_Y]]} stroke={C.teal} lineWidth={5} />
        <Txt ref={calmTxt} x={vx(60)} y={BAR_Y - 86} text={'calm 60'} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={C.teal} />
      </Node>
      <Node ref={limitMark} opacity={0}>
        <Line points={[[vx(40), BAR_Y - 60], [vx(40), AXIS_Y]]} stroke={C.amber} lineWidth={5} lineDash={[12, 8]} />
        <Txt ref={limitTxt} x={vx(40)} y={BAR_Y - 86} text={'calm − DROP = 40'} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={C.amber} />
      </Node>
    </Node>,
  );
  view.add(<Pill refNode={touched} text={'touched!'} color={C.red} x={(vx(0) + vx(40)) / 2} y={275} size={38} />);
  view.add(code.node());

  const h1 = new Headline('One line *reads* the touch', {accent: C.teal});
  view.add(h1.node());

  const ZOOM_AT = 1.1;
  yield glimpse14(view, {from: 52, to: 52, match: LINE}, () => toView(view, code.code().absolutePosition()), 44, ZOOM_AT);

  yield* h1.in();
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);

  // touch read ...
  yield* until(Math.max(useTime(), T.word('read', 2.9, undefined, 1) - 0.4));
  scale().position.y(30);
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('touchRead')), 0.25),
    h1.pulse(),
    scale().opacity(1, 0.3),
    scale().position.y(0, 0.35),
  );
  // a live reading that wobbles around its calm value until the touch
  let live = true;
  yield (function* () {
    const seq = [61, 59, 60, 62, 58, 60, 61, 59];
    for (let k = 0; live; k++) yield* reading(seq[k % seq.length], 0.18);
  })();
  // ... on pin fourteen
  const lPin = addCodeLabel(view, code.code(), 'KEY_PIN[i]', 'pin 14', C.amber, 0, 32);
  yield* until(Math.max(useTime(), T.word('fourteen', 4.46) - 0.3));
  yield* all(code.code().selection(code.code().findFirstRange(lit('touchRead(KEY_PIN[i])')), 0.25), showLabel(lPin));

  // touched means: the number fell well below its calm value
  yield* until(Math.max(useTime(), T.word('touched', 5.56) - 0.2));
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('touchRead(KEY_PIN[i]) < calm[i] - DROP')), 0.25),
  );
  yield* until(Math.max(useTime(), T.word('fell', 7.1) - 0.35));
  live = false; // the wobble thread ends within one 0.18 s step
  yield* all(limitMark().opacity(1, 0.25), zone().opacity(1, 0.25));
  yield* reading(25, 0.9, easeInOutCubic);
  yield* all(bar().fill(C.red, 0.2), popIn(touched(), 0.3));

  const lDrop = addCodeLabel(view, code.code(), 'DROP', '20', C.amber, 0, 32);
  yield* until(Math.max(useTime(), T.word('calm', 8.68) - 0.2));
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('calm[i] - DROP')), 0.25),
    showLabel(lDrop),
    calmTxt().scale(1.15, 0.12).to(1, 0.25, easeOutBack),
    limitTxt().scale(1.15, 0.12).to(1, 0.25, easeOutBack),
  );
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
