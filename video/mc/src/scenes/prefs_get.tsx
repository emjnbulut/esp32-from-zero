/**
 * Ep10 s35 - on boot one line takes the record back out of the drawer:
 * best = prefs.getULong("best", 9999);  An empty drawer gives the huge
 * default 9999, so the very first round is always a record.
 */
import {makeScene2D, Rect, Txt} from '@motion-canvas/2d';
import {
  all,
  createRef,
  DEFAULT,
  delay,
  easeInOutCubic,
  easeOutBack,
  linear,
  useTime,
  Vector2,
} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {Oled} from '../lib/oled';
import {burst, CodePanel, Drawer, flyArc, lit, Pill, popIn, timing, toView, until, ValueCard, exact} from '../lib/ep10';
import {C, FONT} from '../style';

const T = timing('prefs_get');

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);
  const tEmpty = T.word('empty', T.total * 0.45);

  const drawer = new Drawer({x: -520, y: -70});
  const oled = new Oled({x: 520, y: -90, scale: 0.6, label: 'REFLEX 2.0 best:', value: '---', unit: 'ms'});
  const code = new CodePanel({y: 290, size: 54, chip: 'LOAD', chipColor: C.teal, code: ''});
  const fly = createRef<Rect>();
  const big = createRef<Txt>();
  const emptyTag = createRef<Rect>();
  const cmp = createRef<Rect>();
  const rec = createRef<Rect>();

  view.add(drawer.node());
  view.add(oled.node());
  view.add(code.node());
  view.add(<ValueCard refNode={fly} />);
  view.add(
    <Txt ref={big} text={'9999'} fontFamily={FONT.code} fontWeight={800} fontSize={120} fill={C.amber} opacity={0}
      shadowColor={'rgba(255,181,71,0.6)'} shadowBlur={30} />,
  );
  view.add(<Pill refNode={emptyTag} text={'empty'} color={C.dim} x={-200} y={-180} size={34} />);
  view.add(
    <Rect ref={cmp} x={520} y={150} layout gap={18} alignItems="center" padding={[10, 26]} radius={18}
      fill={'rgba(13,22,40,0.95)'} stroke={C.line} lineWidth={3} opacity={0} scale={0.6}>
      <Txt text={'287'} fontFamily={FONT.code} fontWeight={800} fontSize={56} fill={C.text} />
      <Txt text={'<'} fontFamily={FONT.code} fontWeight={800} fontSize={56} fill={C.teal} />
      <Txt text={'9999'} fontFamily={FONT.code} fontWeight={800} fontSize={56} fill={C.amber} />
    </Rect>,
  );
  view.add(<Pill refNode={rec} text={'first round = record ✓'} color={C.teal} x={520} y={-300} size={36} />);

  // unit follows the value so 4 digits never overlap "ms"
  oled.unit().x(() => oled.value().x() + oled.value().width() + 14);

  const h1 = new Headline('Power on → *take* *it* *out*', {accent: C.teal});
  const h2 = new Headline('Empty drawer? A *huge* number');
  view.add(h1.node());
  view.add(h2.node());

  const valueCenter = () => {
    const v = oled.value();
    return toView(view, new Vector2(v.width() / 2, 0).transformAsPoint(v.localToWorld()));
  };

  // ------------------------------------------------------------ boot
  drawer.root().scale(0.5).opacity(0);
  drawer.card().opacity(1);
  oled.content().opacity(0);
  yield* all(
    drawer.root().scale(1, 0.4, easeOutBack),
    drawer.root().opacity(1, 0.25),
    delay(0.1, h1.in()),
    delay(0.2, oled.powerOn()),
  );

  yield* until(Math.max(useTime(), T.word('line', 1.8) - 0.4));
  yield* code.show();
  yield* code.code().code('best = prefs.getULong("best", 9999);', 0.55);
  yield* code.code().selection(code.code().findFirstRange('getULong'), 0.25);

  // takes it back out
  yield* until(Math.max(useTime(), T.word('takes', 3) - 0.1));
  yield* drawer.open(320, 0.4);
  fly().position(toView(view, drawer.card().absolutePosition())).opacity(1).scale(1);
  drawer.card().opacity(0);
  const target = valueCenter().add([60, 0]);
  yield* all(flyArc(fly(), fly().position(), target, 220, 0.7), delay(0.45, fly().scale(0.5, 0.25)), delay(0.3, drawer.close(0.4)));
  fly().opacity(0);
  oled.value().text('214');
  yield* all(oled.value().scale(1.25, 0.1).to(1, 0.3, easeOutBack), burst(view, valueCenter(), [C.teal, C.amber, C.text], 160), h1.pulse());

  // ------------------------------------------------------------ empty drawer
  yield* until(Math.max(useTime(), tEmpty - 0.9));
  yield* all(h1.out(), delay(0.25, h2.in()), oled.powerOff(), code.code().selection(DEFAULT, 0.3));
  oled.value().text('---');
  yield* oled.powerOn();
  yield* drawer.open(320, 0.4);
  yield* all(
    popIn(emptyTag(), 0.3),
    drawer.drawer().rotation(2, 0.06).to(-2, 0.08).to(0, 0.06),
  );
  // the default 9999 jumps out of the code line onto the screen
  yield* until(Math.max(useTime(), T.word('huge', tEmpty + 1.5) - 0.4));
  yield* code.code().selection(code.code().findFirstRange('9999'), 0.25);
  const range = code.code().findFirstRange('9999');
  const box = code.code().getSelectionBBox(range)[0];
  const from = toView(view, box.center.transformAsPoint(code.code().localToWorld()));
  big().position(from).scale(0.45).opacity(1);
  yield* all(
    big().scale(1.6, 0.4, easeOutBack),
    big().position(from.add([0, -200]), 0.4, easeInOutCubic),
    drawer.close(0.4),
    emptyTag().opacity(0, 0.3),
    h2.pulse(),
  );
  yield* all(
    flyArc(big(), big().position(), valueCenter().add([80, 0]), 120, 0.55),
    delay(0.3, big().scale(0.7, 0.25)),
  );
  big().opacity(0);
  oled.value().text('9999');
  yield* oled.value().scale(1.2, 0.1).to(1, 0.3, easeOutBack);

  // so the first round is always a record
  yield* until(Math.max(useTime(), T.word('first', T.total - 3.4) - 1.0));
  yield* all(cmp().opacity(1, 0.2), cmp().scale(1, 0.35, easeOutBack));
  yield* until(Math.max(useTime(), Math.min(T.word('record', T.total - 2) - 0.5, T.total - 1.6)));
  yield* oled.powerOff();
  oled.label().text('NEW RECORD!');
  oled.value().text('287');
  yield* oled.powerOn();
  yield* all(
    popIn(rec(), 0.35),
    burst(view, valueCenter(), [C.amber, C.teal, C.text], 200),
    cmp().stroke(C.teal, 0.2),
  );
  yield all(rec().scale(1.05, 0.5).to(1, 0.5), grid().opacity(0.6, 1.2, linear));
  yield* until(T.total);
}));
