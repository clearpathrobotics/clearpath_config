from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.serial_number import SerialNumber
from clearpath_config.system.system import SystemConfig
from clearpath_config.platform.platform import PlatformConfig
from clearpath_config.accessories.accessories import AccessoryConfig
# from clearpath_config.mounts.mounts import MountsConfig
# from clearpath_config.sensors.sensors import SensorConfig


# ClearpathConfig:
#  - top level configurator
#  - contains
class ClearpathConfig(BaseConfig):

    VERSION = "version"
    SERIAL_NUMBER = "serial_number"
    SYSTEM = "system"
    PLATFORM = "platform"
    ACCESSORIES = "accessories"
    MOUNTS = "mounts"
    SENSORS = "sensors"

    TEMPLATE = {
        VERSION: VERSION,
        SERIAL_NUMBER: SERIAL_NUMBER,
        SYSTEM: SYSTEM,
        PLATFORM: PLATFORM,
        ACCESSORIES: ACCESSORIES,
        MOUNTS: MOUNTS,
        SENSORS: SENSORS
    }

    KEYS = TEMPLATE

    DEFAULTS = {
        VERSION: 0,
        SERIAL_NUMBER: "generic",
        SYSTEM: SystemConfig.DEFAULTS,
        PLATFORM: PlatformConfig.DEFAULTS,
        ACCESSORIES: AccessoryConfig.DEFAULTS,
    }

    def __init__(self, config: dict | str = None) -> None:
        # Initialization
        self._config = {}
        self.version = self.DEFAULTS[self.VERSION]
        self.serial_number = self.DEFAULTS[self.SERIAL_NUMBER]
        self.system = self.DEFAULTS[self.SYSTEM]
        self.platform = self.DEFAULTS[self.PLATFORM]
        self.accessories = self.DEFAULTS[self.ACCESSORIES]
        # Setter Template
        setters = {
            self.SERIAL_NUMBER: ClearpathConfig.serial_number,
            self.VERSION: ClearpathConfig.version,
            self.SYSTEM: ClearpathConfig.system,
            self.PLATFORM: ClearpathConfig.platform,
            self.ACCESSORIES: ClearpathConfig.accessories,
        }
        # Set from Config
        super().__init__(setters, config)

    @property
    def serial_number(self) -> str:
        return BaseConfig._SERIAL_NUMBER.get_serial()

    @serial_number.setter
    def serial_number(self, sn: str) -> None:
        BaseConfig._SERIAL_NUMBER = SerialNumber(sn)
        self.set_config_param(self.SERIAL_NUMBER, self.serial_number)
        # Add propagators here

    @property
    def version(self) -> int:
        return self._version

    @version.setter
    def version(self, v: int) -> None:
        assert isinstance(v, int), (
            "version must be of type 'int'"
        )
        self._version = v
        self.set_config_param(self.VERSION, self.version)
        # Add propagators here

    @property
    def system(self) -> SystemConfig:
        self.set_config_param(
            self.SYSTEM,
            self._system.config[self.SYSTEM])
        return self._system

    @system.setter
    def system(self, config: dict) -> None:
        self._system = SystemConfig(config)

    @property
    def platform(self) -> PlatformConfig:
        self.set_config_param(
            self.PLATFORM,
            self._platform.config[self.PLATFORM])
        return self._platform

    @platform.setter
    def platform(self, config: dict) -> None:
        self._platform = PlatformConfig(config)

    @property
    def accessories(self) -> AccessoryConfig:
        self.set_config_param(
            self.ACCESSORIES,
            self._accessories.config[self.ACCESSORIES])
        return self._accessories

    @accessories.setter
    def accessories(self, value: dict) -> None:
        self._accessories = AccessoryConfig(value)
