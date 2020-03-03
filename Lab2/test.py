import json
from Json import Json
import ast
import re

# x = [12, 'as d, ,  ', ', ', True, None, [12, 'asd', True, None]]
# x = "\\"
# x = "\"foo\bar\u9999 d \\ \a \b \f \n \r \t \v \ooo \x12 \\x \\'"
# x = 'asd23.2'
# x = "\u1234"
# x = 'e5.""5\w'
# x = ['as d, \", ', 4, [4, 5, "qwe", {2: 2}]]
# x = [1, 2, 4, 'asd']
# x = '[12, "asd", true, null, [12, "asd", true, null]]'
# x = {2: 3}
x = [True, "'true'", 'ads \"true, true \\', True, True]
# print(json.dumps(x, indent=4))
# print(Json.dumps(x, indent=4))

j = json.dumps(x)
print(repr(j), j == Json.dumps(x))
print([i for i in range(len(j)) if j.startswith('true', i)])
print([i for i in range(len(j)) if j.startswith('\"', i)])
print([i for i in range(len(j)) if j.startswith('\'', i)])
print([i for i in range(len(j)) if j.startswith(',', i)])

print(repr(str(Json.loads(j))))



