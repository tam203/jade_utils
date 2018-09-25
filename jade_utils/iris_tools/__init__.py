import functools
import operator
from ..human_tools import human_bytes


def estimate_cube_size(cube):
    num_points = functools.reduce(operator.mul, cube.shape, 1)
    num_bytes = 0
    dtype = cube[(0, ) * len(cube.shape)].data.dtype
    if dtype == 'float16':
        num_bytes = 16
    if dtype == 'float32':
        num_bytes = 32
    if dtype == 'float64':
        num_bytes = 64
    return human_bytes((num_points * num_bytes) / 8)
