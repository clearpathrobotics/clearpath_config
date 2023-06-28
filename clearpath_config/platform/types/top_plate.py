from clearpath_config.common.types.accessory import Accessory
from clearpath_config.platform.types.decoration import BaseDecoration
from typing import List


class TopPlate(BaseDecoration):
    """
    TopPlate
     - enabled: can be toggled
     - model: can be swapped to a large or PACS plate
    """
    DECORATION_MODEL = "top_plate"
    DEFAULT = "default"
    LARGE = "large"
    PACS = "pacs"
    MODELS = [DEFAULT, LARGE, PACS]

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
