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
import os

from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.file import File
from clearpath_config.links.types.link import BaseLink
from typing import List


class Mesh(BaseLink):
    LINK_TYPE = "mesh"
    VISUAL = "empty.stl"
    PACKAGE = ""
    # COLLISION = "empty.stl"

    def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            visual: str = VISUAL,
            package: str = PACKAGE,
            # collision: float = COLLISION,
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

        self.visual: str = Mesh.VISUAL
        self.set_visual(visual, package)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['visual'] = self.get_visual()
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'visual' in d:
            if 'package' in d:
                self.set_visual(d['visual'], d['package'])
            else:
                self.set_visual(d['visual'])

    def set_visual(self, visual: str, package: str = "") -> None:
        if package:
            self.visual = os.path.join("$(find " + package + ")",
                                       File.clean(visual, make_abs=False))
        else:
            self.visual = File.clean(visual, make_abs=True)

    def get_visual(self) -> str:
        return self.visual
