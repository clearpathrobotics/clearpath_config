from clearpath_config.common import Accessory
from clearpath_config.accessories.base import BaseAccessory
from typing import List


class Cylinder(BaseAccessory):
    ACCESSORY_TYPE = "cylinder"
    RADIUS = 0.01
    LENGTH = 0.01

    def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            radius: float = RADIUS,
            length: float = LENGTH,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseAccessory.OFFSET_XYZ,
            offset_rpy: List[float] = BaseAccessory.OFFSET_RPY
            ) -> None:
        super().__init__(
            name,
            parent,
            xyz,
            rpy,
            offset_xyz,
            offset_rpy
        )
        self.radius: float = Cylinder.RADIUS
        self.set_radius(radius)
        self.length: float = Cylinder.LENGTH
        self.set_length(length)

    def set_radius(self, radius: float) -> None:
        msg = "Radius must be a positive float value"
        assert isinstance(radius, float), msg
        assert radius >= 0.0, msg
        self.radius = radius

    def get_radius(self) -> float:
        return self.radius

    def set_length(self, length: float) -> None:
        msg = "Length must be a positive float value"
        assert isinstance(length, float), msg
        assert length >= 0.0, msg
        self.length = length

    def get_length(self) -> float:
        return self.length
