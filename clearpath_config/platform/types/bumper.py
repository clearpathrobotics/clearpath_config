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
from clearpath_config.common.types.accessory import Accessory
from clearpath_config.platform.types.attachment import BaseAttachment
from typing import List


class Bumper(BaseAttachment):
    ATTACHMENT_MODEL = "bumper"
    EXTENSION = 0.0
    DEFAULT = "default"
    MODELS = [DEFAULT]

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            enabled: bool = BaseAttachment.ENABLED,
            model: str = DEFAULT,
            extension: float = EXTENSION,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(
            name,
            enabled,
            model,
            parent,
            xyz,
            rpy
        )
        self.extension: float = Bumper.EXTENSION
        self.set_extension(extension)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['extension'] = self.extension
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'extension' in d:
            self.set_extension(d['extension'])

    def get_extension(self) -> float:
        return self.extension

    def set_extension(self, extension: float) -> None:
        try:
            extension = float(extension)
        except ValueError as e:
            raise AssertionError(e.args[0])
        assert isinstance(
            extension, float
        ), " ".join([
            "Bumper extension must be of type float,",
            " unexpected type '%s'" % type(extension)
        ])
        assert extension >= 0, "Bumper extension must be a positive value"
        self.extension = extension
