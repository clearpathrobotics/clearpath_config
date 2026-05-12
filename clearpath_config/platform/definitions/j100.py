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
from clearpath_config.common.types.platform import (
    IndexingProfile,
    PACSProfile,
    Platform,
)
from clearpath_config.platform.attachments.j100 import J100Fender, J100TopPlate
from clearpath_config.platform.battery import BatteryConfig
from clearpath_config.platform.drivetrain import DrivetrainConfig
from clearpath_config.platform.platform import BasePlatformConfig


class J100PlatformConfig(BasePlatformConfig):
    NAME = 'j100'
    PACS = PACSProfile(rows=4, columns=2)
    INDEXING = IndexingProfile(gps=1, imu=1)
    VALID_BATTERIES = {
        BatteryConfig.HE2613: [BatteryConfig.S1P1],
        BatteryConfig.HE2411: [BatteryConfig.S1P1],
        BatteryConfig.HE2410: [BatteryConfig.S1P1],
    }
    VALID_DRIVETRAIN = {
        DrivetrainConfig.CONTROL: [DrivetrainConfig.DIFF_4WD],
        DrivetrainConfig.WHEELS: {
            DrivetrainConfig.FRONT: [DrivetrainConfig.OUTDOOR],
            DrivetrainConfig.REAR: [DrivetrainConfig.OUTDOOR],
        },
    }
    DEFAULT_CAN_ADAPTERS = []
    DEFAULT_CAN_BRIDGES = []
    DEFAULT_ATTACHMENTS = [
        {'name': 'front_fender', 'type': 'j100.fender'},
        {'name': 'rear_fender', 'type': 'j100.fender', 'rpy': [0, 0, 3.1415]},
    ]


Platform.register(J100PlatformConfig)
J100PlatformConfig.register_attachment(J100TopPlate)
J100PlatformConfig.register_attachment(J100Fender)
