/**
 * Pin by Pin Lab - shared look for every Motion Canvas scene.
 * Change colours / fonts / safe areas here, never inside a scene.
 */
export const C = {
  bg: '#0b1220', // deep navy background
  bg2: '#111b2e', // raised panels
  panel: '#15223a',
  line: '#22324f', // grid / hairlines
  text: '#e9edf2',
  dim: '#8a97ab',
  amber: '#ffb547', // primary accent
  teal: '#2dd4bf', // secondary accent
  red: '#ff5d6c',
  oledOn: '#f4f8ff',
  oledBlack: '#020407',
  pcb: '#1d3b8a', // OLED breakout board blue
  metal: '#c9d1dc',
} as const;

export const FONT = {
  ui: 'Segoe UI',
  code: 'Consolas',
  pixel: 'Consolas', // OLED text (pixel grid overlay gives the LCD look)
} as const;

/** 1920x1080 canvas, origin in the centre. */
export const W = 1920;
export const H = 1080;

/**
 * Lower ~12% is reserved for burned-in / YouTube subtitles.
 * Keep every element's bottom edge above SAFE_BOTTOM.
 */
export const SAFE_BOTTOM = H / 2 - Math.round(H * 0.12); // y = 410
export const SAFE_TOP = -H / 2 + 60; // y = -480

/** Code token colours (used by the tiny Arduino/C++ highlighter). */
export const CODE = {
  text: '#e9edf2',
  keyword: '#c792ea',
  type: '#82aaff',
  func: '#2dd4bf',
  string: '#ffb547',
  number: '#f78c6c',
  comment: '#6b7a90',
  punct: '#8a97ab',
} as const;

/** Standard timings (seconds). Fast tempo: nothing should crawl. */
export const T = {
  fast: 0.25,
  base: 0.45,
  slow: 0.8,
} as const;
