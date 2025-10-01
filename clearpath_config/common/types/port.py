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

# Port
# - TCP Port
class Port:

    MIN_PORT = 0
    MAX_PORT = 65535

    def __init__(self, port: int) -> None:
        self.assert_valid(port)
        self.port = int(port)

    def __str__(self) -> str:
        return str(self.port)

    def __int__(self) -> int:
        return self.port

    def __eq__(self, other: object) -> bool:
        try:
            port = int(self)
            other = int(other)
        except Exception:
            return False
        return port == other

    @staticmethod
    def is_valid(port: int) -> None:
        # Must be an integer
        try:
            port = int(port)
        except Exception:
            return False
        # Must be in Range
        return Port.MIN_PORT <= port <= Port.MAX_PORT

    @staticmethod
    def assert_valid(port: int) -> None:
        # Must be an integer
        try:
            port = int(port)
        except ValueError:
            raise TypeError(f'Port {port} must be an integer')
        # Must be in Range
        if port < Port.MIN_PORT or port > Port.MAX_PORT:
            raise ValueError(
                f'Port "{port}" must be in range {Port.MIN_PORT} to {Port.MAX_PORT}')
