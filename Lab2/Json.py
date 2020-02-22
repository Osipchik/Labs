class Json(object):
    NULL = 'null'
    __indent = None
    __offset = 0

    @classmethod
    def dumps(cls, obj, indent=None):
        cls.__indent = indent
        return cls.__get_str(obj)

    @classmethod
    def __get_str(cls, obj):
        result = None

        if isinstance(obj, str):
            result = f'"{obj}"'
        elif isinstance(obj, bool):
            result = str(obj).lower()
        elif isinstance(obj, int) or isinstance(obj, float):
            result = str(obj)
        elif isinstance(obj, type(None)):
            result = cls.NULL
        elif isinstance(obj, list) or isinstance(obj, dict) or isinstance(obj, tuple):
            result = cls.__collection_to_json(obj)
        elif isinstance(obj, dict):
            result = cls.__dict_to_json(obj)
        return result

    @classmethod
    def __collection_to_json(cls, collection):
        brackets = '[]'
        result = ''
        cls.__offset += 1
        if isinstance(collection, list) or isinstance(collection, tuple):
            result = cls.__list_to_json(collection)
        elif isinstance(collection, dict):
            brackets = '{}'
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
            result += cls.__get_spaces() + f'"{k}": ' + cls.__get_str(v) + ','

        return result
