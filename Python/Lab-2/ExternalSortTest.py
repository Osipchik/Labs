import unittest
import random
from ExternalSort import ExternalSort


def create_test_file():
    test_list = []
    for _ in range(1_000_000):
        test_list.append(random.randint(-1000000, 1000000))

    with open('test.txt', 'w') as f:
        f.writelines('{}\n'.format(i) for i in test_list)

    test_list.sort()
    return iter(test_list)


def check_test_file(test_list):
    with open('test_res.txt', 'r') as f:
        for i in f:
            if int(i) != next(test_list):
                return False

    return True


class ExternalSortTest(unittest.TestCase):
    def test_sort(self):
        test_iterator = create_test_file()
        sort = ExternalSort()
        sort.sort_file('test.txt', 'test_res.txt', 100_000)
        self.assertTrue(check_test_file(test_iterator))

    def test_wrong_file(self):
        sort = ExternalSort()
        with self.assertRaises(FileNotFoundError):
            sort.sort_file('tes.txt', 'test_res.txt', 100_000)


if __name__ == '__main__':
    unittest.main()
