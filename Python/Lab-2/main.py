import random
from External_sort import external_sort

with open('numbers.txt', 'w') as f:
    f.writelines('{}\n'.format(random.randint(-1000000, 1000000)) for _ in range(5_000_000))

external_sort.sort_file('numbers.txt', 'sorted_numbers.txt', 1_000_000)
