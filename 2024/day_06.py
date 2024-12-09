"""
given a grid, with cells marked with
. - free cell 
x - visited cell
# - obstacle
^ - starting point
Rules:
  -> keep traversing - till you
    - meet a obstacle - turn right and traverse
    - you leave the grid
Result -
  - return the number of unique cells visited
"""

import os
import sys

DATA_SOURCE = "./inputs/day_06_input.txt"

def read_raw_input():
    with open(DATA_SOURCE, "r") as rfile:
        raw_data = rfile.read()
    return raw_data

def parse_input(raw_input):
    """
    .......
    ........
    .......
    ..^.....
    """
    parsed_input = {}
    starting_pos = None
    grid = []
    for line in raw_input.splitlines():
        row = []
        for char in line:
            row.append(char)
            if char == '^':
                starting_pos = [len(grid) ,len(row)]
        grid.append(row)
    return dict(starting_pos=starting_pos, grid=grid)

def traverse_grid(starting_pos, grid) -> int:
    cells_visited = set([])
    """
    Up -> dx, dy ->  0, -1
    obstacle
    Up -> Right -> right ->   1, 0
    ......#
    .....X
    
    Right-> Down right -> 0, 1
    .....X
    .....#
    Down -> Right right -> 0,-1
    .....X
    ...X..
    .#X...
    Right->Up - right -> -1, 0
    """
    # direction change mapper
    DIRECTION_CHANGE_MAPPER = {
            # ....
            # ...#
            # ...X->X
            "UP": ("RIGHT", (0, 1)),
            # ....X #
            # ....X
            "RIGHT": ("DOWN", (1, 0)),
            # ..xXxX
            # ....#
            "DOWN": ("LEFT", (0, -1)),
            # ..X...
            # .#X...
            "LEFT": ("UP", (-1, 0))
    }
    row, col = starting_pos
    curr_direction = "UP"
    dx, dy = -1, 0
    OBSTACLE = "#"
    row_count = len(grid)
    col_count = len(grid[0])
    while True:
        nrow, ncol = row+dx, col+dy
        if within_bounds(nrow, ncol, row_count, col_count):
            if grid[nrow][ncol] == OBSTACLE:
                curr_direction, (dx,dy) = DIRECTION_CHANGE_MAPPER[curr_direction]
                continue
            else:
                cells_visited.add( (nrow, ncol) )
                row, col = nrow, ncol
        else:
            break
    return len(cells_visited)

def within_bounds(row, col, row_count, col_count):
    if 0<=row<row_count and 0<=col<col_count:
        return True
    return False



if __name__ == "__main__":
    raw_data = read_raw_input()
    parsed_data = parse_input(raw_data)
    cell_visited_count = traverse_grid(starting_pos=parsed_data['starting_pos'],
                                       grid=parsed_data['grid'])
    print(f"The visisted cell count is :: {cell_visited_count}")
