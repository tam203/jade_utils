import os
import base64
import json
from  IPython.display import IFrame

try:
    from urllib.parse import quote # python 3
except ImportError:
    from urllib import quote # python 2


def plot(data=None):
    this_dir = os.path.dirname(__file__)
    textures_dir = os.path.join(this_dir, 'textures')
    html = open(os.path.join(this_dir, 'globe.html')).read()

    # Inject textures
    for filename in os.listdir(textures_dir):
        filepath =  os.path.join(textures_dir, filename)
        ext = os.path.splitext(filename)[1].replace('.','')
        encoded = base64.b64encode(open(filepath, "rb").read())
        data_url = "data:image/{};base64,{}".format(ext, encoded)

        html = html.replace('%{}%'.format(filename), data_url)

    # inject data
    if data is None:
        dummy_data = []
        size = 480000
        for i in range(size):
            r = int((i*1.0/size) *  255)
            b, g, a = 0, 0, 255
            dummy_data += [r, g, b, a]
        data = dummy_data

    html = html.replace(r'%data%', json.dumps(data))
    html_data_url = quote(unicode(html).encode('utf-8'), safe='~()*!.\'')

    return IFrame(html_data_url, width = 805, height = 405)
