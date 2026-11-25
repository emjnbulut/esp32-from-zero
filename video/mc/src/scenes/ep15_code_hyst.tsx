/**
 * Ep15 s16 - "In code, that's two ifs: if it's closed and the light goes
 * above the top line, it opened. If it's open and the light falls below the
 * bottom line, it closed."
 *   if (!isOpen && light > OPEN_AT) {  isOpen = true;
 *   } else if (isOpen && light < CLOSED_AT) {  isOpen = false;  }
 * (drawer_spy.ino, the other lines of each branch left out.) Under the code,
 * one row per if: both checks tick, then the result.
 */
import {makeScene2D, Rect, Txt} from '@motion-canvas/2d';
import {all, createRef, easeOutBack, linear, Reference, useTime} from '@motion-canvas/core';
import {addBackdrop, drift} from '../lib/backdrop';
import {Headline} from '../lib/kinetic';
import {CodePanel, exact, lit, popIn, toView, until} from '../lib/ep10';
import {glimpse15, timing15} from '../lib/ep15';
import {C, FONT} from '../style';

const T = timing15('code_hyst');
const IF1 = 'if (!isOpen && light > OPEN_AT) {';
const IF2 = '} else if (isOpen && light < CLOSED_AT) {';
const CODE = [IF1, '  isOpen = true;', IF2, '  isOpen = false;', '}'].join('\n');

interface Check {
  box: Reference<Rect>;
  tick: Reference<Txt>;
  label: Reference<Txt>;
}
const mkCheck = (): Check => ({box: createRef<Rect>(), tick: createRef<Txt>(), label: createRef<Txt>()});

function Chip(props: {c: Check; text: string}) {
  return (
    <Rect ref={props.c.box} layout direction="row" alignItems="center" gap={12} padding={[10, 22]} radius={16} fill={'rgba(13,22,40,0.95)'} stroke={C.line} lineWidth={3}>
      <Txt ref={props.c.label} text={props.text} fontFamily={FONT.code} fontWeight={800} fontSize={34} fill={C.dim} />
      <Txt ref={props.c.tick} text={'✓'} fontFamily={FONT.ui} fontWeight={900} fontSize={36} fill={C.teal} opacity={0} />
    </Rect>
  );
}

export default makeScene2D(exact(T.total, function* (view) {
  const grid = addBackdrop(view);
  yield drift(grid, T.total);

  const code = new CodePanel({y: -235, size: 36, code: CODE});
  const rows = [createRef<Rect>(), createRef<Rect>()];
  const checks = [
    [mkCheck(), mkCheck()],
    [mkCheck(), mkCheck()],
  ];
  const results = [createRef<Rect>(), createRef<Rect>()];
  const ROW_TXT = [
    ['closed?', 'light 2600 > 1800?', 'opened!', C.amber],
    ['open?', 'light 900 < 1200?', 'closed!', C.teal],
  ];

  [40, 205].forEach((y, r) => {
    const col = ROW_TXT[r][3];
    view.add(
      <Rect ref={rows[r]} x={-560} offsetX={-1} y={y} layout direction="row" alignItems="center" gap={26} opacity={0}>
        <Rect width={58} height={58} radius={29} fill={C.line} layout justifyContent="center" alignItems="center">
          <Txt text={`${r + 1}`} fontFamily={FONT.ui} fontWeight={900} fontSize={32} fill={C.text} />
        </Rect>
        <Chip c={checks[r][0]} text={ROW_TXT[r][0]} />
        <Txt text={'&&'} fontFamily={FONT.code} fontWeight={800} fontSize={36} fill={C.dim} />
        <Chip c={checks[r][1]} text={ROW_TXT[r][1]} />
        <Txt text={'→'} fontFamily={FONT.ui} fontWeight={800} fontSize={44} fill={C.dim} />
        <Rect ref={results[r]} padding={[10, 26]} radius={36} fill={r === 0 ? 'rgba(255,181,71,0.18)' : 'rgba(45,212,191,0.16)'} stroke={col} lineWidth={4} opacity={0} scale={0.6}>
          <Txt text={ROW_TXT[r][2]} fontFamily={FONT.ui} fontWeight={900} fontSize={38} fill={col} />
        </Rect>
      </Rect>,
    );
  });
  view.add(code.node());

  const h1 = new Headline('In code: *two* *ifs*', {accent: C.amber});
  view.add(h1.node());

  const lineCenter = () => {
    const c = code.code();
    const box = c.getSelectionBBox(c.findFirstRange(lit(IF1)))[0];
    return toView(view, box.center.transformAsPoint(c.localToWorld()));
  };
  const ZOOM_AT = 1.0;
  yield glimpse15(view, {from: 68, to: 78, match: IF1}, lineCenter, 36, ZOOM_AT);

  yield* h1.in();
  yield* until(ZOOM_AT + 0.3);
  yield* code.panel().opacity(1, 0.2);

  const sel = (s: string | RegExp) => code.code().selection(code.code().findFirstRange(typeof s === 'string' ? lit(s) : s), 0.25);
  function* tick(c: Check, color: string) {
    yield* all(c.box().stroke(color, 0.2), c.label().fill(C.text, 0.2), c.box().fill('rgba(45,212,191,0.10)', 0.2), popIn(c.tick(), 0.25), c.box().scale(1.08, 0.1).to(1, 0.2));
  }

  // two ifs
  yield* until(Math.max(useTime(), T.word('ifs', 1.52) - 0.3));
  rows[0]().y(60);
  rows[1]().y(225);
  yield* all(
    code.code().selection([...code.code().findAllRanges(lit(IF1)), ...code.code().findAllRanges(lit(IF2))], 0.25),
    rows[0]().opacity(1, 0.3),
    rows[0]().y(40, 0.35),
    rows[1]().opacity(1, 0.3),
    rows[1]().y(205, 0.35),
  );

  // if it's closed ...
  yield* until(Math.max(useTime(), T.word('closed', 2.9) - 0.3));
  yield* all(sel('!isOpen'), tick(checks[0][0], C.teal));
  // ... and the light goes above the top line
  yield* until(Math.max(useTime(), T.word('above', 4.64) - 0.3));
  yield* sel('light > OPEN_AT');
  yield* until(Math.max(useTime(), T.word('top', 5.1) - 0.1));
  yield* tick(checks[0][1], C.teal);
  // it opened
  yield* until(Math.max(useTime(), T.word('opened', 6.3) - 0.25));
  yield* all(sel('isOpen = true;'), popIn(results[0](), 0.35));

  // if it's open ...
  yield* until(Math.max(useTime(), T.word('open', 7.86, undefined, 1) - 0.3));
  yield* all(sel(/(?<=else if \()isOpen/g), tick(checks[1][0], C.teal));
  // ... and the light falls below the bottom line
  yield* until(Math.max(useTime(), T.word('falls', 9.06) - 0.3));
  yield* sel('light < CLOSED_AT');
  yield* until(Math.max(useTime(), T.word('bottom', 9.94) - 0.1));
  yield* tick(checks[1][1], C.teal);
  // it closed
  yield* until(Math.max(useTime(), T.word('closed', 10.9, undefined, 1) - 0.25));
  yield* all(sel('isOpen = false;'), popIn(results[1](), 0.35));
  yield results[1]().scale(1.1, 0.1).to(1, 0.25, easeOutBack);
  yield grid().opacity(0.6, 1.0, linear);
  yield* until(T.total);
}));
