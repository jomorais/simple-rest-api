#!/usr/bin/python
__author__ = 'joaci'
import pytest

from utils.utils import *


def test_key_checker():
    my_dict = {"key_a": "aaa", "key_b": "bbb", "key_c": 0, "key_d": 0.1, "key_e": {}}

    assert key_checker(['key_a', 'key_b', 'key_c', 'key_d', 'key_e'], mydict=my_dict) is True

    assert key_checker(['key_b', 'key_c', 'key_d', 'key_e'], mydict=my_dict) is True

    assert key_checker(['key_a'], mydict=my_dict) is True

    with pytest.raises(Exception):
        key_checker('key_a', mydict=my_dict)

    with pytest.raises(Exception):
        key_checker(['key_a'], mydict='')

    assert key_checker(['key_a', 'key_b', 'key_c', 'key_d', 'key_e', 'key_f'], mydict=my_dict) is False

    assert key_checker(['key_b', 'key_c', 'key_d', 'key_e', 'key_f'], mydict=my_dict) is False
