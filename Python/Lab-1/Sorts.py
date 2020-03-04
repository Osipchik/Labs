import random


class Sorts:
    @staticmethod
    def quick_sort(array, begin=0, end=None):
        if end is None:
            end = len(array) - 1

        def _quick_sort(arr, first, last):
            if first >= last:
                return
            pivot = arr[random.randint(first, last)]
            _quick_sort(arr, first, pivot - 1)
            _quick_sort(arr, pivot + 1, last)

        return _quick_sort(array, begin, end)

    @staticmethod
    def merge_sort(array):
        if len(array) <= 1:
            return array

        half = len(array) // 2
        left = Sorts.merge_sort(array[:half])
        right = Sorts.merge_sort(array[half:])

        return Sorts.merge(left, right)

    @staticmethod
    def merge(left, right):
        left_index, right_index = 0, 0
        result = []
        while left_index < len(left) and right_index < len(right):
            if left[left_index] < right[right_index]:
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1

        result += left[left_index:]
        result += right[right_index:]
        return result