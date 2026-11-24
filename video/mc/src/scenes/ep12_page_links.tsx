/**
 * Ep12 s10 - "Here, the numbers are short links: slash color for the light,
 * slash ring for the buzzer."  The menu numbers on the phone buttons turn
 * into link chips; /color goes to the RGB LED, /ring to the buzzer.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, delay, easeOutBack, easeOutCubic, linear, loop, sequence, useTime, Vector2} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {exact, until} from '../lib/ep10';
import {BUTTONS, Led, LED_OFF, ledSignal, Phone, timing12} from '../lib/ep12';
import {C, FONT} from '../style';

const T = timing12('page_links');

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const phone = new Phone({x: 600, y: 40, scale: 0.9});
  const chips = BUTTONS.map(() => createRef<Rect>());
  const wires = BUTTONS.map(() => createRef<Line>());
  const led = createRef<Node>();
  const ledColor = ledSignal();
  const buzzer = createRef<Node>();
  const waves = [createRef<Circle>(), createRef<Circle>(), createRef<Circle>()];
  const colorTag = createRef<Rect>();
  const ringTag = createRef<Rect>();

  const LED_P = new Vector2(-560, -60);
  const BUZ_P = new Vector2(-560, 250);
  const chipX = 300;

  view.add(<Led refNode={led} color={ledColor} x={LED_P.x} y={LED_P.y} scale={0.9} />);
  view.add(
    <Node ref={buzzer} x={BUZ_P.x} y={BUZ_P.y} opacity={0}>
      <Circle size={130} fill={'#14161c'} stroke={'#3a3f4c'} lineWidth={6} />
      <Circle size={22} fill={'#05060a'} />
      {waves.map(w => (
        <Circle ref={w} size={140} stroke={C.amber} lineWidth={7} startAngle={-40} endAngle={40} opacity={0} />
      ))}
    </Node>,
  );
  view.add(
    <Rect ref={colorTag} x={LED_P.x} y={LED_P.y - 150} layout padding={[6, 18]} radius={12} fill={'#101a2c'} stroke={C.teal} lineWidth={3} opacity={0}>
      <Txt text={'/color  → light'} fontFamily={FONT.code} fontWeight={800} fontSize={36} fill={C.teal} />
    </Rect>,
  );
  view.add(
    <Rect ref={ringTag} x={BUZ_P.x} y={BUZ_P.y - 115} layout padding={[6, 18]} radius={12} fill={'#101a2c'} stroke={C.amber} lineWidth={3} opacity={0}>
      <Txt text={'/ring  → buzzer'} fontFamily={FONT.code} fontWeight={800} fontSize={36} fill={C.amber} />
    </Rect>,
  );
  view.add(phone.node());
  // wires from each link chip to its target
  BUTTONS.forEach((b, i) => {
    const y = 40 + 0.9 * Phone.BTN_Y(i);
    const to = i < 4 ? LED_P.add([110, 0]) : BUZ_P.add([90, 0]);
    view.add(
      <Line
        ref={wires[i]}
        points={[[chipX - 72, y], [chipX - 200, y], to]}
        radius={40}
        stroke={i < 4 ? C.teal : C.amber}
        lineWidth={4}
        lineDash={[12, 10]}
        end={0}
      />,
    );
    view.add(
      <Rect
        ref={chips[i]}
        x={chipX + 80}
        y={y}
        layout
        padding={[4, 14]}
        radius={10}
        fill={'#101a2c'}
        stroke={b.color === '#334155' ? C.dim : b.color}
        lineWidth={3}
        opacity={0}
        scale={0.5}
      >
        <Txt text={i < 4 ? '/color' : '/ring'} fontFamily={FONT.code} fontWeight={800} fontSize={30} fill={C.text} />
      </Rect>,
    );
  });
  // from the previous scene: the menu numbers are on the buttons
  phone.tags.forEach(t => t().opacity(1).scale(1));

  const h1 = new Headline('The numbers are *links*', {accent: C.teal});
  view.add(h1.node());

  // ------------------------------------------------------------ beats
  led().opacity(0);
  yield* delay(0.05, h1.in());
  // numbers -> links: tags leave the buttons and become chips
  yield* until(Math.max(useTime(), T.word('links', 1.8) - 0.3));
  yield* all(
    h1.pulse(),
    ...phone.tags.map(t => t().opacity(0, 0.25)),
    sequence(0.08, ...chips.map(c => all(c().opacity(1, 0.2), c().scale(1, 0.35, easeOutBack), c().x(chipX, 0.35, easeOutCubic)))),
  );

  // /color for the light
  yield* until(Math.max(useTime(), T.word('color', 3.1) - 0.2));
  yield* all(
    led().opacity(1, 0.3),
    colorTag().opacity(1, 0.3),
    ...[0, 1, 2, 3].map(i => wires[i]().end(1, 0.5, easeOutCubic)),
    ...[0, 1, 2, 3].map(i => chips[i]().scale(1.12, 0.12).to(1, 0.25)),
  );
  yield loop(Infinity, function* () {
    for (const c of ['#e5484d', '#2fbf71', '#3b82f6', LED_OFF]) {
      ledColor(c);
      yield* led().scale(0.96, 0.08).to(0.9, 0.3);
    }
  });

  // /ring for the buzzer
  yield* until(Math.max(useTime(), T.word('ring', 5.3) - 0.2));
  yield* all(
    buzzer().opacity(1, 0.3),
    ringTag().opacity(1, 0.3),
    wires[4]().end(1, 0.5, easeOutCubic),
    chips[4]().scale(1.15, 0.12).to(1, 0.25),
  );
  yield loop(Infinity, () =>
    sequence(0.1, ...waves.map(w => all(w().size(140, 0).to(300, 0.5, easeOutCubic), w().opacity(1, 0.05).to(0, 0.45)))),
  );
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
