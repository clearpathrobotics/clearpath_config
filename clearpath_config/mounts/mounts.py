from clearpath_config.common import ListConfig
from clearpath_config.mounts.base import BaseMount
from clearpath_config.mounts.fath_pivot import FathPivot
from clearpath_config.mounts.flir_ptu import FlirPTU
from typing import List


class Mount():
    FATH_PIVOT = FathPivot.MODEL
    FLIR_PTU = FlirPTU.MODEL
    MODEL = {
        FATH_PIVOT: FathPivot,
        FLIR_PTU: FlirPTU,
    }

    def __new__(cls, name: str, model: str) -> BaseMount:
        assert model in Mount.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                Mount.MODEL.keys()
            )
        )
        return Mount.MODEL[model](name)


class MountsConfig:
    def __init__(self, mounts: List[BaseMount] = []) -> None:
        self.__mounts = ListConfig[BaseMount, str](
            uid=lambda obj: obj.get_name()
        )
        self.set_mounts(mounts)

    def get_mount(
            self,
            name: str,
            ) -> BaseMount:
        return self.__mounts.get(name)

    def get_mounts(self) -> List[BaseMount]:
        return self.__mounts.get_all()

    def set_mount(
            self,
            mount: BaseMount,
            ) -> None:
        self.__mounts.set(mount)

    def set_mounts(self, mounts: List[BaseMount]) -> None:
        self.__mounts.set_all(mounts)

    def add_mount(
            self,
            # By Object
            mount: BaseMount = None,
            # By Required Parameters
            name: str = None,
            model: str = None,
            ) -> None:
        assert mount or (name and model), (
            "Mount object or name and model must be passed."
        )
        if (name and model) and not mount:
            mount = Mount(name, model)
        self.__mounts.add(mount)

    def remove_mount(
            self,
            mount: BaseMount = None,
            name: str = None
            ) -> None:
        assert mount or name, (
            "Mount object or name must be passed."
        )
        if name and not mount:
            self.__mounts.remove(name)
        else:
            self.__mounts.remove(mount)
