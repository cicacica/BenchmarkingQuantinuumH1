##################################################################
# Filename  : 20240418_test_best_script_build_functions.py
# Author    : Jonathan Miller
# Date      : 2024-04-18
# Aim       : aim_script
#           : Use this script to test the best functions
#           :
##################################################################

import os


import itertools

def get_bitwise_combinations(N):
    return [''.join(map(str, p)) for p in itertools.product([0, 1], repeat=N)]

N = 7
get_bitwise_combinations(N)