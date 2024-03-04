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

import socket
from typing import List

from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.domain_id import DomainID
from clearpath_config.common.types.hostname import Hostname
from clearpath_config.common.types.namespace import Namespace
from clearpath_config.common.types.username import Username
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.system.hosts import HostConfig, HostListConfig
from clearpath_config.system.middleware import MiddlewareConfig


class SystemConfig(BaseConfig):

    SYSTEM = "system"
    HOSTS = "hosts"
    LOCALHOST = "localhost"
    SELF = "self"
    ROS2 = "ros2"
    USERNAME = "username"
    NAMESPACE = "namespace"
    DOMAIN_ID = "domain_id"
    MIDDLEWARE = MiddlewareConfig.MIDDLEWARE
    WORKSPACES = "workspaces"

    TEMPLATE = {
        SYSTEM: {
            SELF: SELF,
            HOSTS: HOSTS,
            LOCALHOST: LOCALHOST,
            USERNAME: USERNAME,
            ROS2: {
                NAMESPACE: NAMESPACE,
                DOMAIN_ID: DOMAIN_ID,
                MIDDLEWARE: MIDDLEWARE,
                WORKSPACES: WORKSPACES
            }
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        # HOSTS: hostnames and IP's for all computers involved with the system
        HOSTS: HostListConfig.DEFAULTS,
        # LOCALHOST: hostname for the specific devices - automatically determined
        LOCALHOST: socket.gethostname(),
        # USERNAME: administrator
        USERNAME: "administrator",
        # NAMESPACE: serial number
        NAMESPACE: Namespace.clean(BaseConfig.get_serial_number(prefix=True)),
        # DOMAIN_ID: 0
        DOMAIN_ID: 0,
        # Discovery Server Disabled
        MIDDLEWARE: MiddlewareConfig.DEFAULTS,
        # Workpaces: empty list
        WORKSPACES: []
    }

    def __init__(
            self,
            config: dict = {},
            hosts: List[dict] | HostListConfig = DEFAULTS[HOSTS],
            localhost: str | Hostname = DEFAULTS[LOCALHOST],
            username: str | Username = DEFAULTS[USERNAME],
            namespace: str | Namespace = DEFAULTS[NAMESPACE],
            domain_id: int | DomainID = DEFAULTS[DOMAIN_ID],
            middleware: dict | MiddlewareConfig = DEFAULTS[MIDDLEWARE],
            workspaces: list = DEFAULTS[WORKSPACES]
            ) -> None:
        # Initialization
        self._config = {}
        self.hosts = hosts
        self.localhost = localhost
        self.username = username
        self.namespace = namespace
        self.domain_id = domain_id
        self.middleware = middleware
        self.workspaces = workspaces
        # Setter Template
        setters = {
            self.KEYS[self.HOSTS]: SystemConfig.hosts,
            self.KEYS[self.LOCALHOST]: SystemConfig.localhost,
            self.KEYS[self.USERNAME]: SystemConfig.username,
            self.KEYS[self.NAMESPACE]: SystemConfig.namespace,
            self.KEYS[self.DOMAIN_ID]: SystemConfig.domain_id,
            self.KEYS[self.MIDDLEWARE]: SystemConfig.middleware,
            self.KEYS[self.WORKSPACES]: SystemConfig.workspaces,
        }
        # Set from Config
        super().__init__(setters, config, self.SYSTEM)

    def update(self, serial_number=False) -> None:
        if serial_number:
            # check if hosts list is set to default, if so update it
            hosts = self.DEFAULTS[self.HOSTS]
            hosts[0][HostConfig.HOSTNAME] = BaseConfig.get_serial_number()
            if self.hosts.to_dict() == self.DEFAULTS[self.HOSTS]:
                self.hosts = hosts
            # Update if still defaults
            namespace = Namespace.clean(BaseConfig.get_serial_number(prefix=True))
            if self.namespace == self.DEFAULTS[self.NAMESPACE]:
                self.namespace = namespace
            # Update defaults
            self.DEFAULTS[self.HOSTS] = hosts
            self.DEFAULTS[self.NAMESPACE] = namespace

    @property
    def hosts(self) -> HostListConfig:
        self.set_config_param(
            key=self.KEYS[self.HOSTS],
            value=self._hosts.to_dict()
        )
        return self._hosts

    @hosts.setter
    def hosts(self, value: List[dict] | HostListConfig) -> None:
        host_list = []
        if isinstance(value, list):
            for d in value:
                assert isinstance(d, dict), (
                    f"Host value of {d} is invalid, it must be of type 'dict'"
                )
                host_list.append(HostConfig(config=d))

            for host in host_list:
                # Ensure no duplicate hostname or IP
                count = sum(((host.ip_address == h.ip_address) or (host.hostname == h.hostname))
                            for h in host_list)
                assert count == 1, (
                    f"Host {host} conflicts with another host. " +
                    "Each hostname and ip must be unique."
                )

            self._hosts = HostListConfig()
            self._hosts.set_all(host_list)
        elif isinstance(value, HostListConfig):
            self._hosts = value
        else:
            assert isinstance(value, list) or isinstance(value, HostConfig), (
                f"Hosts value of {value} is invalid, " +
                "it must be of type 'List[dict]' or 'HostListConfig'"
            )

    @property
    def localhost(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.LOCALHOST],
            value=str(self._localhost)
        )
        return str(self._localhost)

    @localhost.setter
    def localhost(self, value: str | Hostname) -> None:
        assert isinstance(value, str) or isinstance(value, Hostname), (
            f"Localhost of {value} is invalid, must be of type 'str' or 'Hostname'"
        )
        if isinstance(value, str):
            self._localhost = Hostname(value)
        elif isinstance(value, Hostname):
            self._localhost = value

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
    def middleware(self) -> MiddlewareConfig:
        self.set_config_param(
            key=self.KEYS[self.MIDDLEWARE],
            value=self._middleware.config[self.MIDDLEWARE]
        )
        return self._middleware

    @middleware.setter
    def middleware(self, value: dict | MiddlewareConfig) -> None:
        if isinstance(value, dict):
            self._middleware = MiddlewareConfig(config=value,
                                                hosts=self.hosts,
                                                localhost=self.localhost)
        elif isinstance(value, MiddlewareConfig):
            self._middleware = value
        else:
            assert isinstance(value, dict) or (
                isinstance(value, MiddlewareConfig)), (
                "Middleware configuration must be of type 'dict' or 'MiddlewareConfig'"
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
