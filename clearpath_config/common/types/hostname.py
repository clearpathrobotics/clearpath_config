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

import re


# Hostname
# - hostname class
class Hostname:
    def __init__(self, hostname: str = "hostname") -> None:
        self.assert_valid(hostname)
        self.hostname = hostname

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.hostname == other
        elif isinstance(other, Hostname):
            return self.hostname == other.hostname
        return False

    def __str__(self) -> str:
        return self.hostname

    @staticmethod
    def is_valid(hostname: str) -> bool:
        # Max 253 ASCII Characters
        if len(hostname) > 253:
            return False
        # No Trailing Dots
        # - not exactly a standard, but generally results in undefined
        #       behaviour and should be avoided
        if hostname[-1] == ".":
            return False
        # Only [A-Z][0-9] and '-' Allowed
        # - cannot end or start with a hyphen ('-')
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

    @staticmethod
    def assert_valid(hostname: str):
        assert isinstance(hostname, str), (
            "Hostname '%s' must be of type 'str'" % hostname
        )
        # Min 1 ASCII Characters
        assert len(hostname) > 0, (
            "Hostname '%s' is blank." % hostname
        )
        # Max 253 ASCII Characters
        assert len(hostname) < 254, (
            "Hostname '%s' exceeds 253 ASCII character limit." % hostname
        )
        # No Trailing Dots
        assert hostname[-1] != ".", (
            "Hostname '%s' should not end with a ('.') period." % hostname
        )
        # Only [A-Z][0-9] and '-' Allowed
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        assert all(allowed.match(x) for x in hostname.split(".")), (
            "Hostname '%s' cannot contain characters other than %s." % (
                hostname,
                "[A-Z][0-9] and hypens ('-')"
            )
        )
