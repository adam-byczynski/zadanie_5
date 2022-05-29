import unittest
import unittest.mock
import zadanie_5 as zad5
import random


class TestSortingAlgorithms(unittest.TestCase):

    def generate_list_of_random_numbers(range_start=1, range_end=random.randint(200, 400), list_size=random.randint(5, 10)):
        return random.sample(range(range_start, range_end), list_size)

    generated_nums = generate_list_of_random_numbers()
 
    def test_quick_sort(self):
        test_list = self.generated_nums
        expected = test_list.copy()
        expected.sort()
        result = zad5.Algorithms.quick_sort(test_list.copy())
        self.assertEqual(expected, result)

    def test_merge_sort(self):
        test_list = self.generated_nums
        expected = test_list.copy()
        expected.sort()
        result = zad5.Algorithms.merge_sort(test_list.copy())
        self.assertEqual(expected, result)

    def test_heap_sort(self):
        test_list = self.generated_nums
        expected = test_list.copy()
        expected.sort()
        result = zad5.Algorithms.heap_sort(test_list.copy())
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
