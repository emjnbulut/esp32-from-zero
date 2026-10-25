/* Project Reel overlay (1080x1920, transparent). Data from tools/reel.py:
 * segments [{kind: "footage" | "code" | "end", t0, t1, text, sub, code, missing, desc}].
 * footage: big text over the creator's clip (or a placeholder card while the clip is missing);
 * code: an opaque scene with one big code card; end: the closing card. No narration: text carries it. */
const stage = $("#stage");
const segs = D.segments || [];
const bar = box(stage, 0, 0, 0, 12, "");
bar.id = "bar";
dyn((t) => { bar.style.width = (1080 * Math.min(1, t / D.schedule.duration)) + "px"; });
const fadeBoth = (e, a, b) => { gsap.set(e, { opacity: 0 }); TO(e, a, 0.25, { opacity: 1, ease: "power1.out" }); TO(e, b - 0.2, 0.2, { opacity: 0, ease: "power1.in" }); };
for (const s of segs) {
  if (s.kind === "code" || s.kind === "end" || s.missing) {
    const sc = box(stage, 0, 0, 1080, 1920, "rscene");
    fadeBoth(sc, s.t0, s.t1);
    if (s.missing) sc.innerHTML = `<div class="ph"><div class="k">📹 ${s.missing}</div><div class="d">${s.desc || ""}</div></div>`;
    if (s.kind === "code") {
      const lines = s.code.split("\n").length, size = lines > 6 ? 38 : 44;
      const c = bigCode(sc, 50, 0, 980, s.code, { size, pad: 36 });
      c.c.style.top = (1000 - c.h / 2) + "px";
      gsap.set(c.c, { opacity: 1 });
      if (s.hl != null) {
        const ln = [].concat(s.hl);
        c.hl(ln.map((i, k) => [s.t0 + 0.4 + k * ((s.t1 - s.t0 - 0.6) / ln.length), i]));
      }
    }
    if (s.kind === "end") {
      sc.insertAdjacentHTML("beforeend", `<div class="abs" style="left:0;top:560px;width:1080px">
        <div class="brand">${LOGOS.A().replace("<svg ", '<svg width="70" height="70" ')}<span>PIN BY PIN LAB</span></div></div>`);
    }
  }
  if (s.text || s.sub) {
    const y = s.kind === "end" ? 760 : s.kind === "code" ? 300 : 230;
    const tx = box(stage, 0, y, 0, 0, "rtext", `<div class="big">${s.text || ""}</div>${s.sub ? `<div class="small">${s.sub}</div>` : ""}`);
    css(tx, { width: "980px", left: "50px", height: "auto" });
    gsap.set(tx, { opacity: 0, y: 30 });
    TO(tx, s.t0 + 0.05, 0.35, { opacity: 1, y: 0, ease: "back.out(1.6)" });
    TO(tx, s.t1 - 0.2, 0.2, { opacity: 0, ease: "power1.in" });
  }
}
window.__seek(0);
window.__ready = true;
