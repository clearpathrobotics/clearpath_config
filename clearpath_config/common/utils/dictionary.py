from typing import MutableMapping
from functools import reduce
import operator


def _flatten_dict_gen(d, parent_key, dlim):
    for k, v in d.items():
        new_key = parent_key + dlim + str(k) if parent_key else str(k)
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, dlim=dlim).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = '', dlim: str = '.'):
    return dict(_flatten_dict_gen(d, parent_key, dlim))


def merge_dict(a, b, path=None):
    "merges b into a"
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def _unflatten_dict_gen(d: dict, k: str, v: object, dlim: str = '.'):
    keys = k.split(dlim)
    if len(keys) > 1:
        return _unflatten_dict_gen()


def unflatten_dict(d: MutableMapping, parent_key: str = '', dlim: str = '.'):
    _d = {}
    for k, v in d.items():
        _d_curr = {}
        _d_next = {}
        keys = k.split(dlim)
        keys.reverse()
        for i, _ in enumerate(keys):
            _d_next[keys[i]] = v if i == 0 else _d_curr
            _d_curr = _d_next
            _d_next = {}
        merge_dict(_d, _d_curr)
    return _d


def flip_dict(d: MutableMapping, parent_key: str = '', dlim: str = '.'):
    flat = flatten_dict(d, parent_key, dlim)
    flip = {}
    for k, v in flat.items():
        assert isinstance(v, str), (
            "Flipping dictionary requires all values to be of type 'str'"
        )
        flip[v] = k
    return flip


def get_from_dict(d, map):
    return reduce(operator.getitem, map, d)


def is_in_dict(d, map):
    try:
        get_from_dict(d, map)
    except KeyError:
        return False
    return True


def set_in_dict(d, map, val):
    # get_from_dict(d, map[:-1])[map[-1]] = val
    for key in map[:-1]:
        d = d.setdefault(key, {})
    d[map[-1]] = val
