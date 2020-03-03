from collections import Counter
import re


class Word_count:
    text = Counter()

    @classmethod
    def print_word_count(cls, message):
        cls.text = Counter([re.sub('[^\w-]', '', val) for i, val in enumerate(message)])

        for k, v in cls.text.items():
            print(f'{k}: {v}')

    @classmethod
    def print_most_common(cls):
        most_common_str = ''
        for k, v in cls.text.most_common(10):
            most_common_str += k + ' '
        print(most_common_str)
