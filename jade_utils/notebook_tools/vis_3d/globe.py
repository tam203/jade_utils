from __future__ import division
import os
import json
from  IPython.display import HTML
import iris
import numpy as np
import uuid

try:
    from urllib.parse import quote # python 3
except ImportError:
    from urllib import quote # python 2

target_grid = None
this_dir = os.path.dirname(__file__)

def plot_raw(data):
    callback_name = 'callback_' + str(uuid.uuid1())[:8]
    url = '../jade_ex/static/vis_3d/globe.html?callback=' + callback_name
    html = """
        <script type="text/javascript">
            function {callback_name}(){{
                return {data};
            }}
        </script>
        <iframe src="{url}" width="805", height="405"></iframe>
        """.format(callback_name=callback_name, url=url, data=json.dumps(data));
    return HTML(html)

def dummy_data():
    dummy_data = []
    size = 480000
    for i in range(size):
        r = int((i*1.0/size) *  255)
        b, g, a = 0, 0, 255
        dummy_data += [r, g, b, a]
    return dummy_data

def plot_cube(cube):
    global target_grid
    if len(cube.dim_coords) != 2:
        raise Exception('Cube must be `flat` i.e. have only two dim_coords')

    if not target_grid:
        target_grid = iris.load_raw(os.path.join(this_dir, 'grid.pp'))[0]

    regrided_data = cube.regrid(target_grid, iris.analysis.Linear())
    data = regrided_data.data
    cdata = data.flatten()
    the_max = np.max(cdata)
    the_min = np.min(cdata)
    the_range = the_max - the_min
    norm = lambda x: (x - the_min) / the_range
    rgba = []
    for c in cdata:
        r = int(norm(c)*255)
        b, g, a = 0, 0, 255
        rgba += [r, g, b, a]

    return plot_raw(rgba)
