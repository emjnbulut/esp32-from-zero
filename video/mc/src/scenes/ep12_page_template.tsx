/**
 * Ep12 s13 - "The page itself is a ready template in the sketch. You only
 * change the labels and the colors."
 * Glimpse -> the PAGE template (the five <a> lines, real text); only the
 * labels and the colours light up as editable, and one button is changed
 * live: RED -> LAMP, #e5484d -> #a855f7, on the code and on the phone.
 */
import {Code, makeScene2D, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, delay, easeOutBack, linear, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {arduino} from '../lib/arduinoHighlighter';
import {Headline} from '../lib/kinetic';
import {exact, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {glimpse12, Phone, SKETCH12, timing12} from '../lib/ep12';
import {C, FONT} from '../style';

const T = timing12('page_template');
// the five link lines of PAGE, straight from the sketch (lines 40-44)
const LINKS = SKETCH12.lines.slice(39, 44);
const LABELS = /(?<=>)[A-Z]+(?=<)/g;
const COLORS = /#[0-9a-f]{6}/g;

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const card = createRef<Rect>();
  const code = createRef<Code>();
  const tmpl = createRef<Rect>();
  const sketchPill = createRef<Rect>();
  const phone = new Phone({x: 620, y: 70, scale: 0.82});

  view.add(
    <Rect ref={card} x={-330} y={20} layout direction="column" gap={10} padding={[20, 30, 26, 30]} radius={20} fill={'rgba(13,22,40,0.96)'} stroke={C.line} lineWidth={3} opacity={0}>
      <Rect layout gap={12} alignItems="center">
        <Rect padding={[4, 14]} radius={8} fill={C.amber}>
          <Txt text={'PAGE'} fontFamily={FONT.code} fontWeight={800} fontSize={26} fill={C.bg} />
        </Rect>
        <Txt text={'the web page, inside the sketch'} fontFamily={FONT.ui} fontSize={26} fill={C.dim} />
      </Rect>
      <Code ref={code} highlighter={arduino} fontFamily={FONT.code} fontSize={31} code={LINKS.join('\n')} />
    </Rect>,
  );
  view.add(<Pill refNode={tmpl} text={'ready template ✓'} color={C.teal} x={-300} y={-230} size={34} />);
  view.add(<Pill refNode={sketchPill} text={'you only change labels + colours'} color={C.amber} x={-300} y={270} size={32} />);
  view.add(phone.node());

  const h1 = new Headline('The page is a *ready* *template*', {accent: C.teal});
  view.add(h1.node());

  const firstLine = () => {
    const c = code();
    const box = c.getSelectionBBox(c.findFirstRange(lit(LINKS[0])))[0];
    return toView(view, box.center.transformAsPoint(c.localToWorld()));
  };
  const ZOOM_AT = 1.0;
  yield glimpse12(view, {from: 33, to: 46, match: LINKS[0]}, firstLine, 31, ZOOM_AT);

  phone.root().opacity(0);
  yield* delay(0.1, h1.in());
  yield* until(ZOOM_AT + 0.3);
  yield* all(card().opacity(1, 0.2), phone.root().opacity(1, 0.3));

  // a ready template
  yield* until(Math.max(useTime(), T.word('template', 1.8) - 0.2));
  yield* all(popIn(tmpl(), 0.3), h1.pulse());

  // you only change the labels ...
  yield* until(Math.max(useTime(), T.word('labels', 5.0) - 0.6));
  yield* all(popIn(sketchPill(), 0.3), code().selection(code().findAllRanges(LABELS), 0.3));
  const next = LINKS.join('\n').replace('>RED<', '>LAMP<');
  phone.labels[0]().text('LAMP');
  yield* all(code().code(next, 0.4), phone.buttons[0]().scale(1.1, 0.12).to(1, 0.25, easeOutBack));
  yield* code().selection(code().findAllRanges(LABELS), 0.1);

  // ... and the colours
  yield* until(Math.max(useTime(), T.word('colors', 5.7) - 0.2));
  yield* code().selection(code().findAllRanges(COLORS), 0.25);
  yield* all(
    code().code(next.replace('#e5484d', '#a855f7'), 0.35),
    phone.buttons[0]().fill('#a855f7', 0.35),
    phone.buttons[0]().scale(1.1, 0.12).to(1, 0.25, easeOutBack),
  );
  yield* code().selection(code().findAllRanges(COLORS), 0.1);
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
