import random


class Sorts:
    @staticmethod
    def quick_sort(array, fst=0, lst=None):
        if lst is None:
            lst = len(array) - 1

        if fst >= lst:
            return
        i, j = fst, lst
        pivot = array[random.randint(fst, lst)]

        while i <= j:
            while array[i] < pivot:
                i += 1
            while array[j] > pivot:
                j -= 1
            if i <= j:
                array[i], array[j] = array[j], array[i]
                i, j = i + 1, j - 1
        Sorts.quick_sort(array, fst, j)
        Sorts.quick_sort(array, i, lst)

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