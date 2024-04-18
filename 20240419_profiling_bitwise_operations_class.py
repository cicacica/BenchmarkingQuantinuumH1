from src.bitwise_operations import BitwiseOperations
import cProfile

N = 3
results = {(0, 0, 0): 51, (1, 1, 0): 49}

# Create instances of your classes
bitwise_operations = BitwiseOperations() 



# Profile methods of the first class
profiler = cProfile.Profile()
profiler.enable()
bitwise_operations.return_complete_distribution(N, results)
profiler.disable()
profiler.print_stats()





    
    
    
    
    
    