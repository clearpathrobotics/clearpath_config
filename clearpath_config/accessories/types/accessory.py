from clearpath_config.common.types.accessory import Accessory
from typing import List


class BaseAccessory(Accessory):
    """
    Base Accessory Class
      - inherits from Accessory
      - contains all common parameters shared by all accessories
      - accessories have no mounting points
      - accessories have no drivers
      - accessories can be of the following types:
        - link: just a frame without any visual component
        - box:
        - cylinder:
        - sphere:
        - mesh:
      - accessories `name` MUST be specified
    """
    ACCESSORY_TYPE = "base"
    OFFSET_XYZ = [0.0, 0.0, 0.0]
    OFFSET_RPY = [0.0, 0.0, 0.0]

    def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = OFFSET_XYZ,
            offset_rpy: List[float] = OFFSET_RPY
            ) -> None:
        super().__init__(name, parent, xyz, rpy)
        self.offset_xyz: List[float] = BaseAccessory.OFFSET_XYZ
        self.set_offset_xyz(offset_xyz)
        self.offset_rpy: List[float] = BaseAccessory.OFFSET_RPY
        self.set_offset_rpy(offset_rpy)

    def to_dict(self) -> dict:
        d = {}
        d['name'] = self.get_name()
        d['parent'] = self.get_parent()
        d['xyz'] = self.get_xyz()
        d['rpy'] = self.get_rpy()
        return d

    def from_dict(self, d: dict) -> None:
        if 'name' in d:
            self.set_name(d['name'])
        if 'parent' in d:
            self.set_parent(d['parent'])
        if 'xyz' in d:
            self.set_xyz(d['xyz'])
        if 'rpy' in d:
            self.set_rpy(d['rpy'])

    @classmethod
    def get_accessory_type(cls) -> str:
        return cls.ACCESSORY_TYPE

    def set_offset_xyz(self, xyz: List[float]) -> None:
        Accessory.assert_valid_triplet(
            xyz,
            "Offset XYZ must be a list of exactly three float values"
        )
        self.offset_xyz = xyz

    def get_offset_xyz(self) -> List[float]:
        return self.offset_xyz

    def set_offset_rpy(self, rpy: List[float]) -> None:
        Accessory.assert_valid_triplet(
            rpy,
            "Offset RPY must be a list of exactly three float values"
        )
        self.offset_rpy = rpy
