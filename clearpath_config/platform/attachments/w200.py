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
from clearpath_config.common.types.platform import Platform
from clearpath_config.platform.types.attachment import BaseAttachment, PlatformAttachment


class W200Generator(BaseAttachment):
    PLATFORM = Platform.W200
    ATTACHMENT_MODEL = "%s.generator" % PLATFORM
    DEFAULT = "default"
    MODELS = [DEFAULT]
    PARENT = "default_mount"
    XYZ = [0.0, 0.0, 0.0]
    RPY = [0.0, 0.0, 0.0]

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            model: str = DEFAULT,
            enabled: bool = BaseAttachment.ENABLED,
            parent: str = PARENT,
            xyz: List[float] = XYZ,
            rpy: List[float] = RPY
            ) -> None:
        super().__init__(name, model, enabled, parent, xyz, rpy)


class W200Bulkhead(BaseAttachment):
    PLATFORM = Platform.W200
    ATTACHMENT_MODEL = "%s.bulkhead" % PLATFORM
    DEFAULT = "default"
    ARM_PLATE = "arm_plate"
    MODELS = [DEFAULT, ARM_PLATE]
    PARENT = "default_mount"
    XYZ = [0.0, 0.0, 0.0]
    RPY = [0.0, 0.0, 0.0]

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            model: str = DEFAULT,
            enabled: bool = BaseAttachment.ENABLED,
            parent: str = PARENT,
            xyz: List[float] = XYZ,
            rpy: List[float] = RPY
            ) -> None:
        super().__init__(name, model, enabled, parent, xyz, rpy)


class W200ArmPlate(BaseAttachment):
    PLATFORM = Platform.W200
    ATTACHMENT_MODEL = "%s.arm_plate" % PLATFORM
    DEFAULT = "default"
    MODELS = [DEFAULT]
    PARENT = "default_mount"
    XYZ = [0.0, 0.0, 0.0]
    RPY = [0.0, 0.0, 0.0]

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            model: str = DEFAULT,
            enabled: bool = BaseAttachment.ENABLED,
            parent: str = PARENT,
            xyz: List[float] = XYZ,
            rpy: List[float] = RPY
            ) -> None:
        super().__init__(name, model, enabled, parent, xyz, rpy)


# W200 Attachments
class W200Attachment(PlatformAttachment):
    PLATFORM = Platform.W200
    # Generator
    GENERATOR = W200Generator.ATTACHMENT_MODEL
    # Bulkhead
    BULKHEAD = W200Bulkhead.ATTACHMENT_MODEL
    # ArmPlate
    ARM_PLATE = W200ArmPlate.ATTACHMENT_MODEL

    TYPES = {
        GENERATOR: W200Generator,
        BULKHEAD: W200Bulkhead,
        ARM_PLATE: W200ArmPlate
    }
