/**
 * Ep10 s34 - on a new record, one line puts the time in the drawer with the
 * label "best": prefs.putULong("best", best);
 */
import {makeScene2D, Rect} from '@motion-canvas/2d';
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
  Vector2,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Oled} from '../lib/oled';
import {burst, CodePanel, Drawer, flyArc, lit, Pill, popIn, timing, toView, until, ValueCard, exact} from '../lib/ep10';
import {C} from '../style';

const T = timing('prefs_put');

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const oled = new Oled({x: -500, y: -70, scale: 0.66, label: 'your time', value: '231', unit: 'ms'});
  const drawer = new Drawer({x: 300, y: -60});
  const code = new CodePanel({y: 290, size: 54, chip: 'SAVE', code: ''});
  const fly = createRef<Rect>();
  const saved = createRef<Rect>();

  view.add(oled.node());
  view.add(drawer.node());
  view.add(code.node());
  view.add(<ValueCard refNode={fly} />);
  view.add(<Pill refNode={saved} text={'saved ✓'} x={300} y={160} size={36} />);

  const h1 = new Headline('New record? *Put* *it* *away*');
  view.add(h1.node());

  const valueCenter = () => {
    const v = oled.value();
    return toView(view, new Vector2(v.width() / 2, 0).transformAsPoint(v.localToWorld()));
  };

  // ------------------------------------------------------------ beats
  oled.root().scale(0.4).opacity(0);
  drawer.root().scale(0.5).opacity(0);
  yield* all(
    oled.root().scale(0.66, 0.4, easeOutBack),
    oled.root().opacity(1, 0.25),
    delay(0.1, all(drawer.root().scale(1, 0.4, easeOutBack), drawer.root().opacity(1, 0.25))),
    delay(0.1, h1.in()),
  );

  // you beat the record
  yield* until(Math.max(useTime(), T.word('record', 1.4) - 0.3));
  yield* oled.powerOff();
  oled.label().text('NEW RECORD!');
  oled.value().text('214');
  yield* oled.powerOn();
  yield* all(
    oled.value().scale(1.25, 0.1).to(1, 0.3, easeOutBack),
    burst(view, valueCenter(), [C.amber, C.teal, C.text], 170),
  );

  // one line
  yield* until(Math.max(useTime(), T.word('line', 2.6) - 0.4));
  yield* code.show();
  yield* code.code().code('prefs.putULong("best", best);', 0.55);
  yield* code.code().selection(code.code().findFirstRange('putULong'), 0.25);

  // it goes into the drawer
  yield* until(Math.max(useTime(), T.word('puts', 3.6) - 0.1));
  fly().position(valueCenter()).scale(0.5).opacity(0);
  yield* all(drawer.open(320, 0.4), fly().opacity(1, 0.2), fly().scale(1, 0.35, easeOutBack));
  const tray = toView(view, drawer.card().absolutePosition());
  yield* flyArc(fly(), fly().position(), tray, 220, 0.65);
  drawer.card().opacity(1);
  fly().opacity(0);
  yield* drawer.card().scale([1.1, 0.9], 0.1).to(1, 0.2);

  // with a label: best
  yield* until(Math.max(useTime(), T.word('label', T.total - 2.6) - 0.2));
  yield* all(
    code.code().selection(code.code().findFirstRange(lit('"best"')), 0.25),
    drawer.cardLabel().scale(1.35, 0.15).to(1, 0.3, easeOutBack),
    drawer.cardLabel().fill(C.amber, 0.15).to(C.teal, 0.5),
    h1.pulse(),
  );
  yield* until(Math.max(useTime(), Math.min(T.total - 1.4, useTime() + 0.6)));
  yield* all(drawer.close(0.4), delay(0.25, popIn(saved(), 0.3)), code.code().selection(DEFAULT, 0.3));

  const glow = createSignal(0);
  drawer.body().shadowColor(() => `rgba(45,212,191,${0.2 + glow() * 0.4})`);
  yield loop(Infinity, () => glow(1, 0.6).to(0, 0.6));
  yield all(saved().scale(1.05, 0.5).to(1, 0.5), grid().opacity(0.6, 1.2, linear), oled.root().position.y(-80, 0.8, easeOutCubic));
  yield* until(T.total);
}));
