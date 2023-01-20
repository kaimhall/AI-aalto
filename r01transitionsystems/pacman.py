#!/usr/bin/python3


from sre_parse import State
import time
import queue
from typing_extensions import Self

# Creating a grid for the Pac-Man to wander around.
# The grid is given as a list of string, e.g.

# [
#   "......",
#   ".XX.XX",
#   "......"
# ]

# Here the important information is the size of the grid,
# in Y direction the number of string, and in the X direction
# the length of the strings, and whether there is X in
# a grid cell. Pac-Man can enter any cell that is not a wall
# cell marked with X.
# The bottom left cell is (0,0). Cells outside the explicitly
# stated grid are all wall cells.


class PacManGrid:
    def __init__(self, grid):
        self.grid = grid
        self.xmax = len(grid[0]) - 1
        self.ymax = len(grid) - 1

    # Test whether the cell (x,y) is wall.
    def occupied(self, x, y):
        if x < 0 or y < 0 or x > self.xmax or y > self.ymax:
            return True
        s = self.grid[self.ymax - y]
        return s[x] == "X"


class PacManState:

    # Creating a state:
    def __init__(self, x, y, direction, grid):
        self.x = x
        self.y = y
        self.d = direction
        self.grid = grid

    # Construct a string representing a state.
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + self.d + ")"

    # The hash function for states, mapping each state to an integer
    def __hash__(self):
        return self.x + (self.grid.xmax + 1) * self.y

    # Equality for states
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.d == other.d)

    def moveNorth(self, x, y):
        grid = self.grid
        states = []
        if not grid.occupied(x, y + 1):
            state = PacManState(x, y + 1, "N", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if not grid.occupied(x + 1, y):
            state = PacManState(x + 1, y, "E", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if not grid.occupied(x - 1, y):
            state = PacManState(x + 1, y, "W", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if len(states) == 0:
            state = PacManState(x, y - 1, "S", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        return hash, state

    def moveSouth(self, x, y):
        grid = self.grid
        states = []
        if not grid.occupied(x, y - 1):
            state = PacManState(x, y - 1, "S", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if not grid.occupied(x - 1, y):
            state = PacManState(x - 1, y, "W", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if not grid.occupied(x + 1, y):
            state = PacManState(x + 1, y, "E", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if len(states) == 0:
            state = PacManState(x, y + 1, "N", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        return hash, state

    def moveEast(self, x, y):
        grid = self.grid
        states = []
        if not grid.occupied(x + 1, y):
            state = PacManState(x + 1, y, "E", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if not grid.occupied(x, y + 1):
            state = PacManState(x, y + 1, "N", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if not grid.occupied(x, y - 1):
            state = PacManState(x, y - 1, "S", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if len(states) == 0:
            state = PacManState(x - 1, y, "W", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        return hash, state

    def moveWest(self, x, y):
        grid = self.grid
        states = []
        if not grid.occupied(x - 1, y):
            state = PacManState(x - 1, y, "W", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if not grid.occupied(x, y + 1):
            state = PacManState(x, y + 1, "N", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if not grid.occupied(x, y - 1):
            state = PacManState(x, y - 1, "S", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        if len(states) == 0:
            state = PacManState(x + 1, y, "E", self.grid)
            hash = state.__hash__()
            states.append((hash, state))
        return hash, state

    # All possible successor states of a state
    def successors(self):
        grid = self.grid
        successor_states = []  # state hash name and state
        for y in range(grid.ymax):
            for x in range(grid.xmax):

                n = self.moveNorth(x, y)
                successor_states.append(n)

                s = self.moveSouth(x, y)
                successor_states.append(s)

                e = self.moveEast(x, y)
                successor_states.append(s)

                w = self.moveWest(x, y)
                successor_states.append(s)

        return successor_states


if __name__ == "__main__":
    grid = PacManGrid(["......", ".XX.XX", "......"])
    s = PacManState(0, 0, "N", grid)
    print(s.successors())


# State space search problems are represented in terms of states.
# For each state there are a number of actions that are applicable in
# that state. Any of the applicable actions will produce a successor
# state for the state.
#
# To use a state space in search algorithms, we
# also need functions for producing a hash value for a state
# (the function hash) and for testing equality of two states.

# In this exercise we represent states as Python classes with the
# following components.
#
#   __init__    To create a state (a starting state for search)
#   __repr__    To construct a string that represents the state
#   __hash__    Hash function for states
#   __eq__      Equality for states
#   successors  Returns a list [(a1,s1),...,(aN,sN)] where each si
#               is the successor state when action ai is taken.
#               Here the name ai of an action is a string.

# The state of the Pac-Man (given a grid) consists of
# three components:
#   x: the X coordinate 0..self.grid.xmax
#   y: the Y coordinate 0..self.grid.ymax
#   d: the direction "N", "S", "E", "W" Pac-Man is going

# Based on this information, the possible successor states
# of (x,y,d) are computed by 'successors'.

# Implement successors function (mine is 67 lines, w/ 4 aux functions)
# You can come up with your own names for the different moves
