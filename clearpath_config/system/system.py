# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
# @copyright (c) 2023, Clearpath Robotics, Inc., All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Clearpath Robotics nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.domain_id import DomainID
from clearpath_config.common.types.namespace import Namespace
from clearpath_config.common.types.username import Username
from clearpath_config.common.types.rmw_implementation import RMWImplementation
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.system.hosts import HostsConfig


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
            USERNAME: USERNAME,
            ROS2: {
                NAMESPACE: NAMESPACE,
                DOMAIN_ID: DOMAIN_ID,
                RMW: RMW,
                WORKSPACES: WORKSPACES
            }
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        # HOSTS: platform hostname (serial number) at 192.168.131.1
        HOSTS: HostsConfig.DEFAULTS,
        # USERNAME: administrator
        USERNAME: "administrator",
        # NAMESPACE: serial number
        NAMESPACE: Namespace.clean(BaseConfig.get_serial_number(prefix=True)),
        # DOMAIN_ID: 0
        DOMAIN_ID: 0,
        # RMW: "rmw_fastrtps_cpp"
        RMW: "rmw_fastrtps_cpp",
        # Workpaces: empty list
        WORKSPACES: []
    }

    def __init__(
            self,
            config: dict = {},
            hosts: dict = DEFAULTS[HOSTS],
            username: str = DEFAULTS[USERNAME],
            namespace: str = DEFAULTS[NAMESPACE],
            domain_id: int = DEFAULTS[DOMAIN_ID],
            rmw_implementation: str = DEFAULTS[RMW],
            workspaces: list = DEFAULTS[WORKSPACES]
            ) -> None:
        # Initialization
        self._config = {}
        self.hosts = hosts
        self.username = username
        self.namespace = namespace
        self.domain_id = domain_id
        self.rmw_implementation = rmw_implementation
        self.workspaces = workspaces
        # Setter Template
        setters = {
            self.KEYS[self.HOSTS]: SystemConfig.hosts,
            self.KEYS[self.USERNAME]: SystemConfig.username,
            self.KEYS[self.NAMESPACE]: SystemConfig.namespace,
            self.KEYS[self.DOMAIN_ID]: SystemConfig.domain_id,
            self.KEYS[self.RMW]: SystemConfig.rmw_implementation,
            self.KEYS[self.WORKSPACES]: SystemConfig.workspaces,
        }
        # Set from Config
        super().__init__(setters, config, self.SYSTEM)

    def update(self, serial_number=False) -> None:
        if serial_number:
            self.hosts.update(serial_number=serial_number)
            # Update if still defaults
            namespace = Namespace.clean(self.get_serial_number(prefix=True))
            if self.namespace == self.DEFAULTS[self.NAMESPACE]:
                self.namespace = namespace
            # Update defaults
            self.DEFAULTS[self.NAMESPACE] = namespace

    @property
    def hosts(self) -> HostsConfig:
        self.set_config_param(
            key=self.KEYS[self.HOSTS],
            value=self._hosts.config[self.HOSTS]
        )
        return self._hosts

    @hosts.setter
    def hosts(self, value: dict | HostsConfig) -> None:
        if isinstance(value, dict):
            self._hosts = HostsConfig(config=value)
        elif isinstance(value, HostsConfig):
            self._hosts = value
        else:
            assert isinstance(value, dict) or isinstance(value, HostsConfig), (
                "Hosts must be of type 'dict' or 'HostsConfig'"
            )

    @property
    def username(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.USERNAME],
            value=str(self._username)
        )
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

    @property
    def namespace(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.NAMESPACE],
            value=BaseConfig.get_namespace()
        )
        return BaseConfig.get_namespace()

    @namespace.setter
    def namespace(self, value: str | Namespace) -> None:
        BaseConfig.set_namespace(value)

    @property
    def domain_id(self) -> int:
        self.set_config_param(
            key=self.KEYS[self.DOMAIN_ID],
            value=int(self._domain_id)
        )
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

    @property
    def rmw_implementation(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.RMW],
            value=str(self._rmw_implementation)
        )
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

    @property
    def workspaces(self) -> list:
        return self._workspaces

    @workspaces.setter
    def workspaces(self, value: list) -> None:
        assert isinstance(value, list), (
            "Workspaces must be 'list' of 'str'")
        assert all([isinstance(i, str) for i in value]), (
            "Workspaces must be 'list' of 'str'")
        self._workspaces = value
