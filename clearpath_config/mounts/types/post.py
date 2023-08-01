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
from clearpath_config.mounts.types.mount import BaseMount
from typing import List


class Post(BaseMount):
    MOUNT_MODEL = "post"
    HEIGHT = 0.075
    SPACING = 0.080
    SINGLE = "single"
    DUAL = "dual"
    QUAD = "quad"
    MODELS = [SINGLE, DUAL, QUAD]

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            model: str = SINGLE,
            height: float = HEIGHT,
            spacing: float = SPACING,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        self.model = model
        self.height = height
        self.spacing = spacing
        super().__init__(idx, name, parent, xyz, rpy)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['model'] = self.get_model()
        d['height'] = self.height
        if self.get_model() != self.SINGLE:
            d['spacing'] = self.spacing
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'model' in d:
            self.set_model(d['model'])
        if 'height' in d:
            self.height = d['height']
        if 'spacing' in d:
            self.spacing = d['spacing']

    def get_model(self) -> str:
        return self.model

    def set_model(self, model: str) -> None:
        assert model in self.MODELS, " ".join([
            "Unexpected Post model '%s'," % model,
            "it must be one of the following: %s" % self.MODELS
        ])
        self.model = model

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, height: float) -> None:
        assert height > 0, (
            "Height must be positive 'float'")
        self._height = height

    @property
    def spacing(self) -> float:
        return self._spacing

    @spacing.setter
    def spacing(self, spacing: float) -> None:
        assert spacing > 0, (
            "Spacing must be positive 'float'")
        self._spacing = spacing
