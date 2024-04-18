import itertools
from typing import List, Dict, Tuple

class BitwiseOperations:
    """
    A class to perform various bitwise operations.
    """

    def get_bitwise_combinations(self, N: int) -> List[Tuple[int, ...]]:
        return [p for p in itertools.product([0, 1], repeat=N)]

    def compare_lists(self, list_to_iterate_against: List[Tuple[int, ...]], list_to_compare_to: List[Tuple[int, ...]]) -> List[bool]:
        list_to_compare_to_set = set(list_to_compare_to)
        return [(x in list_to_compare_to_set) for x in list_to_iterate_against]

    def subset_list_by_bools(self, input_list: List[Tuple[int, ...]], bool_list: List[bool]) -> List[Tuple[int, ...]]:
        if len(input_list) != len(bool_list):
            raise ValueError("input_list and bool_list must be of the same length")
        return [x for x, y in zip(input_list, bool_list) if y]

    def create_dict_from_tuples(self, tuple_list: List[Tuple[int, ...]]) -> Dict[Tuple[int, ...], int]:
        return {t: 0 for t in tuple_list}

    def sort_dict_by_keys(self, d: Dict[Tuple[int, ...], int]) -> Dict[Tuple[int, ...], int]:
        return dict(sorted(d.items()))
    
    def return_complete_distribution(self, N: int, results: Dict[Tuple[int, ...], int]) -> Dict[Tuple[int, ...], int]:
        enumerated_tuples = self.get_bitwise_combinations(N)
        sample_tuples = results.keys()
        bool_output = self.compare_lists(enumerated_tuples, sample_tuples)
        tuple_list = self.subset_list_by_bools(enumerated_tuples,[not x for x in bool_output])
        return self.sort_dict_by_keys({**results, **self.create_dict_from_tuples(tuple_list)})