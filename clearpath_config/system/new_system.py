from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.domain_id import DomainID
from clearpath_config.common.types.namespace import Namespace
from clearpath_config.common.types.username import Username
from clearpath_config.common.types.rmw_implementation import RMWImplementation
from clearpath_config.common.types.serial_number import SERIAL_NUMBER
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.system.new_hosts import HostsConfig


class SystemConfig(BaseConfig):

    SYSTEM = "system"
    HOSTS = HostsConfig.HOSTS
    SELF = "self"
    ROS2 = "ros2"
    USERNAME = "username"
    NAMESPACE = "namespace"
    DOMAIN_ID = "domain_id"
    RMW = "rmw_implementation"
    WORKSPACES = "workspaces"

    TEMPLATE = {
        SYSTEM: {
            SELF: SELF,
            HOSTS: HOSTS,
            ROS2: {
                USERNAME: USERNAME,
                NAMESPACE: NAMESPACE,
                DOMAIN_ID: DOMAIN_ID,
                RMW: RMW,
                WORKSPACES: WORKSPACES
            }
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        # SELF: platform hostname (serial number)
        KEYS[SELF]: SERIAL_NUMBER.get_serial(),
        # HOSTS: platform hostname (serial number) at 192.168.131.1
        KEYS[HOSTS]: {"platform": {
            SERIAL_NUMBER.get_serial(): "192.168.131.1"}},
        # USERNAME: administrator
        KEYS[USERNAME]: "administrator",
        # NAMESPACE: serial number
        KEYS[NAMESPACE]: Namespace.clean(SERIAL_NUMBER.get_serial()),
        # DOMAIN_ID: 0
        KEYS[DOMAIN_ID]: 0,
        # RMW: "rmw_fastrtps_cpp"
        KEYS[RMW]: "rmw_fastrtps_cpp"
    }

    def __init__(
            self,
            config: dict = {},
            selfhost: str = DEFAULTS[KEYS[SELF]],
            hosts: dict = DEFAULTS[KEYS[HOSTS]],
            username: str = DEFAULTS[KEYS[USERNAME]],
            namespace: str = DEFAULTS[KEYS[NAMESPACE]],
            domain_id: int = DEFAULTS[KEYS[DOMAIN_ID]],
            rmw_implementation: str = DEFAULTS[KEYS[RMW]],
            ) -> None:
        # Initialization
        self._config = {}
        self.hosts = hosts
        self.username = username
        self.namespace = namespace
        self.domain_id = domain_id
        self.rmw_implementation = rmw_implementation
        # Setter Template
        setters = {
            self.KEYS[self.HOSTS]: self.setter(SystemConfig.hosts),
            self.KEYS[self.USERNAME]: self.setter(SystemConfig.username),
            self.KEYS[self.NAMESPACE]: self.setter(SystemConfig.namespace),
            self.KEYS[self.DOMAIN_ID]: self.setter(SystemConfig.domain_id),
            self.KEYS[self.RMW]: self.setter(SystemConfig.rmw_implementation),
        }
        # Set from Config
        super().__init__(setters, config, self.SYSTEM)

    @property
    def hosts(self) -> HostsConfig:
        return self._hosts

    @hosts.setter
    def hosts(self, value: dict | HostsConfig) -> None:
        if isinstance(value, dict):
            self._hosts = HostsConfig(config=value)
        elif isinstance(value, HostsConfig):
            self._hosts = value
        else:
            assert isinstance(value, dict) or isinstance(value, HostsConfig), (
                "Hosts must be of type 'dict' or 'HostsConfig'        "
            )
        self.set_config_param(
            key=self.KEYS[self.HOSTS],
            value=self.hosts.config[self.HOSTS]
        )

    @property
    def username(self) -> str:
        return str(self._username)

    @username.setter
    def username(self, value: str | Username) -> None:
        if isinstance(value, str):
            self._username = Username(value)
        elif isinstance(value, Username):
            self._username = value
        else:
            assert isinstance(value, str) or isinstance(value, Username), (
                "Username must be of type 'str' or 'Username'"
            )
        self.set_config_param(
            key=self.KEYS[self.USERNAME],
            value=self.username
        )

    @property
    def namespace(self) -> str:
        return str(self._namespace)

    @namespace.setter
    def namespace(self, value: str | Namespace) -> None:
        if isinstance(value, str):
            self._namespace = Namespace(value)
        elif isinstance(value, Namespace):
            self._namespace = value
        else:
            assert isinstance(value, str) or isinstance(value, Namespace), (
                "Namespace must be of type 'str' or 'Namespace'"
            )
        self.set_config_param(
            key=self.KEYS[self.NAMESPACE],
            value=self.namespace
        )

    @property
    def domain_id(self) -> int:
        return int(self._domain_id)

    @domain_id.setter
    def domain_id(self, value: int | DomainID) -> None:
        if isinstance(value, int):
            self._domain_id = DomainID(value)
        elif isinstance(value, DomainID):
            self._domain_id = value
        else:
            assert isinstance(value, int) or isinstance(value, DomainID), (
                "Domain ID must be of type 'int' or 'DomainID'"
            )
        self.set_config_param(
            key=self.KEYS[self.DOMAIN_ID],
            value=self.domain_id
        )

    @property
    def rmw_implementation(self) -> str:
        return str(self._rmw_implementation)

    @rmw_implementation.setter
    def rmw_implementation(self, value: str | RMWImplementation) -> None:
        if isinstance(value, str):
            self._rmw_implementation = RMWImplementation(value)
        elif isinstance(value, RMWImplementation):
            self._rmw_implementation = value
        else:
            assert (
                isinstance(value, str)) or (
                isinstance(value, RMWImplementation)), (
                "RMW must be of type 'str' or 'RMWImplementation'"
            )
        self.set_config_param(
            key=self.KEYS[self.RMW],
            value=self.rmw_implementation
        )
