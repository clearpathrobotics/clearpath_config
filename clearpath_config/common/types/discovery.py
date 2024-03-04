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

class Discovery:
    SIMPLE = "simple"
    SERVER = "server"

    # All supported discovery modes, currently only set up for FastDDS
    ALL_SUPPORTED = [SIMPLE, SERVER]

    # The discovery mode that the system will default to
    DEFAULT = SIMPLE

    def __init__(
            self,
            mode: str = DEFAULT
            ) -> None:
        self.assert_valid(mode)
        self.mode = mode

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.mode == other
        elif isinstance(other, Discovery):
            return self.mode == other.mode
        else:
            return False

    def __str__(self) -> str:
        return self.mode

    @classmethod
    def is_valid(cls, mode: str) -> bool:
        return mode in cls.ALL_SUPPORTED

    @classmethod
    def assert_valid(cls, mode: str) -> None:
        assert cls.is_valid(mode), ("\n".join[
            f"Discovery mode '{mode}' not supported."
            f"Discovery mode must be one of: '{cls.ALL_SUPPORTED}'"
        ])
