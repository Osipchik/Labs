from collections import Counter
import re


class Word_count:
    SPACE = ' '
    text = Counter()

    @classmethod
    def print_word_count(cls, message):
        cls.text = Counter([re.sub('[^\w-]', '', val) for i, val in enumerate(message)])

        for k, v in cls.text.items():
            print(f'{k}: {v}')

    @classmethod
    def get_most_common(cls):
        return cls.SPACE.join(dict(cls.text.most_common(10)).keys())
