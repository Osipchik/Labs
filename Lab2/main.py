import random
from External_sort import External_sort

# with open('numbers.txt', 'w') as f:
#     f.writelines('{}\n'.format(random.randint(-1000000, 1000000)) for _ in range(5_000_000))


sort = External_sort()
sort.sort_file('numbers.txt')
