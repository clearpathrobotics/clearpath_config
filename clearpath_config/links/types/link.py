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
from typing import List


class BaseLink(Accessory):
    """
    Base Link object contains all common methods for links.

    Parameters
    ----------
    name : str
        Required. Results in "{name}_link" in URDF.
    parent : str
        Parent link in URDF.
    xyz: List[float]
        Translational offset from parent link.
    rpy: List[float]
        Rotational offset from parent link.
    offset_xyz: List[float]
        Translational offset of visual w.r.t. link.
    offset_rpy: List[float]
        Rotational offset of visual w.r.t. link.

    Attributes
    ----------
    LINK_TYPE : str
        Type of string used to generate URDF link.

    """

    LINK_TYPE = "base"
    OFFSET_XYZ = [0.0, 0.0, 0.0]
    OFFSET_RPY = [0.0, 0.0, 0.0]

    def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = OFFSET_XYZ,
            offset_rpy: List[float] = OFFSET_RPY
            ) -> None:
        super().__init__(name, parent, xyz, rpy)
        self.offset_xyz: List[float] = BaseLink.OFFSET_XYZ
        self.set_offset_xyz(offset_xyz)
        self.offset_rpy: List[float] = BaseLink.OFFSET_RPY
        self.set_offset_rpy(offset_rpy)

    def to_dict(self) -> dict:
        d = {}
        d['name'] = self.get_name()
        d['parent'] = self.get_parent()
        d['xyz'] = self.get_xyz()
        d['rpy'] = self.get_rpy()
        return d

    def from_dict(self, d: dict) -> None:
        if 'name' in d:
            self.set_name(d['name'])
        if 'parent' in d:
            self.set_parent(d['parent'])
        if 'xyz' in d:
            self.set_xyz(d['xyz'])
        if 'rpy' in d:
            self.set_rpy(d['rpy'])

    @classmethod
    def get_link_type(cls) -> str:
        return cls.LINK_TYPE

    def set_offset_xyz(self, xyz: List[float]) -> None:
        Accessory.assert_valid_triplet(
            xyz,
            "Offset XYZ must be a list of exactly three float values"
        )
        self.offset_xyz = xyz

    def get_offset_xyz(self) -> List[float]:
        return self.offset_xyz

    def set_offset_rpy(self, rpy: List[float]) -> None:
        Accessory.assert_valid_triplet(
            rpy,
            "Offset RPY must be a list of exactly three float values"
        )
        self.offset_rpy = rpy
