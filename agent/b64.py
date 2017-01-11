# -*- coding: UTF-8 -*-
import base64
import json

def json_to_b64(obj):
    try:
        str = json.dumps(obj, ensure_ascii=False)
        str = base64.b64encode(str)
        return str
    except Exception as e:
        print e
pass

def b64_to_json(str):
    return json.loads(base64.b64decode(str))
pass