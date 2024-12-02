import os
from typing import List, Tuple

"""
Find the number of safe levels
"""
DATA_SOURCE = "./inputs/day_02_input.txt"
MIN_THRESHOLD = 1
MAX_THRESHOLD = 3
TOLERANCE = 1

def read_extract_data():
    extracted_data = []
    with open(DATA_SOURCE, "r") as rfile:
        for line in rfile.readlines():
            line = line.strip()
            report = []
            for level in line.split(" "):
                if not level:
                    continue
                report.append(int(level))
            extracted_data.append( report )
    print(f" The extracted data contains : {len(extracted_data)}")
    return extracted_data

def get_safe_levels(report_data:List[List[int]]) -> int:
    safe_levels = 0
    # 0 for DECREASING
    # 1 for INCREASING
    DECREASING = 0
    INCREASING = 1
    for report in report_data:
        curr_order = INCREASING if report[0] < report[1] else DECREASING
        for idx in range(1, len(report)):
            if report[idx-1] < report[idx]:
                if curr_order != INCREASING:
                    break
            else:
                if curr_order != DECREASING:
                    break
            if not MIN_THRESHOLD <= abs(report[idx] - report[idx-1]) <= MAX_THRESHOLD:
                break
        else:
            safe_levels += 1
    print(f"The number of safe levels is :: {safe_levels}")
    return safe_levels

def is_valid_sequence(report: List[int], skip_idx: int = -1) -> Tuple[bool, int]:
    """
    Checks if a sequence is valid by skipping one optional index.
    Returns (is_valid, direction) where direction is INCREASING(1) or DECREASING(0)
    """
    if len(report) < 2:
        return True, 1
    
    DECREASING = 0
    INCREASING = 1
    
    # Find first valid pair to determine direction
    first_idx = 0
    second_idx = 1
    while second_idx < len(report):
        if first_idx != skip_idx and second_idx != skip_idx:
            curr_order = INCREASING if report[first_idx] < report[second_idx] else DECREASING
            break
        first_idx += 1
        second_idx += 1
    else:
        return True, 1  # If we can't find a valid pair, sequence is valid
    
    prev_valid_idx = first_idx
    
    # Check remaining elements
    for idx in range(first_idx + 1, len(report)):
        if idx == skip_idx:  # Skip the bad element
            continue
            
        if prev_valid_idx == skip_idx:  # If previous was skipped, update and continue
            prev_valid_idx = idx
            continue
            
        # Check direction
        if report[prev_valid_idx] < report[idx]:
            if curr_order != INCREASING:
                return False, curr_order
        elif report[prev_valid_idx] > report[idx]:
            if curr_order != DECREASING:
                return False, curr_order
        else:  # Equal values not allowed
            return False, curr_order
            
        # Check threshold
        if not MIN_THRESHOLD <= abs(report[idx] - report[prev_valid_idx]) <= MAX_THRESHOLD:
            return False, curr_order
            
        prev_valid_idx = idx
    
    return True, curr_order

def get_safe_levels(report_data: List[List[int]]) -> int:
    """
    Counts the number of safe reports in the data, allowing for one tolerance.
    A safe report maintains strictly increasing or decreasing order
    and has adjacent values differing by 1-3 units, with possibly one exception.
    """
    safe_levels = 0

    for report in report_data:
        if len(report) <= 2:  # Reports of length 1 or 2 are always safe
            safe_levels += 1
            continue
        
        # Try without skipping any element first
        is_safe, _ = is_valid_sequence(report)
        if is_safe:
            safe_levels += 1
            continue
        # If not safe, try skipping each element once
        for skip_idx in range(len(report)):
            is_safe, _ = is_valid_sequence(report[:skip_idx]+report[skip_idx+1:])
            if is_safe:
                safe_levels += 1
                break
    print(f"The number of safe levels is: {safe_levels}")
    return safe_levels

def get_safe_levels_with_tolerance(report_data: List[List[int]]):
    """
    so check if by removing one adjacent level the level is safe
    """
    safe_levels = 0
    # 0 for DECREASING
    # 1 for INCREASING
    DECREASING = 0
    INCREASING = 1
    for report in report_data:
        curr_order = INCREASING if report[0] < report[1] else DECREASING
        curr_invalid_levels = 0
        for idx in range(2, len(report)):
            if report[idx-1] < report[idx]:
                if curr_order != INCREASING:
                    if curr_invalid_levels > TOLERANCE:
                        break
                    elif curr_invalid_levels == 1:
                        if report[idx-2] < report[idx]:
                            curr_order = INCREASING
                    else:
                        curr_invalid_levels += 1
                        continue
            else:
                if curr_order != DECREASING:
                    if curr_invalid_levels > TOLERANCE:
                        break
                    elif curr_invalid_levels == 1:
                        if report[idx-2] > report[idx]:
                            curr_order = DECREASING
                    else:
                        curr_invalid_levels += 1
                        continue
            
            if not MIN_THRESHOLD <= abs(report[idx] - report[idx-1]) <= MAX_THRESHOLD:
                if curr_invalid_levels < TOLERANCE:
                    curr_invalid_levels += 1
                elif curr_invalid_levels == 1:
                    prev_diff = abs(report[idx] - report[idx-2])
                    if not MIN_THRESHOLD <= prev_diff <= MAX_THRESHOLD:
                        break
                else:
                    break
        else:
            safe_levels += 1
    print(f"The number of safe levels is :: {safe_levels}")
    return safe_levels


if __name__ == "__main__":
    extracted_data = read_extract_data()
    # get_safe_levels(report_data=extracted_data)
    # get_safe_levels_with_tolerance(report_data=extracted_data)
    safe_count = get_safe_levels(report_data=extracted_data)
    print(f"Safe count with skip :: {safe_count}")
