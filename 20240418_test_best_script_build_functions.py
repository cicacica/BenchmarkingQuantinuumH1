##################################################################
# Filename  : 20240418_test_best_script_build_functions.py
# Author    : Jonathan Miller
# Date      : 2024-04-18
# Aim       : aim_script
#           : Use this script to test the best functions
#           :
##################################################################

from src.bitwise_operations_v1 import BitwiseOperationsV1
from src.bitwise_operations_v2 import BitwiseOperationsV2
import cProfile

N = 3
results = {(0, 0, 0): 51, (1, 1, 0): 49}

# Create instances of your classes
bitwise_operations_v1 = BitwiseOperationsV1() 
bitwise_operations_v2 = BitwiseOperationsV2()


# Profile methods of the first class
profiler = cProfile.Profile()
profiler.enable()
bitwise_operations_v1.return_complete_distribution(N, results)
profiler.disable()
profiler.print_stats()

# Profile methods of the second class
profiler = cProfile.Profile()
profiler.enable()
bitwise_operations_v2.return_complete_distribution(N, results)
profiler.disable()
profiler.print_stats()



