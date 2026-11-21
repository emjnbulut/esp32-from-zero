import {defineConfig} from 'vite';
import motionCanvasPlugin from '@motion-canvas/vite-plugin';
import ffmpegPlugin from '@motion-canvas/ffmpeg';

// Both plugins are CommonJS modules with `exports.default`; depending on how
// the config gets bundled the default import may be the module object.
const unwrap = <T>(m: any): T => (typeof m === 'function' ? m : m.default);
const motionCanvas = unwrap<typeof motionCanvasPlugin>(motionCanvasPlugin);
const ffmpeg = unwrap<typeof ffmpegPlugin>(ffmpegPlugin);

export default defineConfig({
  plugins: [
    motionCanvas({
      project: ['./src/project.ts'],
      output: './output',
    }),
    ffmpeg(),
  ],
});
