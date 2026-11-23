import {makeProject} from '@motion-canvas/core';

import prefsRecord from './scenes/prefsRecord?scene';
// Ep10 "Reflex Game 2.0" (timing: src/timing/ep10.json <- tools/ep10_timing.mjs)
import i2c_chat from './scenes/i2c_chat?scene';
import code_screen from './scenes/code_screen?scene';
import buffer from './scenes/buffer?scene';
import code_show from './scenes/code_show?scene';
import steps from './scenes/steps?scene';
import code_tone from './scenes/code_tone?scene';
import prefs_ram from './scenes/prefs_ram?scene';
import prefs_drawer from './scenes/prefs_drawer?scene';
import prefs_put from './scenes/prefs_put?scene';
import prefs_get from './scenes/prefs_get?scene';
import mistake from './scenes/mistake?scene';
import code_full from './scenes/code_full?scene';

/**
 * All scenes of the course live in this one project so the editor
 * (npm run serve -> http://localhost:9000) can preview any of them.
 * render.mjs renders one scene at a time by name.
 */
export default makeProject({
  scenes: [
    prefsRecord,
    i2c_chat,
    code_screen,
    buffer,
    code_show,
    steps,
    code_tone,
    prefs_ram,
    prefs_drawer,
    prefs_put,
    prefs_get,
    mistake,
    code_full,
  ],
});
