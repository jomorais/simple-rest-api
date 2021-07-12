#!/usr/bin/python
__author__ = 'joaci'


def key_checker(keys: list, mydict):
    if type(keys) != list:
        raise Exception("keys must be a list: keys=['key_1', 'key_2', ..., 'key_n']")
    if type(mydict) != dict:
        raise Exception("keys must be a dict: dict={'key_1': 'value_1', 'key_2': 'value_2', ..., 'key_n': 'value_n'}}")
    if all(k in mydict for k in keys):
        return True
    return False



