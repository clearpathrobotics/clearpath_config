from clearpath_config.common.types.accessory import Accessory
from clearpath_config.accessories.types.accessory import BaseAccessory
from typing import List


class Sphere(BaseAccessory):
    ACCESSORY_TYPE = "sphere"
    RADIUS = 0.01

    def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            radius: float = RADIUS,
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
        self.radius: float = Sphere.RADIUS
        self.set_radius(radius)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['radius'] = self.get_radius()
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'radius' in d:
            self.set_radius(d['radius'])

    def set_radius(self, radius: float) -> None:
        msg = "Radius must be a positive float value"
        assert isinstance(radius, float), msg
        assert radius >= 0.0, msg
        self.radius = radius

    def get_radius(self) -> float:
        return self.radius
