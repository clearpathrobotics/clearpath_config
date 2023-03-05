from clearpath_config.common import Platform

# DecorationAccessories
class Decorations():

    # General Decorations
    class Bumper():
        '''
        Bumpers on the Husky can be:
            - toggled on/off
            - extended
            - swapped for a Wibotic charger bumper
        '''
        DEFAULT = "default"
        WIBOTIC = "wibotic"
        MODELS = [DEFAULT, WIBOTIC]

        def __init__(self,
                        enable: bool = True,
                        extension: float = 0.0,
                        model: str = DEFAULT) -> None:
            self.enabled = True
            self.extension = 0.0
            self.model = self.DEFAULT
            if enable:
                self.enable()
            if extension:
                self.set_extension(extension)
            if model:
                self.set_model(model)

        def enable(self) -> None:
            self.enabled = True

        def disable(self) -> None:
            self.enabled = False

        def get_extension(self) -> float:
            return self.extension

        def set_extension(self, extension) -> None:
            assert isinstance(extension, float), "Bumper extension must be of type float, unexpected type '%s'" % type(extension)
            self.extension = extension

        def get_model(self) -> str:
            return self.model

        def set_model(self, model: str) -> None:
            assert model in self.MODELS, "Bumper model '%s' is not one of: %s" % (model, self.MODELS)
            self.model = model


    # Husky Specific Decorations
    class A200():
        class TopPlate():
            '''
            Top Plate on the Husky can be:
                - toggled on/off
                - swapped for larger plate and pacs plate
                - PACS plate is required
            '''
            DEFAULT = "default"
            LARGE = "large"
            PACS = "pacs"
            MODELS = [DEFAULT, LARGE, PACS]

            def __init__(self,
                         enable: bool = True,
                         model: str = DEFAULT) -> None:
                self.enabled = True
                self.extension = 0.0
                self.model = self.DEFAULT
                if enable:
                    self.enable()
                if model:
                    self.set_model(model)

            def enable(self) -> None:
                self.enabled = True

            def disable(self) -> None:
                self.enabled = False

            def get_model(self) -> str:
                return self.model

            def set_model(self, model: str) -> None:
                assert model in self.MODELS, "Top plate model '%s' is not one of: %s" % (model, self.MODELS)
                self.model = model

# Base Decorations Config
# - holds the model name for that config
# - to be used by all other configurations.
class BaseDecorationsConfig():

    def __init__(self, model) -> None:
        assert model in Platform.ALL, "Model passed '%s' is not expected. must be one of the following: %s" % (model, Platform.ALL)
        self.model = model

