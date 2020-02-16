from collections import Counter
import re

class word_count(object):
    def __init__(self):
        self.text = Counter()

    def print_word_count(self, message):
        self.text = Counter([re.sub('[^\w-]', '', val) for i, val in enumerate(message)])

        for k, v in self.text.items():
            print(f'{k}: {v}')

    def print_most_common(self):
        most_common_str = ''
        for k, v in self.text.most_common(10):
            most_common_str += k + ' '
        print(most_common_str)
