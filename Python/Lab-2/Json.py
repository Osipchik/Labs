import ast

from Singleton import Singleton


class cache:
    def __init__(self, method):
        self.function = method
        self.prev_data = None

    def __call__(self, *args):
        if args[1] != self.prev_data:
            self.prev_data = args[1]
            self.prev_result = self.function(*args)

        return self.prev_result


def method_friendly_decorator(method_to_decorate):
    def wrapper(self, lie):
        return method_to_decorate(self, lie)
    return wrapper


class Json(metaclass=Singleton):
    __indent = None
    __offset = 0

    __lists = []
    __dicts = []

    def dumps(self, obj, indent=None):
        self.__indent = indent
        return self.__get_str(self, obj)

    @cache
    def __get_str(self, obj):
        result = None

        if isinstance(obj, str):
            result = '"{}"'.format(self.__disable_escape_sequences(obj))
        elif isinstance(obj, bool):
            result = str(obj).lower()
        elif isinstance(obj, int) or isinstance(obj, float):
            result = str(obj)
        elif isinstance(obj, type(None)):
            result = 'null'
        elif isinstance(obj, list) or isinstance(obj, dict) or isinstance(obj, tuple):
            result = self.__collection_to_json(obj)

        return result

    @staticmethod
    def __disable_escape_sequences(string):
        string = string.encode('unicode_escape').decode('utf-8')
        string = string.replace('\"', '\\"')
        string = string.replace('\\x08', '\\b')
        string = string.replace('\\x0c', '\\f')
        string = string.replace('\\x12', '\\u0012')
        string = string.replace('\\x0', '\\u000')
        return string

    def __collection_to_json(self, collection):
        brackets = '[]'
        result = ''
        self.__offset += 1
        if isinstance(collection, list) or isinstance(collection, tuple):
            result = self.__list_to_json(collection)
        elif isinstance(collection, dict):
            brackets = '{}'
            result = self.__dict_to_json(collection)
        self.__offset -= 1

        if len(result):
            result = result[:-1] + self.__get_spaces() if self.__indent is not None else result[1:-1]
        return brackets[:1] + result + brackets[1:]

    def __get_spaces(self):
        return '\n' + ' ' * self.__indent * self.__offset if self.__indent is not None else ' '

    def __list_to_json(self, obj):
        result = ''
        for v in obj:
            result += self.__get_spaces() + self.__get_str(self, v) + ','

        return result

    def __dict_to_json(self, obj):
        result = ''
        for k, v in obj.items():
            if isinstance(k, tuple):
                raise TypeError('keys must be str, int, float, bool or None, ')

            key = '{}: '.format(self.__get_str(self, k)) if isinstance(k, str) else '"{}": '.format(self.__get_str(self, k))
            result += self.__get_spaces() + key + self.__get_str(self, v) + ','
        return result

    @staticmethod
    def loads(string):
        return ast.literal_eval(string.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
