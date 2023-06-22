from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.host import Host
from clearpath_config.common.types.hostname import Hostname
from clearpath_config.common.types.ip import IP
from clearpath_config.common.types.list import ListConfig
from clearpath_config.common.types.serial_number import SERIAL_NUMBER
from clearpath_config.common.utils.dictionary import flip_dict
from typing import List


# HostListConfig
# - list of hosts
class HostListConfig(ListConfig[Host, IP]):
    def __init__(self) -> None:
        super().__init__(
            uid=lambda obj: obj.get_hostname(),
            obj_type=Host,
            uid_type=str
        )

    def to_dict(self) -> dict:
        hostdict = {}
        for host in self.get_all():
            hostdict[host.get_hostname()] = host.get_ip()
        return hostdict


# HostsConfig
# - these are the hosts that are involved in this system
class HostsConfig(BaseConfig):

    HOSTS = "hosts"
    SELF = "self"
    PLATFORM = "platform"
    ONBOARD = "onboard"
    REMOTE = "remote"

    TEMPLATE = {
        HOSTS: {
            SELF: SELF,
            PLATFORM: PLATFORM,
            ONBOARD: ONBOARD,
            REMOTE: REMOTE,
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        KEYS[SELF]: SERIAL_NUMBER.get_serial(),
        KEYS[PLATFORM]: {
            SERIAL_NUMBER.get_serial(): "192.168.131.1"
        },
        KEYS[ONBOARD]: {},
        KEYS[REMOTE]: {}
    }

    def __init__(
            self,
            config: dict = {},
            selfhost: str | Hostname = DEFAULTS[KEYS[SELF]],
            platform: dict | Host = DEFAULTS[KEYS[PLATFORM]],
            onboard: dict | List[Host] = DEFAULTS[KEYS[ONBOARD]],
            remote: dict | List[Host] = DEFAULTS[KEYS[REMOTE]],
            ) -> None:
        # Initialization
        self._config = {}
        self.self = selfhost
        self.platform = platform
        self.onboard = onboard
        self.remote = remote
        # Setter Template
        setters = {
            self.KEYS[self.SELF]: self.setter(HostsConfig.self),
            self.KEYS[self.PLATFORM]: self.setter(HostsConfig.platform),
            self.KEYS[self.ONBOARD]: self.setter(HostsConfig.onboard),
            self.KEYS[self.REMOTE]: self.setter(HostsConfig.remote)
        }
        # Set from Config
        super().__init__(setters, config, self.HOSTS)

    # Self:
    # - the hostname of the computer running this config
    @property
    def self(self) -> str:
        return str(self._self)

    @self.setter
    def self(self, value: str | Hostname) -> None:
        if isinstance(value, str):
            self._self = Hostname(value)
        elif isinstance(value, Hostname):
            self._self = value
        else:
            assert isinstance(value, str) or isinstance(value, Hostname), (
                "Self must be of type 'str' or 'Hostname'"
            )
        self.set_config_param(
            key=self.KEYS[self.SELF],
            value=self.self
        )

    # Platform:
    # - the main computer for this system (i.e. the robot's computer)
    @property
    def platform(self) -> dict:
        return self._platform.to_dict()

    @platform.setter
    def platform(self, value: dict | Host) -> None:
        if isinstance(value, dict):
            entry = [{'hostname': k, 'ip': v} for k, v in value.items()]
            assert len(entry) == 1, (
                "Platform must only be one hostname, ip pair"
            )
            self._platform = Host(
                hostname=entry[0]['hostname'],
                ip=entry[0]['ip'])
        elif isinstance(value, Host):
            self._platform = value
        else:
            assert isinstance(value, dict) or isinstance(value, Host), (
                "Platform must be of type 'dict' or 'Host'"
            )
        self.set_config_param(
            key=self.KEYS[self.PLATFORM],
            value=self.platform
        )

    @property
    def platform_ip(self) -> str:
        return self._platform.get_ip()

    @platform_ip.setter
    def platform_ip(self, value: str):
        self._platform.set_ip(value)
        self.config[self.KEYS[self.PLATFORM]] = self.platform

    @property
    def platform_hostname(self) -> str:
        return self._platform.get_hostname()

    @platform_hostname.setter
    def platform_hostname(self, value: str) -> None:
        self._platform.set_hostname(value)

    # Onboard:
    # - these are additional on-board computer
    @property
    def onboard(self) -> HostListConfig:
        return self._onboard

    @onboard.setter
    def onboard(self, value: dict | List[Host] | HostListConfig) -> None:
        if isinstance(value, dict):
            onboard = HostListConfig()
            onboard.set_all([Host(k, v) for k, v in value.items()])
            self._onboard = onboard
        elif isinstance(value, list):
            assert all([isinstance(i, Host) for i in value]), (
                "Onboard hosts passed as list must be of type 'List[Host]'"
            )
            onboard = HostListConfig()
            onboard.set_all(value)
            self._onboard = value

        elif isinstance(value, HostListConfig):
            self._onboard = value
        else:
            assert ((
                isinstance(value, dict)) or (
                isinstance(value, list)) or (
                isinstance(value, HostListConfig))), (
                "Onboard hosts must be of type '%s', '%s' or '%s'" % (
                    dict.__name__, list.__name__, HostListConfig.__name__
                )
            )
        self.set_config_param(
            key=self.KEYS[self.ONBOARD],
            value=self.onboard.to_dict()
        )

    # Remote:
    # - these are remote machines which need to interact with the system
    # - ex. laptops or other robots
    @property
    def remote(self) -> HostListConfig:
        return self._remote

    @remote.setter
    def remote(self, value: dict | List[Host] | HostListConfig) -> None:
        if isinstance(value, dict):
            remote = HostListConfig()
            remote.set_all([Host(k, v) for k, v in value.items()])
            self._remote = remote
        elif isinstance(value, list):
            assert all([isinstance(i, Host) for i in value]), (
                "Remote hosts passed as list must be of type 'List[Host]'"
            )
            remote = HostListConfig()
            remote.set_all(value)
            self._remote = value

        elif isinstance(value, HostListConfig):
            self._remote = value
        else:
            assert ((
                isinstance(value, dict)) or (
                isinstance(value, list)) or (
                isinstance(value, HostListConfig))), (
                "Remote hosts must be of type '%s', '%s' or '%s'" % (
                    dict.__name__, list.__name__, HostListConfig.__name__
                )
            )
        self.set_config_param(
            key=self.KEYS[self.REMOTE],
            value=self.remote.to_dict()
        )
