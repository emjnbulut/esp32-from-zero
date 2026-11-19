/* Mini project 1 circuit (episodes 8-10), the creator's real desk layout. Every connection is listed in
 * ep09/3d/scene.js. buildP1(K, hot) -> { L, R, esp, red, yel, grn, btn, rgb, pot } */
import { COL } from "./kit.js";

export function buildP1(K, hot = ["D23", "D22", "D18", "TX2", "D25", "D26", "D34", "GND", "3V3"]) {
  const L = K.breadboard(-28, { zc: -35.56 }), R = K.breadboard(28, { zc: -35.56 });
  const esp = K.esp32({ xl: L.hole(18, "j")[0], xr: R.hole(18, "a")[0], z0: R.zOf(18), hot });

  const red = K.led(R.hole(21, "h"), R.hole(22, "h"), "red");
  K.resistor(R.hole(18, "d"), R.hole(21, "g"));
  K.wire(R.hole(22, "j"), R.rail(22, "r", "-"), COL.wireBlack);

  K.wire(R.hole(17, "c"), R.hole(26, "c"), COL.wireYellow);
  const btn = K.button([R.hole(26, "e"), R.hole(28, "e"), R.hole(26, "f"), R.hole(28, "f")]);
  K.wire(R.hole(28, "j"), R.rail(28, "r", "-"), COL.wireBlack);

  const yel = K.led(R.hole(14, "h"), R.hole(15, "h"), "yellow");
  K.resistor(R.hole(12, "d"), R.hole(14, "g"));
  K.wire(R.hole(15, "j"), R.rail(15, "r", "-"), COL.wireBlack);

  const grn = K.led(R.hole(8, "h"), R.hole(7, "h"), "green");
  K.resistor(R.hole(10, "d"), R.hole(8, "g"));
  K.wire(R.hole(7, "j"), R.rail(7, "r", "-"), COL.wireBlack);

  K.wire(R.hole(5, "e"), R.rail(5, "r", "-"), COL.wireBlack, { h: 4 });
  { // 3V3 -> left (+) rail, routed around the USB end of the board
    const a = R.hole(4, "e"), b = L.rail(3, "l", "+"), zOut = esp.zU + 22; // passes under the USB cable
    K.wire(a, b, COL.wireRed, { h: 2.6, via: [[a[0] + 1, a[2] + 4], [a[0] - 6, zOut], [b[0] + 30, zOut], [b[0] + 4, b[2] + 3]] });
  }

  const rgb = K.rgbLed([L.hole(24, "c"), L.hole(25, "c"), L.hole(26, "c"), L.hole(27, "c")]);
  for (const n of [24, 26, 27]) K.resistor(L.hole(n, "f"), L.hole(n, "e"));
  K.wire(L.hole(25, "a"), L.rail(25, "l", "-"), COL.wireBlack);
  K.wire(L.hole(11, "i"), L.hole(24, "g"), COL.wireRed, { h: 7 });
  K.wire(L.hole(10, "i"), L.hole(26, "h"), COL.wireGreen, { h: 8 });
  K.wire(L.hole(9, "i"), L.hole(27, "i"), COL.wireBlue, { h: 9 });

  const pot = K.pot([L.hole(8, "c"), L.hole(10, "c"), L.hole(12, "c")], 0.6);
  K.wire(L.hole(8, "a"), L.rail(8, "l", "-"), COL.wireBlack);
  K.wire(L.hole(12, "a"), L.rail(13, "l", "+"), COL.wireRed);
  K.wire(L.hole(10, "d"), L.hole(15, "h"), COL.wireOrange, { h: 10 });
  K.wire(L.hole(5, "g"), L.rail(5, "l", "-"), COL.wireBlack, { h: 11 });
  return { L, R, esp, red, yel, grn, btn, rgb, pot };
}
