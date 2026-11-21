import type {CodeHighlighter, HighlightResult} from '@motion-canvas/2d';
import {CODE} from '../style';

/**
 * A tiny regex highlighter for Arduino C++ snippets. Avoids pulling in
 * @lezer/cpp - good enough for the 1-3 lines we ever show on screen.
 */
interface Span {
  from: number;
  to: number;
  color: string;
}

const KEYWORDS = new Set([
  'if', 'else', 'for', 'while', 'return', 'void', 'const', 'static', 'true',
  'false', 'auto', 'break', 'continue', 'switch', 'case', 'new',
]);
const TYPES = new Set([
  'int', 'long', 'unsigned', 'bool', 'char', 'float', 'double', 'uint8_t',
  'uint16_t', 'uint32_t', 'String', 'Preferences', 'byte',
]);

const TOKEN = /\/\/[^\n]*|"(?:[^"\\n]|\.)*"|\b\d+(?:\.\d+)?\b|[A-Za-z_]\w*|\s+|./g;

function color(token: string, next: string): string | null {
  if (token.startsWith('//')) return CODE.comment;
  if (token.startsWith('"')) return CODE.string;
  if (/^\d/.test(token)) return CODE.number;
  if (/^[A-Za-z_]/.test(token)) {
    if (KEYWORDS.has(token)) return CODE.keyword;
    if (TYPES.has(token)) return CODE.type;
    if (next === '(') return CODE.func;
    return null;
  }
  if (/^\s+$/.test(token)) return null;
  return CODE.punct;
}

export class ArduinoHighlighter implements CodeHighlighter<Span[]> {
  initialize(): boolean {
    return true;
  }

  prepare(code: string): Span[] {
    const spans: Span[] = [];
    const tokens = [...code.matchAll(TOKEN)];
    tokens.forEach((m, i) => {
      const t = m[0];
      const next = tokens[i + 1]?.[0] ?? '';
      const c = color(t, next);
      if (c) spans.push({from: m.index!, to: m.index! + t.length, color: c});
    });
    return spans;
  }

  highlight(index: number, cache: Span[]): HighlightResult {
    if (!cache) return {color: null, skipAhead: 0};
    for (const s of cache) {
      if (index >= s.from && index < s.to) {
        return {color: s.color, skipAhead: s.to - index};
      }
      if (s.from > index) break;
    }
    return {color: null, skipAhead: 0};
  }

  tokenize(code: string): string[] {
    return [...code.matchAll(TOKEN)].map(m => m[0]);
  }
}

export const arduino = new ArduinoHighlighter();
