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
from clearpath_config.platform.attachments.a200 import A200Attachment
from clearpath_config.platform.platform import BasePlatformConfig


class A200PlatformConfig(BasePlatformConfig):
    NAME = 'a200'
    PACS = PACSProfile(rows=8, columns=7)
    INDEXING = IndexingProfile()
    VALID_BATTERIES = {
        'ES20_12C': ['S2P1'],
        'HE2613': ['S1P3', 'S1P4'],
        'HE2411': ['S1P3', 'S1P4'],
        'HE2410': ['S1P3', 'S1P4'],
    }
    VALID_DRIVETRAIN = {
        'control': ['diff_4wd'],
        'wheels': {
            'front': ['outdoor', 'indoor'],
            'rear': ['outdoor', 'indoor'],
        },
    }
    DEFAULT_CAN_ADAPTERS = []
    DEFAULT_CAN_BRIDGES = []
    ATTACHMENT_CLASS = A200Attachment


Platform.register(A200PlatformConfig)
