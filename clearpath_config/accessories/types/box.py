from clearpath_config.common.types.accessory import Accessory
from clearpath_config.accessories.types.accessory import BaseAccessory
from typing import List


class Box(BaseAccessory):
    ACCESSORY_TYPE = "box"
    SIZE = [0.01, 0.01, 0.01]

    def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            size: List[float] = SIZE,
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
        self.size: List[float] = Box.SIZE
        self.set_size(size)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['size'] = self.get_size()
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'size' in d:
            self.set_size(d['size'])

    def set_size(self, size: List[float]) -> None:
        msg = "Box size must be a list of three positive floats"
        Accessory.assert_valid_triplet(size, msg)
        assert all([i >= 0.0 for i in size]), msg
        self.size = size

    def get_size(self) -> List[float]:
        return self.size
