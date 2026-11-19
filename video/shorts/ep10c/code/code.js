/* Ep10 challenge Short: three code cards for the false-start fix (clip picked by __DATA.clip = c1 | c2 | c3).
 * Card is centred on x=960 and stays inside the middle square (x 420..1500) for the 1080x1080 crop. */
const CLIP = D.clip || "c1";
const DUR = D.schedule.duration;
const ui = $("#ui");
const SIZE = 40, W_CARD = 1000, X = 960 - W_CARD / 2;

// real code from challenge_false_start.ino (c2/c3 dedented by 2 so the longest line fits at 40 px)
const CLIPS = {
  c1: {
    kick: "THE FIX · <b>NEW STEP</b>",
    src: [
      "int state = 0;",
      "// 0 wait",
      "// 1 red",
      "// 2 yellow",
      "// 3 green",
      "// 4 result",
      "// 5 false start",
    ].join("\n"),
    // [time, firstLine, lineCount, color?]
    hl: [[0.4, 0, 1], [1.6, 1, 1], [2.0, 2, 1], [2.4, 3, 1], [2.8, 4, 1], [3.2, 5, 1], [3.9, 6, 1, "rgba(255,93,108,.28)"]],
    hot: [[3.9, 6]],
  },
  c2: {
    kick: "THE FIX · <b>NEW CHECK</b>",
    src: [
      "} else if ((state == 1 ||",
      "            state == 2) && pressed) {",
      "  Serial.println(\"FALSE START!\");",
      "  lights(LOW, LOW, LOW);",
      "  goTo(5, now);",
      "}",
    ].join("\n"),
    hl: [[0.4, 0, 2], [3.0, 4, 1, "rgba(255,93,108,.28)"]],
  },
  c3: {
    kick: "THE FIX · <b>STEP 5</b>",
    src: [
      "} else {",
      "  if (now - lastFlash >= 150) {",
      "    lastFlash = now;",
      "    flashOn = !flashOn;",
      "    setColor(flashOn ? 255 : 0, 0, 0);",
      "  }",
      "  if (inState >= 2000) {",
      "    setColor(0, 0, 40);",
      "    goTo(0, now);",
      "  }",
      "}",
    ].join("\n"),
    hl: [[0.4, 1, 1], [1.2, 2, 3, "rgba(255,93,108,.26)"], [2.8, 6, 1], [3.8, 7, 2], [5.0, 8, 1]],
  },
};
const cfg = CLIPS[CLIP];

const kick = el("div", "kick", cfg.kick, ui);
const lines = cfg.src.split("\n").length;
const lh = Math.round(SIZE * 1.55), pad = 32, h = lines * lh + pad * 2;
const y = Math.round(560 - h / 2 + 40);
const code = bigCode(ui, X, y, W_CARD, cfg.src, { size: SIZE, pad });

// own highlight bar (can span several lines)
const bar = box(code.c, 14, pad, W_CARD - 28, lh, "hlbar");
dyn((t) => {
  let cur = null;
  for (const e of cfg.hl) if (t >= e[0]) cur = e;
  bar.style.opacity = cur ? 1 : 0;
  if (cur) {
    const [, i, n, col] = cur;
    bar.style.top = pad + i * lh + "px";
    bar.style.height = n * lh + "px";
    bar.style.background = col || "rgba(255,181,71,.2)";
    bar.style.borderColor = col ? "rgba(255,93,108,.9)" : "rgba(255,181,71,.85)";
  }
});
// c1: the "5 false start" line turns bright once it is highlighted
if (cfg.hot) {
  const rows = code.body.children;
  dyn((t) => { for (const [t0, i] of cfg.hot) rows[i].classList.toggle("hotc", t >= t0); });
}

show(kick, 0.05, 0.35);
show(code.c, 0.1, 0.4);
hide([kick, code.c], DUR - 0.25, 0.2);

window.__ready = true;
