from clearpath_config.common import Accessory
from typing import List


class BaseMount(Accessory):
    MOUNT_MODEL = "base_mount"

    def __init__(
        self,
        name: str,
        parent: str = Accessory.PARENT,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
    ) -> None:
        super().__init__(name, parent, xyz, rpy)

    @classmethod
    def get_mount_model(cls) -> str:
        return cls.MOUNT_MODEL

    @classmethod
    def get_name_from_idx(cls, idx: int) -> str:
        return "%s_%s" % (
            cls.get_mount_model(),
            idx
        )
