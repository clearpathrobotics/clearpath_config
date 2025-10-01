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
class DomainID:

    MIN_DOMAIN = 0
    MAX_DOMAIN = 101

    def __init__(self, _id: int = 0) -> None:
        self.assert_valid(_id)
        self.id = _id

    def __int__(self) -> int:
        return self.id

    @staticmethod
    def is_valid(_id: int) -> bool:
        # Check Type
        if not isinstance(_id, int):
            return False
        # 0-101 Range
        if not (0 <= _id <= 101):
            return False
        return True

    @staticmethod
    def assert_valid(_id: int) -> None:
        # Check Type
        if not isinstance(_id, int):
            raise TypeError(f'Domain ID {_id} must be an integer')
        # 0 - 101 Range
        if _id < DomainID.MIN_DOMAIN or _id > DomainID.MAX_DOMAIN:
            raise ValueError(
                f'Domain ID {_id} must be in range {DomainID.MIN_DOMAIN} - {DomainID.MAX_DOMAIN}'
            )
        return
