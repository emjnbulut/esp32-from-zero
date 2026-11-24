/**
 * Ep12 s12d - "Then it answers the phone with the same page again, so your
 * remote stays on the screen."   server.send(200, "text/html", PAGE);
 * Glimpse -> the line; the page flies from the board back to the phone.
 */
import {makeScene2D, Node, Rect} from '@motion-canvas/2d';
import {all, createRef, delay, easeOutBack, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, Esp32Board, exact, flyArc, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {addCodeLabel, BUTTONS, glimpse12, Phone, showLabel, timing12} from '../lib/ep12';
import {C} from '../style';

const T = timing12('code_answer');
const LINE = 'server.send(200, "text/html", PAGE);';

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -280, size: 52, code: LINE});
  const esp = createRef<Node>();
  const phone = new Phone({x: 500, y: 120, scale: 0.62});
  const doc = createRef<Node>();
  const stays = createRef<Rect>();

  view.add(<Esp32Board refNode={esp} x={-500} y={150} scale={0.75} />);
  view.add(phone.node());
  // a mini "page": the same five buttons
  view.add(
    <Node ref={doc} x={-500} y={60} opacity={0}>
      <Rect width={130} height={170} radius={10} fill={'#0b1220'} stroke={C.text} lineWidth={4} />
      {BUTTONS.map((b, i) => (
        <Rect y={-56 + i * 28} width={96} height={20} radius={5} fill={b.color} />
      ))}
    </Node>,
  );
  view.add(<Pill refNode={stays} text={'your remote stays ✓'} color={C.teal} x={0} y={300} size={32} />);
  view.add(code.node());

  const h1 = new Headline('Answer with the *same* *page*', {accent: C.teal});
  view.add(h1.node());

  const ZOOM_AT = 1.0;
  yield glimpse12(view, {from: 66, to: 68, match: LINE}, () => toView(view, code.code().absolutePosition()), 52, ZOOM_AT);

  phone.page().opacity(0.25);
  yield* delay(0.1, h1.in());
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);
  const lOk = addCodeLabel(view, code.code(), '200', 'OK', C.teal, 0, 30);
  const lPage = addCodeLabel(view, code.code(), 'PAGE', 'the page', C.amber, 0, 30);
  yield* all(code.code().selection(code.code().findFirstRange(lit('server.send')), 0.25), showLabel(lOk));

  // the same page, again: it flies back to the phone
  yield* until(Math.max(useTime(), T.word('same', 1.9) - 0.2));
  yield* all(code.code().selection(code.code().findFirstRange('PAGE'), 0.25), showLabel(lPage));
  doc().position([-500, 60]).scale(0.6);
  yield* all(doc().opacity(1, 0.15), doc().scale(1, 0.3, easeOutBack));
  const target = toView(view, phone.screen().absolutePosition());
  yield* all(flyArc(doc(), doc().position(), target, 200, 0.7), delay(0.4, doc().scale(0.6, 0.3)));
  doc().opacity(0);
  yield* all(
    phone.page().opacity(1, 0.1),
    phone.screen().fill('#1c2433', 0.05).to('#0b1220', 0.3),
    phone.root().scale(0.66, 0.1).to(0.62, 0.3, easeOutBack),
  );

  // ... so your remote stays on the screen
  yield* until(Math.max(useTime(), T.word('remote', 3.8) - 0.2));
  yield* all(popIn(stays(), 0.3), h1.pulse(), code.code().selection(code.code().findFirstRange(lit(LINE)), 0.3));
  yield* phone.tap(2);
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
