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

    def get_model(self) -> str:
        return self.MOUNT_MODEL
