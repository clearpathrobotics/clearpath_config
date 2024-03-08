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
from clearpath_config.common.types.hostname import Hostname
from clearpath_config.common.types.ip import IP
from clearpath_config.common.types.list import ListConfig
from clearpath_config.common.utils.dictionary import flip_dict
from typing import List


# HostConfig
# - this is the format for which each host involved in the system will be described
class HostConfig(BaseConfig):

    HOSTNAME = "hostname"
    IP_ADDRESS = "ip"

    TEMPLATE = {
        HOSTNAME: HOSTNAME,
        IP_ADDRESS: IP_ADDRESS
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        HOSTNAME: BaseConfig.get_serial_number(),
        IP_ADDRESS: "192.168.131.1",
    }

    def __init__(
            self,
            config: dict = {},
            hostname: str | Hostname = DEFAULTS[HOSTNAME],
            ip_address: str | IP = DEFAULTS[IP_ADDRESS],
            ) -> None:
        # Initialization
        self.hostname = hostname
        self.ip_address = ip_address
        # Setter Template
        setters = {
            self.KEYS[self.HOSTNAME]: HostConfig.hostname,
            self.KEYS[self.IP_ADDRESS]: HostConfig.ip_address,
        }
        # Set from Config
        super().__init__(setters, config, None)

    def __eq__(self, other) -> bool:
        return self.hostname == other.hostname and self.ip_address == other.ip_address

    def __str__(self) -> str:
        return "{ hostname: %s, ip: %s }" % (str(self.hostname), str(self.ip_address))

    def to_dict(self) -> dict:
        return {str(self.hostname): str(self.ip_address)}

    # Hostname:
    # - the hostname of the computer
    @property
    def hostname(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.HOSTNAME],
            value=str(self._hostname)
        )
        return str(self._hostname)

    @hostname.setter
    def hostname(self, value: str | Hostname) -> None:
        if isinstance(value, str):
            self._hostname = Hostname(value)
        elif isinstance(value, Hostname):
            self._hostname = value
        else:
            assert isinstance(value, str) or isinstance(value, Hostname), (
                f"Hostname of {value} is invalid, must be of type 'str' or 'Hostname'"
            )

    # IP Address:
    # - the IP address at which the computer can be accessed
    @property
    def ip_address(self) -> IP:
        self.set_config_param(
            key=self.KEYS[self.IP_ADDRESS],
            value=self._ip
        )
        return self._ip

    @ip_address.setter
    def ip_address(self, value: str | IP) -> None:
        if isinstance(value, str):
            self._ip = IP(value)
        elif isinstance(value, IP):
            self._ip = value
        else:
            assert isinstance(value, dict) or isinstance(value, IP), (
                f"IP address of {value} is invalid, must be of type 'str' or 'IP'"
            )


# HostListConfig
# - list of hosts that are involved with the system
class HostListConfig(ListConfig[HostConfig, str]):

    DEFAULTS = [HostConfig.DEFAULTS]

    def __init__(self) -> None:
        super().__init__(
            uid=lambda obj: obj.hostname,
            obj_type=HostConfig,
            uid_type=str
        )

    def to_dict(self) -> List[dict]:
        hosts = []
        for host in self.get_all():
            hosts.append(host.config)
        return hosts
