from IPython.display import Javascript
import os.path
import json
from math import sqrt

with open(os.path.join(os.path.dirname(__file__), 'sphear.js')) as fp:
    js = fp.read();

def show(data):
    ele_id = 'content'
    if not sqrt(len(data)) % 1 == 0:
        raise Exception("length of 'data' must be a square number")
    code = _get_code(data, ele_id)


    return Javascript(code)

def _get_code(data, ele_id):
    code = """element.append("<div id='%s'></div>");\n""" % ele_id
    code += js.replace("%ELEMENT_ID%", ele_id).replace("%DATA%", json.dumps(data))
    return code
