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

import os
from typing import List

from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.discovery import Discovery
from clearpath_config.common.types.hostname import Hostname
from clearpath_config.common.types.rmw_implementation import RMWImplementation
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.system.hosts import HostListConfig
from clearpath_config.system.servers import ServerListConfig, ServerConfig


class MiddlewareConfig(BaseConfig):
    MIDDLEWARE = "middleware"
    RMW = "implementation"
    DISCOVERY = "discovery"
    PROFILE = "profile"
    OVERRIDE_SERVER_ID = "override_server_id"
    SERVERS = "servers"

    TEMPLATE = {
        MIDDLEWARE: {
            RMW: RMW,
            DISCOVERY: DISCOVERY,
            PROFILE: PROFILE,
            OVERRIDE_SERVER_ID: OVERRIDE_SERVER_ID,
            SERVERS: SERVERS,
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        RMW: RMWImplementation.DEFAULT,
        DISCOVERY: Discovery.DEFAULT,
        PROFILE: "",
        OVERRIDE_SERVER_ID: False,
        SERVERS: [],
    }

    def __init__(
            self,
            config: dict = {},
            rmw_implementation: str | RMWImplementation = DEFAULTS[RMW],
            discovery: str | Discovery = DEFAULTS[DISCOVERY],
            profile: str = DEFAULTS[PROFILE],
            override_server_id: bool = DEFAULTS[OVERRIDE_SERVER_ID],
            servers: List[dict] | ServerListConfig = DEFAULTS[SERVERS],
            hosts: HostListConfig = None,
            localhost: Hostname = None
            ) -> None:
        # Initialization
        self._config = {}
        self.hosts = hosts
        self.localhost = localhost
        self.rmw_implementation = rmw_implementation
        self.discovery = discovery
        self.profile = profile
        self.override_server_id = override_server_id
        if servers:
            self.servers = servers
        elif hosts:
            self.servers = hosts.to_dict()
        setters = {
            self.KEYS[self.RMW]: MiddlewareConfig.rmw_implementation,
            self.KEYS[self.DISCOVERY]: MiddlewareConfig.discovery,
            self.KEYS[self.PROFILE]: MiddlewareConfig.profile,
            self.KEYS[self.OVERRIDE_SERVER_ID]: MiddlewareConfig.override_server_id,
            self.KEYS[self.SERVERS]: MiddlewareConfig.servers,
        }
        super().__init__(setters, config, self.MIDDLEWARE)

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
            assert (isinstance(value, str)) or (isinstance(value, RMWImplementation)), (
                f"RMW value of {value} is invalid, must be of type 'str' or 'RMWImplementation'"
            )

    @property
    def discovery(self) -> Discovery:
        self.set_config_param(
            key=self.KEYS[self.DISCOVERY],
            value=str(self._discovery)
        )
        return str(self._discovery)

    @discovery.setter
    def discovery(self, value: str | Discovery) -> None:
        if isinstance(value, str):
            self._discovery = Discovery(value)
        elif isinstance(value, Discovery):
            self._discovery = value
        else:
            assert (
                isinstance(value, str)) or (isinstance(value, Discovery)), (
                f"Discovery mode value of {value} is invalid."
                f"Discovery mode must be of type 'str' or 'RMWImplementation'"
            )
        self._discovery = value

    @property
    def profile(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.PROFILE],
            value=self._profile
        )
        return self._profile

    @profile.setter
    def profile(self, value: str) -> None:
        # Check Type
        assert isinstance(value, str), (
            f"Middleware profile {value} is invalid, must be a string"
        )
        # Valid file
        if value != self.DEFAULTS[self.PROFILE]:
            assert os.path.exists(value), (
                f"Middleware profile path {value} does not exist"
            )
        self._profile = value
        return

    @property
    def override_server_id(self) -> bool:
        self.set_config_param(
            key=self.KEYS[self.OVERRIDE_SERVER_ID],
            value=self._override_server_id
        )
        return self._override_server_id

    @override_server_id.setter
    def override_server_id(self, value: bool) -> None:
        assert isinstance(value, bool), (
            f"Override server_id value of {value} is invalid, must be a boolean")
        self._override_server_id = value

    @property
    def servers(self) -> List[dict]:
        if self._servers:
            self.set_config_param(
                key=self.KEYS[self.SERVERS],
                value=self._servers.to_dict()
            )
        return self._servers

    @servers.setter
    def servers(self, value: List[dict] | ServerListConfig) -> None:
        # Generate a list of ServerConfig Objects based on how the input was provided
        server_list = []
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                f"Server {value} is invalid, must be list of " +
                "type 'dict' or of type 'ServerListConfig'"
            )
            # If the servers were not explicitly listed, assume every device in the hosts list
            # should have its own discovery server running
            if (not value) and (self.discovery == Discovery.SERVER):
                value = []
                [value.append({ServerConfig.HOSTNAME: h.hostname}) for h in self.hosts.get_all()]

            for d in value:
                assert isinstance(d, dict), (
                    f"Server value of {d} is invalid, it must be of type 'dict'"
                )
                server_list.append(ServerConfig(config=d))
        else:
            assert isinstance(value, ServerListConfig), (
                f"Servers {value} is invalid, must be list of " +
                "type 'dict' or of type 'ServerListConfig'"
            )
            server_list = value.get_all()

        # set IP addresses based on the host names provided
        for server in server_list:
            # if a host name was provided, use the look up to determine the ip address
            if server.hostname:
                assert any(server.hostname == s.hostname for s in self.hosts.get_all()), (
                    f"Provided hostname: {server.hostname} is not listed in the hosts list"
                )
                match = next((s for s in self.hosts.get_all() if s.hostname == server.hostname))
                server.ip_address = match.ip_address
            else:
                assert server.ip_address, (
                    f"Server {server} is listed without a host name or IP address."
                )

        for server in server_list:
            # Ensure no duplicate server host/ip + port
            count = sum(((s.ip_address == server.ip_address) and (s.port == server.port))
                        for s in server_list)
            assert count == 1, (
                f"Discovery server {server} conflicts with another discovery server. " +
                "Each combination of host/ip and port number must be unique."
            )

        # sort the servers by host/ip address and then port
        # required for consistent server id numbering
        server_list.sort(key=lambda s: (str.lower(s.hostname), s.ip_address, s.port))

        if not self.override_server_id:
            # assign server id numbering - this numbering must be consistent across all devices
            for i, server in enumerate(server_list):
                server.server_id = i
        else:
            # Only for edge cases where server id is needed to be manually specified in the config
            # Ensure no duplicate server server_id
            # (unspecified ones will default and show up as duplicates)
            for server in server_list:
                count = sum(s.server_id == server.server_id for s in server_list)
                assert count == 1, (
                    f"Server {server} does not have a unique server id. While " +
                    "override_server_id is true, each server must have a unique id specified."
                )

        servers = ServerListConfig()
        servers.set_all(server_list)
        self._servers = servers

    def get_servers_string(self) -> str:
        server_list = self.servers.get_all()

        servers_str = ''
        i = 0
        for s in server_list:
            if not s.enabled:
                continue
            while i < s.server_id:
                servers_str += ';'
                i += 1
            if s.hostname == self.localhost:
                servers_str += f'127.0.0.1:{s.port};'
            else:
                servers_str += f'{s.ip_address}:{s.port};'
            i += 1

        return servers_str

    def get_local_server(self) -> ServerConfig:
        # check for the localhost in the server list
        server_list = self.servers.get_all()
        local_server = next((s for s in server_list if (s.hostname == self.localhost and
                                                        s.enabled)), None)
        # returns None if the localhost is not listed in the server list
        return local_server
