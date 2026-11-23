# Motion Canvas scenes (Pin by Pin Lab)

Fast, kinetic 2D explainer scenes for *ESP32 From Zero*, built with
[Motion Canvas](https://motioncanvas.io/) 3.17.2. This replaces the old static
slide-card engine in `video/engine` for 2D scenes: show only the few lines
of code that matter and keep things moving.

## Layout

```
video/mc/
  vite.config.ts          Motion Canvas + FFmpeg plugins
  render.html             headless render page (used by render.mjs)
  render.mjs              one-command headless render
  src/
    project.ts            registers every scene (editor + renderer)
    style.ts              ALL colours, fonts, safe areas, timings
    scenes/<name>.tsx     one file per scene (scene name = file name)
    lib/                  shared building blocks
      backdrop.tsx        navy bg + drifting grid + vignette
      kinetic.tsx         Headline: word-by-word masked kinetic text
      oled.tsx            0.96" SSD1306 breakout (powerOn / powerOff)
      arduinoHighlighter.ts  tiny C++ highlighter for the Code node
    render/entry.ts       drives core's Renderer for render.html
  output/<name>.mp4       render results (+ <name>_frames/ check PNGs)
```

## Render

From the repo root:

```
node video/mc/render.mjs prefsRecord              # 1920x1080, 30 fps (course standard)
node video/mc/render.mjs prefsRecord --fps 60     # smoother, 2x the render time
node video/mc/render.mjs prefsRecord --frames     # also dump 4 PNG check frames
node video/mc/render.mjs prefsRecord --to 3       # only the first 3 s (quick look)
node video/mc/render.mjs prefsRecord --exporter ffmpeg   # use @motion-canvas/ffmpeg
```

What it does: starts `vite --port 9000 --strictPort` (or reuses a dev server
that is already running on 9000), opens `render.html?scene=<name>` in headless
Chromium (Playwright from `video/node_modules`). That page builds Motion
Canvas' own `Renderer` for just that one scene - no editor UI clicks, so it is
reliable unattended. When the renderer reports done, the mp4 is checked with
ffprobe and the server is stopped. Output: `video/mc/output/<name>.mp4`.

Two exporters:

- `images` (default): Motion Canvas' image-sequence exporter writes JPEG q98
  frames to `output/<name>/`, then the system ffmpeg encodes them
  (x264, CRF 16, yuv420p, +faststart) and the frames are deleted. Browser PNG
  encoding of a busy 1080p frame costs ~190 ms vs ~20 ms for JPEG, so this is
  about 2x faster; `--png` forces PNG frames, `--crf N` changes quality.
- `ffmpeg`: the official `@motion-canvas/ffmpeg` exporter (bundled ffmpeg,
  default CRF 23, softer). Same scene, slower (one server round trip per frame).

Speed on this PC: ~0.3 s per frame, i.e. the 14 s `prefsRecord` takes ~2.5 min
at 30 fps (~4 min at 60 fps). Most of that is canvas drawing in software
(shadows, gradients); fewer `shadowBlur` effects = faster.

## Preview / edit interactively

```
cd video/mc
npm run serve          # http://localhost:9000  (editor with timeline)
```

The editor's own Render button also works (Video Settings tab, exporter
"FFmpeg"); it renders the whole project into `output/project.mp4`.

## Add a scene

1. Create `src/scenes/myScene.tsx`:

   ```tsx
   import {makeScene2D, Txt} from '@motion-canvas/2d';
   import {createRef} from '@motion-canvas/core';
   import {addBackdrop, drift} from '../lib/backdrop';
   import {Headline} from '../lib/kinetic';
   import {C, FONT} from '../style';

   export default makeScene2D(function* (view) {
     const grid = addBackdrop(view);
     yield drift(grid);                  // background thread
     const h = new Headline('Hello *ESP32*');
     view.add(h.node());
     yield* h.in();
     // ...
   });
   ```

2. Register it in `src/project.ts`:

   ```ts
   import myScene from './scenes/myScene?scene';
   export default makeProject({scenes: [prefsRecord, myScene]});
   ```

3. `node video/mc/render.mjs myScene --frames` and look at the PNGs.

## Style rules

- Every colour / font / timing comes from `src/style.ts` (`C`, `FONT`, `CODE`, `T`).
  Brand: navy `#0b1220`, amber `#ffb547`, teal `#2dd4bf`, text `#e9edf2`;
  UI font Segoe UI, code font Consolas (system fonts, nothing downloaded).
- Keep everything above `SAFE_BOTTOM` (y = 410, the lower 12% is for subtitles).
  Headlines sit at y = -440.
- At most 1-2 lines of code on screen. Use `code().code('new line', 0.6)` to
  morph between lines and `code().selection(code().findFirstRange('x'), 0.3)`
  to point at a token (reset with `DEFAULT`).
- Something should move at all times, but every beat needs ~0.5 s of hold so
  it can be read.
- Coordinates: the view's origin is the canvas centre. `absolutePosition()` and
  `localToWorld()` are in canvas pixels (top-left origin) - convert with
  `p.transformAsPoint(view.worldToLocal())` before using them as a view-child
  position (see `toView` in `scenes/prefsRecord.tsx`).

## Ep10 scenes and narration timing

Ep10 ("Reflex Game 2.0") scenes: `i2c_chat`, `code_screen`, `buffer`,
`code_show`, `steps`, `code_tone`, `prefs_ram`, `prefs_drawer`, `prefs_put`,
`prefs_get`, `mistake` (one per `mc:<id>` run in `video/ep10/script.json`).

```
node video/mc/tools/ep10_timing.mjs     # rerun after every narration change
```

reads `video/ep10/build/schedule.json` (falls back to a 2.45 words/s
estimate if it does not exist yet) and writes `src/timing/ep10.json`:
`{scene: {total, estimated, segments: [{id, start, dur, words}]}}`. A scene
lasts from its first segment's start to the next segment's start (same rule
as the Blender shots). Scenes use `lib/ep10.tsx`: `timing(id)` (segment
starts + spoken-word times), `until(t)` to place beats on words, and
`exact(T.total, ...)` so the rendered length always equals `total`.
Re-render the scenes after rerunning the timing script.

## Notes

- Do not put JSX fragments (`<>...</>`) inside `.map()` children: they are
  silently not rendered. Use `.flatMap(x => [<A/>, <B/>])` instead.

- The FFmpeg exporter uses the ffmpeg binary bundled in
  `node_modules/@ffmpeg-installer` (libx264, yuv420p, +faststart).
- Code highlighting uses `lib/arduinoHighlighter.ts` instead of `@lezer/cpp`
  (not installed). Add keywords/types there if a snippet needs them.
