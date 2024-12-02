import os
import requests
from collections import Counter


DATA_SOUCE = "./inputs/day_01_part_1_input.txt"

def read_input():
	left_data,right_data = [],[]
	with open(DATA_SOUCE, "r") as rfile:
		for line in rfile.readlines():
			line_data = line.strip().split(" ")
			l,r = line_data[0], line_data[-1]
			l,r = int(l), int(r)
			left_data.append(l)
			right_data.append(r)
	left_data.sort()
	right_data.sort()
	return left_data, right_data


def find_difference(left_data, right_data):
	diff_sum = 0
	for left_val, right_val in zip(left_data, right_data):
		diff_sum += abs( left_val - right_val )
	return diff_sum

def get_similarity_score(left_data, right_data):
    right_counter = Counter(right_data)
    similarity_score = 0
    for elem in left_data:
    	similarity_score += elem*right_counter[elem]
    return similarity_score




if __name__ == "__main__":
	left_data, right_data = read_input()
	print(f"The number of lines present at : {len(left_data)} -- {len(right_data)}")
	diff_sum = find_difference(left_data, right_data)
	print(f"The difference between the values are :: {diff_sum}")
	similarity_score = get_similarity_score(left_data, right_data)
	print(f"The similarity score between the left and right are :: {similarity_score}")


