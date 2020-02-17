import random
import time
from External_sort import External_sort
from Sort import Sort

# start_time = time.time()
# with open('numbers.txt', 'w') as f:
#     # f.writelines(f'{i}\n' for i in range(1_00))
#     f.writelines('{}\n'.format(random.randint(-1000000, 1000000)) for _ in range(625_00))
# print("--- %s seconds ---" % (time.time() - start_time))

# C:\\Users\\ASUS\\PycharmProjects\\

sort = External_sort()
sort.sort_file('numbers.txt')

