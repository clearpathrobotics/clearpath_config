# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
# @copyright (c) 2024, Clearpath Robotics, Inc., All rights reserved.
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
import copy

from typing import Callable, List

from clearpath_config.common.types.accessory import Accessory, IndexedAccessory
from clearpath_config.common.utils.dictionary import flatten_dict, unflatten_dict


class BaseManipulator(IndexedAccessory):
    MANIPULATOR_MODEL = 'base'
    MANIPULATOR_TYPE = 'manipulator'
    ROS_PARAMETERS = {}
    ROS_PARAMETERS_TEMPLATE = {}

    class ROSParameter:
        def __init__(
                self,
                key: str,
                get: Callable,
                set: Callable  # noqa:A002
                ) -> None:
            self.key = key
            self.get = get
            self.set = set

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            ros_parameters: dict = ROS_PARAMETERS,
            ros_parameters_template: dict = ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # ROS Parameters
        self.ros_parameters_template = ros_parameters_template
        self.ros_parameters = ros_parameters
        super().__init__(idx, name, parent, xyz, rpy)

    def to_dict(self) -> dict:
        d = {}
        d['model'] = self.get_manipulator_model()
        d['parent'] = self.get_parent()
        d['xyz'] = self.get_xyz()
        d['rpy'] = self.get_rpy()
        d['ros_parameters'] = self.get_ros_parameters()
        return d

    def from_dict(self, d: dict) -> None:
        if 'parent' in d:
            self.set_parent(d['parent'])
        if 'xyz' in d:
            self.set_xyz(d['xyz'])
        if 'rpy' in d:
            self.set_rpy(d['rpy'])
        if 'ros_parameters' in d:
            self.set_ros_parameters(d['ros_parameters'])

    @classmethod
    def get_manipulator_model(cls) -> str:
        return cls.MANIPULATOR_MODEL

    @classmethod
    def get_manipulator_type(cls) -> str:
        return cls.MANIPULATOR_TYPE

    @classmethod
    def get_name_from_idx(cls, idx: int) -> str:
        return '%s_%s' % (
            cls.get_manipulator_type(),
            idx
        )

    @property
    def ros_parameters_template(self) -> dict:
        return self._ros_parameters_template

    @ros_parameters_template.setter
    def ros_parameters_template(self, d: dict) -> None:
        assert isinstance(d, dict), ('Template must be of type "dict"')
        # Check that template has all properties
        flat = flatten_dict(d)
        for _, val in flat.items():
            assert isinstance(val, property), (
                'All entries in template must be properties.'
            )
        self._ros_parameters_template = d

    @property
    def ros_parameters(self) -> dict:
        d = flatten_dict(copy.deepcopy(self._ros_parameters))
        for key, prop in flatten_dict(self.ros_parameters_template).items():
            d[key] = self.getter(prop)()
        d = unflatten_dict(d)
        for node_name in d:
            d[node_name] = flatten_dict(d[node_name])
        return d

    @ros_parameters.setter
    def ros_parameters(self, d: dict) -> None:
        assert isinstance(d, dict), ('ROS paramaters must be a dictionary')
        for d_k, d_v in flatten_dict(d).items():
            for key, prop in flatten_dict(self.ros_parameters_template).items():
                if d_k == key:
                    self.setter(prop)(d_v)
        self._ros_parameters = d

    def set_ros_parameters(self, d: dict) -> None:
        self.ros_parameters = d

    def get_ros_parameters(self) -> dict:
        return self.ros_parameters

    def setter(self, prop: property):
        return prop.fset.__get__(self)

    def getter(self, prop: property):
        return prop.fget.__get__(self)
