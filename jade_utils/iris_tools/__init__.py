"""Tools for working with iris cubes."""
import functools
import operator
from ..human_tools import human_bytes


def estimate_cube_size(cube, humanize=True):
    """Estimate the total size of an iris cube.

    Take an iris cube and estimate how much memory or disk would be needed to store the whole
    cube with no compression.

    This is likely to underestimate as it only predicts the data storage and doesn't include the
    metadata or dimensions.

    Args:
        cube (iris.cube.Cube): The cube you wish to estimate the size of.
        humanize (bool, optional): Convert the size into a human readable string. Defaults to True

    Returns:
        str/int: The estimated cube size. Will return a string if humanized or an int if not.

    Examples:
        >>> print(estimate_cube_size(cube))
        8.0GiB

    """
    num_points = functools.reduce(operator.mul, cube.shape, 1)
    num_bytes = 0
    dtype = cube[(0, ) * len(cube.shape)].data.dtype
    if dtype == 'float16':
        num_bytes = 16
    if dtype == 'float32':
        num_bytes = 32
    if dtype == 'float64':
        num_bytes = 64
    total_bytes = (num_points * num_bytes) / 8
    if humanize:
        return human_bytes(total_bytes)
    return total_bytes
