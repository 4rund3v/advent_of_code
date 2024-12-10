"""
Day - 10 : Hoof It
Inference:
- you determine that a good hiking trail is as long as possible and has an even, gradual, uphill slop
- hiking trail is any path that starts at height 0, ends at height 9, and always increases by a height of exactly 1 at each step.
- trailhead's score is the number of 9-height positions reachable from that trailhead via a hiking trail

"""
from collections import defaultdict
import pprint
DATA_SOURCE = "./inputs/day_10_input.txt"
def get_input():
    with open(DATA_SOURCE, 'r') as rfile:
        data = rfile.read()
    return data

def parse_input(raw_input):
    return [ list(map(int, line.strip())) for line in raw_input.splitlines() if line ]

def get_trails(grid):
    ROW_COUNT = len(grid)
    COL_COUNT = len(grid[0])
    trail_heads = [ (row,col) for row in range(ROW_COUNT) for col in range(COL_COUNT)  if grid[row][col] == 0 ]
    DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    trails = []
    is_valid = lambda nrow, ncol, curr_cell_value, visited: 0<=nrow<ROW_COUNT and 0<=ncol<COL_COUNT and grid[nrow][ncol]-curr_cell_value==1 and (nrow, ncol) not in visited
    def dfs(row, col, path, visited, peaks):
        if grid[row][col] == 9:
            trails.append(path[:])
            if (row, col) not in peaks:
                peaks.add( (row, col) )
            return peaks
        curr_cell_value = grid[row][col]
        for dx, dy in DIRECTIONS:
            nrow, ncol = row+dx, col+dy
            if is_valid(nrow, ncol, curr_cell_value, visited):
                dfs(nrow, ncol, path+[(nrow, ncol)], {(nrow, ncol)} | visited, peaks)
        return peaks
    trail_peaks = []
    for trail_head in trail_heads:
        peaks_visited = dfs(row=trail_head[0], col=trail_head[1], path=[trail_head], visited=set([trail_head]), peaks=set())
        trail_peaks.append(peaks_visited)
    return trails, trail_peaks

if __name__ == "__main__":
    raw_input = get_input()
    grid = parse_input(raw_input)
    print(f"The shape of the grid is :: {len(grid)}x{len(grid[0])} ")
    trails, peaks = get_trails(grid)
    pprint.pprint(f"Peaks are ::{sum([len(peak) for peak in peaks])}")
    pprint.pprint(f"Trails are ::{len(trails)}")