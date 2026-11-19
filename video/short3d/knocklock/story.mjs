/* Secret knock lock Short: the whole story as a pure function of time, timed to the narration words.
 * Shared by scene.js (browser: 3D + captions + overlay) and events.mjs (node: sound effects for mix.py).
 * The lock follows the real sketch (projects/06-secret-knock-lock): a press shorter than 250 ms is SHORT;
 * the rhythm SHORT SHORT LONG opens it; a wrong beat flashes red 4 x 240 ms and forgets; 3 s of quiet forgets;
 * open = rainbow 3 x 5 x 90 ms, then green for 2.5 s, then locked again. The yellow LED is on while held.
 */
const norm = (w) => w.toLowerCase().normalize("NFKD").replace(/[^a-z0-9ıüöçşğ]/g, "");

export function makeStory(schedule) {
  const L = Object.fromEntries(schedule.lines.map((l) => [l.id, l]));
  const DUR = schedule.duration;
  /** time of the nth word of a line (index), + offset */
  const Wi = (id, i, off = 0) => { const ws = L[id].words; return ws[Math.max(0, Math.min(ws.length - 1, i < 0 ? ws.length + i : i))].t + off; };
  const t0 = (id) => L[id].t0, t1 = (id) => L[id].t1;

  /* ---- presses [down, up] (Short seconds) ---- */
  const presses = [];
  // l03 "Short. Short. Long." : one word each, in both languages
  const p1 = Wi("l03", 0), p2 = Wi("l03", 1), p3 = Wi("l03", 2);
  presses.push([p1 - 0.02, p1 + 0.12], [p2 - 0.02, p2 + 0.12], [p3 - 0.02, p3 + 0.55]);
  const OPEN_AT = p3 + 0.55; // the release of the long beat opens the lock
  const RELOCK = OPEN_AT + 15 * 0.09 + 2.5;
  // l06 the stranger: a long press first ("Long..."), released on "wrong!"
  const s0 = Math.max(Wi("l06", 0) - 0.02, RELOCK + 0.2);
  const s1 = Math.max(s0 + 0.5, Wi("l06", 1) - 0.08);
  presses.push([s0, s1]);
  // l08 the parking ticket: the right rhythm again, each press timed on screen; the long one opens the lock
  const n8 = L.l08.words.length;
  const q1 = Math.max(s1 + 1.2, Wi("l08", Math.round(n8 * 0.52))), q2 = Math.max(q1 + 0.4, Wi("l08", Math.round(n8 * 0.7)));
  const q3 = Math.max(q2 + 0.4, Wi("l08", n8 - 3) - 0.05);
  presses.push([q1, q1 + 0.12], [q2, q2 + 0.14], [q3, q3 + 0.6]);
  const OPEN2 = q3 + 0.6, RELOCK2 = OPEN2 + 15 * 0.09 + 2.5;
  // l10: one right beat, then nothing: 3 s later the lock forgets (countdown on screen)
  const c1 = Math.max(RELOCK2 + 0.3, t0("l10") - 0.5);
  presses.push([c1, c1 + 0.12]);
  const FORGET_AT = c1 + 0.12 + 3.0;

  /* ---- the lock, simulated like the sketch ---- */
  // walk the presses in order and record the state changes
  const changes = []; // [t, {step, mode}] mode: idle | wrong | party | open
  let step = 0, busyUntil = -1, lastKnock = -1;
  const ev = []; // sound events [t, kind, value]
  const pushStep = (t, s) => changes.push([t, { mode: "idle", step: s }]);
  pushStep(-1, 0);
  for (const [a, b] of presses) {
    // quiet for 3 s in the middle of a rhythm
    if (step > 0 && lastKnock >= 0 && a - lastKnock >= 3) { const tf = lastKnock + 3; pushStep(tf, 0); ev.push([tf, "forget", 0]); step = 0; }
    if (a < busyUntil) continue; // delay() in the sketch: presses during the show are ignored
    ev.push([a, "down", 0], [b, "up", 0]);
    const beat = b - a >= 0.25 ? "LONG" : "SHORT";
    const want = step === 2 ? "LONG" : "SHORT";
    lastKnock = b;
    if (beat === want) {
      step += 1;
      ev.push([b, "beat", step]);
      if (step === 3) {
        changes.push([b, { mode: "party", step: 3 }]);
        changes.push([b + 15 * 0.09, { mode: "open", step: 3 }]);
        busyUntil = b + 15 * 0.09 + 2.5;
        pushStep(busyUntil, 0);
        ev.push([b, "unlock", 0], [busyUntil, "relock", 0]);
        step = 0; lastKnock = -1;
      } else pushStep(b, step);
    } else {
      changes.push([b, { mode: "wrong", step: 0 }]);
      busyUntil = b + 0.96;
      pushStep(busyUntil, 0);
      ev.push([b, "wrong", 0]);
      step = 0; lastKnock = -1;
    }
  }
  if (step > 0 && lastKnock >= 0) { pushStep(lastKnock + 3, 0); ev.push([lastKnock + 3, "forget", 0]); }
  for (let k = 1; k <= 3; k++) ev.push([FORGET_AT - 3 + k, "tick", k]); // the countdown 3-2-1
  ev.sort((x, y) => x[0] - y[0]);
  changes.sort((x, y) => x[0] - y[0]);

  const PARTY = [[1, 0, 0], [1, 160 / 255, 0], [0, 1, 0], [0, 120 / 255, 1], [150 / 255, 0, 1]];
  const PROGRESS = [[0, 0, 40 / 255], [0, 0, 1], [0, 200 / 255, 1], [0, 1, 0]];
  /** the lights at time t: { red, yellow, green, rgb: [r, g, b], step, mode } */
  function lock(t) {
    let cur = changes[0];
    for (const c of changes) if (t >= c[0]) cur = c; else break;
    const [tc, st] = cur;
    const held = presses.some(([a, b]) => t >= a && t < b && !(a < 0));
    const out = { yellow: held ? 1 : 0, red: 1, green: 0, rgb: PROGRESS[st.step] || PROGRESS[0], step: st.step, mode: st.mode };
    if (st.mode === "wrong") { const k = t - tc; out.rgb = Math.floor(k / 0.12) % 2 === 0 ? [1, 0, 0] : [0, 0, 0]; }
    if (st.mode === "party") { out.red = 0; out.green = 1; out.rgb = PARTY[Math.floor((t - tc) / 0.09) % 5]; }
    if (st.mode === "open") { out.red = 0; out.green = 1; out.rgb = [0, 1, 0]; }
    return out;
  }
  /** button cap 0..1 and the ring pulse */
  function button(t) {
    let p = 0, pulse = -1;
    for (const [a, b] of presses) {
      if (t >= a && t < b) p = Math.max(p, Math.min(1, (t - a) / 0.06));
      else if (t >= b && t < b + 0.08) p = Math.max(p, 1 - (t - b) / 0.08);
      if (t >= a && t < a + 0.6) pulse = (t - a) / 0.6;
    }
    return { p, pulse };
  }
  // the montage (l07): parts snap in over the line, the circuit is complete before l08
  const MONT = [t0("l07") - 0.1, t1("l07") + 0.2];
  return { L, DUR, Wi, t0, t1, presses, lock, button, ev, OPEN_AT, RELOCK, OPEN2, RELOCK2, FORGET_AT, MONT, s0, s1, q1, q2, q3, c1, norm };
}
