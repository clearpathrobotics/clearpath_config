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
# A200 Husky Platform Configuration
from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.platform import Platform
from clearpath_config.platform.types.attachment import BaseAttachment, PlatformAttachment
from clearpath_config.platform.types.bumper import Bumper
from typing import List


class A200TopPlate(BaseAttachment):
    PLATFORM = Platform.A200
    ATTACHMENT_MODEL = "%s.top_plate" % PLATFORM
    DEFAULT = "default"
    LARGE = "large"
    PACS = "pacs"
    MODELS = [DEFAULT, LARGE, PACS]
    PARENT = "default_mount"

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


class A200Bumper(Bumper):
    PLATFORM = Platform.A200
    ATTACHMENT_MODEL = "%s.bumper" % PLATFORM
    EXTENSION = 0.0
    DEFAULT = "default"
    MODELS = [DEFAULT]
    PARENT = "front_bumper_mount"

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


class A200SensorArch(BaseAttachment):
    PLATFORM = Platform.A200
    ATTACHMENT_MODEL = "%s.sensor_arch" % PLATFORM
    ARCH_300 = "sensor_arch_300"
    ARCH_510 = "sensor_arch_510"
    DEFAULT = ARCH_300
    MODELS = [ARCH_300, ARCH_510]
    PARENT = "default_mount"

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


class A200Attachment(PlatformAttachment):
    PLATFORM = Platform.A200
    # Top Plates
    TOP_PLATE = A200TopPlate.ATTACHMENT_MODEL
    # Bumper
    BUMPER = A200Bumper.ATTACHMENT_MODEL
    # Archs
    SENSOR_ARCH = A200SensorArch.ATTACHMENT_MODEL

    TYPES = {
        TOP_PLATE: A200TopPlate,
        BUMPER: A200Bumper,
        SENSOR_ARCH: A200SensorArch,
    }
