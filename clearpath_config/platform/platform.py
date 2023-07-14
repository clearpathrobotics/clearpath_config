from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.platform.extras import ExtrasConfig
from clearpath_config.platform.attachments.config import BaseAttachmentsConfig
from clearpath_config.platform.attachments.mux import AttachmentsConfigMux


class PlatformConfig(BaseConfig):

    PLATFORM = "platform"
    # Controllers
    PS4 = "ps4"
    LOGITECH = "logitech"
    CONTROLLER = "controller"
    ATTACHMENTS = "attachments"
    # Extras
    EXTRAS = "extras"

    TEMPLATE = {
        PLATFORM: {
            CONTROLLER: CONTROLLER,
            ATTACHMENTS: ATTACHMENTS,
            EXTRAS: EXTRAS
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        # PLATFORM
        CONTROLLER: PS4,
        ATTACHMENTS: {},
        EXTRAS: ExtrasConfig.DEFAULTS
    }

    def __init__(
            self,
            config: dict = {},
            controller: str = DEFAULTS[CONTROLLER],
            attachments: str = DEFAULTS[ATTACHMENTS],
            extras: str = DEFAULTS[EXTRAS]
            ) -> None:
        # Initialization
        self._config = {}
        self.controller = controller
        self.attachments = attachments
        self.extras = extras
        # Setter Template
        setters = {
            self.KEYS[self.CONTROLLER]: PlatformConfig.controller,
            self.KEYS[self.ATTACHMENTS]: PlatformConfig.attachments,
            self.KEYS[self.EXTRAS]: PlatformConfig.extras
        }
        super().__init__(setters, config, self.PLATFORM)

    def update(self, serial_number=False) -> None:
        if serial_number:
            # Reload attachments
            self.attachments = None
            # TODO: Set PACS Profile

    @property
    def controller(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.CONTROLLER],
            value=self._controller
        )
        return self._controller

    @controller.setter
    def controller(self, value: str) -> None:
        assert value.lower() in [self.PS4, self.LOGITECH], (
            "'%s' controller is invalid. Must be one of: '%s'" % (
                value.lower(),
                [self.PS4, self.LOGITECH]))
        self._controller = value.lower()

    @property
    def attachments(self) -> BaseAttachmentsConfig:
        self.set_config_param(
            key=self.KEYS[self.ATTACHMENTS],
            value=self._attachments.config[self.ATTACHMENTS]
        )
        return self._attachments

    @attachments.setter
    def attachments(self, value: dict) -> None:
        self._attachments = AttachmentsConfigMux(
            BaseConfig._SERIAL_NUMBER.get_model(), value)

    @property
    def extras(self) -> ExtrasConfig:
        self.set_config_param(
            key=self.KEYS[self.EXTRAS],
            value=self._extras.config[self.EXTRAS]
        )
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

    def get_controller(self) -> str:
        return self.controller

    def get_unit_number(self) -> str:
        return BaseConfig._SERIAL_NUMBER.get_unit()

    def get_model(self) -> str:
        return BaseConfig._SERIAL_NUMBER.get_model()
