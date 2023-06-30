from clearpath_config.common.types.accessory import Accessory, IndexedAccessory
from typing import List


class BaseMount(IndexedAccessory):
    MOUNT_MODEL = "base_mount"

    def __init__(
        self,
        idx: int = None,
        name: str = None,
        parent: str = Accessory.PARENT,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
    ) -> None:
        super().__init__(idx, name, parent, xyz, rpy)

    def to_dict(self) -> dict:
        d = {}
        d['parent'] = self.get_parent()
        d['xyz'] = self.get_xyz()
        d['rpy'] = self.get_rpy()
        return d

    def from_dict(self, d: dict) -> None:
        if 'parent' in d:
            self.set_parent(d['parent'])
        if 'xyz' in d:
            self.set_xyz(d['xyz'])
        if 'rpy' in d:
            self.set_rpy(d['rpy'])

    @classmethod
    def get_mount_model(cls) -> str:
        return cls.MOUNT_MODEL

    @classmethod
    def get_name_from_idx(cls, idx: int) -> str:
        return "%s_%s" % (
            cls.get_mount_model(),
            idx
        )
