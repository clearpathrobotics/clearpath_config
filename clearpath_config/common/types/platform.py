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
            lidar3d: int = 0
            ) -> None:
        self.camera = camera
        self.gps = gps
        self.imu = imu
        self.lidar2d = lidar2d
        self.lidar3d = lidar3d


# Platform
# - all supported platforms
class Platform:
    # Dingo D V1
    DD100 = "dd100"
    # Dingo O V1
    DO100 = "do100"
    # Dingo D V1.5
    DD150 = "dd150"
    # Dingo D V1.5
    DO150 = "d0150"
    # Jackal V1
    J100 = "j100"
    # Husky V2
    A200 = "a200"
    # Ridgeback V1
    R100 = "r100"
    # Warthog V2
    W200 = "w200"
    # Genric Robot
    GENERIC = "generic"

    ALL = [
        DD100,
        DO100,
        DD150,
        DO150,
        J100,
        A200,
        R100,
        W200,
        GENERIC
    ]

    PACS = {
        GENERIC: PACSProfile(rows=100, columns=100),
        A200: PACSProfile(rows=8, columns=7),
        J100: PACSProfile(rows=4, columns=2),
        W200: PACSProfile(rows=100, columns=100),
    }

    INDEX = {
        GENERIC: IndexingProfile(),
        A200: IndexingProfile(),
        DD100: IndexingProfile(imu=1),
        DO100: IndexingProfile(imu=1),
        DD150: IndexingProfile(imu=1),
        DO150: IndexingProfile(imu=1),
        J100: IndexingProfile(gps=1, imu=1),
        W200: IndexingProfile(imu=1),
    }
