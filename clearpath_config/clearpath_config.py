from clearpath_config.system.system import SystemConfig
from clearpath_config.platform.platform import PlatformConfig
from clearpath_config.accessories.accessories import AccessoryConfig
from clearpath_config.mounts.mounts import MountsConfig
from clearpath_config.sensors.sensors import SensorConfig


# ClearpathConfig:
#  - top level configurator
#  - contains
class ClearpathConfig:
    def __init__(self, config: dict = None) -> None:
        self.config = config
        self.version = 0
        self.system = SystemConfig()
        self.platform = PlatformConfig()
        self.accessories = AccessoryConfig()
        self.mounts = MountsConfig()
        self.sensors = SensorConfig()
