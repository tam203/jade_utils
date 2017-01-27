import os
import base64
import json
from  IPython.display import IFrame
import iris

try:
    from urllib.parse import quote # python 3
except ImportError:
    from urllib import quote # python 2

target_grid = None

def plot(data=None):
    this_dir = os.path.dirname(__file__)
    textures_dir = os.path.join(this_dir, 'textures')
    html = open(os.path.join(this_dir, 'globe.html')).read()

    # Inject textures
    for filename in os.listdir(textures_dir):
        filepath =  os.path.join(textures_dir, filename)
        ext = os.path.splitext(filename)[1].replace('.','')
        encoded = base64.b64encode(open(filepath, "rb").read()).decode('utf-8')
        data_url = "data:image/{};base64,{}".format(ext, str(encoded))

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

    html_data_url = quote(html.encode('UTF-8'), safe='~()*!.\'')
    src = "data:text/html;charset=UTF-8,{}".format(html_data_url)
    return IFrame(src, width = 805, height = 405)

def plot_cube(cube):
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

    return plot(rgba)
