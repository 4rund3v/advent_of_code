"""
Day - 08 : Resonant collinearity
"""
from collections import defaultdict

DATA_SOURCE = "./inputs/day_08_input.txt"
def get_input():
    with open(DATA_SOURCE, 'r') as rfile:
        data = rfile.read()
    return data

def parse_input(raw_input):
    grid = [list(line) for line in raw_input.splitlines()]
    return grid

def get_frequency_positions(grid):
    frequency_positions = defaultdict(list) # frequency:list(tuple)
    for r_idx, row in enumerate(grid):
        for c_idx, cell in enumerate(row):
            if cell == ".":
                continue
            frequency_positions[cell].append( (r_idx, c_idx) )
    return frequency_positions

def get_antinodes(row_count, col_count, curr_node_pos, next_node_pos):
    antinodes = []
    next_node_antinode = (
            curr_node_pos[0] + curr_node_pos[0]-next_node_pos[0],
            curr_node_pos[1] + curr_node_pos[1]-next_node_pos[1]
            )
    if 0<=next_node_antinode[0]<row_count and 0<=next_node_antinode[1]<col_count:
        antinodes.append(next_node_antinode)

    curr_node_antinode = (
            next_node_pos[0] + next_node_pos[0]-curr_node_pos[0],
            next_node_pos[1] + next_node_pos[1]-curr_node_pos[1]
            )
    if 0<=curr_node_antinode[0]<row_count and 0<=curr_node_antinode[1]<col_count:
        antinodes.append(curr_node_antinode)
    return antinodes


def get_resonant_antinodes(row_count, col_count, curr_node_pos, next_node_pos):
    antinodes = [curr_node_pos, next_node_pos]
    curr_node, next_node = curr_node_pos, next_node_pos
    while True:
        next_node_antinode = (
                curr_node[0] + curr_node[0]-next_node[0],
                curr_node[1] + curr_node[1]-next_node[1]
                )
        if 0<=next_node_antinode[0]<row_count and 0<=next_node_antinode[1]<col_count:
            antinodes.append(next_node_antinode)
            curr_node, next_node = next_node_antinode, curr_node
        else:
            break
    curr_node, next_node = curr_node_pos, next_node_pos
    while True:
        curr_node_antinode = (
                next_node[0] + next_node[0]-curr_node[0],
                next_node[1] + next_node[1]-curr_node[1]
                )
        if 0<=curr_node_antinode[0]<row_count and 0<=curr_node_antinode[1]<col_count:
            antinodes.append(curr_node_antinode)
            curr_node, next_node = next_node, curr_node_antinode
        else:
            break
    return antinodes

def get_antinode_positions(frequency_positions, grid, resonant=False):
    row_count = len(grid)
    col_count = len(grid[0])
    # contains the position of an anitnode
    # (r_idx, c_idx )
    antinode_positions = set()
    for frequency in frequency_positions:
        frequencies = sorted(frequency_positions[frequency])
        if len(frequencies) == 1:
            continue
        for node_idx in range(len(frequencies)):
            curr_node_pos = frequencies[node_idx]
            for next_node_idx in range(node_idx+1, len(frequencies)):
                next_node_pos = frequencies[next_node_idx]
                if resonant:
                    antinodes = get_resonant_antinodes(row_count, col_count, curr_node_pos, next_node_pos)
                else:
                    antinodes = get_antinodes(row_count, col_count, curr_node_pos, next_node_pos)
                antinode_positions.update(antinodes)
    return antinode_positions


if __name__ == "__main__":
    """
     The shape of the grid is :: 50x50 
     Number of unique frequency positions are :: 38
     The number of antinodes are :: 247
     The number of resonant antinodes are :: 861
    """
    raw_input = get_input()
    grid = parse_input(raw_input)
    print(f"The shape of the grid is :: {len(grid)}x{len(grid[0])} ")
    frequency_positions = get_frequency_positions(grid)
    print(f"Number of unique frequency positions are :: {len(frequency_positions)}")
    antinodes = get_antinode_positions( frequency_positions, grid )
    print(f" The number of antinodes are :: {len(antinodes)}")
    resonant_antinodes = get_antinode_positions( frequency_positions, grid, resonant=True)
    print(f" The number of resonant antinodes are :: {len(resonant_antinodes)}")
   
