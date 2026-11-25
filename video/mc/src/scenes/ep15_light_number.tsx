/**
 * Ep15 s07 - "In a closed drawer it's dark, so the light number is low.
 * Open it, and the number jumps."
 * Cut-away desk: the sensor sits in the drawer; closed = in the dark, the
 * meter on the right shows ~180. The drawer slides out into the room light,
 * the number jumps to ~2900.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, createSignal, easeInOutCubic, easeOutBack, easeOutCubic, linear, useTime, Vector2} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {burst, exact, Pill, popIn, until} from '../lib/ep10';
import {timing15} from '../lib/ep15';
import {C, FONT} from '../style';

const T = timing15('light_number');

// desk cut-away (left half)
const DESK_L = -520;
const DESK_R = -60;
const IN_T = -40; // interior top
const IN_B = 150; // interior bottom
const DRAWER_W = 400;
const DRAWER_H = 150;
const OPEN_DX = -330;

// meter (right half)
const MX = 330;
const MT = -290;
const MB = 300;
const my = (v: number) => MB - ((MB - MT) * v) / 4095;

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const slide = createSignal(0); // 0 closed .. 1 open
  const light = createSignal(180);
  const drawer = createRef<Node>();
  const dark = createRef<Rect>();
  const cone = createRef<Line>();
  const sensorGlow = createRef<Circle>();
  const numTxt = createRef<Txt>();
  const darkPill = createRef<Rect>();
  const lowPill = createRef<Rect>();
  const jumpPill = createRef<Rect>();
  const scene = createRef<Node>();

  const front = () => DESK_L + 10 + OPEN_DX * slide();
  const sensorX = () => front() + 95;
  const lit = () => Math.max(0, Math.min(1, (DESK_L - 20 - sensorX()) / 120));

  view.add(
    <Node ref={scene} opacity={0}>
      {/* room light: a hanging lamp and its cone */}
      <Line points={[[-700, -480], [-700, -330]]} stroke={C.dim} lineWidth={4} />
      <Rect x={-700} y={-305} width={120} height={50} radius={[60, 60, 6, 6]} fill={'#3a4660'} />
      <Circle x={-700} y={-278} size={34} fill={'#fff3c4'} shadowColor={'#ffd36b'} shadowBlur={40} />
      <Line
        ref={cone}
        points={[[-712, -270], [-688, -270], [-520, IN_T + DRAWER_H], [-880, IN_T + DRAWER_H]]}
        closed
        fill={'rgba(255,230,150,0.13)'}
      />
      {/* desk interior (dark) */}
      <Rect x={(DESK_L + DESK_R) / 2} y={(IN_T + IN_B) / 2} width={DESK_R - DESK_L} height={IN_B - IN_T} fill={'#070b14'} />
      {/* the drawer (open box + front panel + knob) with the sensor inside */}
      <Node ref={drawer} x={() => OPEN_DX * slide()}>
        <Rect x={DESK_L + 10 + DRAWER_W / 2} y={IN_T + 8 + DRAWER_H / 2} width={DRAWER_W} height={DRAWER_H} fill={'#5c3b20'} />
        <Rect x={DESK_L + 10 + DRAWER_W / 2} y={IN_T + 8 + DRAWER_H / 2 + 6} width={DRAWER_W - 36} height={DRAWER_H - 30} fill={'#3d2714'} />
        <Rect x={DESK_L + 2} y={IN_T + 8 + DRAWER_H / 2} width={30} height={DRAWER_H + 30} radius={6} fill={'#a8743f'} stroke={'#7a5129'} lineWidth={3} />
        <Circle x={DESK_L - 26} y={IN_T + 8 + DRAWER_H / 2} size={30} fill={'#c9d1dc'} stroke={'#8a97ab'} lineWidth={3} />
        {/* LDR module, facing up */}
        <Rect x={DESK_L + 105} y={IN_T + DRAWER_H - 22} width={90} height={26} radius={4} fill={'#1d5fb8'} stroke={'#0f3d7a'} lineWidth={2} />
        <Circle ref={sensorGlow} x={DESK_L + 105} y={IN_T + DRAWER_H - 40} size={70} fill={'#fff1b0'} opacity={() => lit() * 0.55} shadowColor={'#ffd36b'} shadowBlur={30} />
        <Circle x={DESK_L + 105} y={IN_T + DRAWER_H - 40} size={30} fill={'#e9c46a'} stroke={'#8f6d2a'} lineWidth={3} />
        <Line points={[[DESK_L + 100 + 50, IN_T + DRAWER_H - 22], [DESK_L + 330, IN_T + DRAWER_H - 22], [DESK_L + 380, IN_T + DRAWER_H + 30]]} stroke={'#ff5d6c'} lineWidth={4} />
      </Node>
      {/* darkness inside the desk */}
      <Rect ref={dark} x={(DESK_L + DESK_R) / 2} y={(IN_T + IN_B) / 2} width={DESK_R - DESK_L} height={IN_B - IN_T} fill={'rgba(0,0,0,0.58)'} />
      {/* desk frame drawn on top */}
      <Rect x={(DESK_L + DESK_R) / 2 - 10} y={IN_T - 22} width={DESK_R - DESK_L + 80} height={44} radius={8} fill={'#a8743f'} stroke={'#7a5129'} lineWidth={3} />
      <Rect x={DESK_R + 8} y={(IN_T + IN_B) / 2 + 60} width={36} height={IN_B - IN_T + 120} radius={4} fill={'#8d5f32'} />
      <Rect x={(DESK_L + DESK_R) / 2} y={IN_B + 12} width={DESK_R - DESK_L} height={24} fill={'#8d5f32'} />
      <Rect x={DESK_L - 6} y={IN_B + 70} width={30} height={140} fill={'#8d5f32'} />
      {/* meter */}
      <Rect x={MX} y={(MT + MB) / 2} width={90} height={MB - MT} radius={16} fill={'#101a2c'} stroke={C.line} lineWidth={4} />
      <Rect
        x={MX}
        y={() => MB - 6}
        offsetY={1}
        width={66}
        height={() => Math.max(10, MB - my(light()) - 6)}
        radius={10}
        fill={() => (light() > 1000 ? C.amber : C.teal)}
      />
      {[0, 1000, 2000, 3000, 4095].flatMap(v => [
        <Line points={[[MX - 60, my(v)], [MX - 46, my(v)]]} stroke={C.dim} lineWidth={3} />,
        <Txt x={MX - 70} y={my(v)} offsetX={1} text={String(v)} fontFamily={FONT.code} fontSize={26} fill={C.dim} />,
      ])}
      <Rect x={660} y={0} width={420} height={260} radius={24} fill={'rgba(13,22,40,0.95)'} stroke={C.line} lineWidth={3}>
        <Txt y={-80} text={'light number'} fontFamily={FONT.ui} fontWeight={700} fontSize={34} fill={C.dim} />
        <Txt
          ref={numTxt}
          y={25}
          text={() => String(Math.round(light()))}
          fontFamily={FONT.code}
          fontWeight={800}
          fontSize={130}
          fill={() => (light() > 1000 ? C.amber : C.text)}
        />
      </Rect>
    </Node>,
  );
  view.add(<Pill refNode={darkPill} text={'☾ dark'} color={C.dim} x={-290} y={270} size={36} />);
  view.add(<Pill refNode={lowPill} text={'low'} color={C.teal} x={660} y={200} size={36} />);
  view.add(<Pill refNode={jumpPill} text={'jumps!'} color={C.amber} x={660} y={200} size={36} />);

  const h1 = new Headline('The *light* *number*', {accent: C.amber});
  view.add(h1.node());

  // the closed drawer reads ~180, wobbling a little
  let wobble = true;
  yield (function* () {
    const seq = [176, 188, 181, 172, 185, 179];
    for (let k = 0; wobble; k++) yield* light(seq[k % seq.length], 0.25);
  })();

  yield* all(h1.in(), scene().opacity(1, 0.4));

  // it's dark
  yield* until(Math.max(useTime(), T.word('dark', 1.38) - 0.2));
  yield* all(popIn(darkPill(), 0.3), dark().fill('rgba(0,0,0,0.7)', 0.3));
  // ... so the light number is low
  yield* until(Math.max(useTime(), T.word('low', 3.24) - 0.25));
  yield* all(popIn(lowPill(), 0.3), numTxt().scale(1.12, 0.12).to(1, 0.25, easeOutBack));

  // open it ...
  yield* until(Math.max(useTime(), T.word('open', 4.1) - 0.15));
  yield lowPill().opacity(0, 0.2);
  yield darkPill().opacity(0, 0.25);
  yield* slide(1, 0.85, easeInOutCubic);
  // ... and the number jumps
  wobble = false;
  yield* until(Math.max(useTime(), T.word('jumps', 5.72) - 0.45));
  yield* light(2900, 0.4, easeOutCubic);
  yield burst(view, new Vector2(660, 25), [C.amber, '#fff3c4', C.text], 220);
  yield* all(popIn(jumpPill(), 0.3), numTxt().scale(1.15, 0.12).to(1, 0.25, easeOutBack));
  yield (function* () {
    const seq = [2880, 2925, 2895, 2910];
    for (let k = 0; ; k++) yield* light(seq[k % seq.length], 0.25);
  })();
  yield grid().opacity(0.6, 1.0, linear);
  yield* until(T.total);
}));
