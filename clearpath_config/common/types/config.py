from clearpath_config.common.utils.dictionary import (
    flatten_dict,
    get_from_dict,
    is_in_dict,
    set_in_dict
)
from typing import Any, Callable


class BaseConfig:
    DLIM = "."

    def __init__(
            self,
            template: dict,
            config: dict = {},
            parent_key: str = None,
            ) -> None:
        # Dictionaries are Stored Flat
        self.template = template
        if parent_key is not None:
            if parent_key not in config:
                config = {parent_key: config}
        self.config = config

    @property
    def template(self) -> dict:
        """Return template configuration dictionary"""
        return self._template

    @template.setter
    def template(self, value: dict) -> None:
        assert isinstance(value, dict), (
            "template must of type 'dict'"
        )
        # Check that template has all callable leaves
        flat_template = flatten_dict(d=value, dlim=BaseConfig.DLIM)
        for _, val in flat_template.items():
            assert isinstance(val, Callable), (
                "All entries in template must be Callable setters"
            )
        self._template = value

    @property
    def config(self) -> dict:
        """Return configuration dictionary"""
        return self._config

    @config.setter
    def config(self, value: dict) -> None:
        assert isinstance(value, dict), (
            "config must be of type 'dict'"
        )
        for map, setter in flatten_dict(
                d=self.template, dlim=BaseConfig.DLIM).items():
            if is_in_dict(value, map.split(BaseConfig.DLIM)):
                setter(get_from_dict(value, map.split(BaseConfig.DLIM)))

    def setter(self, prop: property):
        return prop.fset.__get__(self)

    def set_config_param(self, key: str, value: Any) -> None:
        keys = key.split(BaseConfig.DLIM)
        set_in_dict(d=self.config, map=keys, val=value)
