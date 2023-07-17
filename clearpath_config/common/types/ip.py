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

# IP
# - ip class
class IP:
    def __init__(self, ip: str = "0.0.0.0") -> None:
        self.assert_valid(ip)
        self.ip_str = ip

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.ip_str == other
        elif isinstance(other, IP):
            return self.ip_str == other.ip_str
        else:
            return False

    def __str__(self) -> str:
        return self.ip_str

    @staticmethod
    def is_valid(ip: str) -> bool:
        # Must be String
        if not isinstance(ip, str):
            return False
        # Must have Four Fields Delimited by '.'
        fields = ip.split(".")
        if not len(fields) == 4:
            return False
        # All Fields must be Integers and 8 Bit Wide
        for field in fields:
            if not field.isdecimal():
                return False
            field_int = int(field)
            if not (0 <= field_int < 256):
                return False
        return True

    @staticmethod
    def assert_valid(ip: str) -> None:
        # Must be String
        assert isinstance(ip, str), (
            "IP '%s' must be string" % ip)
        # Must have Four Fields Delimited by '.'
        fields = ip.split(".")
        assert len(fields) == 4, (
            "IP '%s' must have four entries" % ip)
        for field in fields:
            # Fields Must be Integer
            assert field.isdecimal(), (
                "IP '%s' entries must be integers" % ip)
            # Fields Must be 8-Bits Wide
            field_int = int(field)
            assert 0 <= field_int < 256, (
                "IP '%s' entries must in range 0 to 255" % ip)
