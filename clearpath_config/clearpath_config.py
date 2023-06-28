from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.serial_number import SerialNumber
from clearpath_config.system.system import SystemConfig
from clearpath_config.platform.platform import PlatformConfig
# from clearpath_config.accessories.accessories import AccessoryConfig
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
    }

    def __init__(self, config: dict | str = None) -> None:
        # Initialization
        self._config = {}
        self._system = SystemConfig()
        self.serial_number = self.DEFAULTS[self.SERIAL_NUMBER]
        self.version = self.DEFAULTS[self.VERSION]
        # Setter Template
        setters = {
            self.SERIAL_NUMBER: self.setter(ClearpathConfig.serial_number),
            self.VERSION: self.setter(ClearpathConfig.version),
            self.SYSTEM: self.setter(ClearpathConfig.system),
        }
        # Set from Config
        super().__init__(setters, config)
        # self.version = 0
        # self.serial_number.from_dict(config)
        # self.system = SystemConfig()
        # self.platform = PlatformConfig()
        # # self.accessories = AccessoryConfig()
        # # self.mounts = MountsConfig()
        # # self.sensors = SensorConfig()

    @BaseConfig.config.getter
    def config(self) -> dict:
        self.set_config_param(self.SYSTEM, self._system.config[self.SYSTEM])
        return super().config

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
        return self._system

    @system.setter
    def system(self, config: dict) -> None:
        self._system = SystemConfig(config)
