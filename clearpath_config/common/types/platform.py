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
from clearpath_config.common.ros import ROS_DISTRO
from clearpath_config.common.types.exception import UnsupportedPlatformException


class PACSProfile:
    def __init__(
            self,
            rows: int,
            columns: int
            ) -> None:
        self.rows = rows
        self.columns = columns


class IndexingProfile:
    def __init__(
            self,
            camera: int = 0,
            gps: int = 0,
            imu: int = 0,
            lidar2d: int = 0,
            lidar3d: int = 0,
            ins: int = 0,
            ) -> None:
        self.camera = camera
        self.gps = gps
        self.imu = imu
        self.lidar2d = lidar2d
        self.lidar3d = lidar3d
        self.ins = ins


# Platform
# - all supported platforms
class Platform:
    # Dingo D V1
    DD100 = 'dd100'
    # Dingo O V1
    DO100 = 'do100'
    # Dingo D V1.5
    DD150 = 'dd150'
    # Dingo D V1.5
    DO150 = 'do150'
    # Jackal V1
    J100 = 'j100'
    # Husky V2
    A200 = 'a200'
    # Husky V3
    A300 = 'a300'
    # Ridgeback V1
    R100 = 'r100'
    # Warthog V2
    W200 = 'w200'
    # Genric Robot
    GENERIC = 'generic'

    ALL = [
        DD100,
        DO100,
        DD150,
        DO150,
        J100,
        A200,
        A300,
        R100,
        W200,
        GENERIC
    ]

    PACS = {
        GENERIC: PACSProfile(rows=100, columns=100),
        A200: PACSProfile(rows=8, columns=7),
        A300: PACSProfile(rows=9, columns=5),
        J100: PACSProfile(rows=4, columns=2),
        W200: PACSProfile(rows=100, columns=100),
        R100: PACSProfile(rows=100, columns=100),
    }

    INDEX = {
        GENERIC: IndexingProfile(),
        A200: IndexingProfile(),
        A300: IndexingProfile(),
        DD100: IndexingProfile(imu=1),
        DO100: IndexingProfile(imu=1),
        DD150: IndexingProfile(imu=1),
        DO150: IndexingProfile(imu=1),
        J100: IndexingProfile(gps=1, imu=1),
        R100: IndexingProfile(imu=1),
        W200: IndexingProfile(imu=1),
    }

    @staticmethod
    def assert_is_supported(platform):
        """
        Raise an exception if the platform is not presently supported/usable.

        Unsupported platforms may become supported in a future release, and there are no plans
        to remove it; it simply is not (yet) compatible with the current ROS release.

        @param platform  The platform-identifying serial number prefix (e.g. 'a200', 'j100')

        @exception UnsupportedPlatformException if the platform is not supported
        """
        platform = platform.lower()

        match platform:
            case Platform.W200:
                raise UnsupportedPlatformException(
                    f'Platform {platform} is still in-development and not yet supported on {ROS_DISTRO}')  # noqa:E501

    @staticmethod
    def notify_if_deprecated(platform):
        """
        Print a notification that the selected platform is deprecated.

        Deprecated platforms may have their support removed in a future version

        @param platform  The platform-identifying serial number prefix (e.g. 'a200', 'j100')
        """
        # currently nothing is deprecated, so nothing to do here (yet)
        pass
