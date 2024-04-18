##################################################################
# Filename  : 20240418_test_best_script_build_functions.py
# Author    : Jonathan Miller
# Date      : 2024-04-18
# Aim       : aim_script
#           : Use this script to test the best functions
#           :
##################################################################

from src.bitwise_operations import BitwiseOperations

N = 3
results = {(0, 0, 0): 51, (1, 1, 0): 49}

# Create instances of your classes
bitwise_operations = BitwiseOperations() 
dist = bitwise_operations.return_complete_distribution(N, results)

dist


import matplotlib.pyplot as plt

# Your data
data = {(0, 0, 0): 51, (0, 0, 1): 0, (0, 1, 0): 0, (0, 1, 1): 0, (1, 0, 0): 0, (1, 0, 1): 0, (1, 1, 0): 49, (1, 1, 1): 0}

# Convert the keys from tuples to strings
keys = [''.join(map(str, k)) for k in data.keys()]

# Get the values
values = list(data.values())

# Create the bar chart
plt.bar(keys, values)

# Add labels
plt.xlabel('Bins')
plt.ylabel('Values')

# Show the plot
plt.show()