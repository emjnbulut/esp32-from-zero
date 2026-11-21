/**
 * Ep10 "Reflex Game 2.0" - pilot scene: the best time survives unplugging.
 *
 * Beat 1 (0-3 s)   unplug -> OLED goes dark, RAM variables fall away
 * Beat 2 (3-8 s)   Preferences drawer (flash): 214 is filed under "best",
 *                  putULong -> getULong code morph
 * Beat 3 (8-13 s)  power on, 214 flies back out onto the OLED, pop
 */
import {
  Circle,
  Code,
  Line,
  makeScene2D,
  Node,
  Rect,
  Txt,
} from '@motion-canvas/2d';
import {
  all,
  chain,
  createRef,
  createSignal,
  DEFAULT,
  delay,
  easeInBack,
  easeInCubic,
  easeInOutCubic,
  easeOutBack,
  easeOutCubic,
  linear,
  loop,
  Reference,
  sequence,
  tween,
  Vector2,
  waitFor,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {arduino} from '../lib/arduinoHighlighter';
import {Headline} from '../lib/kinetic';
import {Oled} from '../lib/oled';
import {C, FONT} from '../style';

/** Exact-text pattern for Code.findFirstRange (strings are treated as RegExp). */
const lit = (s: string) => new RegExp(s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');

/** Small key/value card: "best" -> 214 */
function ValueCard(props: {
  refNode: Reference<Rect>;
  opacity?: number;
  x?: number;
  y?: number;
}) {
  return (
    <Rect
      ref={props.refNode}
      x={props.x ?? 0}
      y={props.y ?? 0}
      opacity={props.opacity ?? 1}
      layout
      direction="row"
      alignItems="center"
      gap={18}
      padding={[14, 24, 14, 18]}
      radius={16}
      fill={'#1e2a40'}
      stroke={C.amber}
      lineWidth={4}
      shadowColor={'rgba(255,181,71,0.45)'}
      shadowBlur={26}
    >
      <Rect padding={[6, 12]} radius={8} fill={'rgba(45,212,191,0.16)'}>
        <Txt
          text={'"best"'}
          fontFamily={FONT.code}
          fontSize={30}
          fill={C.teal}
        />
      </Rect>
      <Txt
        text={'214'}
        fontFamily={FONT.code}
        fontWeight={700}
        fontSize={60}
        fill={C.amber}
      />
    </Rect>
  );
}

export default makeScene2D(function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, 16);

  // ------------------------------------------------------------------ nodes
  const oled = new Oled({x: 230, y: -40, scale: 0.95});
  const oledFloat = createRef<Node>();
  const plug = createRef<Node>();
  const cable = createRef<Line>();

  const ram = createRef<Rect>();
  const ramCards = [createRef<Rect>(), createRef<Rect>(), createRef<Rect>()];
  const ramEmpty = createRef<Txt>();

  const cabinet = createRef<Node>();
  const drawer = createRef<Node>();
  const trayCard = createRef<Rect>();
  const savedPill = createRef<Rect>();

  const codePanel = createRef<Rect>();
  const code = createRef<Code>();
  const codeChip = createRef<Rect>();
  const codeChipTxt = createRef<Txt>();
  const note = createRef<Node>();

  const flyCard = createRef<Rect>();
  const burst = createRef<Node>();
  const check = createRef<Rect>();

  const plugBase = new Vector2(Oled.BOARD_W / 2 + 48, 70);
  // world space (canvas pixels) -> view space (origin in the centre)
  const toView = (p: Vector2) => p.transformAsPoint(view.worldToLocal());
  const oledValueCenter = () => {
    const v = oled.value();
    return toView(new Vector2(v.width() / 2, 0).transformAsPoint(v.localToWorld()));
  };

  // OLED + USB cable (cable/plug live in the OLED's local space)
  view.add(
    <Node ref={oledFloat}>
      {oled.node()}
    </Node>,
  );
  oled.root().add(
    <>
      <Line
        ref={cable}
        stroke={'#2a3550'}
        lineWidth={18}
        lineCap={'round'}
        radius={80}
        points={() => {
          const p = plug().position();
          return [p.add([40, 0]), p.add([240, 0]), p.add([330, 140]), p.add([900, 160])];
        }}
      />
      <Node ref={plug} position={plugBase}>
        <Rect x={-46} width={36} height={34} radius={4} fill={C.metal} />
        <Rect width={80} height={60} radius={12} fill={'#3a4766'} stroke={'#56658a'} lineWidth={3} />
        <Txt x={22} y={-60} text={'USB 5V'} fontFamily={FONT.ui} fontWeight={700} fontSize={28} fill={C.dim} />
      </Node>
    </>,
  );
  // board is drawn above the cable start
  oled.root().children()[0].moveToTop();

  // RAM panel
  const ramVars = ['best = 214', 'reaction = 187', 'round = 3'];
  view.add(
    <Rect
      ref={ram}
      x={-600}
      y={-30}
      width={460}
      height={430}
      radius={26}
      fill={C.panel}
      stroke={C.line}
      lineWidth={3}
    >
      <Rect x={-150} y={-168} padding={[6, 18]} radius={10} fill={'rgba(45,212,191,0.15)'} layout>
        <Txt text={'RAM'} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={C.teal} />
      </Rect>
      <Txt x={60} y={-168} text={'variables'} fontFamily={FONT.ui} fontSize={30} fill={C.dim} />
      {ramVars.map((v, i) => (
        <Rect
          ref={ramCards[i]}
          y={-64 + i * 100}
          width={380}
          height={78}
          radius={14}
          fill={'#1d2b47'}
          stroke={i === 0 ? C.amber : C.line}
          lineWidth={i === 0 ? 4 : 2}
        >
          <Txt
            text={v}
            fontFamily={FONT.code}
            fontSize={38}
            fill={i === 0 ? C.amber : C.text}
          />
        </Rect>
      ))}
      <Txt
        ref={ramEmpty}
        y={40}
        text={'(empty)'}
        fontFamily={FONT.ui}
        fontStyle={'italic'}
        fontSize={40}
        fill={C.dim}
        opacity={0}
      />
    </Rect>,
  );

  // Preferences cabinet (drawer slides out to the right, behind the body)
  view.add(
    <Node ref={cabinet} x={-1300} y={-130} opacity={0}>
      <Node ref={drawer} x={0}>
        <Rect width={380} height={150} fill={'#0f1a2e'} stroke={C.teal} lineWidth={4} radius={[0, 0, 12, 12]} />
        <Rect x={190} width={30} height={190} radius={8} fill={C.teal} />
        <Rect x={218} width={26} height={70} radius={8} fill={'#1aa391'} />
        <ValueCard refNode={trayCard} x={50} y={-30} opacity={0} />
      </Node>
      <Rect
        width={430}
        height={330}
        radius={28}
        fill={'#132036'}
        stroke={C.teal}
        lineWidth={4}
        shadowColor={'rgba(0,0,0,0.5)'}
        shadowBlur={40}
        shadowOffsetY={12}
      >
        {/* little flash chip icon */}
        <Rect y={-84} width={84} height={64} radius={8} fill={'#0b1220'} stroke={C.teal} lineWidth={3}>
          {[-27, -9, 9, 27].map(x => (
            <>
              <Rect x={x} y={-42} width={8} height={14} fill={C.teal} />
              <Rect x={x} y={42} width={8} height={14} fill={C.teal} />
            </>
          ))}
          <Txt text={'FLASH'} fontFamily={FONT.code} fontWeight={700} fontSize={18} fill={C.teal} />
        </Rect>
        <Txt y={20} text={'Preferences'} fontFamily={FONT.ui} fontWeight={800} fontSize={52} fill={C.text} />
        <Txt y={80} text={'(flash memory)'} fontFamily={FONT.ui} fontSize={32} fill={C.teal} />
        {/* slot on the right edge */}
        <Rect x={213} width={8} height={160} radius={4} fill={'#07101e'} />
      </Rect>
      <Rect
        ref={savedPill}
        y={210}
        layout
        padding={[8, 22]}
        radius={30}
        fill={'rgba(45,212,191,0.18)'}
        stroke={C.teal}
        lineWidth={2}
        opacity={0}
        scale={0.6}
      >
        <Txt text={'saved ✓'} fontFamily={FONT.ui} fontWeight={700} fontSize={32} fill={C.teal} />
      </Rect>
    </Node>,
  );

  // Code panel
  view.add(
    <Rect
      ref={codePanel}
      y={300}
      layout
      direction="row"
      alignItems="center"
      gap={30}
      padding={[26, 40]}
      radius={22}
      fill={'rgba(13,22,40,0.94)'}
      stroke={C.line}
      lineWidth={3}
      opacity={0}
    >
      <Rect ref={codeChip} padding={[8, 18]} radius={10} fill={C.amber}>
        <Txt ref={codeChipTxt} text={'SAVE'} fontFamily={FONT.ui} fontWeight={800} fontSize={30} fill={C.bg} />
      </Rect>
      <Code
        ref={code}
        highlighter={arduino}
        fontFamily={FONT.code}
        fontSize={48}
        code={''}
      />
    </Rect>,
  );

  // flying card + burst + check (top layer)
  view.add(<ValueCard refNode={flyCard} opacity={0} />);
  view.add(<Node ref={burst} />);
  view.add(
    <Rect
      ref={check}
      layout
      padding={[8, 22]}
      radius={30}
      fill={'rgba(45,212,191,0.18)'}
      stroke={C.teal}
      lineWidth={2}
      opacity={0}
      scale={0.5}
    >
      <Txt text={'same record ✓'} fontFamily={FONT.ui} fontWeight={700} fontSize={34} fill={C.teal} />
    </Rect>,
  );

  const h1 = new Headline('Unplug it → *RAM* *forgets*');
  const h2 = new Headline('So file it in *flash* first', {accent: C.teal});
  const h3 = new Headline('Power on → still *214*');
  view.add(h1.node());
  view.add(h2.node());
  view.add(h3.node());

  // helper: fly the card along an arc between two absolute points
  function* flyArc(from: Vector2, to: Vector2, lift: number, dur: number) {
    yield* tween(dur, v => {
      const t = easeInOutCubic(v);
      const p = Vector2.lerp(from, to, t);
      flyCard().position(p.add([0, -Math.sin(Math.PI * t) * lift]));
      flyCard().rotation(Math.sin(Math.PI * t) * -8);
    });
  }

  // ---------------------------------------------------------------- BEAT 1
  oled.root().scale(0.85).opacity(0);
  ram().scale(0.9).opacity(0).x(-680);
  yield* all(
    oled.root().scale(0.95, 0.4, easeOutBack),
    oled.root().opacity(1, 0.3),
    ram().scale(1, 0.4, easeOutBack),
    ram().opacity(1, 0.3),
    ram().x(-600, 0.4, easeOutCubic),
    delay(0.15, h1.in()),
  );
  yield* waitFor(0.25);

  // yank the plug
  yield* plug().position(plugBase.add([260, 30]), 0.4, easeInBack);
  yield* all(
    oled.powerOff(),
    plug().opacity(0, 0.3),
    cable().opacity(0, 0.3),
    oled.board().stroke('#1b2f63', 0.3),
    sequence(
      0.09,
      ...ramCards.map((card, i) =>
        all(
          card().position.y(card().position.y() + 520, 0.7, easeInCubic),
          card().rotation(i % 2 ? 22 : -18, 0.7, easeInCubic),
          card().opacity(0, 0.7, easeInCubic),
        ),
      ),
    ),
    delay(0.55, ramEmpty().opacity(1, 0.3)),
  );
  yield* h1.pulse();
  yield* waitFor(0.15);

  // ---------------------------------------------------------------- BEAT 2  (~3.0 s)
  yield* all(
    h1.out(),
    ram().opacity(0, 0.2),
    ram().scale(0.9, 0.2),
    oled.root().position([520, -150], 0.6, easeInOutCubic),
    oled.root().scale(0.62, 0.6, easeInOutCubic),
    delay(0.15, cabinet().x(-560, 0.55, easeOutCubic)),
    delay(0.15, cabinet().opacity(1, 0.35)),
    delay(0.42, h2.in()),
    delay(0.3, codePanel().opacity(1, 0.3)),
    delay(0.3, codePanel().y(290, 0.4, easeOutCubic)),
  );
  // code line 1 types in while the drawer opens and a ghost of 214 lifts off the dark OLED
  const start = oledValueCenter();
  flyCard().position(start).scale(0.4);
  yield* all(
    code().code('prefs.putULong("best", best);', 0.55),
    drawer().x(320, 0.45, easeOutCubic),
    flyCard().opacity(1, 0.25),
    flyCard().scale(1, 0.35, easeOutBack),
  );
  const trayTarget = toView(trayCard().absolutePosition());
  yield* all(
    flyArc(flyCard().position(), trayTarget, 200, 0.65),
    code().selection(code().findFirstRange('putULong'), 0.3),
  );
  trayCard().opacity(1);
  flyCard().opacity(0);
  yield* all(
    trayCard().scale([1.08, 0.92], 0.1).to(1, 0.15),
    code().selection(code().findFirstRange(lit('"best", best')), 0.3),
  );
  yield* all(
    drawer().x(0, 0.4, easeInOutCubic),
    delay(0.25, all(savedPill().opacity(1, 0.2), savedPill().scale(1, 0.3, easeOutBack))),
  );

  // morph to the load line (~5.5 s)
  yield* all(
    code().selection(DEFAULT, 0.2),
    codeChip().fill(C.teal, 0.3),
    codeChipTxt().text('LOAD', 0.3),
    delay(0.3, savedPill().opacity(0, 0.3)),
    code().code('best = prefs.getULong("best", 9999);', 0.6),
  );
  yield* code().selection(code().findFirstRange('getULong'), 0.3);
  yield* waitFor(0.2);

  // "9999 = nothing saved yet" note above the token
  const range9999 = code().findFirstRange('9999');
  const box = code().getSelectionBBox(range9999)[0];
  const anchor = toView(box.center.transformAsPoint(code().localToWorld()));
  view.add(
    <Node ref={note} position={anchor.add([0, -150])} opacity={0}>
      <Line
        points={[
          [0, 40],
          [0, 104],
        ]}
        stroke={C.teal}
        lineWidth={4}
        endArrow
        arrowSize={14}
      />
      <Rect layout padding={[10, 22]} radius={14} fill={'#0f2a2c'} stroke={C.teal} lineWidth={3}>
        <Txt text={'9999 = nothing saved yet'} fontFamily={FONT.ui} fontWeight={700} fontSize={34} fill={C.teal} />
      </Rect>
    </Node>,
  );
  yield* all(
    code().selection(range9999, 0.3),
    note().opacity(1, 0.25),
    note().position.y(note().position.y() + 20, 0.35, easeOutCubic),
  );
  yield* waitFor(0.9);

  // ---------------------------------------------------------------- BEAT 3  (~8 s)
  yield* all(
    h2.out(),
    note().opacity(0, 0.25),
    code().selection(code().findFirstRange(lit('prefs.getULong("best", 9999)')), 0.3),
    delay(0.42, h3.in()),
    oled.root().position([430, -130], 0.5, easeInOutCubic),
    oled.root().scale(0.7, 0.5, easeInOutCubic),
  );
  // plug back in, screen boots with no value yet
  plug().position(plugBase.add([260, 30]));
  oled.value().text('---');
  yield* all(
    plug().opacity(1, 0.15),
    cable().opacity(1, 0.15),
    plug().position(plugBase, 0.35, easeOutBack),
  );
  yield* all(oled.powerOn(), oled.board().stroke('#2b56b8', 0.3));

  // drawer opens, 214 flies out onto the OLED
  yield* drawer().x(320, 0.35, easeOutCubic);
  flyCard().position(toView(trayCard().absolutePosition())).rotation(0).scale(1).opacity(1);
  trayCard().opacity(0);
  const target = oledValueCenter();
  yield* all(
    flyArc(flyCard().position(), target, 220, 0.7),
    delay(0.45, flyCard().scale(0.55, 0.25, easeInCubic)),
    delay(0.3, drawer().x(0, 0.4, easeInOutCubic)),
  );
  flyCard().opacity(0);
  oled.value().text('214');

  // pop!
  check().position([430, 80]);
  const center = target;
  const colors = [C.amber, C.teal, C.text];
  const parts = Array.from({length: 16}, (_, i) => {
    const ref = createRef<Circle>();
    burst().add(
      <Circle
        ref={ref}
        position={center}
        size={i % 3 === 0 ? 18 : 12}
        fill={colors[i % 3]}
      />,
    );
    return {ref, angle: (i / 16) * Math.PI * 2 + (i % 2) * 0.2, dist: 190 + (i % 4) * 40};
  });
  const ring = createRef<Circle>();
  burst().add(<Circle ref={ring} position={center} size={40} stroke={C.amber} lineWidth={8} />);
  yield* all(
    oled.value().scale(1.3, 0.12, easeOutCubic).to(1, 0.35, easeOutBack),
    ring().size(460, 0.6, easeOutCubic),
    ring().opacity(0, 0.6, easeInCubic),
    ...parts.map(p =>
      all(
        p.ref().position(center.add(Vector2.fromRadians(p.angle).scale(p.dist)), 0.65, easeOutCubic),
        p.ref().opacity(0, 0.65, easeInCubic),
      ),
    ),
    delay(0.15, chain(
      all(check().opacity(1, 0.2), check().scale(1, 0.35, easeOutBack)),
    )),
    delay(0.1, h3.pulse()),
  );

  // hold with gentle life: float + glow pulse
  const glow = createSignal(0);
  oled.value().shadowBlur(() => 18 + glow() * 16);
  yield loop(Infinity, () => glow(1, 0.6).to(0, 0.6));
  yield* all(
    oledFloat().position.y(-10, 0.9, easeInOutCubic).to(0, 0.9, easeInOutCubic),
    grid().opacity(0.6, 1.2, linear),
  );

  // out
  yield* all(
    h3.out(),
    codePanel().opacity(0, 0.4),
    check().opacity(0, 0.3),
    cabinet().opacity(0, 0.4),
    oled.root().opacity(0, 0.5),
  );
});
