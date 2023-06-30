from clearpath_config.common.types.list import ListConfig
from clearpath_config.common.utils.dictionary import merge_dict
from clearpath_config.platform.types.decoration import BaseDecoration
from clearpath_config.platform.types.bumper import Bumper
from clearpath_config.platform.types.structure import Structure
from clearpath_config.platform.types.top_plate import TopPlate
from typing import List


class DecorationListConfig(ListConfig[BaseDecoration, str]):
    def __init__(self) -> None:
        super().__init__(
            uid=lambda obj: obj.get_name(),
            obj_type=BaseDecoration,
            uid_type=str
        )

    def to_dict(self) -> dict:
        d = {}
        for decoration in self.get_all():
            merge_dict(d, decoration.to_dict())
        return d


# Base Decorations Config
# - to be used by all other configurations.
class BaseDecorationsConfig:

    def __init__(self) -> None:
        # Standard Platform Decorations
        self.__bumpers = ListConfig[Bumper, str](
            uid=ListConfig.uid_name,
            obj_type=Bumper,
            uid_type=str)
        self.__top_plates = ListConfig[TopPlate, str](
            uid=ListConfig.uid_name,
            obj_type=TopPlate,
            uid_type=str)
        self.__structures = ListConfig[Structure, str](
            uid=ListConfig.uid_name,
            obj_type=Structure,
            uid_type=str)

    def to_dict(self):
        d = {}
        for decoration in self.get_all():
            merge_dict(d, decoration)
        return d

    @property
    def top_plates(self):
        return self.__top_plates

    @top_plates.setter
    def top_plates(self, value: List[TopPlate] | ListConfig) -> None:
        if isinstance(value, list):
            self.__top_plates.set_all(value)
        elif isinstance(value, ListConfig):
            self.__top_plates = value
        else:
            assert isinstance(value, list) or isinstance(value, ListConfig), (
                "Top plates must be list of 'TopPlate' or 'ListConfig'"
            )

    @property
    def bumpers(self):
        return self.__bumpers

    @bumpers.setter
    def bumpers(self, value: List[Bumper] | ListConfig) -> None:
        if isinstance(value, list):
            self.__bumpers.set_all(value)
        elif isinstance(value, ListConfig):
            self.__bumpers = value
        else:
            assert isinstance(value, list) or isinstance(value, ListConfig), (
                "Bumpers must be list of 'Bumper' or 'ListConfig'"
            )

    @property
    def structures(self):
        return self.__structures

    @structures.setter
    def structures(self, value: List[Structure] | ListConfig) -> None:
        if isinstance(value, list):
            self.__structures.set_all(value)
        elif isinstance(value, ListConfig):
            self.__structures = value
        else:
            assert isinstance(value, list) or isinstance(value, ListConfig), (
                "Structures must be list of 'Structure' or 'ListConfig'"
            )

    def get_all(self) -> List[BaseDecoration]:
        decorations = []
        decorations.extend(self.bumpers.get_all())
        decorations.extend(self.top_plates.get_all())
        decorations.extend(self.structures.get_all())
        return decorations
