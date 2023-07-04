from clearpath_config.platform.types.decoration import BaseDecoration
from clearpath_config.common.types.accessory import Accessory
from typing import List


class Structure(BaseDecoration):
    """
    Structure:
     - enabled: can be toggled
     - model: type of structure must be selected
    """
    DECORATION_MODEL = "structure"
    ARCH_300 = "sensor_arch_300"
    ARCH_510 = "sensor_arch_510"
    DEFAULT = ARCH_300
    ENABLED = False
    MODELS = [DEFAULT, ARCH_300, ARCH_510]

    def __init__(
            self,
            name: str = DECORATION_MODEL,
            enabled: bool = BaseDecoration.ENABLED,
            model: str = DEFAULT,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(
            name,
            enabled,
            model,
            parent,
            xyz,
            rpy
        )
