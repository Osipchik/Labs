import argparse
from WordCount import word_count
from Sorts import sorts
from fibonachi import fibonachi

STORE_TRUE = 'store_true'
NARGS = '+'

parser = argparse.ArgumentParser()
parser.add_argument('-m', dest='message', default='', type=str, nargs=NARGS)
parser.add_argument('-f', dest='float_list', default=0, type=float, nargs=NARGS)
parser.add_argument('-fib', dest='count', default=0, type=int, action='store')
parser.add_argument('-mf', dest='filename', type=str)
parser.add_argument('-top', action=STORE_TRUE)
parser.add_argument('-q', action=STORE_TRUE)
parser.add_argument('-s', action=STORE_TRUE)

args = parser.parse_args()
message = list(args.message)
filename = args.filename
float_list = args.float_list
count = args.count

if filename:
    with open(f'D:/DEV/PythonLabs/Lab_1/{filename}.txt', 'r') as file:
        message = file.read().split()

if message:
    word_count = word_count()
    word_count.print_word_count(message)
    if args.top:
        word_count.print_most_common()
elif float_list:
    sort = sorts()
    if args.q:
        print(sort.quick_sort(float_list, 0, len(float_list) - 1))
    elif args.s:
        print(sort.merge_sort(float_list))
elif count:
    for i in fibonachi(count):
        print(i)
