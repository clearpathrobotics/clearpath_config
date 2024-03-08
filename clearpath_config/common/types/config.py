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
from clearpath_config.common.types.serial_number import SerialNumber
from clearpath_config.common.types.namespace import Namespace
from clearpath_config.common.utils.dictionary import (
    flatten_dict,
    get_from_dict,
    is_in_dict,
    set_in_dict,
    unflatten_dict
)
from typing import Any


class BaseConfig:
    _SERIAL_NUMBER = SerialNumber("generic")
    _NAMESPACE = Namespace()
    _VERSION = 0
    DLIM = "."

    def __init__(
            self,
            template: dict,
            config: dict = {},
            parent_key: str = None,
            ) -> None:
        # Dictionaries are Stored Flat
        self._config = {}
        self.template = template
        self._parent_key = parent_key
        if self._parent_key is not None and self._parent_key not in config:
            self._config = {self._parent_key: {}}
        self.config = config

    def update(
            self,
            serial_number=False,
            ) -> None:
        """Update any variables based on inputs."""
        return

    @property
    def template(self) -> dict:
        """Return template configuration dictionary."""
        return self._template

    @template.setter
    def template(self, value: dict) -> None:
        assert isinstance(value, dict), (
            "template must of type 'dict'"
        )
        # Check that template has all properties
        flat_template = flatten_dict(d=value, dlim=BaseConfig.DLIM)
        for _, val in flat_template.items():
            assert isinstance(val, property), (
                "All entries in template must be properties"
            )
        self._template = value

    @property
    def config(self) -> dict:
        """Return configuration dictionary."""
        for _, prop in flatten_dict(
                d=self.template, dlim=BaseConfig.DLIM).items():
            self.getter(prop)()
        return self._config

    @config.setter
    def config(self, value: dict) -> None:
        if value is None:
            return
        assert isinstance(value, dict), (
            "config must be of type 'dict'"
        )
        if self._parent_key is not None and self._parent_key not in value:
            value = {self._parent_key: value}
        value = unflatten_dict(value)
        for map, prop in flatten_dict(
                d=self.template, dlim=BaseConfig.DLIM).items():
            keys = map.split(BaseConfig.DLIM)
            if is_in_dict(value, keys):
                self.setter(prop)(get_from_dict(value, keys))

    def setter(self, prop: property):
        return prop.fset.__get__(self)

    def getter(self, prop: property):
        return prop.fget.__get__(self)

    def set_config_param(self, key: str, value: Any) -> None:
        keys = key.split(BaseConfig.DLIM)
        set_in_dict(d=self._config, map=keys, val=value)

    @classmethod
    def get_serial_number(cls, prefix: bool = False) -> str:
        return BaseConfig._SERIAL_NUMBER.get_serial(prefix=prefix)

    @classmethod
    def set_serial_number(cls, sn: str) -> None:
        BaseConfig._SERIAL_NUMBER = SerialNumber(sn)

    @classmethod
    def get_unit_number(cls) -> str:
        return BaseConfig._SERIAL_NUMBER.get_unit()

    @classmethod
    def get_platform_model(cls) -> str:
        return BaseConfig._SERIAL_NUMBER.get_model()

    @classmethod
    def get_namespace(cls) -> str:
        return str(BaseConfig._NAMESPACE)

    @classmethod
    def set_namespace(cls, namespace: str | Namespace) -> None:
        if isinstance(namespace, Namespace):
            BaseConfig._NAMESPACE = namespace
        elif isinstance(namespace, str):
            BaseConfig._NAMESPACE = Namespace(namespace)
        else:
            assert isinstance(namespace, str) or isinstance(namespace, Namespace), (
                "Namespace must be of type 'str' or 'Namespace'"
            )
