import yaml


class SystemConfig():
    pass

class PlatformConfig():
    pass

class MountsConfig():
    pass

class SensorsConfig():
    pass

# ClearpathConfig: 
#  - top level configurator
#  - contains 
class ClearpathConfig():
    def __init__(self, config) -> None:
        self.version = 0
        # Sub-Level Configs
        self.system = SystemConfig()
        self.platform = PlatformConfig()
        self.mounts = MountsConfig()
        self.sensors = SensorsConfig()

