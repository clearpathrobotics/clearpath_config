
from clearpath_config.common import Accessory
from typing import List


class BaseMount(Accessory):
    MOUNTING_LINK = None

    def __init__(
        self,
        name: str,
        model: str,
        parent: str = Accessory.PARENT,
        mounting_link: str = MOUNTING_LINK,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
    ) -> None:
        super().__init__(name, parent, xyz, rpy)
        self.model = model
        self.mounting_link = "%s_mount" % self.get_name()
        if mounting_link:
            self.set_mounting_link(mounting_link)

    def get_model(self) -> str:
        return self.model

    def get_mounting_link(self) -> str:
        return self.mounting_link

    def set_mounting_link(self, mounting_link: str) -> None:
        self.assert_valid_link(mounting_link)
        self.mounting_link = mounting_link
