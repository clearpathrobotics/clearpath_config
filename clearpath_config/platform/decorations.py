from clearpath_config.common import Accessory
from typing import List


class BaseDecoration(Accessory):
    """
    BaseDecoration
     - enable: whether decoration is enabled or not
     - model: what type of that decoration it is
    """
    DECORATION_MODEL = "base_decoration"
    ENABLED = True
    DEFAULT = "default"
    MODELS = [DEFAULT]

    def __init__(
            self,
            name: str = DECORATION_MODEL,
            enabled: bool = ENABLED,
            model: str = DEFAULT,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(name, parent, xyz, rpy)
        self.enabled: bool = bool(enabled)
        self.model: str = BaseDecoration.DEFAULT
        self.set_model(model)

    def set_enabled(self, enable: bool) -> None:
        self.enable = bool(enable)

    def get_enabled(self) -> bool:
        return self.enabled

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def get_model(self) -> str:
        return self.model

    def set_model(self, model: str) -> None:
        assert model in self.MODELS, (
            "%s model '%s' is not one of: '%s'" % (
                self.DECORATION_MODEL.title(),
                model,
                self.MODELS,
            )
        )
        self.model = model


class Bumper(BaseDecoration):
    """
    Bumper
     - enabled: can be toggled
     - model: can be swapped to a Wibotic charger bumper
     - extension: meters by which it is extended
    """
    DECORATION_MODEL = "bumper"
    EXTENSION = 0.0
    DEFAULT = "default"
    WIBOTIC = "wibotic"
    MODELS = [DEFAULT, WIBOTIC]

    def __init__(
            self,
            name: str = DECORATION_MODEL,
            enabled: bool = BaseDecoration.ENABLED,
            model: str = DEFAULT,
            extension: float = EXTENSION,
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
        self.extension: float = Bumper.EXTENSION
        self.set_extension(extension)

    def get_extension(self) -> float:
        return self.extension

    def set_extension(self, extension: float) -> None:
        try:
            extension = float(extension)
        except ValueError as e:
            raise AssertionError(e.args[0])
        assert isinstance(
            extension, float
        ), " ".join([
            "Bumper extension must be of type float,",
            " unexpected type '%s'" % type(extension)
        ])
        assert extension >= 0, "Bumper extension must be a positive value"
        self.extension = extension


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


class Structure(BaseDecoration):
    """
    Structure:
     - enabled: can be toggled
     - model: type of structure must be selected
    """
    DECORATION_MODEL = "structure"
    DEFAULT = ""
    ARCH_300 = "sensor_arch_300"
    ARCH_510 = "sensor_arch_510"
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


class Decoration():
    BUMPER = Bumper.DECORATION_MODEL
    TOP_PLATE = TopPlate.DECORATION_MODEL
    STRUCTURE = Structure.DECORATION_MODEL

    MODEL = {
        BUMPER: Bumper,
        TOP_PLATE: TopPlate,
        STRUCTURE: Structure
    }

    def __new__(cls, model: str) -> BaseDecoration:
        assert model in Decoration.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                Decoration.MODEL.keys()
            )
        )
        return Decoration.MODEL[model]()
