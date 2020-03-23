import unittest
import random
from External_sort import external_sort


def create_test_file():
    test_list = []
    for _ in range(5000):
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


class external_sort_test(unittest.TestCase):
    def test_sort(self):
        test_iterator = create_test_file()
        sort = external_sort()
        sort.sort_file('test.txt', 'test_res.txt', 1000)
        self.assertTrue(check_test_file(test_iterator))

    def test_wrong_file(self):
        sort = external_sort()
        with self.assertRaises(FileNotFoundError):
            sort.sort_file('tes.txt', 'test_res.txt', 1000)


if __name__ == '__main__':
    unittest.main()
