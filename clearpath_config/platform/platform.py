from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.platform.extras import ExtrasConfig
from clearpath_config.platform.decorations.config import BaseDecorationsConfig
from clearpath_config.platform.decorations.mux import DecorationsConfigMux


class PlatformConfig(BaseConfig):

    PLATFORM = "platform"
    # Controllers
    PS4 = "ps4"
    LOGITECH = "logitech"
    CONTROLLER = "controller"
    DECORATIONS = "decorations"
    # Extras
    EXTRAS = "extras"

    TEMPLATE = {
        PLATFORM: {
            CONTROLLER: CONTROLLER,
            DECORATIONS: DECORATIONS,
            EXTRAS: EXTRAS
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        # PLATFORM
        CONTROLLER: PS4,
        DECORATIONS: {},
        EXTRAS: ExtrasConfig.DEFAULTS
    }

    def __init__(
            self,
            config: dict = {},
            controller: str = DEFAULTS[CONTROLLER],
            decorations: str = DEFAULTS[DECORATIONS],
            extras: str = DEFAULTS[EXTRAS]
            ) -> None:
        # Initialization
        self._config = {}
        self.controller = controller
        self.decorations = decorations
        self.extras = extras
        # Setter Template
        setters = {
            self.KEYS[self.CONTROLLER]:
                self.setter(PlatformConfig.controller),
            self.KEYS[self.DECORATIONS]:
                self.setter(PlatformConfig.decorations),
            self.KEYS[self.EXTRAS]:
                self.setter(PlatformConfig.extras)
        }
        super().__init__(setters, config, self.PLATFORM)

    @property
    def controller(self) -> str:
        return self._controller

    @controller.setter
    def controller(self, value: str) -> None:
        assert value.lower() in [self.PS4, self.LOGITECH], (
            "'%s' controller is invalid. Must be one of: '%s'" % (
                value.lower(),
                [self.PS4, self.LOGITECH]))
        self._controller = value.lower()
        self.set_config_param(
            key=self.KEYS[self.CONTROLLER],
            value=self.controller
        )

    @property
    def decorations(self) -> BaseDecorationsConfig:
        return self._decorations

    @decorations.setter
    def decorations(self, value: dict) -> None:
        self._decorations = DecorationsConfigMux(
            BaseConfig._SERIAL_NUMBER.get_model(), value)
        self.set_config_param(
            key=self.KEYS[self.DECORATIONS],
            value=self.decorations.config
        )

    @property
    def extras(self) -> ExtrasConfig:
        return self._extras

    @extras.setter
    def extras(self, value: dict | ExtrasConfig) -> None:
        if isinstance(value, dict):
            self._extras = ExtrasConfig(config=value)
        elif isinstance(value, ExtrasConfig):
            self._extras = value
        else:
            assert isinstance(value, dict) or (
                    isinstance(value, ExtrasConfig)), (
                "Extras must be of type 'dict' or 'ExtrasConfig'"
            )
        self.set_config_param(
            key=self.KEYS[self.EXTRAS],
            value=self.extras.config[self.EXTRAS]
        )
