from sorting import *
import unittest
import random
import sys


class SortTest(unittest.TestCase):
    def setUp(self):
        self.sort_funcs = {"radix": radix_sort, "bucket": bucket_sort}

    def run_test(self, arr, key=lambda x: x):
        expected = sorted(arr, key=key)
        for sort_name, sort_func in self.sort_funcs.items():
            with self.subTest(sort_method=sort_name):
                actual = sort_func(arr, key=key)
                msg = f"{sort_name} sort failed"
                self.assertEqual(actual, expected, msg)

    def test_empty(self):
        arr = []
        self.run_test(arr)

    def test_sorted(self):
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.run_test(arr)

    def test_reversed(self):
        arr = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        self.run_test(arr)

    def test_repeated_numbers(self):
        arr = [5, 5, 0, 1, 1, 1, 9]
        self.run_test(arr)

    def test_multi_digits(self):
        arr = [100, 21, 1, 1500, 34, 10]
        self.run_test(arr)

    def test_key(self):
        arr = {"a": 100, "b": 21, "c": 1, "d": 1500, "e": 34, "f": 10}
        self.run_test(arr.items(), key=lambda x: x[1])

    def test_random(self):
        for i in range(10):
            arr = [random.randint(0, sys.maxsize) for _ in range(100000)]
            self.run_test(arr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
