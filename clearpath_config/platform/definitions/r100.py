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
from clearpath_config.platform.attachments.r100 import R100Attachment
from clearpath_config.platform.can import CANAdapterConfig, CANBridgeConfig
from clearpath_config.platform.platform import BasePlatformConfig


class R100PlatformConfig(BasePlatformConfig):
    NAME = 'r100'
    PACS = PACSProfile(rows=100, columns=100)
    INDEXING = IndexingProfile(imu=1)
    VALID_BATTERIES = {
        '8A31DTM': ['S1P2'],
    }
    VALID_DRIVETRAIN = {
        'control': ['omni_4wd', 'diff_4wd'],
        'wheels': {
            'front': ['mecanum'],
            'rear': ['mecanum'],
        },
    }
    DEFAULT_CAN_ADAPTERS = [CANAdapterConfig.VCAN0_DEFAULT]
    DEFAULT_CAN_BRIDGES = CANBridgeConfig.SINGLE_VCAN_DEFAULT
    ATTACHMENT_CLASS = R100Attachment


Platform.register(R100PlatformConfig)
