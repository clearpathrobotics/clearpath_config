from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.serial_number import SerialNumber
from clearpath_config.common.utils.yaml import read_yaml, write_yaml
from clearpath_config.system.system import SystemConfig
from clearpath_config.platform.platform import PlatformConfig
from clearpath_config.accessories.accessories import AccessoryConfig
from clearpath_config.mounts.mounts import MountsConfig
from clearpath_config.sensors.sensors import SensorConfig


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
        SYSTEM: SystemConfig.DEFAULTS,
        PLATFORM: PlatformConfig.DEFAULTS,
        ACCESSORIES: AccessoryConfig.DEFAULTS,
        MOUNTS: MountsConfig.DEFAULTS,
        SENSORS: SensorConfig.DEFAULTS,
        SERIAL_NUMBER: "generic",
        VERSION: 0,
    }

    def __init__(self, config: dict | str = None) -> None:
        # Read YAML
        config = self.read(config)
        # Initialization
        self._config = {}
        self.system = self.DEFAULTS[self.SYSTEM]
        self.platform = self.DEFAULTS[self.PLATFORM]
        self.accessories = self.DEFAULTS[self.ACCESSORIES]
        self.mounts = self.DEFAULTS[self.MOUNTS]
        self.sensors = self.DEFAULTS[self.SENSORS]
        self.serial_number = self.DEFAULTS[self.SERIAL_NUMBER]
        self.version = self.DEFAULTS[self.VERSION]
        # Setter Template
        setters = {
            self.SYSTEM: ClearpathConfig.system,
            self.PLATFORM: ClearpathConfig.platform,
            self.ACCESSORIES: ClearpathConfig.accessories,
            self.MOUNTS: ClearpathConfig.mounts,
            self.SENSORS: ClearpathConfig.sensors,
            self.SERIAL_NUMBER: ClearpathConfig.serial_number,
            self.VERSION: ClearpathConfig.version,
        }
        # Set from Config
        super().__init__(setters, config)

    def read(self, file: str | dict) -> None:
        self._file = None
        if isinstance(file, dict):
            return file
        self._file = file
        return read_yaml(file)

    def write(self, file: str) -> None:
        write_yaml(file)

    @property
    def serial_number(self) -> str:
        self.set_config_param(
            self.SERIAL_NUMBER,
            str(BaseConfig._SERIAL_NUMBER.get_serial()))
        return BaseConfig._SERIAL_NUMBER.get_serial()

    @serial_number.setter
    def serial_number(self, sn: str) -> None:
        BaseConfig._SERIAL_NUMBER = SerialNumber(sn)
        self._system.update(serial_number=True)
        self._platform.update(serial_number=True)
        self._accessories.update(serial_number=True)
        self._mounts.update(serial_number=True)
        self._sensors.update(serial_number=True)

    @property
    def version(self) -> int:
        self.set_config_param(self.VERSION, self._version)
        return self._version

    @version.setter
    def version(self, v: int) -> None:
        assert isinstance(v, int), (
            "version must be of type 'int'"
        )
        self._version = v
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

    @property
    def mounts(self) -> MountsConfig:
        self.set_config_param(
            self.MOUNTS,
            self._mounts.config[self.MOUNTS])
        return self._mounts

    @mounts.setter
    def mounts(self, value: dict) -> None:
        self._mounts = MountsConfig(value)

    @property
    def sensors(self) -> SensorConfig:
        self.set_config_param(
            self.SENSORS,
            self._sensors.config[self.SENSORS])
        return self._sensors

    @sensors.setter
    def sensors(self, value: dict) -> None:
        self._sensors = SensorConfig(value)
