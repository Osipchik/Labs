class sorts:
    @classmethod
    def quick_sort(cls, arr):
        less = []
        pivots = []
        more = []
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            for i in arr:
                if i < pivot:
                    less.append(i)
                elif i > pivot:
                    more.append(i)
                else:
                    pivots.append(i)
            less = cls.quick_sort(less)
            more = cls.quick_sort(more)
            return less + pivots + more

    @classmethod
    def merge_sort(cls, array):
        if len(array) <= 1:
            return array

        half = len(array) // 2
        left = cls.merge_sort(array[:half])
        right = cls.merge_sort(array[half:])

        return cls.merge(left, right)

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

