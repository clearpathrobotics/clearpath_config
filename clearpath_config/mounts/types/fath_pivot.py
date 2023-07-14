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
from math import pi
from typing import List


class FathPivot(BaseMount):
    MOUNT_MODEL = "fath_pivot"
    # Default Values
    ANGLE = 0.0

    def __init__(
        self,
        parent: str = Accessory.PARENT,
        angle: float = ANGLE,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
    ) -> None:
        super().__init__(
            name=FathPivot.get_name_from_idx(0),
            parent=parent,
            xyz=xyz,
            rpy=rpy)
        self.angle = 0.0
        if angle:
            self.set_angle(angle)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['angle'] = self.get_angle()
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'angle' in d:
            self.set_angle(d['angle'])

    def get_angle(self) -> float:
        return self.angle

    def set_angle(self, angle: float) -> None:
        assert -pi < angle <= pi, (
            "Angle '%s' must be in radian and  between pi and -pi"
        )
        self.angle = angle
