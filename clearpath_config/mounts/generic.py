from clearpath_config.common import Accessory
from typing import List


# Generic
class Generic:
    class Box(Accessory):
        def __init__(
                self,
                name: str,
                parent: str = ...,
                xyz: List[float] = ...,
                rpy: List[float] = ...
                ) -> None:
            super().__init__(name, parent, xyz, rpy)

    # Cylinder
    class Cylinder(Accessory):
        def __init__(
                self,
                name: str,
                parent: str = ...,
                xyz: List[float] = ...,
                rpy: List[float] = ...
                ) -> None:
            super().__init__(name, parent, xyz, rpy)
    # Sphere
