import base64
import json

def json_to_b64(obj):
    return base64.b64encode(json.dumps(obj))
pass

def b64_to_json(str):
    return json.loads(base64.b64decode(str))
pass