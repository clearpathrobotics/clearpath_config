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


class Namespace:
    def __init__(
            self,
            name: str = '/'
            ) -> None:
        self.assert_valid(name)
        self.name = name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Namespace):
            return self.name == other.name
        else:
            return False

    def __str__(self) -> str:
        return str(self.name)

    @staticmethod
    def is_valid(name: str) -> bool:
        # Must not be Empty
        if name == '':
            return False
        # Must Contain:
        #  - [0-9|a-z|A-Z]
        #  - Underscores (_)
        #  - Forward Slashed (/)
        allowed = re.compile('[a-z|0-9|_|/|~]', re.IGNORECASE)
        if not all(allowed.match(c) for c in name):
            return False
        # May start with (~) but be followed by (/)
        if name[0] == '~':
            if name[1] != '/':
                return False
        # Must not Start with Digit [0-9], May Start with (~)
        if str(name[0]).isdigit():
            return False
        # Must not End with Forward Slash (/)
        if name[-1] == '/':
            return False
        # Must not contain any number of repeated forward slashed (/)
        if '//' in name:
            return False
        # Must not contain any number of repeated underscores (_)
        if '__' in name:
            return False

    @staticmethod
    def assert_valid(name: str) -> None:
        # Empty
        if not name:
            raise ValueError('Namespace cannot be empty')
        # Allowed characters
        allowed = re.compile('[a-z|0-9|_|/|~]', re.IGNORECASE)
        if not all(allowed.match(c) for c in name):
            raise ValueError(f"""Namespace "{name}" can only contain:
 - [A-Z|a-z|0-9],
 - underscores (_),
 - forward slahes (/),
 - leading tilde (~)""")
        # Leading Tilde (~)
        if name[0] == '~':
            if name[1] != '/':
                raise ValueError('Namespace starting with "~" must be followed by "/"')
        # Leading Digit
        if str(name[0]).isdigit():
            raise ValueError(f'Namespace "{name}" may not start with a digit')
        # Ending Forward Slash (/)
        if len(name) != 1 and name[-1] == '/':
            raise ValueError(f'Namespace "{name}" may not end with a forward slash (/)')
        # Repeated Forward Slash (/)
        if '//' in name:
            raise ValueError(f'Namespace "{name}" may not contain repeated forward slashes (/)')
        # Repeated Underscores (/)
        if '__' in name:
            raise ValueError(f'Namespace "{name}" may not contain repeated underscores (_)')

    @staticmethod
    def clean(name: str) -> str:
        # Swap dashes to underscores
        clean = name.replace('-', '_')
        # Remove repeated forward slashes
        while '//' in clean:
            clean = clean.replace('//', '/')
        # Remove repeated underscores
        while '__' in clean:
            clean = clean.replace('__', '_')
        return clean
