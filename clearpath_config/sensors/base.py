from clearpath_config.common import Accessory, List

class BaseSensor(Accessory):

    def __init__(
        self,
        name: str,
        parent: str = Accessory.PARENT,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
        ) -> None:
        super().__init__(name, parent, xyz, rpy)

