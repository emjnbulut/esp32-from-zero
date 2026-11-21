import {makeProject} from '@motion-canvas/core';

import prefsRecord from './scenes/prefsRecord?scene';

/**
 * All scenes of the course live in this one project so the editor
 * (npm run serve -> http://localhost:9000) can preview any of them.
 * render.mjs renders one scene at a time by name.
 */
export default makeProject({
  scenes: [prefsRecord],
});
