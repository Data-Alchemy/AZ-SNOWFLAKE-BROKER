
import json
dict_input = '{"name":"test"}'
print(type(dict_input))
if type(dict_input) == str:
    dict_input= json.loads(dict_input)
else:
    dict_input = dict_input

print(type(dict_input))