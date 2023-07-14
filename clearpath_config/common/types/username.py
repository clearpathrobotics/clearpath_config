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


# Username
class Username:
    def __init__(self, username: str = "administrator") -> None:
        self.assert_valid(username)
        self.username = username

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.username == other
        elif isinstance(other, Username):
            return self.username == other.username
        return False

    def __str__(self) -> str:
        return self.username

    @staticmethod
    def is_valid(username: str):
        # Check Type
        if not isinstance(username, str):
            return False
        # Max 255 Characters
        if len(username) > 255:
            return False
        # Convention
        # - [a-z] lowercase characters
        # - [0-9] numbers
        # - underscores
        # - dashes
        # - may end in $
        allowed = re.compile(r"[-a-z0-9_]")
        return all(allowed.match(c) for c in username)

    @staticmethod
    def assert_valid(username: str):
        # Check Type
        assert isinstance(username, str), (
            "Username '%s' must of type 'str'" % username
        )
        # Max 255 Characters
        assert len(username) < 256, (
            "Username '%s' exceeds 255 ASCII character limit." % username
        )
        # Regex Convention
        allowed = re.compile(r"[-a-z0-9_]")
        assert all(allowed.match(c) for c in username), (
            "Username '%s' cannot contain characters other than: %s, %s, %s, %s" % (
                username,
                "lowercase letters",
                "digits",
                "underscores",
                "dashes"
            )
        )
