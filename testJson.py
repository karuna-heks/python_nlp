# -*- coding: utf-8 -*-
import json

d = {'a': 2, 'b': 24, 'c': 41, 'lovdsa': 0, 'teeg': 24}
print(d)


d_json = json.dumps(d)
print(d_json)

d2 = json.loads(d_json)
print(d2)