import {makeProject} from '@motion-canvas/core';

import prefsRecord from './scenes/prefsRecord?scene';
// Ep10 "Reflex Game 2.0" (timing: src/timing/ep10.json <- node video/mc/tools/timing.mjs ep10)
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
// Ep11 "Motion Alarm" (timing: src/timing/ep11.json <- node video/mc/tools/timing.mjs ep11)
import ep11_code_read from './scenes/ep11_code_read?scene';
import ep11_alarm_steps from './scenes/ep11_alarm_steps?scene';
import ep11_code_siren from './scenes/ep11_code_siren?scene';
import ep11_parking_ticket from './scenes/ep11_parking_ticket?scene';
import ep11_code_last from './scenes/ep11_code_last?scene';
import ep11_ago_calc from './scenes/ep11_ago_calc?scene';
import ep11_code_full from './scenes/ep11_code_full?scene';
// Ep12 "Phone remote" (timing: src/timing/ep12.json <- node video/mc/tools/timing.mjs ep12)
import ep12_code_softap from './scenes/ep12_code_softap?scene';
import ep12_page_menu from './scenes/ep12_page_menu?scene';
import ep12_page_links from './scenes/ep12_page_links?scene';
import ep12_code_on from './scenes/ep12_code_on?scene';
import ep12_code_loop from './scenes/ep12_code_loop?scene';
import ep12_order_slip from './scenes/ep12_order_slip?scene';
import ep12_code_arg from './scenes/ep12_code_arg?scene';
import ep12_code_answer from './scenes/ep12_code_answer?scene';
import ep12_page_template from './scenes/ep12_page_template?scene';
import ep12_code_full from './scenes/ep12_code_full?scene';
// Ep14 "Fruit piano" DRAFT (timing: src/timing/ep14.json <- node video/mc/tools/timing.mjs ep14)
import ep14_bucket from './scenes/ep14_bucket?scene';
import ep14_bucket_finger from './scenes/ep14_bucket_finger?scene';
import ep14_code_touch from './scenes/ep14_code_touch?scene';
import ep14_calibrate from './scenes/ep14_calibrate?scene';
import ep14_array_boxes from './scenes/ep14_array_boxes?scene';
import ep14_code_array from './scenes/ep14_code_array?scene';
import ep14_code_loop_keys from './scenes/ep14_code_loop_keys?scene';
import ep14_song_boxes from './scenes/ep14_song_boxes?scene';
import ep14_code_full from './scenes/ep14_code_full?scene';
// Ep15 "Drawer spy" DRAFT (timing: src/timing/ep15.json <- node video/mc/tools/timing.mjs ep15)
import ep15_light_number from './scenes/ep15_light_number?scene';
import ep15_code_read from './scenes/ep15_code_read?scene';
import ep15_one_line from './scenes/ep15_one_line?scene';
import ep15_thermostat from './scenes/ep15_thermostat?scene';
import ep15_two_lines from './scenes/ep15_two_lines?scene';
import ep15_code_hyst from './scenes/ep15_code_hyst?scene';
import ep15_code_counter from './scenes/ep15_code_counter?scene';
import ep15_code_full from './scenes/ep15_code_full?scene';

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
    ep11_code_read,
    ep11_alarm_steps,
    ep11_code_siren,
    ep11_parking_ticket,
    ep11_code_last,
    ep11_ago_calc,
    ep11_code_full,
    ep12_code_softap,
    ep12_page_menu,
    ep12_page_links,
    ep12_code_on,
    ep12_code_loop,
    ep12_order_slip,
    ep12_code_arg,
    ep12_code_answer,
    ep12_page_template,
    ep12_code_full,
    ep14_bucket,
    ep14_bucket_finger,
    ep14_code_touch,
    ep14_calibrate,
    ep14_array_boxes,
    ep14_code_array,
    ep14_code_loop_keys,
    ep14_song_boxes,
    ep14_code_full,
    ep15_light_number,
    ep15_code_read,
    ep15_one_line,
    ep15_thermostat,
    ep15_two_lines,
    ep15_code_hyst,
    ep15_code_counter,
    ep15_code_full,
  ],
});
