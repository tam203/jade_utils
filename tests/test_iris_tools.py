import os.path

import iris

import pytest
from unittest.mock import patch


def test_human_bytes():
    from jade_utils.iris_tools import estimate_cube_size
    test_cube_path = os.path.join(os.path.dirname(__file__), 'data', 'test.nc')
    test_cube = iris.load_cube(test_cube_path, 'air_temperature')
    assert estimate_cube_size(test_cube) == '407.8KiB'