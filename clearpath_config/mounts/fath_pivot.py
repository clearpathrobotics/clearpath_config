
from clearpath_config.common import Accessory
from clearpath_config.mounts.base import BaseMount
from math import pi
from typing import List


class FathPivot(BaseMount):
    MOUNT_MODEL = "fath_pivot"
    # Default Values
    ANGLE = 0.0

    def __init__(
        self,
        parent: str = Accessory.PARENT,
        angle: float = ANGLE,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
    ) -> None:
        super().__init__(
            name=FathPivot.get_name_from_idx(0),
            parent=parent,
            xyz=xyz,
            rpy=rpy)
        self.angle = 0.0
        if angle:
            self.set_angle(angle)

    def get_angle(self) -> float:
        return self.angle

    def set_angle(self, angle: float) -> None:
        assert -pi < angle <= pi, (
            "Angle '%s' must be in radian and  between pi and -pi"
        )
        self.angle = angle
