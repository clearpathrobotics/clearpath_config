from clearpath_config.common.types.accessory import Accessory
from clearpath_config.platform.types.attachment import BaseAttachment
from typing import List


class TopPlate(BaseAttachment):
    """
    TopPlate
     - enabled: can be toggled
     - model: can be swapped to a large or PACS plate
    """
    ATTACHMENT_MODEL = "top_plate"
    DEFAULT = "default"
    LARGE = "large"
    PACS = "pacs"
    MODELS = [DEFAULT, LARGE, PACS]

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            enabled: bool = BaseAttachment.ENABLED,
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
