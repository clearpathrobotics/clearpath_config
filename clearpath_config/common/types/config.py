from clearpath_config.common.types.serial_number import SerialNumber
from clearpath_config.common.utils.dictionary import (
    flatten_dict,
    get_from_dict,
    is_in_dict,
    set_in_dict
)
from typing import Any


class BaseConfig:
    _SERIAL_NUMBER = SerialNumber("generic")
    _VERSION = 0
    DLIM = "."

    def __init__(
            self,
            template: dict,
            config: dict = {},
            parent_key: str = None,
            ) -> None:
        # Dictionaries are Stored Flat
        self.template = template
        self._parent_key = parent_key
        if self._parent_key is not None and self._parent_key not in config:
            self._config = {self._parent_key: {}}
        self.config = config

    def update(
            self,
            serial_number=False,
            ) -> None:
        """Update any variables based on inputs"""
        return

    @property
    def template(self) -> dict:
        """Return template configuration dictionary"""
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
        """Return configuration dictionary"""
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
