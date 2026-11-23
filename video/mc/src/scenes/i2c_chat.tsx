/**
 * Ep10 s08+s09 - I2C as a group chat.
 * s08: data wire carries bits one by one, the clock wire is the beat; both
 *      ends read each bit on the same beat ("Hi!" arrives on the OLED).
 * s09: several devices share the two wires, each with an address tag; the
 *      screen answers to 0x3C; a new part can join the same wires.
 */
import {Circle, Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  createSignal,
  delay,
  easeInCubic,
  easeInOutCubic,
  easeOutBack,
  easeOutCubic,
  linear,
  loop,
  sequence,
  useTime as useNow,
  Vector2,
  waitFor,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Oled} from '../lib/oled';
import {burst, Esp32Board, Pill, popIn, timing, until, exact} from '../lib/ep10';
import {C, FONT} from '../style';

const SDA_C = '#5b9bff'; // blue wire (data) - same colours as the real wiring
const SCL_C = '#3ddc84'; // green wire (clock)

const T = timing('i2c_chat');

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const S9 = T.seg('s09').start;

  // ------------------------------------------------------------ s08 layout
  const esp = createRef<Node>();
  const espLed = createRef<Circle>();
  const oled = new Oled({x: 690, y: -20, scale: 0.5, label: '', value: '', unit: ''});
  const wires = createRef<Node>();
  const sda = createRef<Line>();
  const scl = createRef<Line>();
  const dataLbl = createRef<Rect>();
  const clockLbl = createRef<Rect>();
  const bubble = createRef<Rect>();
  const bitsHost = createRef<Node>();
  const wave = createRef<Line>();
  const readLine = createRef<Node>();
  const readFlash = createRef<Rect>();
  const reg = createRef<Txt>();
  const beatDots = [createRef<Circle>(), createRef<Circle>()];

  const X0 = -500;
  const X1 = 500;
  const YD = -90; // data wire
  const YC = 60; // clock wire
  const SLOT = 116;
  const READ_X = 440;

  const message = 'Hi!';
  const bits: number[] = [];
  for (const ch of message) {
    const b = ch.charCodeAt(0).toString(2).padStart(8, '0');
    for (const c of b) bits.push(+c);
  }
  // phase p: bit k sits at x = READ_X - (k - p) * SLOT ; bit k is read when p reaches k
  const phase = createSignal(-0.6);

  view.add(<Esp32Board refNode={esp} x={-700} y={-15} scale={0.6} led={espLed} />);
  view.add(oled.node());
  view.add(
    <Node ref={wires}>
      <Line ref={sda} points={[[X0, YD], [X1, YD]]} stroke={SDA_C} lineWidth={12} lineCap={'round'} end={0} />
      <Line ref={scl} points={[[X0, YC], [X1, YC]]} stroke={SCL_C} lineWidth={12} lineCap={'round'} end={0} />
      {/* clock square wave riding on the green wire */}
      <Rect x={0} y={YC - 26} width={X1 - X0} height={90} clip>
        <Line
          ref={wave}
          opacity={0}
          stroke={'#9ff5c6'}
          lineWidth={6}
          lineJoin={'round'}
          points={() => {
            const pts: [number, number][] = [];
            const shift = (phase() % 1) * SLOT;
            for (let n = -2; n < 12; n++) {
              const x = -560 + n * SLOT + shift;
              pts.push([x, 20], [x, -20], [x + SLOT / 2, -20], [x + SLOT / 2, 20]);
            }
            return pts;
          }}
        />
      </Rect>
      {/* data bits riding on the blue wire */}
      <Rect x={0} y={YD} width={X1 - X0 + 40} height={90} clip>
        <Node ref={bitsHost} opacity={0} />
      </Rect>
      {/* read marker: both sides sample here on the beat */}
      <Node ref={readLine} x={READ_X} opacity={0}>
        <Line points={[[0, YD - 70], [0, YC + 50]]} stroke={C.dim} lineWidth={3} lineDash={[10, 10]} />
        <Rect ref={readFlash} y={(YD + YC) / 2} width={70} height={YC - YD + 120} radius={14} fill={'rgba(255,181,71,0.0)'} />
      </Node>
      {beatDots.map((d, i) => (
        <Circle ref={d} x={i === 0 ? X0 - 6 : X1 + 6} y={YC} size={30} fill={SCL_C} opacity={0} />
      ))}
    </Node>,
  );
  bits.forEach((b, k) => {
    bitsHost().add(
      <Rect
        x={() => READ_X - (k - phase()) * SLOT}
        opacity={() => {
          const x = READ_X - (k - phase()) * SLOT;
          // fade in at the sender end, fade out after the read line
          const a = Math.min(1, Math.max(0, (x - X0 + 30) / 80));
          const b2 = Math.min(1, Math.max(0, (X1 + 30 - x) / 50));
          return Math.min(a, b2);
        }}
        width={64}
        height={64}
        radius={12}
        fill={b ? SDA_C : '#1a2a48'}
        stroke={SDA_C}
        lineWidth={4}
      >
        <Txt text={String(b)} fontFamily={FONT.code} fontWeight={800} fontSize={40} fill={b ? C.bg : C.text} />
      </Rect>,
    );
  });

  view.add(
    <Rect ref={dataLbl} x={X0} y={YD - 78} offsetX={-1} layout gap={14} alignItems="center" opacity={0}>
      <Txt text={'DATA'} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={SDA_C} />
      <Txt text={'the message, bit by bit'} fontFamily={FONT.ui} fontSize={32} fill={C.text} />
    </Rect>,
  );
  view.add(
    <Rect ref={clockLbl} x={X0} y={YC + 78} offsetX={-1} layout gap={14} alignItems="center" opacity={0}>
      <Txt text={'CLOCK'} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={SCL_C} />
      <Txt text={'the beat'} fontFamily={FONT.ui} fontSize={32} fill={C.text} />
    </Rect>,
  );
  view.add(
    <Txt ref={reg} x={690} y={-160} text={''} fontFamily={FONT.code} fontWeight={700} fontSize={40} letterSpacing={2} fill={SDA_C} />,
  );
  view.add(
    <Rect
      ref={bubble}
      x={-700}
      y={-200}
      layout
      padding={[14, 30]}
      radius={30}
      fill={C.text}
      opacity={0}
      scale={0.4}
    >
      <Txt text={'Hi!'} fontFamily={FONT.ui} fontWeight={800} fontSize={48} fill={C.bg} />
    </Rect>,
  );

  const h1 = new Headline('Two wires = a *group* *chat*');
  const h2 = new Headline('Every device has an *address*', {accent: C.teal});
  view.add(h1.node());
  view.add(h2.node());

  // ------------------------------------------------------------ s08 beats
  esp().scale(0.45).opacity(0);
  oled.root().scale(0.3).opacity(0);
  yield* all(
    esp().scale(0.6, 0.4, easeOutBack),
    esp().opacity(1, 0.25),
    oled.root().scale(0.5, 0.4, easeOutBack),
    oled.root().opacity(1, 0.25),
    delay(0.1, h1.in()),
    delay(0.2, sda().end(1, 0.5, easeInOutCubic)),
    delay(0.3, scl().end(1, 0.5, easeInOutCubic)),
  );
  // chat bubble from the ESP32 drops onto the data wire as bits
  yield* popIn(bubble(), 0.3);
  yield* until(Math.max(1.4, T.word('group', 1.2) + 0.5));
  yield* h1.pulse();
  yield* all(
    bubble().position([-560, YD], 0.35, easeInCubic),
    bubble().scale(0.2, 0.35, easeInCubic),
    bubble().opacity(0, 0.35, easeInCubic),
    phase(0.4, 0.5, easeOutCubic),
    bitsHost().opacity(1, 0.35),
    delay(0.2, popIn(dataLbl(), 0.3)),
  );
  yield all(wave().opacity(0.35, 0.3), readLine().opacity(1, 0.3));

  const tStart = Math.max(T.word('carries', 2.6), 2.6);
  yield* until(tStart);
  const beatAt = Math.min(T.word('beat', tStart + 3), S9 - 2);
  const stepDur = Math.max(0.3, Math.min(0.5, (S9 - 0.7 - tStart) / bits.length));
  let clockShown = false;
  for (let k = 0; k < bits.length; k++) {
    if (!clockShown && T.word('other', beatAt - 1) - 0.2 <= tStart + k * stepDur) {
      clockShown = true;
      yield all(wave().opacity(1, 0.3), popIn(clockLbl(), 0.3), ...beatDots.map(d => d().opacity(1, 0.3)));
    }
    // move one slot (the beat), then both ends read the bit under the marker
    yield* phase(k + 1, stepDur * 0.45, easeInOutCubic);
    const bit = bits[k];
    const chars = Math.floor((k + 1) / 8);
    reg().text(reg().text().length >= 8 ? String(bit) : reg().text() + bit);
    if ((k + 1) % 8 === 0) oled.value().text(message.slice(0, chars));
    yield all(
      readFlash().fill('rgba(255,181,71,0.28)', 0.05).to('rgba(255,181,71,0)', stepDur * 0.5),
      ...beatDots.map(d => d().scale(1.6, 0.06).to(1, stepDur * 0.4)),
      (k + 1) % 8 === 0 ? oled.value().scale(1.25, 0.08).to(1, 0.25) : waitFor(0),
      (k + 1) % 8 === 0 ? reg().fill(C.amber, 0.05).to(SDA_C, 0.3) : waitFor(0),
    );
    if (Math.abs(tStart + k * stepDur - beatAt) < stepDur / 2) {
      yield all(
        clockLbl().scale(1.12, 0.15).to(1, 0.25),
        delay(0.1, dataLbl().scale(1.12, 0.15).to(1, 0.25)),
      );
    }
    yield* until(tStart + (k + 1) * stepDur);
  }
  if (!clockShown) {
    yield all(wave().opacity(1, 0.3), popIn(clockLbl(), 0.3), ...beatDots.map(d => d().opacity(1, 0.3)));
  }

  // ------------------------------------------------------------ s09
  yield* until(S9 - 0.45);
  const BY = -230; // bus: data line, clock line 40 px below
  const BX0 = -650;
  const BX1 = 900;
  const DEV_Y = 110;
  const devX = [-300, 90, 480];
  const ghostX = 790;

  const bus = createRef<Node>();
  const busD = createRef<Line>();
  const busC = createRef<Line>();
  const drops = devX.map(() => createRef<Node>());
  const tags = devX.map(() => createRef<Rect>());
  const tagTxt = devX.map(() => createRef<Txt>());
  const sensor = createRef<Node>();
  const rtc = createRef<Node>();
  const ghost = createRef<Node>();
  const ghostDrop = createRef<Node>();
  const env = createRef<Rect>();
  const notMe = [createRef<Rect>(), createRef<Rect>()];
  const addrs = ['0x76', '0x3C', '0x68'];

  view.add(
    <Node ref={bus}>
      <Line ref={busD} points={[[BX0, BY], [BX1, BY]]} stroke={SDA_C} lineWidth={10} lineCap={'round'} end={0} />
      <Line ref={busC} points={[[BX0, BY + 40], [BX1, BY + 40]]} stroke={SCL_C} lineWidth={10} lineCap={'round'} end={0} />
      {devX.map((x, i) => (
        <Node ref={drops[i]} opacity={0}>
          <Line points={[[x - 14, BY], [x - 14, DEV_Y - 100]]} stroke={SDA_C} lineWidth={7} />
          <Line points={[[x + 14, BY + 40], [x + 14, DEV_Y - 100]]} stroke={SCL_C} lineWidth={7} />
          <Circle x={x - 14} y={BY} size={18} fill={SDA_C} />
          <Circle x={x + 14} y={BY + 40} size={18} fill={SCL_C} />
          <Rect
            ref={tags[i]}
            x={x}
            y={BY + 125}
            layout
            padding={[6, 18]}
            radius={12}
            fill={'#1e2a40'}
            stroke={C.dim}
            lineWidth={3}
          >
            <Txt ref={tagTxt[i]} text={addrs[i]} fontFamily={FONT.code} fontWeight={700} fontSize={36} fill={C.text} />
          </Rect>
        </Node>
      ))}
      <Node ref={ghostDrop} opacity={0}>
        <Line points={[[ghostX - 14, BY], [ghostX - 14, DEV_Y - 80]]} stroke={SDA_C} lineWidth={7} lineDash={[12, 10]} />
        <Line points={[[ghostX + 14, BY + 40], [ghostX + 14, DEV_Y - 80]]} stroke={SCL_C} lineWidth={7} lineDash={[12, 10]} />
      </Node>
    </Node>,
  );
  // backdrop = first 4 children; the bus goes right above it (behind the devices)
  bus().moveTo(4);

  view.add(
    <Node ref={sensor} x={devX[0]} y={DEV_Y} opacity={0} scale={0.6}>
      <Rect width={250} height={170} radius={18} fill={'#5b2a86'} stroke={'#8a4cc4'} lineWidth={4} />
      <Rect y={-10} width={70} height={70} radius={8} fill={'#d9dde4'} />
      <Txt y={56} text={'SENSOR'} fontFamily={FONT.ui} fontWeight={800} fontSize={30} fill={C.text} />
    </Node>,
  );
  view.add(
    <Node ref={rtc} x={devX[2]} y={DEV_Y} opacity={0} scale={0.6}>
      <Rect width={250} height={170} radius={18} fill={'#1f6b4a'} stroke={'#33a072'} lineWidth={4} />
      <Circle y={-12} size={78} fill={'#0b1220'} stroke={C.text} lineWidth={5}>
        <Line points={[[0, 0], [0, -24]]} stroke={C.text} lineWidth={5} lineCap={'round'} />
        <Line points={[[0, 0], [18, 8]]} stroke={C.text} lineWidth={5} lineCap={'round'} />
      </Circle>
      <Txt y={56} text={'CLOCK'} fontFamily={FONT.ui} fontWeight={800} fontSize={30} fill={C.text} />
    </Node>,
  );
  view.add(
    <Node ref={ghost} x={ghostX} y={DEV_Y} opacity={0} scale={0.7}>
      <Rect width={210} height={160} radius={18} stroke={C.dim} lineWidth={4} lineDash={[14, 10]} />
      <Txt y={-14} text={'+'} fontFamily={FONT.ui} fontWeight={800} fontSize={80} fill={C.dim} />
      <Txt y={48} text={'new part'} fontFamily={FONT.ui} fontWeight={700} fontSize={30} fill={C.dim} />
    </Node>,
  );
  view.add(
    <Rect
      ref={env}
      x={BX0 + 40}
      y={BY - 70}
      layout
      gap={12}
      alignItems="center"
      padding={[10, 22]}
      radius={30}
      fill={C.amber}
      opacity={0}
      scale={0.5}
    >
      <Txt text={'@0x3C'} fontFamily={FONT.code} fontWeight={800} fontSize={36} fill={C.bg} />
      <Txt text={'"GO!"'} fontFamily={FONT.code} fontWeight={700} fontSize={34} fill={C.bg} />
    </Rect>,
  );
  view.add(<Pill refNode={notMe[0]} text={'not me'} color={C.dim} x={devX[0]} y={DEV_Y + 125} size={30} />);
  view.add(<Pill refNode={notMe[1]} text={'not me'} color={C.dim} x={devX[2]} y={DEV_Y + 125} size={30} />);

  // morph: old wires out, OLED + ESP32 move into the bus layout
  oled.value().text('');
  reg().text('');
  yield* all(
    h1.out(),
    wires().opacity(0, 0.3),
    dataLbl().opacity(0, 0.25),
    clockLbl().opacity(0, 0.25),
    esp().position([-760, BY + 20], 0.6, easeInOutCubic),
    esp().scale(0.5, 0.6, easeInOutCubic),
    oled.root().position([devX[1], DEV_Y + 4], 0.6, easeInOutCubic),
    oled.root().scale(0.4, 0.6, easeInOutCubic),
    delay(0.3, busD().end(1, 0.55, easeInOutCubic)),
    delay(0.35, busC().end(1, 0.55, easeInOutCubic)),
    delay(0.35, h2.in()),
  );
  yield* all(
    sequence(0.12, ...drops.map(d => d().opacity(1, 0.25))),
    delay(0.05, all(sensor().opacity(1, 0.3), sensor().scale(0.9, 0.4, easeOutBack))),
    delay(0.3, all(rtc().opacity(1, 0.3), rtc().scale(0.9, 0.4, easeOutBack))),
    delay(0.2, sequence(0.15, ...tags.map(t => t().scale(1.2, 0.15).to(1, 0.2)))),
  );
  yield* until(T.word('address', S9 + 2.2, 's09'));
  yield* sequence(0.12, ...tags.map(t => all(t().stroke(C.amber, 0.15).to(C.dim, 0.3), t().scale(1.15, 0.15).to(1, 0.25))));
  yield* h2.pulse();

  // the message travels the bus; only 0x3C answers
  yield* until(Math.max(useNow(), T.word('screen', S9 + 4, 's09') - 0.6));
  yield* popIn(env(), 0.25);
  yield* env().x(devX[0], 0.45, easeInOutCubic);
  yield* all(
    tags[0]().stroke(C.red, 0.1),
    tags[0]().x(tags[0]().x() + 8, 0.05).to(tags[0]().x() - 8, 0.05).to(tags[0]().x(), 0.05),
    popIn(notMe[0](), 0.25),
    sensor().opacity(0.4, 0.3),
    tagTxt[0]().fill(C.dim, 0.3),
  );
  yield* env().x(devX[1], 0.4, easeInOutCubic);
  // this one is for me
  yield* all(
    tags[1]().stroke(C.amber, 0.15),
    tags[1]().fill('#3a2c10', 0.15),
    tagTxt[1]().fill(C.amber, 0.15),
    tags[1]().scale(1.3, 0.15, easeOutCubic).to(1.1, 0.2),
    env().position([devX[1], DEV_Y - 10], 0.35, easeInCubic),
    env().scale(0.3, 0.35, easeInCubic),
    env().opacity(0, 0.35, easeInCubic),
  );
  oled.value().text('GO!');
  yield* all(
    oled.powerOn(),
    burst(view, new Vector2(devX[1], DEV_Y), [C.amber, C.teal, C.text], 170),
    delay(0.15, all(
      rtc().opacity(0.4, 0.3),
      tagTxt[2]().fill(C.dim, 0.3),
      popIn(notMe[1](), 0.25),
    )),
  );

  // later: more parts on the very same two wires
  yield* until(Math.max(useNow(), T.word('more', S9 + 8, 's09') - 0.3));
  yield* all(
    notMe[0]().opacity(0, 0.25),
    notMe[1]().opacity(0, 0.25),
    sensor().opacity(1, 0.3),
    rtc().opacity(1, 0.3),
    tagTxt[0]().fill(C.text, 0.3),
    tagTxt[2]().fill(C.text, 0.3),
    tags[0]().stroke(C.dim, 0.3),
    ghostDrop().opacity(1, 0.3),
    all(ghost().opacity(1, 0.3), ghost().scale(1, 0.45, easeOutBack)),
  );
  // gentle pulse on the two shared wires until the end
  yield loop(Infinity, () =>
    all(busD().lineWidth(16, 0.35).to(10, 0.35), busC().lineWidth(16, 0.35).to(10, 0.35), ghost().scale(1.05, 0.35).to(1, 0.35)),
  );
  yield all(
    oled.root().position.y(DEV_Y - 6, 0.9, easeInOutCubic).to(DEV_Y + 4, 0.9, easeInOutCubic),
    grid().opacity(0.6, 1.2, linear),
  );
  yield* until(T.total);
}));
