class sorts(object):
    def __partition(self, array, low, high):
        i = low - 1

        for j in range(low, high):
            if array[j] <= array[high]:
                i = i + 1
                array[i], array[j] = array[j], array[i]

        array[i + 1], array[high] = array[high], array[i + 1]
        return i + 1

    def quick_sort(self, array, low, high):
        if low < high:
            pi = self.__partition(array, low, high)

            self.quick_sort(array, low, pi - 1)
            self.quick_sort(array, pi + 1, high)

        return array

    def __merge(self, left_list, right_list):
        sorted_list = []
        left_list_index = right_list_index = 0

        left_list_length, right_list_length = len(left_list), len(right_list)

        for _ in range(left_list_length + right_list_length):
            if left_list_index < left_list_length and right_list_index < right_list_length:
                if left_list[left_list_index] <= right_list[right_list_index]:
                    sorted_list.append(left_list[left_list_index])
                    left_list_index += 1
                else:
                    sorted_list.append(right_list[right_list_index])
                    right_list_index += 1

            elif left_list_index == left_list_length:
                sorted_list.append(right_list[right_list_index])
                right_list_index += 1

            elif right_list_index == right_list_length:
                sorted_list.append(left_list[left_list_index])
                left_list_index += 1

        return sorted_list

    def merge_sort(self, nums):
        if len(nums) <= 1:
            return nums

        mid = len(nums) // 2

        left_list = self.merge_sort(nums[:mid])
        right_list = self.merge_sort(nums[mid:])

        return self.__merge(left_list, right_list)
