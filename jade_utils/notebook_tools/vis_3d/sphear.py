from IPython.display import Javascript
import os.path
import json
with open(os.path.join(os.path.dirname(__file__), 'sphear.py')) as fp:
js = fp.read();

def return_a_thing():
    ele_id = 'content'
    data = []
    for i in range(32):
        for j in range(32):
            r=0
            g=i*j%255
            b=0
            a=255
            data = data + [r, g, b, a]

    json.dumps(data)
    code = js.replace("%ELEMENT_ID%", ele_id).repalce("%DATA%", data)

    return Javascript(code)
