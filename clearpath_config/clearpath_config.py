from clearpath_config.base.config import BaseConfig
from clearpath_config.base.keys import Keys
from clearpath_config.utils import read_yaml, write_yaml

# HostsConfig
# - these are the hosts that are involved in this system
class HostsConfig(BaseConfig):

    def __init__(self, config) -> None:
        super().__init__(name=Keys.HOSTS, config=config)
        self.required_keys = [Keys.PLATFORM]
        self.optional_keys = [Keys.ONBOARD, Keys.REMOTE]

    # Self:
    # - the hostname of the computer this config was made/is running on. 
    def get_self(self) -> str:
        _self = self.get_key(Keys.SELF)
        assert Keys.is_valid(Keys.SELF, _self)
        return _self

    def set_self(self, _self) -> bool:
        return self.set_key(Keys.PLATFORM, _self)

    # Platform:
    # - the main computer for tis system (i.e. the robot's computer)
    def get_platform(self) -> tuple:
        platform = self.get_key(Keys.PLATFORM)
        assert Keys.is_valid(Keys.PLATFORM, platform)
        hostname, ip = list(platform.items())[0]
        return hostname, ip

    def get_platform_hostname(self) -> str:
        hostname, _ = self.get_platform()
        return hostname

    def get_platform_ip(self) -> str:
        _, ip = self.get_platform()
        return ip

    def set_platform(self, platform: tuple) -> bool:
        entry = {platform[0]: platform[2]}
        return self.set_key(Keys.PLATFORM, entry)

    def set_platform_hostname(self, hostname: str) -> bool:
        ip = self.get_platform_ip()
        entry = {hostname: ip}
        return self.set_key(Keys.PLATFORM, entry)

    def set_platform_ip(self, ip: str) -> bool:
        hostname = self.get_platform_hostname()
        entry = {hostname: ip}
        return self.set_key(Keys.PLATFORM, entry)

    # Onboard:
    # - these are additional on-board computer
    def get_onboard(self) -> list:
        onboard = self.get_key(Keys.ONBOARD)
        if onboard == None:
            return []
        else:
            return onboard

class SystemConfig(BaseConfig):

    def __init__(self, config) -> None:
        super().__init__(name=Keys.SYSTEM, config=config)
        self.required_keys = [Keys.SELF, Keys.HOSTS]
        self.hosts = HostsConfig(self.get_key(Keys.HOSTS))

    def update_config(self):
        self.set_key(Keys.HOSTS, self.hosts)


class PlatformConfig():
    pass

class MountsConfig():
    pass

class SensorsConfig():
    pass


# ClearpathConfig: 
#  - top level configurator
#  - contains 
class ClearpathConfig(BaseConfig):

    def __init__(self, config) -> None:
        super().__init__(name=Keys.SYSTEM, config=config)
        self.version = 0
        # Sub-Level Configs
        self.system = SystemConfig(self.get_key(Keys.SYSTEM))
        #self.platform = PlatformConfig()
        #self.mounts = MountsConfig()
        #self.sensors = SensorsConfig()

def main():
    test_config = "/home/lcamero/Scripts/clearpath_config/test_config.yaml"
    clearpath_config = ClearpathConfig(config=read_yaml(test_config))
    print("Platform:", clearpath_config.system.hosts.get_platform())
    print("  hostname: ", clearpath_config.system.hosts.get_platform_hostname())
    print("  ip: ", clearpath_config.system.hosts.get_platform_ip())
    print()
    clearpath_config.system.hosts.set_platform_hostname("TEST_HOST")
    print("Platform:", clearpath_config.system.hosts.get_platform())
    print("  hostname: ", clearpath_config.system.hosts.get_platform_hostname())
    print("  ip: ", clearpath_config.system.hosts.get_platform_ip())
    print()
    clearpath_config.system.hosts.set_platform_ip("TEST_IP")
    print("Platform:", clearpath_config.system.hosts.get_platform())
    print("  hostname: ", clearpath_config.system.hosts.get_platform_hostname())
    print("  ip: ", clearpath_config.system.hosts.get_platform_ip())
    print()

main()