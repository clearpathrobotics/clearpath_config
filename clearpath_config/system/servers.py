# Software License Agreement (BSD)
#
# @author    Hilary Luo <hluo@clearpathrobotics.com>
# @copyright (c) 2024, Clearpath Robotics, Inc., All rights reserved.
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

from typing import List

from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.hostname import Hostname
from clearpath_config.common.types.ip import IP
from clearpath_config.common.types.port import Port
from clearpath_config.common.types.list import ListConfig
from clearpath_config.common.utils.dictionary import flip_dict


class ServerConfig(BaseConfig):
    HOSTNAME = "hostname"
    IP_ADDRESS = "ip"
    PORT = "port"
    SERVER_ID = "server_id"
    ENABLED = "enabled"

    TEMPLATE = {
        HOSTNAME: HOSTNAME,
        IP_ADDRESS: IP_ADDRESS,
        PORT: PORT,
        SERVER_ID: SERVER_ID,
        ENABLED: ENABLED
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        HOSTNAME: '',
        IP_ADDRESS: '',
        PORT: 11811,
        SERVER_ID: 0,
        ENABLED: True
    }

    def __init__(
            self,
            config: dict = {},
            hostname: str | Hostname = DEFAULTS[HOSTNAME],
            ip_address: str | IP = DEFAULTS[IP_ADDRESS],
            port: int | Port = DEFAULTS[PORT],
            server_id: int = DEFAULTS[SERVER_ID],
            enabled: bool = DEFAULTS[ENABLED]
            ) -> None:
        self.hostname = hostname
        self.ip_address = ip_address
        self.port = port
        self.server_id = server_id
        self.enabled = enabled
        # Setter Template
        setters = {
            self.KEYS[self.HOSTNAME]: ServerConfig.hostname,
            self.KEYS[self.IP_ADDRESS]: ServerConfig.ip_address,
            self.KEYS[self.PORT]: ServerConfig.port,
            self.KEYS[self.SERVER_ID]: ServerConfig.server_id,
            self.KEYS[self.ENABLED]: ServerConfig.enabled,
        }
        super().__init__(setters, config, None)

    def __str__(self) -> str:
        return "{ hostname: %s, ip: %s, port: %s, server_id: %s, enabled: %s}" % (
            str(self.hostname), str(self.ip_address), str(self.port),
            str(self.server_id), str(self.enabled))

    @property
    def server_id(self) -> int:
        self.set_config_param(
            key=self.KEYS[self.SERVER_ID],
            value=int(self._server_id)
        )
        return int(self._server_id)

    @server_id.setter
    def server_id(self, value: int) -> None:
        # Check Type
        assert isinstance(value, int), (
            f"Remote Server ID {value} is invalid, must be an integer"
        )
        # [0-255] Range
        assert 0 <= value < 255, (
            f"Discovery Server ID {value} is invalid, must be in range 0 - 254"
        )
        self._server_id = value
        return

    @property
    def hostname(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.HOSTNAME],
            value=str(self._hostname)
        )
        return str(self._hostname)

    @hostname.setter
    def hostname(self, value: str | Hostname) -> None:
        if not value:
            self._hostname = ''
        elif isinstance(value, str):
            self._hostname = Hostname(value)
        elif isinstance(value, Hostname):
            self._hostname = value
        else:
            assert isinstance(value, str) or isinstance(value, Hostname), (
                f"Hostname of {value} is invalid, must be of type 'str' or 'Hostname'"
            )
        return

    @property
    def ip_address(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.IP_ADDRESS],
            value=str(self._ip_address)
        )
        return str(self._ip_address)

    @ip_address.setter
    def ip_address(self, value: str | IP) -> None:
        if not value:
            self._ip_address = ''
        elif isinstance(value, str):
            self._ip_address = IP(value)
        elif isinstance(value, IP):
            self._ip_address = value
        else:
            assert isinstance(value, dict) or isinstance(value, IP), (
                f"IP address of {value} is invalid, must be of type 'str' or 'IP'"
            )
        return

    @property
    def port(self) -> int:
        self.set_config_param(
            key=self.KEYS[self.PORT],
            value=int(self._port)
        )
        return int(self._port)

    @port.setter
    def port(self, value: int | Port) -> None:
        if isinstance(value, int):
            self._port = Port(value)
        elif isinstance(value, Port):
            self._port = value
        else:
            assert isinstance(value, dict) or isinstance(value, Port), (
                f"Port of {value} is invalid, must be of type 'str' or 'Port'"
            )
        return

    @property
    def enabled(self) -> bool:
        self.set_config_param(
            key=self.KEYS[self.ENABLED],
            value=self._enabled
        )
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        # Check Type
        assert (isinstance(value, bool)), (
            f"Enabled {value} is invalid, must be a boolean"
        )
        self._enabled = value
        return


# LinkListConfig
class ServerListConfig(ListConfig[ServerConfig, int]):
    def __init__(self) -> None:
        super().__init__(
            uid=lambda obj: obj.server_id,
            obj_type=ServerConfig,
            uid_type=int
        )

    def to_dict(self) -> List[dict]:
        d = []
        for server in self.get_all():
            d.append(server.config)
        return d
