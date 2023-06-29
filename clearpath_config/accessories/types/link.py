from clearpath_config.common.types.accessory import Accessory
from clearpath_config.accessories.types.accessory import BaseAccessory
from typing import List


class Link(BaseAccessory):
    ACCESSORY_TYPE = "link"

    def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseAccessory.XYZ,
            offset_rpy: List[float] = BaseAccessory.RPY
            ) -> None:
        super().__init__(
            name,
            parent,
            xyz,
            rpy,
            offset_xyz,
            offset_rpy
        )
