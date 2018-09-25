import pytest
from unittest.mock import patch


def test_human_bytes():
    from jade_utils.human_tools import human_bytes

    assert human_bytes(1024) == '1.0KiB'
    assert human_bytes(1024*1024) == '1.0MiB'
    assert human_bytes(1024*1024*1024) == '1.0GiB'
    assert human_bytes(1024*1024*1024*1024) == '1.0TiB'
    assert human_bytes(1024*1024*1024*1024*1024) == '1.0PiB'
    assert human_bytes(1024*1024*1024*1024*1024*1024) == '1.0EiB'
    assert human_bytes(1024*1024*1024*1024*1024*1024*1024) == '1.0ZiB'
    assert human_bytes(1024*1024*1024*1024*1024*1024*1024*1024) == '1.0YiB'

    assert human_bytes(1024, ' Bytes') == '1.0Ki Bytes'
