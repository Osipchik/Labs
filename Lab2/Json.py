import ast


class cache:
    prev_data = None
    prev_result = None

    def __init__(self, func):
        self.function = func

    def __call__(self, *args):
        if args[1] != self.prev_data:
            self.prev_data = args[1]
            self.prev_result = self.function(*args)

        return self.prev_result


class Json:
    NULL = 'null'
    UTF = 'utf-8'
    UNICODE_ESCAPE = 'unicode_escape'
    LIST_BRACKETS = '[]'
    DICT_BRACKETS = '{}'
    __indent = None
    __offset = 0

    __lists = []
    __dicts = []

    @classmethod
    def dumps(cls, obj, indent=None):
        cls.__indent = indent
        return cls.__get_str(obj)

    @classmethod
    @cache
    def __get_str(cls, obj):
        result = None

        if isinstance(obj, str):
            result = '"{}"'.format(cls.__disable_escape_sequences(obj))
        elif isinstance(obj, bool):
            result = str(obj).lower()
        elif isinstance(obj, int) or isinstance(obj, float):
            result = str(obj)
        elif isinstance(obj, type(None)):
            result = cls.NULL
        elif isinstance(obj, list) or isinstance(obj, dict) or isinstance(obj, tuple):
            result = cls.__collection_to_json(obj)
        return result

    @classmethod
    def __disable_escape_sequences(cls, string):
        string = string.encode(cls.UNICODE_ESCAPE).decode(cls.UTF)
        string = string.replace('\"', '\\"')
        string = string.replace('\\x08', '\\b')
        string = string.replace('\\x0c', '\\f')
        string = string.replace('\\x12', '\\u0012')
        string = string.replace('\\x0', '\\u000')
        return string

    @classmethod
    def __collection_to_json(cls, collection):
        brackets = cls.LIST_BRACKETS
        result = ''
        cls.__offset += 1
        if isinstance(collection, list) or isinstance(collection, tuple):
            result = cls.__list_to_json(collection)
        elif isinstance(collection, dict):
            brackets = cls.DICT_BRACKETS
            result = cls.__dict_to_json(collection)
        cls.__offset -= 1

        if len(result):
            result = result[:-1] + cls.__get_spaces() if cls.__indent is not None else result[1:-1]
        return brackets[:1] + result + brackets[1:]

    @classmethod
    def __get_spaces(cls):
        return '\n' + ' ' * cls.__indent * cls.__offset if cls.__indent is not None else ' '

    @classmethod
    def __list_to_json(cls, obj):
        result = ''
        for v in obj:
            result += cls.__get_spaces() + cls.__get_str(v) + ','

        return result

    @classmethod
    def __dict_to_json(cls, obj):
        result = ''
        for k, v in obj.items():
            if isinstance(k, tuple):
                raise TypeError('keys must be str, int, float, bool or None, ')

            key = '{}: '.format(cls.__get_str(k)) if isinstance(k, str) else '"{}": '.format(cls.__get_str(k))
            result += cls.__get_spaces() + key + cls.__get_str(v) + ','
        return result

    @staticmethod
    def loads(string):
        return ast.literal_eval(string.replace('true', 'True').replace('false', 'False').replace('null', 'None'))
