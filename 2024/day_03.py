import os
import sys
import re


DATA_SOURCE = "./inputs/day_03_input.txt"

def read_input() -> str:
    raw_input = None
    with open(DATA_SOURCE, 'r') as rfile:
        raw_input = rfile.read()
    return raw_input

def get_matching_expressions(raw_input):
    start_index = 0
    curr_window = []
    PATTERN = r"""(?P<multiply_expression>(?P<keyword>\bmul\b)\((?P<left_var>[\d]{1,3})([\s]?)(\,)([\s]?)(?P<right_var>[\d]{1,3})\))|(?P<do_operation>\bdo\b\(\))|(?P<dont_operation>\bdon\'t\b\(\))"""
    skip = False
    for match in re.finditer(PATTERN, raw_input, re.IGNORECASE):
        result = match.groupdict()
        print(result)
        if result.get("do_operation") and skip:
            skip = False
        if result.get('dont_operation'):
            skip = True
        if result.get("multiply_expression"):
            if skip:
                print(f'skipping :: {result}')
                continue
            left_var, right_var = result['left_var'], result['right_var']
            yield int(left_var), int(right_var)
    
    print(f"Finished finding matching expressions")
    return

def compute_result(raw_input):
    result = 0
    for left_var, right_var in get_matching_expressions(raw_input):
        result += left_var*right_var
    print(f"Result generated is :: {result}")
    return result

if __name__ == "__main__":
    raw_input = read_input()
    print(f"The raw input size is :: {len(raw_input)}")
    compute_result(raw_input)
