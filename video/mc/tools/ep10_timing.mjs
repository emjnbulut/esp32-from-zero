#!/usr/bin/env node
/**
 * Kept for the old command: node video/mc/tools/ep10_timing.mjs
 * Same as: node video/mc/tools/timing.mjs ep10   (see timing.mjs)
 */
process.argv[2] = 'ep10';
await import('./timing.mjs');
