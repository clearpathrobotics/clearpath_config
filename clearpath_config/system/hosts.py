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
from clearpath_config.common.types.host import Host
from clearpath_config.common.types.hostname import Hostname
from clearpath_config.common.types.list import ListConfig
from clearpath_config.common.utils.dictionary import flip_dict
from typing import List


# HostListConfig
# - list of hosts
class HostListConfig(ListConfig[Host, str]):
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
        SELF: BaseConfig.get_serial_number(),
        PLATFORM: {
            BaseConfig.get_serial_number(): "192.168.131.1"
        },
        ONBOARD: {},
        REMOTE: {}
    }

    def __init__(
            self,
            config: dict = {},
            selfhost: str | Hostname = DEFAULTS[SELF],
            platform: dict | Host = DEFAULTS[PLATFORM],
            onboard: dict | List[Host] = DEFAULTS[ONBOARD],
            remote: dict | List[Host] = DEFAULTS[REMOTE],
            ) -> None:
        # Initialization
        self.self = selfhost
        self.platform = platform
        self.onboard = onboard
        self.remote = remote
        # Setter Template
        setters = {
            self.KEYS[self.SELF]: HostsConfig.self,
            self.KEYS[self.PLATFORM]: HostsConfig.platform,
            self.KEYS[self.ONBOARD]: HostsConfig.onboard,
            self.KEYS[self.REMOTE]: HostsConfig.remote
        }
        # Set from Config
        super().__init__(setters, config, self.HOSTS)

    def update(self, serial_number=False) -> None:
        if serial_number:
            sn = BaseConfig.get_serial_number()
            # Update if still defaults
            if self.self == self.DEFAULTS[self.SELF]:
                self.self = sn
            if self.platform.get_hostname() == sn:
                self.platform.set_hostname(sn)
            # Update Defaults
            self.DEFAULTS[self.SELF] = sn
            self.DEFAULTS[self.PLATFORM] = {sn: "192.168.131.1"}

    # Self:
    # - the hostname of the computer running this config
    @property
    def self(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.SELF],
            value=str(self._self)
        )
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

    # Platform:
    # - the main computer for this system (i.e. the robot's computer)
    @property
    def platform(self) -> Host:
        self.set_config_param(
            key=self.KEYS[self.PLATFORM],
            value=self._platform.to_dict()
        )
        return self._platform

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
        self.set_config_param(
            key=self.KEYS[self.ONBOARD],
            value=self._onboard.to_dict()
        )
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

    # Remote:
    # - these are remote machines which need to interact with the system
    # - ex. laptops or other robots
    @property
    def remote(self) -> HostListConfig:
        self.set_config_param(
            key=self.KEYS[self.REMOTE],
            value=self._remote.to_dict()
        )
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
