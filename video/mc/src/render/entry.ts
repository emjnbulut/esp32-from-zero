/**
 * Headless render entry, loaded by render.html (driven by render.mjs).
 * Renders ONE scene of src/project.ts with the FFmpeg exporter, no editor UI.
 *
 *   /render.html?scene=prefsRecord&fps=60[&to=3][&exporter=images|ffmpeg]
 *
 * exporter=ffmpeg  -> @motion-canvas/ffmpeg writes output/<scene>.mp4 itself
 * exporter=images  -> JPEG (q98, or &format=png) sequence in output/<scene>/ (pipelined, ~2x faster);
 *                     render.mjs then encodes it with the system ffmpeg
 *
 * Progress is published on window.__mc for the Playwright driver.
 */
import {Renderer, RendererResult, Vector2} from '@motion-canvas/core';
import project from '../project?project';
import {C, H, W} from '../style';

interface Status {
  state: 'loading' | 'rendering' | 'done' | 'failed';
  frame: number;
  total: number;
  error: string | null;
  logs: string[];
}

const status: Status = {state: 'loading', frame: 0, total: 0, error: null, logs: []};
(window as any).__mc = status;
const pre = document.getElementById('status')!;
const show = () =>
  (pre.textContent = `${status.state} frame ${status.frame}${status.error ? '\n' + status.error : ''}`);

project.logger.onLogged.subscribe(log => {
  const line = `[${log.level}] ${log.message}${log.stack ? '\n' + log.stack : ''}`;
  status.logs.push(line);
  if (log.level === 'error') status.error = line;
});

async function main() {
  const params = new URLSearchParams(location.search);
  const sceneName = params.get('scene');
  const fps = Number(params.get('fps') ?? 60);
  const scale = Number(params.get('scale') ?? 1);
  const to = params.has('to') ? Number(params.get('to')) : Infinity;

  const scenes = sceneName
    ? project.scenes.filter(s => s.name === sceneName)
    : project.scenes;
  if (scenes.length === 0) {
    throw new Error(
      `Scene "${sceneName}" not found. Available: ${project.scenes.map(s => s.name).join(', ')}`,
    );
  }

  const renderer = new Renderer({...project, scenes});
  renderer.onFrameChanged.subscribe(f => {
    status.frame = f;
    show();
  });
  const finished = new Promise<RendererResult>(resolve =>
    renderer.onFinished.subscribe(resolve),
  );

  status.state = 'rendering';
  show();
  await renderer.render({
    ...project.meta.getFullRenderingSettings(),
    name: sceneName ?? project.name,
    fps,
    resolutionScale: scale,
    size: new Vector2(W, H),
    range: [0, to],
    background: C.bg,
    colorSpace: 'srgb',
    exporter:
      params.get('exporter') === 'ffmpeg'
        ? {
            name: '@motion-canvas/ffmpeg',
            options: {fastStart: true, includeAudio: false},
          }
        : {
            name: '@motion-canvas/core/image-sequence',
            options: {
              // JPEG q98 encodes ~10x faster than PNG in the browser and is
              // visually lossless next to the final yuv420p x264 encode
              fileType: params.get('format') === 'png' ? 'image/png' : 'image/jpeg',
              quality: 98,
              groupByScene: false,
            },
          },
  });
  const result = await finished;
  status.state = result === RendererResult.Success ? 'done' : 'failed';
  if (result !== RendererResult.Success && !status.error) {
    status.error = `Renderer finished with result ${RendererResult[result]}`;
  }
  show();
}

main().catch(e => {
  status.state = 'failed';
  status.error = String(e?.stack ?? e);
  show();
});
