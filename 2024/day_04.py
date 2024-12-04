
from typing import List
import os
import sys

RAW_DATA  = "./inputs/day_04_input.txt"
VALID_CHARS = set(["X", "M", "A", "S"])
def read_raw_data():
    with open(RAW_DATA, "r") as f:
        data = f.read()
    return data

def get_word_matrix(raw_data) -> List[List[str]]:
    word_matrix = []
    for line in raw_data.splitlines():
        word_matrix.append(list(line))
        continue
        char_line = []
        for char in line:
            if char in VALID_CHARS:
                char_line.append(char)
            else:
                char_line.append(".")
        word_matrix.append(char_line[:])
    return word_matrix

def get_positions_of_char(word_matrix, char):
    char_positions = []
    ROWS = len(word_matrix)
    COLS = len(word_matrix[0])
    for row in range(ROWS):
        for col in range(COLS):
            cell = word_matrix[row][col]
            if cell == char:
                char_positions.append( (row, col) )
    return char_positions


def get_matching_word_counts(word_matrix):
    starting_positions = get_positions_of_char(word_matrix, "X")
    word_count = 0
    DIRECTIONS = [
            (0,1), (1,0), (0,-1), (-1,0),
            (1,1), (1,-1), (-1,1), (-1,-1)
            ]
    ROWS = len(word_matrix)
    COLS = len(word_matrix[0])
    valid_paths = set()

    def dfs(row, col, pos, dx, dy) -> int:
        if pos==4:
            return 1

        nrow, ncol = row+dx, col+dy
        if 0<=nrow<ROWS and 0<=ncol<COLS and word_matrix[nrow][ncol] == "XMAS"[pos]:
            return dfs(nrow, ncol, pos+1, dx, dy )
        return 0 
    found = 0
    for starting_pos in starting_positions:
        visited = set([starting_pos])
        print(f" Starting from the position : {starting_pos} ")
        for dx,dy in DIRECTIONS:
            found += dfs(row=starting_pos[0], col=starting_pos[1], pos=1, dx=dx,dy=dy)
    return found

def get_diagonal_matching_counts(word_matrix):
    starting_positions = get_positions_of_char(word_matrix, "A")
    counts = 0
    ROWS = len(word_matrix)
    COLS = len(word_matrix[0])
    def check_if_valid_xmas(row, col):
        ltd = -1, -1
        rtd = 1, -1
        lbd =  -1, 1
        rbd = 1, 1
        # check top left positions are possible
        if ((0<=row+ltd[0]<ROWS and  0<=col+ltd[1]<COLS) and 
           (0<=row+rtd[0]<ROWS and  0<=col+rtd[1]<COLS) and 
           (0<=row+lbd[0]<ROWS and  0<=col+lbd[1]<COLS) and 
           (0<=row+rbd[0]<ROWS and  0<=col+rbd[1]<COLS)):
               left_top_diag = word_matrix[row+ltd[0]][col+ltd[1]]
               left_bot_diag = word_matrix[row+lbd[0]][col+lbd[1]]

               right_top_diag = word_matrix[row+rtd[0]][col+rtd[1]]
               right_bot_diag = word_matrix[row+rbd[0]][col+rbd[1]]

               if left_bot_diag == left_top_diag == 'M' and right_top_diag == right_bot_diag == 'S':
                   print(f"{left_top_diag} . {right_top_diag}")
                   print(f" .{word_matrix[row][col]}. ")
                   print(f"{left_bot_diag} . {right_bot_diag}")
                   return True
        return False    

    for row, col in starting_positions:
        if check_if_valid_xmas( row, col ):
            print(f"The matching xmas is found at :: {row, col}")
            counts += 1
    return counts


def get_diagonal_matching_counts(word_matrix):
   ROWS = len(word_matrix)
   COLS = len(word_matrix[0])
   count = 0

   def check_mas(r, c, dr, dc):
       # Check if MAS or SAM exists in given direction
       if not (0 <= r < ROWS and 0 <= c < COLS and 
               0 <= r+2*dr < ROWS and 0 <= c+2*dc < COLS):
           return False
           
       # Check MAS
       if (word_matrix[r][c] == 'M' and
           word_matrix[r+dr][c+dc] == 'A' and 
           word_matrix[r+2*dr][c+2*dc] == 'S'):
           return True
           
       # Check SAM
       if (word_matrix[r][c] == 'S' and
           word_matrix[r+dr][c+dc] == 'A' and
           word_matrix[r+2*dr][c+2*dc] == 'M'):
           return True
           
       return False

   def check_if_valid_xmas(row, col):
       if word_matrix[row][col] != 'A':
           return False
           
       # Check both possible X formations:
       # Formation 1: / and \ from top
       formation1 = (check_mas(row-1, col-1, 1, 1) and 
                    check_mas(row-1, col+1, 1, -1))
                    
       # Formation 2: \ and / from bottom
       formation2 = (check_mas(row+1, col+1, -1, -1) and
                    check_mas(row+1, col-1, -1, 1))
                    
       return formation1 or formation2

   for r in range(1, ROWS-1):
       for c in range(1, COLS-1):
           if check_if_valid_xmas(r, c):
               count += 1
               
   return count

if __name__ == "__main__":
    raw_data = read_raw_data()
    print(f"The raw data read is of {len(raw_data)}")
    word_matrix = get_word_matrix(raw_data)
    print(f"The word matrix size is :: {len(word_matrix)}, {len(word_matrix[0])}")
    matching_word_counts = get_matching_word_counts(word_matrix)
    print(f"The matching word counts are :: {matching_word_counts}")
    x_mas_counts = get_diagonal_matching_counts(word_matrix)
    print(f"The diagonal matching counts are :: {x_mas_counts}")
