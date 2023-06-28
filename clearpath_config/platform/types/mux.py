from clearpath_config.platform.types.decoration import BaseDecoration
from clearpath_config.platform.types.bumper import Bumper
from clearpath_config.platform.types.structure import Structure
from clearpath_config.platform.types.top_plate import TopPlate


class DecorationMux():
    BUMPER = Bumper.DECORATION_MODEL
    TOP_PLATE = TopPlate.DECORATION_MODEL
    STRUCTURE = Structure.DECORATION_MODEL

    MODEL = {
        BUMPER: Bumper,
        TOP_PLATE: TopPlate,
        STRUCTURE: Structure
    }

    def __new__(cls, model: str) -> BaseDecoration:
        assert model in DecorationMux.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                DecorationMux.MODEL.keys()
            )
        )
        return DecorationMux.MODEL[model]()
