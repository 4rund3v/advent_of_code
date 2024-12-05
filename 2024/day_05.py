
"""
problem: safety manual dont print correctly
1. print in a order
x|y indicates that page x must be printed before page y
2. each update has the pages in the right order


ex: 47 | 53 
---> if an update includes both 47 and 53 - > page 47 must be printed at some point before 53
47 ----- 53


second section indicates the updates
line - update - 75,47, 61, 53, 29


find the valid orderings
from the valid ordering get the middle element
1. assume all update lines are odd

"""

import os
import sys
from typing import List, Tuple
from collections import defaultdict
from collections import deque


DATA_SOURCE = "./inputs/day_05_input.txt"
def get_raw_data():
    """
    Get the raw_data
    """
    with open(DATA_SOURCE, "r") as rfile:
        raw_data = rfile.read()
    return raw_data

def parse_raw_data(raw_data:str) -> dict:
    """
    given a blob of string input
    parse based on rows
    rules 
    empty line
    updates
    """
    rules = []
    updates = []
    raw_data.strip()
    split_data = raw_data.split('\n')
    idx_split = split_data.index('')
    # add rules
    for line in split_data[:idx_split]:
        page_before, page_after = line.split('|')
        rules.append( [int(page_before), int(page_after)] )

    # add updates
    for line in split_data[idx_split+1:]:
        if not line:
            continue
        pages = line.split(',')
        updates.append( [int(page) for page in pages] )
    return dict(rules=rules, updates=updates)

def build_rule_mapper(rules: List[int]) -> dict:
    rule_mapper = defaultdict(set)
    for page_before, page_after in rules:
        rule_mapper[page_before].add( page_after )
    return rule_mapper

def validate_update(update: List[int], rule_mapper: dict) -> bool:
    """
    [ 75,47,61,53,29 ]
    """
    seen = set()
    for page in update:
        for page_after in rule_mapper[page]:
            if page_after in seen:
                return False
        seen.add( page )
    return True

def validate_updates(updates: List[List[int]], rule_mapper: dict) -> Tuple[List[List], List[List]]:
    valid_updates = []
    invalid_updates = []
    for update in updates:
        if validate_update(update, rule_mapper):
            valid_updates.append( update )
        else:
            invalid_updates.append( update )
    return valid_updates, invalid_updates

def prepare_inorder_map(rule_mapper: dict) -> dict:
    inorder_map = defaultdict(int)
    for page in rule_mapper:
        # This page goes before all of the rule_mapper[page]
        # 75 -> [53, 47,13]
        """{
                53: 1
                47:1 
                13:1
                75: 0
        }"""
        for page_after in rule_mapper[page]:
            inorder_map[page_after] += 1
    return inorder_map

def fix_invalid_updates(invalid_updates: List[List[int]], rule_mapper: dict, inorder_map: dict) -> List[List[int]]:
    """
     -> 75,97,47,61,53
     convert to
     -> 97,75,47,61,53
    """
    fixed_updates = []
    # O(l)
    for invalid_update in invalid_updates:
        pages_to_udpate = set(invalid_update)
        # 13
        pages_inorder_mapper = defaultdict(int)
        # O(m,n) -> m*n
        for page in rule_mapper:
            for page_after in rule_mapper[page]:
                if page in pages_to_udpate:
                    pages_inorder_mapper[page_after] += 1
        # o(n)
        queue = deque([])
        for page in pages_to_udpate:
            if pages_inorder_mapper[page] == 0:
                queue.append(page)
        # n*n
        fixed_update = []
        while queue:
            page = queue.popleft()
            fixed_update.append(page)
            for page_after in rule_mapper[page]:
                if page_after in pages_to_udpate:
                    pages_inorder_mapper[page_after] -= 1
                    if pages_inorder_mapper[page_after] == 0:
                        queue.append( page_after )
        if len(fixed_update) == len(invalid_update):
            fixed_updates.append(fixed_update)
        else:
            print(fixed_update, invalid_update)
    return fixed_updates


def find_sum_of_mid_pages(updates: List[List[int]]) -> int:
    mid_page_sum = 0
    for update in updates:
        update_len = len(update)
        if update_len % 2 == 0:
           update_mid_pos = update_len // 2
        else:
           update_mid_pos = (update_len // 2) + 1
        mid_page = update[update_mid_pos -1 ]
        mid_page_sum += mid_page
    return mid_page_sum

def fix_invalid_updates_optimized(invalid_updates, rule_mapper):
    """
    Optimized version using cached topological ordering
    Time Complexity: O(V + E) for preprocessing, O(n log n) for each update sort
    where V = vertices(pages), E = edges(rules), n = update length
    """
    # Preprocess full topological order once - O(V + E)
    def get_topological_order():
        visited = set()
        order_map = {}
        order = 0
        
        def dfs(node):
            nonlocal order
            if node in visited:
                return
            visited.add(node)
            for next_node in rule_mapper[node]:
                dfs(next_node)
            order_map[node] = order
            order += 1
            
        for node in rule_mapper:
            dfs(node)
        return order_map
    
    topo_order = get_topological_order()
    fixed_updates = []
    
    # Fix each invalid update using the precomputed order - O(n log n) per update
    for update in invalid_updates:
        fixed_update = sorted(update, key=lambda x: topo_order.get(x, float('inf')))
        fixed_updates.append(fixed_update)
        
    return fixed_updates


if __name__ == "__main__":
    raw_data = get_raw_data()
    print(f"The raw data read contains : {len(raw_data)}")
    parsed_data = parse_raw_data(raw_data)
    print(f"Number of rules :: {len(parsed_data['rules'])}")
    print(f"Number of updates :: {len(parsed_data['updates'])}")
    rule_mapper = build_rule_mapper(rules=parsed_data['rules'])
    print(f"Number of rules are :: {len(rule_mapper)}")
    valid_updates,invalid_updates = validate_updates(updates=parsed_data['updates'], rule_mapper=rule_mapper)
    print(f"Number of valid updates are :: {len(valid_updates)}")
    print(f"Number of invalid updates are :: {len(invalid_updates)}")
    mid_page_sum = find_sum_of_mid_pages(updates=valid_updates)
    print(f"The mid page sum is :: {mid_page_sum}")
    inorder_map = prepare_inorder_map(rule_mapper=rule_mapper)
    print(f"the inorder map prepared is :: {inorder_map}")
    fixed_updates = fix_invalid_updates(invalid_updates=invalid_updates, rule_mapper=rule_mapper, inorder_map=inorder_map)
    mid_page_sum_invalids = find_sum_of_mid_pages(updates=fixed_updates)
    print(f"The mid page sum for the invalid updates are :: {mid_page_sum_invalids}")
    
    fixed_updates = fix_invalid_updates_optimized(invalid_updates=invalid_updates, rule_mapper=rule_mapper)
    mid_page_sum_invalids = find_sum_of_mid_pages(updates=fixed_updates)
    print(f"The mid page sum for the invalid updates are :: {mid_page_sum_invalids}")
