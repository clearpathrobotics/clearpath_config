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

class RMWImplementation:
    CONNEXT = "rmw_connext_cpp"
    CYCLONE_DDS = "rmw_cyclonedds_cpp"
    FAST_RTPS = "rmw_fastrtps_cpp"
    GURUM_DDS = "rmw_gurumdds_cpp"

    ALL_SUPPORTED = [FAST_RTPS]

    DEFAULT = FAST_RTPS

    def __init__(
            self,
            rmw: str = DEFAULT
            ) -> None:
        self.assert_valid(rmw)
        self.rmw = rmw

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.rmw == other
        elif isinstance(other, RMWImplementation):
            return self.rmw == other.rmw
        else:
            return False

    def __str__(self) -> str:
        return self.rmw

    @classmethod
    def is_valid(cls, rmw: str) -> bool:
        return rmw in cls.ALL_SUPPORTED

    @classmethod
    def assert_valid(cls, rmw: str) -> None:
        assert cls.is_valid(rmw), ("\n".join[
            "RMW '%s' not supported." % rmw,
            "RMW must be one of: '%s'" % cls.ALL_SUPPORTED
        ])
