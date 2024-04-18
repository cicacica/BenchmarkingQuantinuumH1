import unittest
from typing import List, Tuple, Dict
import itertools
from src.bitwise_operations import BitwiseOperations

class TestBitwiseOperations(unittest.TestCase):
    def setUp(self):
        self.bitwise = BitwiseOperations()

    def test_get_bitwise_combinations(self):
        self.assertEqual(self.bitwise.get_bitwise_combinations(2), [(0, 0), (0, 1), (1, 0), (1, 1)])

    def test_compare_lists(self):
        self.assertEqual(self.bitwise.compare_lists([(0, 0), (0, 1)], [(0, 0), (1, 1)]), [True, False])

    def test_subset_list_by_bools(self):
        self.assertEqual(self.bitwise.subset_list_by_bools([(0, 0), (0, 1), (1, 0), (1, 1)], [True, False, True, False]), [(0, 0), (1, 0)])
        with self.assertRaises(ValueError):
            self.bitwise.subset_list_by_bools([(0, 0), (0, 1)], [True, False, True])

    def test_create_dict_from_tuples(self):
        self.assertEqual(self.bitwise.create_dict_from_tuples([(0, 0), (0, 1)]), {(0, 0): 0, (0, 1): 0})

    def test_sort_dict_by_keys(self):
        self.assertEqual(self.bitwise.sort_dict_by_keys({(0, 1): 0, (0, 0): 0}), {(0, 0): 0, (0, 1): 0})

    def test_return_complete_distribution(self):
        self.assertEqual(self.bitwise.return_complete_distribution(2, {(0, 0): 1}), {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 0})

if __name__ == '__main__':
    unittest.main()