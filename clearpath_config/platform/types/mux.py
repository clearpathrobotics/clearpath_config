from clearpath_config.platform.types.attachment import BaseAttachment
from clearpath_config.platform.types.bumper import Bumper
from clearpath_config.platform.types.structure import Structure
from clearpath_config.platform.types.top_plate import TopPlate


class AttachmentMux():
    BUMPER = Bumper.ATTACHMENT_MODEL
    TOP_PLATE = TopPlate.ATTACHMENT_MODEL
    STRUCTURE = Structure.ATTACHMENT_MODEL

    MODEL = {
        BUMPER: Bumper,
        TOP_PLATE: TopPlate,
        STRUCTURE: Structure
    }

    def __new__(cls, model: str) -> BaseAttachment:
        assert model in AttachmentMux.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                AttachmentMux.MODEL.keys()
            )
        )
        return AttachmentMux.MODEL[model]()
