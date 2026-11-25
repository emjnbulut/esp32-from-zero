/**
 * Ep15 s18 - "And the counter goes up by one, written into the notebook from
 * episode ten. Only when the drawer opens, never every loop."
 *   openings++;
 *   prefs.putInt("openings", openings);     (inside the "it opened" if)
 * The openings box goes 2 -> 3, the value is written into the notebook
 * (Preferences = "the notebook from Episode 10"; in this episode always
 * "notebook", never "drawer"). A row of loop() ticks: only the one where the
 * drawer opens writes.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, createSignal, easeOutBack, easeOutCubic, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {Box} from '../lib/ep14';
import {glimpse15, timing15} from '../lib/ep15';
import {C, FONT} from '../style';

const T = timing15('code_counter');
const PUT = 'prefs.putInt("openings", openings);';
const CODE = 'openings++;\n' + PUT;
const NX = 330;
const NY = 30;
const TICKS = 14;
const OPEN_TICK = 5;
const STRIP_Y = 322;
const tickX = (i: number) => -620 + i * 100;

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -275, size: 44, code: CODE});
  const box = new Box({x: -520, y: NY, w: 270, h: 190, label: 'openings', value: '2', labelSize: 30, valueSize: 80});
  const plus = createRef<Txt>();
  const arrow = createRef<Line>();
  const book = createRef<Node>();
  const oldVal = createRef<Txt>();
  const strike = createRef<Line>();
  const written = createSignal('');
  const sticker = createRef<Rect>();
  const strip = createRef<Node>();
  const ticks = Array.from({length: TICKS}, () => createRef<Circle>());
  const openTag = createRef<Rect>();
  const pen = createRef<Txt>();
  const never = createRef<Rect>();

  view.add(box.node());
  view.add(<Txt ref={plus} x={-380} y={NY - 120} text={'+1'} fontFamily={FONT.ui} fontWeight={900} fontSize={60} fill={C.amber} opacity={0} />);
  view.add(<Line ref={arrow} points={[[-360, NY], [NX - 210, NY]]} stroke={C.amber} lineWidth={6} endArrow arrowSize={18} end={0} />);
  // the notebook (spiral-bound page)
  view.add(
    <Node ref={book} x={NX} y={NY} opacity={0}>
      <Rect width={380} height={300} radius={12} fill={'#fbf6e6'} stroke={'#d6cdb6'} lineWidth={3} shadowColor={'rgba(0,0,0,0.45)'} shadowBlur={24} shadowOffsetY={8} />
      {[-90, -30, 30, 90].map(y => (
        <Line points={[[-160, y + 20], [160, y + 20]]} stroke={'#c9d7ea'} lineWidth={2} />
      ))}
      <Line points={[[-130, -140], [-130, 140]]} stroke={'#f2b8b8'} lineWidth={2} />
      {Array.from({length: 9}, (_, i) => (
        <Circle x={-160 + i * 40} y={-150} size={22} stroke={'#8a97ab'} lineWidth={4} fill={'#0b1220'} />
      ))}
      <Txt x={-110} y={-48} offsetX={-1} text={'openings: '} fontFamily={FONT.ui} fontStyle={'italic'} fontWeight={700} fontSize={40} fill={'#1b2a4a'} />
      <Txt ref={oldVal} x={102} y={-48} text={'2'} fontFamily={FONT.ui} fontStyle={'italic'} fontWeight={700} fontSize={40} fill={'#1b2a4a'} />
      <Line ref={strike} points={[[87, -40], [117, -56]]} stroke={'#c0392b'} lineWidth={5} end={0} />
      <Txt x={150} y={-48} text={() => written()} fontFamily={FONT.ui} fontStyle={'italic'} fontWeight={800} fontSize={44} fill={'#c0392b'} />
    </Node>,
  );
  view.add(
    <Rect ref={sticker} x={NX + 70} y={NY - 192} rotation={3} layout padding={[6, 16]} radius={10} fill={C.teal} opacity={0} scale={0.5}>
      <Txt text={'the notebook from Episode 10'} fontFamily={FONT.ui} fontWeight={800} fontSize={28} fill={C.bg} />
    </Rect>,
  );
  // loop() ticks
  view.add(
    <Node ref={strip} opacity={0}>
      <Txt x={tickX(0) - 40} y={STRIP_Y} offsetX={1} text={'loop()'} fontFamily={FONT.code} fontWeight={800} fontSize={30} fill={C.dim} />
      <Line points={[[tickX(0), STRIP_Y], [tickX(TICKS - 1), STRIP_Y]]} stroke={C.line} lineWidth={4} />
      {ticks.map((r, i) => (
        <Circle ref={r} x={tickX(i)} y={STRIP_Y} size={26} fill={'#22324f'} stroke={i === OPEN_TICK ? C.amber : C.line} lineWidth={3} />
      ))}
    </Node>,
  );
  view.add(<Pill refNode={openTag} text={'drawer opens'} color={C.amber} x={tickX(OPEN_TICK)} y={STRIP_Y - 52} size={28} />);
  view.add(<Txt ref={pen} x={tickX(OPEN_TICK) + 125} offsetX={-1} y={STRIP_Y - 52} text={'✎ write'} fontFamily={FONT.ui} fontWeight={800} fontSize={30} fill={C.amber} opacity={0} />);
  view.add(<Pill refNode={never} text={'✗ not every loop'} color={C.red} x={NX + 70} y={NY + 210} size={30} />);
  view.add(code.node());

  const h1 = new Headline('Count it, *write* it down', {accent: C.amber});
  view.add(h1.node());

  const lineCenter = () => {
    const c = code.code();
    const b = c.getSelectionBBox(c.findFirstRange(lit(PUT)))[0];
    return toView(view, b.center.transformAsPoint(c.localToWorld()));
  };
  const ZOOM_AT = 0.9;
  yield glimpse15(view, {from: 71, to: 72, match: PUT}, lineCenter, 44, ZOOM_AT);

  yield* h1.in();
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);

  // the counter goes up by one
  yield* until(Math.max(useTime(), T.word('up', 0.82) - 0.1));
  plus().y(NY - 90);
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('openings++;')), 0.25),
    plus().opacity(1, 0.15),
    plus().y(NY - 140, 0.4, easeOutCubic),
    box.body().stroke(C.amber, 0.2),
  );
  box.value().text('3');
  yield* all(box.root().scale(1.1, 0.1).to(1, 0.25, easeOutBack), plus().opacity(0, 0.3));

  // ... written into the notebook from episode ten
  yield* until(Math.max(useTime(), T.word('written', 1.74) - 0.25));
  book().y(NY + 30);
  yield* all(
    code.code().selection(code.code().findFirstRange(lit(PUT)), 0.25),
    book().opacity(1, 0.3),
    book().y(NY, 0.35, easeOutCubic),
    arrow().end(1, 0.45, easeOutCubic),
  );
  yield* strike().end(1, 0.2);
  written('3');
  yield* all(oldVal().opacity(0.45, 0.2));
  yield* until(Math.max(useTime(), T.word('episode', 3.74) - 0.3));
  yield* popIn(sticker(), 0.35);

  // only when the drawer opens, never every loop
  yield* until(Math.max(useTime(), T.word('only', 5.12) - 0.3));
  yield* strip().opacity(1, 0.25);
  for (let i = 0; i < TICKS; i++) {
    const r = ticks[i]();
    if (i === OPEN_TICK) {
      yield* all(r.fill(C.amber, 0.08), r.scale(1.5, 0.1).to(1.2, 0.15), popIn(openTag(), 0.25));
      yield all(pen().opacity(1, 0.2), book().scale(1.06, 0.1).to(1, 0.2), arrow().stroke('#ffe0a6', 0.1).to(C.amber, 0.2));
    } else {
      r.fill(C.dim);
      yield r.fill('#22324f', 0.25);
      yield* until(useTime() + 0.13);
    }
  }
  yield* until(Math.max(useTime(), T.word('never', 6.8) - 0.2));
  yield* popIn(never(), 0.3);
  yield grid().opacity(0.6, 1.0, linear);
  yield* until(T.total);
}));
