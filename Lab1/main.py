import argparse
import WordCount
import Sorts
import fibonacci

STORE_TRUE = 'store_true'
NARGS = '+'

parser = argparse.ArgumentParser()
parser.add_argument('-m', dest='message', default='', type=str, nargs=NARGS)
parser.add_argument('-f', dest='floats', default=0, type=float, nargs=NARGS)
parser.add_argument('-fib', dest='fib_count', default=0, type=int, action='store')
parser.add_argument('-mf', dest='filename', type=str)
parser.add_argument('-top', action=STORE_TRUE)
parser.add_argument('-q', action=STORE_TRUE)
parser.add_argument('-s', action=STORE_TRUE)

args = parser.parse_args()
message = list(args.message)
filename = args.filename
float_list = args.floats
fib_count = args.fib_count

if filename:
    with open('D:/DEV/PythonLabs/Lab1/{}.txt'.format(filename), 'r') as file:
        message = file.read().split()

if message:
    WordCount.word_count.print_word_count(message)
    if args.top:
        WordCount.word_count.print_most_common()
elif float_list:
    if args.q:
        print(Sorts.sorts.quick_sort(float_list))
    elif args.s:
        print(Sorts.sorts.merge_sort(float_list))
    else:
        print(float_list)
elif count:
    for i in fibonacci.fibonacci(fib_count):
        print(i)
