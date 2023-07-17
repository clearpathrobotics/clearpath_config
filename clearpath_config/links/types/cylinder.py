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
from clearpath_config.links.types.link import BaseLink
from typing import List


class Cylinder(BaseLink):
    LINK_TYPE = "cylinder"
    RADIUS = 0.01
    LENGTH = 0.01

    def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            radius: float = RADIUS,
            length: float = LENGTH,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseLink.OFFSET_XYZ,
            offset_rpy: List[float] = BaseLink.OFFSET_RPY
            ) -> None:
        super().__init__(
            name,
            parent,
            xyz,
            rpy,
            offset_xyz,
            offset_rpy
        )
        self.radius: float = Cylinder.RADIUS
        self.set_radius(radius)
        self.length: float = Cylinder.LENGTH
        self.set_length(length)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['radius'] = self.get_radius()
        d['length'] = self.get_length()
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'radius' in d:
            self.set_radius(d['radius'])
        if 'length' in d:
            self.set_length(d['length'])

    def set_radius(self, radius: float) -> None:
        msg = "Radius must be a positive float value"
        assert isinstance(radius, float), msg
        assert radius >= 0.0, msg
        self.radius = radius

    def get_radius(self) -> float:
        return self.radius

    def set_length(self, length: float) -> None:
        msg = "Length must be a positive float value"
        assert isinstance(length, float), msg
        assert length >= 0.0, msg
        self.length = length

    def get_length(self) -> float:
        return self.length
