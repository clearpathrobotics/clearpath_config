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
from clearpath_config.common.types.hostname import Hostname
from clearpath_config.common.types.ip import IP


# Host
# - hostname and config pair
class Host:
    def __init__(
            self,
            hostname: str = "hostname",
            ip: str = "0.0.0.0"
            ) -> None:
        self.hostname = Hostname()
        self.ip = IP()
        self.set_hostname(hostname)
        self.set_ip(ip)

    def __eq__(self, other) -> bool:
        return self.hostname == other.hostname and self.ip == other.ip

    def __str__(self) -> str:
        return "{ hostname: %s, ip: %s }" % (str(self.hostname), str(self.ip))

    def to_dict(self) -> dict:
        return {str(self.hostname): str(self.ip)}

    # Hostname:
    # - the hostname of this host
    def get_hostname(self) -> str:
        return str(self.hostname)

    def set_hostname(self, hostname: str) -> None:
        self.hostname = Hostname(hostname)

    # IP
    # - the ip of this host
    def get_ip(self) -> str:
        return str(self.ip)

    def set_ip(self, ip: str) -> None:
        self.ip = IP(ip)
