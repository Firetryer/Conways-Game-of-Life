# Conways Game Of Life
A simple project I made long ago, using Python 2.7, but converted to 3.x using 2to3.
So it should work on both.

**What is conways game of life?** According to the Wiki:

>> The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970.

>>The "game" is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves, or, for advanced "players", by creating patterns with particular properties.

**Each cell in the map follows 4 rules**:

>>Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

The map isn't infinite, theres a limited area where the cells are confined to.

## Requirements

Python3

Pygame

To Run:

python3 CGOL.py


## Controls

Esc        - To Exit

  q        - Zoom in

  e        - Zoom out

Arrow Keys - Pan Camera

Equals     - Increase Speed

Minus      - Decrease Speed

Left Click - Kill or Revive a Cell


