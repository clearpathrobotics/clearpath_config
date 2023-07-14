from clearpath_config.common.types.accessory import Accessory
from clearpath_config.links.types.link import BaseLink
from typing import List


class Frame(BaseLink):
    LINK_TYPE = "frame"

    def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseLink.XYZ,
            offset_rpy: List[float] = BaseLink.RPY
            ) -> None:
        super().__init__(
            name,
            parent,
            xyz,
            rpy,
            offset_xyz,
            offset_rpy
        )
