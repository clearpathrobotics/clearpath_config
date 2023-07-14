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

from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.file import File
from clearpath_config.common.types.ip import IP
from clearpath_config.mounts.types.mount import BaseMount
from typing import List


class FlirPTU(BaseMount):
    MOUNT_MODEL = "flir_ptu"
    # Default Values
    TTY_PORT = "/dev/ptu"
    TCP_PORT = 4000
    IP_ADDRESS = "192.168.131.70"
    LIMITS_ENABLED = False
    TTY = "tty"
    TCP = "tcp"
    CONNECTION_TYPE = TTY
    # TTY (uses tty_port)
    # TCP (uses ip_addr and tcp_port)
    CONNECTION_TYPES = [TTY, TCP]

    def __init__(
        self,
        parent: str = Accessory.PARENT,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
        tty_port: str = TTY_PORT,
        tcp_port: int = TCP_PORT,
        ip: str = IP_ADDRESS,
        connection_type: str = CONNECTION_TYPE,
        limits_enabled: bool = LIMITS_ENABLED,
    ) -> None:
        super().__init__(
            name=FlirPTU.get_name_from_idx(0),
            parent=parent,
            xyz=xyz,
            rpy=rpy,
        )
        # Serial Port
        self.tty_port = File(self.TTY_PORT)
        self.set_tty_port(tty_port)
        # TCP Port
        self.tcp_port = self.TCP_PORT
        self.set_tcp_port(tcp_port)
        # IP
        self.ip = IP()
        self.set_ip(ip)
        # Connection Type
        self.connection_type = self.TTY
        self.set_connection_type(connection_type)
        # Limits
        self.limits_enabled = False
        self.set_limits_enabled(limits_enabled)

    def get_tty_port(self) -> str:
        return self.tty_port.get_path()

    def set_tty_port(self, tty_port: str) -> None:
        self.tty_port = File(tty_port)

    def get_tcp_port(self) -> str:
        return self.tcp_port

    def set_tcp_port(self, tcp_port: int) -> None:
        assert 1024 < tcp_port < 65536, (
            "TCP port '%s' must be in range 1024 to 65536" % tcp_port
        )
        self.tcp_port = tcp_port

    def get_ip(self) -> str:
        return str(self.ip)

    def set_ip(self, ip: str) -> None:
        self.ip = IP(ip)

    def get_connection_type(self) -> str:
        return self.connection_type

    def set_connection_type(self, connection_type: str) -> None:
        assert connection_type in self.CONNECTION_TYPES, (
            "Connection type '%s' must be one of '%s'" % (
                connection_type,
                self.CONNECTION_TYPES,
            )
        )
        self.connection_type = connection_type

    def get_limits_enabled(self) -> bool:
        return self.limits_enabled

    def set_limits_enabled(self, limits_enabled: bool) -> None:
        self.limits_enabled = limits_enabled
