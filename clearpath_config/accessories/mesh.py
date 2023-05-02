from clearpath_config.common import Accessory, File
from clearpath_config.accessories.base import BaseAccessory
from typing import List


class Mesh(BaseAccessory):
    ACCESSORY_TYPE = "mesh"
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
        self.visual: File = File(Mesh.VISUAL)
        self.set_visual(visual)

    def set_radius(self, radius: float) -> None:
        msg = "Radius must be a positive float value"
        assert isinstance(radius, float), msg
        assert radius >= 0.0, msg
        self.radius = radius

    def get_radius(self) -> float:
        return self.radius

    def set_visual(self, visual: str) -> None:
        self.visual = File(visual)

    def get_visual(self) -> str:
        return self.visual.get_path()
