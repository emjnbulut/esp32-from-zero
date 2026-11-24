/**
 * Ep12 s08 - "In code, opening the network is one line: soft A P, with a name
 * and a password."   WiFi.softAP(WIFI_NAME, WIFI_PASSWORD);
 * Glimpse -> the line; the board sends out Wi-Fi like a phone hotspot and
 * the network shows up in the phone's Wi-Fi list.
 */
import {Circle, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, delay, easeOutBack, linear, loop, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, Esp32Board, exact, Pill, popIn, toView, until} from '../lib/ep10';
import {addCodeLabel, glimpse12, pulseWifi, showLabel, timing12, Wifi} from '../lib/ep12';
import {C, FONT} from '../style';

const T = timing12('code_softap');
const LINE = 'WiFi.softAP(WIFI_NAME, WIFI_PASSWORD);';

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -270, size: 56, code: LINE});
  const esp = createRef<Node>();
  const arcs = [createRef<Circle>(), createRef<Circle>(), createRef<Circle>()];
  const hotspot = createRef<Rect>();
  const phone = createRef<Node>();
  const net = createRef<Rect>();
  const netName = createRef<Txt>();
  const lock = createRef<Node>();

  view.add(<Esp32Board refNode={esp} x={-430} y={190} scale={0.75} />);
  view.add(<Wifi refs={arcs} x={-430} y={70} />);
  view.add(<Pill refNode={hotspot} text={'like your phone’s hotspot'} color={C.teal} x={-430} y={330} size={32} />);
  // the phone's Wi-Fi list
  view.add(
    <Node ref={phone} x={440} y={150} opacity={0}>
      <Rect width={420} height={300} radius={30} fill={'#0d1117'} stroke={'#3a4766'} lineWidth={5} />
      <Txt x={-170} y={-110} offsetX={-1} text={'Wi-Fi'} fontFamily={FONT.ui} fontWeight={800} fontSize={34} fill={C.text} />
      <Rect y={-40} width={380} height={56} radius={12} fill={'#151d2b'}>
        <Txt x={-170} offsetX={-1} text={'Home-WiFi'} fontFamily={FONT.ui} fontSize={26} fill={C.dim} />
      </Rect>
      <Rect ref={net} y={30} width={380} height={64} radius={12} fill={'#151d2b'} stroke={C.teal} lineWidth={0}>
        <Txt ref={netName} x={-170} offsetX={-1} text={'PinByPin-ESP32'} fontFamily={FONT.ui} fontWeight={800} fontSize={30} fill={C.text} />
        <Node ref={lock} x={160}>
          <Rect y={6} width={26} height={22} radius={4} fill={C.amber} />
          <Circle y={-6} size={22} stroke={C.amber} lineWidth={5} startAngle={180} endAngle={360} />
        </Node>
      </Rect>
      <Rect y={100} width={380} height={56} radius={12} fill={'#151d2b'}>
        <Txt x={-170} offsetX={-1} text={'Cafe-Guest'} fontFamily={FONT.ui} fontSize={26} fill={C.dim} />
      </Rect>
    </Node>,
  );
  view.add(code.node());

  const h1 = new Headline('The board opens its *own* Wi-Fi', {accent: C.teal});
  view.add(h1.node());

  const ZOOM_AT = 1.1;
  yield glimpse12(view, {from: 95, to: 96, match: LINE}, () => toView(view, code.code().absolutePosition()), 56, ZOOM_AT);

  esp().scale(0.4).opacity(0);
  yield* all(esp().scale(0.75, 0.4, easeOutBack), esp().opacity(1, 0.3), delay(0.1, h1.in()));
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);
  // the network opens: waves + hotspot analogy
  yield loop(Infinity, () => pulseWifi(arcs));
  yield* popIn(hotspot(), 0.3);

  // soft A P
  yield* until(Math.max(useTime(), T.word('soft', 3.3) - 0.1));
  yield* all(
    code.code().selection(code.code().findFirstRange('softAP'), 0.25),
    phone().opacity(1, 0.3),
    phone().position.y(150, 0.3),
    h1.pulse(),
  );
  // with a name ...
  const lName = addCodeLabel(view, code.code(), 'WIFI_NAME', '"PinByPin-ESP32"', C.teal);
  const lPass = addCodeLabel(view, code.code(), 'WIFI_PASSWORD', '"esp32lab"', C.amber);
  yield* until(Math.max(useTime(), T.word('name', 5.3) - 0.2));
  yield* all(
    code.code().selection(code.code().findFirstRange('WIFI_NAME'), 0.25),
    showLabel(lName),
    net().lineWidth(4, 0.2),
    netName().fill(C.teal, 0.2),
    net().scale(1.06, 0.12).to(1, 0.25),
  );
  // ... and a password
  yield* until(Math.max(useTime(), T.word('password', 5.8) - 0.1));
  yield* all(
    code.code().selection(code.code().findFirstRange('WIFI_PASSWORD'), 0.25),
    showLabel(lPass),
    lock().scale(1.5, 0.15).to(1, 0.3, easeOutBack),
  );
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
