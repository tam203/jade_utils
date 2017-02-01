from __future__ import division
import os
import json
from  IPython.display import HTML
import iris
import numpy as np
import uuid
from collections import OrderedDict

try:
    from urllib.parse import quote # python 3
except ImportError:
    from urllib import quote # python 2

target_grid = None
this_dir = os.path.dirname(__file__)
data_store = OrderedDict()

def add_to_data_holder(data, id):
    data_store[id] = data
    while len(data_store) > 5:
        del data_store[data_store.keys()[0]]

def get_from_data_holder_and_delete(id):
    data = data_store[id]
    del data_store[id]
    return data

def get_from_data_holder_as_json(id):
    return json.dumps(get_from_data_holder(id))

def plot_raw(data, cmap=None):
    data_id = str(uuid.uuid1())[:8]
    callback_name = 'callback_' + data_id
    add_to_data_holder(data, data_id)
    url = '../jade_ex/static/vis_3d/globe.html?callback=' + callback_name
    if cmap:
        url += '&cmap=' + cmap
    code = """'from jade_utils.notebook_tools.vis_3d import globe;' +
                'print(globe.get_from_data_holder_and_delete("{data_id}"))'""".format(data_id=data_id)
    html = """
        <script type="text/javascript">
            function {callback_name}(callback){{
                // Comment
                Jupyter.notebook.kernel.execute(
                    {code},
                    {{
                        iopub : {{
                            output : callback
                        }}
                    }}
                );

            }}
        </script>
        <iframe src="{url}" width="805", height="405"></iframe>
        """.format(callback_name=callback_name, url=url, data=json.dumps(data), code=code);
    return HTML(html)

def dummy_data():
    dummy_data = []
    size = 480000
    for i in range(size):
        r = int((i*1.0/size) *  255)
        b, g, a = 0, 0, 200
        dummy_data += [r, g, b, a]
    return dummy_data

def plot_cube(cube, cmap=None):
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
        if not np.ma.is_masked(c):
            r = int(norm(c)*255)
            a = 200
        else:
            r = 0
            a = 0
        b, g = 0, 0
        rgba += [r, g, b, a]

    return plot_raw(rgba, cmap)
