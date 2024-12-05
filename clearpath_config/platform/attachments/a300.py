# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
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
# A300 Husky Platform Configuration
from typing import List

from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.platform import Platform
from clearpath_config.platform.types.attachment import BaseAttachment, PlatformAttachment
from clearpath_config.platform.types.bumper import Bumper


class A300TopPlate(BaseAttachment):
    PLATFORM = Platform.A300
    ATTACHMENT_MODEL = '%s.top_plate' % PLATFORM
    DEFAULT = 'default'
    PACS = 'pacs'
    MODELS = [DEFAULT, PACS]
    PARENT = 'default_mount'

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            model: str = DEFAULT,
            enabled: bool = BaseAttachment.ENABLED,
            parent: str = PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(name, model, enabled, parent, xyz, rpy)


class A300Bumper(Bumper):
    PLATFORM = Platform.A300
    ATTACHMENT_MODEL = '%s.bumper' % PLATFORM
    EXTENSION = 0.0
    DEFAULT = 'default'
    MODELS = [DEFAULT]
    PARENT = 'front_bumper_mount'

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            model: str = DEFAULT,
            enabled: bool = BaseAttachment.ENABLED,
            extension: float = EXTENSION,
            parent: str = PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(name, model, enabled, extension, parent, xyz, rpy)


class A300AMPFrame(BaseAttachment):
    PLATFORM = Platform.A300
    ATTACHMENT_MODEL = '%s.amp_frame' % PLATFORM
    DEFAULT = 'default'
    MODELS = [DEFAULT]
    PARENT = 'default_mount'

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            model: str = DEFAULT,
            enabled: bool = BaseAttachment.ENABLED,
            parent: str = PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(name, model, enabled, parent, xyz, rpy)


class A300Attachment(PlatformAttachment):
    PLATFORM = Platform.A300
    # Top Plates
    TOP_PLATE = A300TopPlate.ATTACHMENT_MODEL
    # Bumper
    BUMPER = A300Bumper.ATTACHMENT_MODEL
    # AMP frame
    AMP_FRAME = A300AMPFrame.ATTACHMENT_MODEL

    TYPES = {
        TOP_PLATE: A300TopPlate,
        BUMPER: A300Bumper,
        AMP_FRAME: A300AMPFrame,
    }
