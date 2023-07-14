from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.file import File
from clearpath_config.links.types.link import BaseLink
from typing import List


class Mesh(BaseLink):
    LINK_TYPE = "mesh"
    VISUAL = "empty.stl"
    # COLLISION = "empty.stl"

    def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            visual: float = VISUAL,
            # collision: float = COLLISION,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseLink.OFFSET_XYZ,
            offset_rpy: List[float] = BaseLink.OFFSET_RPY
            ) -> None:
        super().__init__(
            name,
            parent,
            xyz,
            rpy,
            offset_xyz,
            offset_rpy
        )
        self.visual: File = File(Mesh.VISUAL)
        self.set_visual(visual)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['visual'] = self.get_visual()
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'visual' in d:
            self.set_visual(d['visual'])

    def set_visual(self, visual: str) -> None:
        self.visual = File(visual)

    def get_visual(self) -> str:
        return self.visual.get_path()
