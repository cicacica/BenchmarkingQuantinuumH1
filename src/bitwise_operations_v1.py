##################################################################
# Filename  : bitwise_operations.py
# Author    : Jonathan Miller
# Date      : 2024-04-18
# Aim       : aim_script
#           : Class to  ensure all elements of qubits set
#           : are present for data analysis
##################################################################


import itertools

class BitwiseOperationsV1:
    """
    A class to perform various bitwise operations.
    """

    def get_bitwise_combinations(self, N):
        """
        Generate all 2^N bitwise combinations.

        Parameters:
        N (int): The number of bits.

        Returns:
        list: A list of tuples representing all 2^N bitwise combinations.
        """
        return [p for p in itertools.product([0, 1], repeat=N)]

    def compare_lists(self, list_to_iterate_against, list_to_compare_to):
        """
        Compare two lists of tuples.

        Parameters:
        list_to_iterate_against (list): The first list of tuples.
        list_to_compare_to (list): The second list of tuples.

        Returns:
        list: A list of boolean values. Each value is True if the corresponding tuple from the first list is in the second list, and False otherwise.
        """
        return [(x in list_to_compare_to) for x in list_to_iterate_against]

    def subset_list_by_bools(self, input_list, bool_list):
        """
        Subset a list by a list of booleans.

        Parameters:
        input_list (list): The list to subset.
        bool_list (list): The list of booleans.

        Returns:
        list: A new list that contains only the elements from the input list where the corresponding value in the bool list is True.
        """
        return [x for x, y in zip(input_list, bool_list) if y]

    def create_dict_from_tuples(self, tuple_list):
        """
        Create a dictionary from a list of tuples.

        Parameters:
        tuple_list (list): The list of tuples.

        Returns:
        dict: A dictionary where each key is a tuple from the tuple list and each value is 0.
        """
        return {t: 0 for t in tuple_list}

    def sort_dict_by_keys(self, d):
        """
        Sort a dictionary by its keys.

        Parameters:
        d (dict): The dictionary to sort.

        Returns:
        dict: A new dictionary that contains the same keys and values as the input dictionary, but sorted in ascending order by key.
        """
        return dict(sorted(d.items()))
    
    def return_complete_distribution(self, N: int,results: dict):
        enumerated_tuples = self.get_bitwise_combinations(N)
        sample_tuples = results.keys()
        bool_output = self.compare_lists(enumerated_tuples, sample_tuples)
        tuple_list = self.subset_list_by_bools(enumerated_tuples,[not x for x in bool_output])
        return self.sort_dict_by_keys({**results, **self.create_dict_from_tuples(tuple_list)})
    