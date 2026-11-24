/**
 * Ep12 s09 - "Then the board serves a tiny web page. Think of a restaurant
 * menu where every dish has a number: tap a button, and the phone calls out
 * that number."  Menu card (numbered dishes) next to the phone page; the
 * buttons get the same numbers; a tap sends the number to the board.
 */
import {Line, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, delay, easeInOutCubic, easeOutBack, linear, sequence, useTime, Vector2} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Esp32Board, exact, flyArc, until} from '../lib/ep10';
import {Phone, timing12} from '../lib/ep12';
import {C, FONT} from '../style';

const T = timing12('page_menu');
const DISHES = ['Red light', 'Green light', 'Blue light', 'Lights off', 'Doorbell'];

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const phone = new Phone({x: 560, y: 40, scale: 0.9});
  const menu = createRef<Node>();
  const nums = DISHES.map(() => createRef<Rect>());
  const esp = createRef<Node>();
  const call = createRef<Rect>();
  const callTxt = createRef<Txt>();

  view.add(
    <Node ref={menu} x={-560} y={40} opacity={0} rotation={-3}>
      <Rect width={460} height={600} radius={14} fill={'#f3efe3'} shadowColor={'rgba(0,0,0,0.5)'} shadowBlur={30} shadowOffsetY={10} />
      <Txt y={-240} text={'MENU'} fontFamily={FONT.ui} fontWeight={900} fontSize={54} letterSpacing={10} fill={'#2a2418'} />
      <Line points={[[-170, -195], [170, -195]]} stroke={'#c8bfa8'} lineWidth={3} />
      {DISHES.map((d, i) => (
        <Node y={-130 + i * 84}>
          <Rect ref={nums[i]} x={-160} width={58} height={58} radius={29} fill={'#2a2418'}>
            <Txt text={String(i + 1)} fontFamily={FONT.ui} fontWeight={900} fontSize={32} fill={'#f3efe3'} />
          </Rect>
          <Txt x={-110} offsetX={-1} text={d} fontFamily={FONT.ui} fontWeight={700} fontSize={34} fill={'#2a2418'} />
          <Line points={[[60, 14], [190, 14]]} stroke={'#c8bfa8'} lineWidth={2} lineDash={[4, 6]} />
        </Node>
      ))}
    </Node>,
  );
  view.add(<Esp32Board refNode={esp} x={0} y={-150} scale={0.55} />);
  view.add(phone.node());
  view.add(
    <Rect ref={call} layout padding={[10, 22]} radius={[24, 24, 24, 6]} fill={C.amber} opacity={0} scale={0.5}>
      <Txt ref={callTxt} text={'number 1!'} fontFamily={FONT.ui} fontWeight={900} fontSize={36} fill={C.bg} />
    </Rect>,
  );

  const h1 = new Headline('The board serves a *web* *page*', {accent: C.teal});
  const h2 = new Headline('Like a *numbered* menu');
  view.add(h1.node());
  view.add(h2.node());

  // ------------------------------------------------------------ beats
  phone.root().scale(0.5).opacity(0);
  esp().scale(0.3).opacity(0);
  yield* all(
    delay(0.05, h1.in()),
    esp().scale(0.55, 0.4, easeOutBack),
    esp().opacity(1, 0.3),
  );
  // the page travels from the board to the phone
  yield* until(Math.max(useTime(), T.word('serves', 0.8) - 0.1));
  yield* all(
    phone.root().opacity(1, 0.3),
    phone.root().scale(0.9, 0.45, easeOutBack),
    phone.page().opacity(0).opacity(1, 0.5),
  );
  yield* sequence(0.08, ...phone.buttons.map(b => b().scale(1.08, 0.1).to(1, 0.2)));

  // a restaurant menu where every dish has a number
  yield* until(Math.max(useTime(), T.word('restaurant', 3.3) - 0.3));
  menu().x(-760);
  yield* all(h1.out(), delay(0.25, h2.in()), menu().opacity(1, 0.3), menu().x(-560, 0.5, easeOutBack));
  yield* until(Math.max(useTime(), T.word('every', 4.7) - 0.1));
  yield* sequence(
    0.18,
    ...nums.map((n, i) =>
      all(
        n().scale(1.3, 0.12).to(1, 0.25, easeOutBack),
        n().fill(C.amber, 0.1),
        phone.tags[i]().opacity(1, 0.2),
        phone.tags[i]().scale(1, 0.3, easeOutBack),
      ),
    ),
  );
  yield* h2.pulse();

  // tap a button ...
  yield* until(Math.max(useTime(), T.word('tap', 6.7) - 0.2));
  yield* phone.tap(0);
  // ... and the phone calls out that number
  yield* until(Math.max(useTime(), T.word('calls', 8.8) - 0.6));
  const from = phone.buttonPos(view, 0);
  call().position(from);
  yield* all(call().opacity(1, 0.15), call().scale(1, 0.3, easeOutBack), nums[0]().scale(1.3, 0.12).to(1, 0.3));
  yield* flyArc(call(), from, new Vector2(0, -290), 120, 0.7);
  yield* all(esp().scale(0.62, 0.12).to(0.55, 0.3, easeOutBack), call().rotation(0, 0.2));
  yield all(grid().opacity(0.6, 1.2, linear), call().position.y(-300, 0.6, easeInOutCubic));
  yield* until(T.total);
}));
