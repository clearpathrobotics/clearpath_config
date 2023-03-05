from clearpath_config.system.system import SystemConfig
from clearpath_config.platform.platform import PlatformConfig

# ClearpathConfig: 
#  - top level configurator
#  - contains 
class ClearpathConfig():

    def __init__(self, config: dict = None) -> None:
        self.config = config
        self.version = 0
        self.system = SystemConfig()
        self.platform = PlatformConfig()
        #self.mounts = MountsConfig()
        #self.sensors = SensorsConfig()
