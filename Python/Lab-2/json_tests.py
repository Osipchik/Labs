import unittest
import json
from Json import Json

ESCAPE_SEQUENCES = "\"foo\bar\u9999 d \\ \a \b \f \n \r \t \v \ooo \x12 \\x \\'"
NESTED_COLLECTION = ['as d, \", ', 4, [4, 5, "qwe", {2: 2, 'asd': 2, 3: ('as d, \", ', 4)}]]
EMPTY_COLLECTION = []
COLLECTIONS = [NESTED_COLLECTION, EMPTY_COLLECTION]
FAILED_COLLECTION = {(1, 2): 3}
FAILED_JSON = '{[2, 2, 2, 2]: 2}'
CACHE = [ESCAPE_SEQUENCES, ESCAPE_SEQUENCES]


class json_test(unittest.TestCase):
    my_json = Json()

    def test_dumps_escape_sequences(self):
        data = ESCAPE_SEQUENCES
        result = self.my_json.dumps(data)
        self.assertEqual(result, json.dumps(data))

    def test_loads_escape_sequences(self):
        data = json.dumps(ESCAPE_SEQUENCES)
        result = Json.loads(data)
        self.assertEqual(result, json.loads(data))

    def test_dump_collections(self):
        for i in COLLECTIONS:
            self.assertEqual(self.my_json.dumps(i), json.dumps(i))

    def test_load_collections(self):
        for i in COLLECTIONS:
            data = json.dumps(i)
            self.assertEqual(Json.loads(data), json.loads(data))

    def test_dump_failed_collection(self):
        with self.assertRaises(TypeError):
            self.my_json.dumps(FAILED_COLLECTION)

    def test_dump_failed_json(self):
        with self.assertRaises(TypeError):
            Json.loads(FAILED_JSON)

    def test_dump_cache(self):
        data = CACHE
        result = self.my_json.dumps(data)
        self.assertEqual(result, json.dumps(data))


if __name__ == '__main__':
    unittest.main()
