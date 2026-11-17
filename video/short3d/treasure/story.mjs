/* Treasure-detector Short: the whole animation as a pure function of time, timed to the narration words.
 * Used by track.mjs (writes build/track.json for Blender) and by overlay.js in the browser (captions, code card).
 * The LEDs follow the real sketch (projects/05-treasure-detector): heat = map(distance, 0, 50, 255, 0),
 * RGB = (heat, 0, 255 - heat), beep every map(distance, 0, 50, 40, 700) ms, party() = 3 x 6 colours of 90 ms.
 */
export const FPS = 30;
const clamp01 = (x) => Math.min(1, Math.max(0, x));
const smooth = (x) => { x = clamp01(x); return x * x * (3 - 2 * x); };
const lerp = (a, b, k) => a + (b - a) * k;
const norm = (w) => w.toLowerCase().replace(/[^a-z0-9]/g, "");
const amap = (x, a, b, c, d) => Math.trunc(((x - a) * (d - c)) / (b - a) + c); // Arduino map(): integer maths

export function makeStory(schedule, info) {
  const L = Object.fromEntries(schedule.lines.map((l) => [l.id, l]));
  /** time of a word in a line (first match of the word text, or index), + offset */
  const W = (id, word, off = 0) => {
    const ws = L[id].words;
    const w = typeof word === "number" ? ws[word] : ws.find((x) => norm(x.w) === norm(word));
    if (!w) throw new Error(`word ${word} not in ${id}`);
    return w.t + off;
  };
  const DUR = schedule.duration;
  const T_PRESS = W("l07", "button", 0.15);
  const T_PARTY = T_PRESS + 0.06;
  const T_PARTY_END = T_PARTY + 18 * 0.09;
  const SECRET0 = 63, SECRET1 = 0; // party(): 63 + 37 = 100 -> 0

  /* knob number keys [time, number] (eased between keys) */
  const NK = [
    [0, 61], [L.l02.t0, 61], [W("l02", "knob"), 34], [W("l02", "treasure"), 78], [L.l02.t1, 22], [L.l03.t0 + 0.6, 9],
    [L.l04.t0 - 0.1, 9], [L.l04.t1, 38], [L.l05.t1, 52], [W("l06", "warmer"), 55], [W("l06", "hotter"), 60],
    [W("l07", "here"), 63], [T_PARTY_END + 0.6, 63],
    [W("l09", "zero"), 0], [W("l09", "ninetynine", 0.3), 99], [W("l10", "far"), 47], [L.l10.t1, 30],
    [W("l11", "color"), 12], [W("l11", "speed"), 4], [L.l12.t0, 4], [L.l12.t1, 18],
    [L.l13.t0 + 0.5, 18], [DUR - 1.2, 37], [DUR, 37],
  ];
  const number = (t) => {
    let i = 0;
    while (i < NK.length - 2 && t >= NK[i + 1][0]) i++;
    const [t0, a] = NK[i], [t1, b] = NK[i + 1];
    return Math.round(lerp(a, b, smooth((t - t0) / Math.max(1e-3, t1 - t0))));
  };
  const secretAt = (t) => (t < T_PARTY_END ? SECRET0 : SECRET1);
  // l13: the treasure moved to 37 (second round), so the ending is "hot" again and loops into the hook
  const secret = (t) => (t >= L.l13.t0 ? 37 : secretAt(t));

  /* beeper: the sketch's millis() logic, stepped at 1 ms */
  const beep = [];
  { let last = 0, on = false;
    for (let ms = 0; ms <= DUR * 1000 + 50; ms++) {
      const t = ms / 1000;
      const inParty = t >= T_PARTY && t < T_PARTY_END;
      if (!inParty) {
        let d = Math.abs(number(t) - secret(t)); if (d > 50) d = 50;
        if (ms - last >= amap(d, 0, 50, 40, 700)) { last = ms; on = !on; }
      }
      beep.push(on);
    } }
  const PARTY = [[255, 0, 0], [255, 120, 0], [255, 255, 0], [0, 255, 0], [0, 120, 255], [150, 0, 255]];

  /* camera shots: [t0, t1, from {pos, tgt, fov}, to {...}] in three.js mm, vertical fov in degrees */
  const S = (pos, tgt, fov) => ({ pos, tgt, fov });
  const A = info.anchors;
  const knob = A.knobCenter, rgbT = A.rgbTop, rled = A.rledTop, btnT = A.btnTop;
  const press = W("l07", "press", -0.05);
  const SHOTS = [
    [0, L.l02.t0, S([rgbT[0] + 14, 30, rgbT[2] + 36], [rgbT[0] - 1, rgbT[1] - 4, rgbT[2]], 34), S([rgbT[0] + 10, 27, rgbT[2] + 28], [rgbT[0] - 1, rgbT[1] - 4, rgbT[2]], 31)],
    [L.l02.t0, L.l03.t0, S([knob[0] + 26, 62, knob[2] + 42], [knob[0], knob[1] + 2, knob[2]], 34), S([knob[0] - 12, 66, knob[2] + 46], [knob[0], knob[1] + 2, knob[2]], 32)],
    [L.l03.t0, L.l05.t0, S([86, 86, 78], [50, 14, -14], 40), S([80, 80, 70], [50, 14, -14], 38)],
    [L.l05.t0, L.l06.t0, S([rled[0] + 16, 32, rled[2] + 38], [rled[0] + 1, rled[1] - 4, rled[2] - 2], 34), S([rled[0] + 12, 28, rled[2] + 29], [rled[0] + 1, rled[1] - 4, rled[2] - 2], 31)],
    [L.l06.t0, W("l07", "crazy", 0.45), S([knob[0] + 10, 72, knob[2] + 56], [knob[0] - 4, knob[1] - 2, knob[2] + 4], 38), S([knob[0] + 7, 64, knob[2] + 46], [knob[0] - 4, knob[1] - 2, knob[2] + 4], 35)],
    [W("l07", "crazy", 0.45), L.l08.t0, S([btnT[0] + 18, 36, btnT[2] + 34], [btnT[0], btnT[1] - 3, btnT[2]], 34), S([btnT[0] + 13, 30, btnT[2] + 25], [btnT[0], btnT[1] - 3, btnT[2]], 31)],
    [L.l08.t0, L.l09.t0, S([60, 64, 92], [42, 24, -8], 44), S([36, 66, 92], [42, 26, -8], 42)],
    [L.l09.t0, L.l12.t0, S([150, 150, 30], [16, 6, 0], 42), S([144, 160, 16], [14, 6, 0], 40)],
    [L.l12.t0, L.l13.t0, S([knob[0] + 6, 128, knob[2] + 34], [knob[0], A.knobTop[1], knob[2]], 34), S([knob[0] + 3, 118, knob[2] + 28], [knob[0], A.knobTop[1], knob[2]], 32)],
    [L.l13.t0, DUR + 0.1, S([130, 70, 118], [22, 8, 0], 40), S([84, 62, 146], [22, 8, 0], 38)],
  ];
  const camera = (t) => {
    const s = SHOTS.find((x) => t >= x[0] && t < x[1]) || SHOTS[SHOTS.length - 1];
    const k = smooth((t - s[0]) / (s[1] - s[0])) * 0.85 + clamp01((t - s[0]) / (s[1] - s[0])) * 0.15;
    const m = (a, b) => a.map((v, i) => lerp(v, b[i], k));
    return { pos: m(s[2].pos, s[3].pos), tgt: m(s[2].tgt, s[3].tgt), fov: lerp(s[2].fov, s[3].fov, k), shot: SHOTS.indexOf(s) };
  };

  function state(t) {
    const n = number(t), sec = secret(t);
    let d = Math.abs(n - sec); if (d > 50) d = 50;
    const heat = amap(d, 0, 50, 255, 0);
    let rgb = [heat, 0, 255 - heat];
    const inParty = t >= T_PARTY && t < T_PARTY_END;
    if (inParty) rgb = PARTY[Math.min(17, Math.floor((t - T_PARTY) / 0.09)) % 6];
    const capDown = t >= T_PRESS - 0.05 && t < T_PRESS + 0.28 ? smooth((t - (T_PRESS - 0.05)) / 0.06) * (1 - smooth((t - T_PRESS - 0.18) / 0.1)) : 0;
    const coinK = clamp01((t - T_PARTY) / 0.5);
    const coinOut = smooth((t - (L.l09.t0 - 0.4)) / 0.4);
    const dim = smooth((t - (L.l09.t0 - 0.2)) / 0.5) * (1 - smooth((t - (L.l12.t0 - 0.3)) / 0.6));
    return {
      t, number: n, secret: sec, distance: d, heat,
      knobDeg: -135 + (n / 99) * 270,
      rgb, rgbOn: 1,
      rled: beep[Math.min(beep.length - 1, Math.round(t * 1000))] ? 1 : 0,
      cap: capDown,
      party: inParty ? 1 : 0,
      coin: t >= T_PARTY && coinOut < 1 ? { y: lerp(0, 34, 1 - (1 - coinK) ** 3), spin: (t - T_PARTY) * 540, scale: Math.min(1, coinK * 2) * (1 - coinOut) } : null,
      rings: !inParty && t < L.l09.t0 - 0.3 && t > L.l02.t0 ? heat / 255 : 0,
      dim,
      cam: camera(t),
      T: { press: T_PRESS, party: T_PARTY, partyEnd: T_PARTY_END },
    };
  }
  return { state, L, W, DUR, SHOTS };
}
