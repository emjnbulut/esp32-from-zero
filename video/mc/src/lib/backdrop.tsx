import {Gradient, Line, Node, Rect, View2D} from '@motion-canvas/2d';
import {createRef, linear, Reference} from '@motion-canvas/core';
import {C, H, W} from '../style';

/**
 * Navy background + slowly drifting grid + vignette.
 * Call once at the top of a scene; returns the grid ref so the scene can
 * start its drift: `yield drift(grid)` (runs in the background).
 */
export function addBackdrop(view: View2D): Reference<Node> {
  const grid = createRef<Node>();
  const step = 80;
  const lines = [];
  for (let x = -W / 2 - step; x <= W / 2 + step; x += step) {
    lines.push(
      <Line
        points={[
          [x, -H / 2 - step],
          [x, H / 2 + step],
        ]}
        stroke={C.line}
        lineWidth={1}
      />,
    );
  }
  for (let y = -H / 2 - step; y <= H / 2 + step; y += step) {
    lines.push(
      <Line
        points={[
          [-W / 2 - step, y],
          [W / 2 + step, y],
        ]}
        stroke={C.line}
        lineWidth={1}
      />,
    );
  }

  view.fill(C.bg);
  view.add(
    <>
      <Node ref={grid} opacity={0.45}>
        {lines}
      </Node>
      {/* soft accent glows */}
      <Rect
        width={W}
        height={H}
        fill={
          new Gradient({
            type: 'radial',
            from: [-520, -260],
            to: [-520, -260],
            fromRadius: 0,
            toRadius: 700,
            stops: [
              {offset: 0, color: 'rgba(45,212,191,0.07)'},
              {offset: 1, color: 'rgba(45,212,191,0)'},
            ],
          })
        }
      />
      <Rect
        width={W}
        height={H}
        fill={
          new Gradient({
            type: 'radial',
            from: [560, 120],
            to: [560, 120],
            fromRadius: 0,
            toRadius: 760,
            stops: [
              {offset: 0, color: 'rgba(255,181,71,0.06)'},
              {offset: 1, color: 'rgba(255,181,71,0)'},
            ],
          })
        }
      />
      {/* vignette */}
      <Rect
        width={W}
        height={H}
        fill={
          new Gradient({
            type: 'radial',
            fromRadius: 300,
            toRadius: 1150,
            stops: [
              {offset: 0, color: 'rgba(3,6,12,0)'},
              {offset: 1, color: 'rgba(3,6,12,0.75)'},
            ],
          })
        }
      />
    </>,
  );
  return grid;
}

/** Background thread: grid drifts diagonally for `seconds`. */
export function drift(grid: Reference<Node>, seconds = 20) {
  return grid().position([80, 80], seconds, linear);
}
