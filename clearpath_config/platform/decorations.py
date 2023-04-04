class BaseDecoration:
    """
    BaseDecoration
     - enable: whether decoration is enabled or not
     - model: what type of that decoration it is
    """
    DECORATION_MODEL = "base_decoration"
    DEFAULT = "default"
    MODELS = [DEFAULT]

    def __init__(
            self,
            name: str = DECORATION_MODEL,
            enabled: bool = False,
            model: str = DEFAULT
            ) -> None:
        self.enabled: bool = bool(enabled)
        self.name: str = BaseDecoration.DECORATION_MODEL
        self.set_name(name)
        self.model: str = BaseDecoration.DEFAULT
        self.set_model(model)

    def get_name(self) -> str:
        return self.name

    def set_name(self, name) -> None:
        self.name = name

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
    DEFAULT = "default"
    WIBOTIC = "wibotic"
    MODELS = [DEFAULT, WIBOTIC]

    def __init__(
            self,
            name: str = DECORATION_MODEL,
            enabled: bool = False,
            model: str = DEFAULT,
            extension: float = 0.0,
            ) -> None:
        super().__init__(name, enabled, model)
        self.extension: float = 0.0
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
            enabled: bool = False,
            model: str = DEFAULT
            ) -> None:
        super().__init__(name, enabled, model)
