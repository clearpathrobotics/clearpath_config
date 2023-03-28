# DecorationAccessories
class Decorations:
    # General Decorations
    class Bumper:
        """
        Bumpers on the Husky can be:
            - toggled on/off
            - extended
            - swapped for a Wibotic charger bumper
        """

        DEFAULT = "default"
        WIBOTIC = "wibotic"
        MODELS = [DEFAULT, WIBOTIC]

        def __init__(
                self,
                name: str,
                enable: bool = True,
                extension: float = 0.0,
                model: str = DEFAULT
                ) -> None:
            self.name = name
            self.enabled = True
            self.extension = 0.0
            self.model = self.DEFAULT
            if enable:
                self.enable()
            if extension:
                self.set_extension(extension)
            if model:
                self.set_model(model)

        def get_name(self) -> str:
            return self.name

        def set_name(self, name) -> None:
            self.name = name

        def enable(self) -> None:
            self.enabled = True

        def disable(self) -> None:
            self.enabled = False

        def get_extension(self) -> float:
            return self.extension

        def set_extension(self, extension) -> None:
            try:
                extension = float(extension)
            except ValueError as e:
                raise AssertionError(e.args[0])
            assert isinstance(
                extension, float
            ), "Bumper extension must be of type float, unexpected type '%s'" % type(
                extension
            )
            assert extension >= 0, "Bumper extension must be a positive value"
            self.extension = extension

        def get_model(self) -> str:
            return self.model

        def set_model(self, model: str) -> None:
            assert model in self.MODELS, "Bumper model '%s' is not one of: %s" % (
                model,
                self.MODELS,
            )
            self.model = model

    class TopPlate:
        """
        Top Plate on the Husky can be:
            - toggled on/off
            - swapped for larger plate and pacs plate
            - PACS plate is required
        """

        DEFAULT = "default"
        LARGE = "large"
        PACS = "pacs"
        MODELS = [DEFAULT, LARGE, PACS]

        def __init__(
                self,
                name: str,
                enable: bool = True,
                model: str = DEFAULT
                ) -> None:
            self.name = name
            self.enabled = True
            self.extension = 0.0
            self.model = self.DEFAULT
            if enable:
                self.enable()
            if model:
                self.set_model(model)

        def set_name(self, name: str) -> None:
            self.name = name

        def get_name(self) -> str:
            return self.name

        def enable(self) -> None:
            self.enabled = True

        def disable(self) -> None:
            self.enabled = False

        def get_model(self) -> str:
            return self.model

        def set_model(self, model: str) -> None:
            assert (
                model in self.MODELS
            ), "Top plate model '%s' is not one of: %s" % (model, self.MODELS)
            self.model = model
