from clearpath_config.parser import ConfigParser
from clearpath_config.system import SystemConfig, Host
from clearpath_config.utils import read_yaml, write_yaml

# ClearpathConfig: 
#  - top level configurator
#  - contains 
class ClearpathConfig():

    def __init__(self, config: dict = None) -> None:
        self.config = config
        self.version = 0
        self.system = ConfigParser.load_system_config(config)
        #self.platform = PlatformConfig()
        #self.mounts = MountsConfig()
        #self.sensors = SensorsConfig()

    def load_config(self, config: dict):
        self.config = config

    def export_config(self) -> dict:
        config = {}
        return config
