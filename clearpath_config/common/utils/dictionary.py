# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
# @copyright (c) 2023, Clearpath Robotics, Inc., All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Clearpath Robotics nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
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
    """Merge dict b into dict a."""
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
        if isinstance(v, dict):
            v = unflatten_dict(v, parent_key, dlim)
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
    for key in map[:-1]:
        d = d.setdefault(key, {})
    d[map[-1]] = val


def extend_dict(a: dict, b: dict):
    for key, value in flatten_dict(b).items():
        keys = key.split(".")
        set_in_dict(a, keys, value)
    return a


def extend_flat_dict(a: dict, b: dict):
    for key, value in flatten_dict(b).items():
        a[key] = value
    return a
