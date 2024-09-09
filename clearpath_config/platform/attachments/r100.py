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
from typing import List
from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.platform import Platform
from clearpath_config.platform.types.attachment import BaseAttachment, PlatformAttachment


class R100FAMS(BaseAttachment):
    PLATFORM = Platform.R100
    ATTACHMENT_MODEL = "%s.fams" % PLATFORM
    DEFAULT = "default"
    MODELS = [DEFAULT]
    PARENT = "default_mount"
    TABLE_HEIGHT = 0.3

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            model: str = DEFAULT,
            table_height: float = TABLE_HEIGHT,
            enabled: bool = BaseAttachment.ENABLED,
            parent: str = PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ) -> None:
        super().__init__(name, model, enabled, parent, xyz, rpy)
        self.table_height = table_height

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['table_height'] = self.table_height
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'table_height' in d:
            self.table_height = d['table_height']
        return d


class R100HAMS(BaseAttachment):
    PLATFORM = Platform.R100
    ATTACHMENT_MODEL = "%s.hams" % PLATFORM
    DEFAULT = "default"
    MODELS = [DEFAULT]
    PARENT = "default_mount"
    TABLE_HEIGHT = 0.6
    MOUNT_HEIGHT = 0.3

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            model: str = DEFAULT,
            table_height: float = TABLE_HEIGHT,
            mount_height: float = MOUNT_HEIGHT,
            enabled: bool = BaseAttachment.ENABLED,
            parent: str = PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ) -> None:
        super().__init__(name, model, enabled, parent, xyz, rpy)
        self.table_height = table_height
        self.mount_height = mount_height

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['table_height'] = self.table_height
        d['mount_height'] = self.mount_height
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'table_height' in d:
            self.table_height = d['table_height']
        if 'mount_height' in d:
            self.mount_height = d['mount_height']
        return d


class R100Tower(BaseAttachment):
    PLATFORM = Platform.R100
    ATTACHMENT_MODEL = "%s.tower" % PLATFORM
    DEFAULT = "default"
    MODELS = [DEFAULT]
    PARENT = "default_mount"
    LEFT_HEIGHT = 0.0
    RIGHT_HEIGHT = 0.0

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            model: str = DEFAULT,
            enabled: bool = BaseAttachment.ENABLED,
            parent: str = PARENT,
            left_height: float = LEFT_HEIGHT,
            right_height: float = RIGHT_HEIGHT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ) -> None:
        super().__init__(name, model, enabled, parent, xyz, rpy)
        self.left_height = left_height
        self.right_height = right_height

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['left_height'] = self.left_height
        d['right_height'] = self.right_height

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'left_height' in d:
            self.left_height = d['left_height']
        if 'right_height' in d:
            self.right_height = d['right_height']


# R100 Attachments
class R100Attachment(PlatformAttachment):
    PLATFORM = Platform.R100
    # Arm Mount
    HAMS = R100HAMS.ATTACHMENT_MODEL
    FAMS = R100FAMS.ATTACHMENT_MODEL
    TOWER = R100Tower.ATTACHMENT_MODEL

    TYPES = {
        HAMS: R100HAMS,
        FAMS: R100FAMS,
        TOWER: R100Tower
    }
