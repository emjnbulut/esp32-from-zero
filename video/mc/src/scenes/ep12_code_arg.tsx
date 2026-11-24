/**
 * Ep12 s12c - "The helper reads that note with one line, server arg c, and
 * picks the color with a few ifs, just like episode six."
 *   String c = server.arg("c");   + the if / else if chain -> setColor
 */
import {Code, lines, makeScene2D, Node, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, delay, easeOutBack, linear, useTime, Vector2} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {arduino} from '../lib/arduinoHighlighter';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, flyArc, lit, Pill, popIn, toView, until} from '../lib/ep10';
import {glimpse12, Led, ledSignal, timing12} from '../lib/ep12';
import {C, FONT} from '../style';

const T = timing12('code_arg');
const LINE = 'String c = server.arg("c");';
const IFS = [
  'if (c == "red") setColor(255, 0, 0);',
  'else if (c == "green") setColor(0, 255, 0);',
  'else if (c == "blue") setColor(0, 0, 255);',
  'else setColor(0, 0, 0);',
].join('\n');

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -280, size: 56, code: LINE});
  const slip = createRef<Rect>();
  const value = createRef<Rect>();
  const ifPanel = createRef<Rect>();
  const ifs = createRef<Code>();
  const check = createRef<Txt>();
  const led = createRef<Node>();
  const ledColor = ledSignal();
  const ep6 = createRef<Rect>();

  view.add(
    <Rect ref={slip} x={-640} y={-60} rotation={-4} layout direction="column" alignItems="center" padding={[14, 30]} radius={8} fill={'#fbf8ef'} opacity={0}>
      <Txt text={'note:'} fontFamily={FONT.ui} fontWeight={700} fontSize={26} fill={'#8a7f6a'} />
      <Txt text={'c = red'} fontFamily={'Segoe Print'} fontWeight={700} fontSize={44} fill={'#c0392b'} />
    </Rect>,
  );
  view.add(
    <Rect ref={value} x={330} y={-150} layout padding={[8, 22]} radius={14} fill={'#101a2c'} stroke={C.amber} lineWidth={3} opacity={0} scale={0.5}>
      <Txt text={'c = "red"'} fontFamily={FONT.code} fontWeight={800} fontSize={40} fill={C.amber} />
    </Rect>,
  );
  view.add(
    <Rect ref={ifPanel} x={-170} y={120} padding={[22, 32]} layout radius={20} fill={'rgba(13,22,40,0.95)'} stroke={C.line} lineWidth={3} opacity={0}>
      <Code ref={ifs} highlighter={arduino} fontFamily={FONT.code} fontSize={36} code={IFS} />
    </Rect>,
  );
  view.add(<Txt ref={check} text={'✓'} fontFamily={FONT.ui} fontWeight={900} fontSize={56} fill={C.teal} opacity={0} />);
  view.add(<Led refNode={led} color={ledColor} x={640} y={90} scale={0.85} />);
  view.add(<Pill refNode={ep6} text={'just like Episode 6'} color={C.teal} x={640} y={300} size={32} />);
  view.add(code.node());

  const h1 = new Headline('Read the *note*, pick the colour', {accent: C.amber});
  view.add(h1.node());

  const ZOOM_AT = 1.1;
  yield glimpse12(view, {from: 70, to: 75, match: LINE}, () => toView(view, code.code().absolutePosition()), 56, ZOOM_AT);

  led().opacity(0);
  yield* delay(0.1, h1.in());
  yield* until(ZOOM_AT + 0.3);
  yield* all(code.panel().opacity(1, 0.2), slip().opacity(1, 0.3), led().opacity(1, 0.3));

  // one line: server.arg("c") reads the note
  yield* until(Math.max(useTime(), T.word('server', 3.0) - 0.2));
  yield* code.code().selection(code.code().findFirstRange(lit('server.arg("c")')), 0.25);
  const argPos = (() => {
    const c = code.code();
    const box = c.getSelectionBBox(c.findFirstRange(lit('server.arg("c")')))[0];
    return toView(view, box.center.transformAsPoint(c.localToWorld()));
  })();
  yield* all(flyArc(slip(), slip().position(), argPos, 140, 0.55), slip().scale(0.4, 0.55));
  slip().opacity(0);
  yield* all(popIn(value(), 0.3), code.code().selection(code.code().findFirstRange(lit('String c')), 0.25));

  // ... and picks the colour with a few ifs
  yield* until(Math.max(useTime(), T.word('picks', 5.3) - 0.2));
  ifPanel().position.y(150);
  yield* all(ifPanel().opacity(1, 0.3), ifPanel().position.y(120, 0.35, easeOutBack), ifs().selection(lines(0, 0), 0));
  yield* until(Math.max(useTime(), T.word('ifs', 6.8) - 0.4));
  // c == "red"? yes -> setColor(255, 0, 0)
  yield* ifs().selection(lines(0, 0), 0.2);
  const ifBox = ifs().getSelectionBBox(lines(0, 0))[0];
  const rowRight = toView(view, new Vector2(ifBox.right + 30, ifBox.center.y).transformAsPoint(ifs().localToWorld()));
  check().position(rowRight.add([20, 0]));
  ledColor('#e5484d');
  yield* all(
    check().opacity(1, 0.15),
    check().scale(1.4, 0.1).to(1, 0.25, easeOutBack),
    led().scale(1, 0.12).to(0.85, 0.3, easeOutBack),
    value().scale(1.1, 0.1).to(1, 0.2),
  );

  // just like episode six
  yield* until(Math.max(useTime(), T.word('episode', 8.3) - 0.2));
  yield* all(popIn(ep6(), 0.3), ifs().selection(lines(0, 3), 0.3), h1.pulse());
  yield grid().opacity(0.6, 1.2, linear);
  yield* until(T.total);
}));
