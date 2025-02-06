# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
# @copyright (c) 2025, Clearpath Robotics, Inc., All rights reserved.
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

from clearpath_config.common.types.package_path import PackagePath


class Material():
    NAME = 'name'
    COLOR = 'color'
    TEXTURE = 'texture'

    def __init__(
            self,
            name: str = None,
            color: List = None,
            texture: PackagePath | dict = None,
            ) -> None:
        self.name = name
        self.color = color
        self.texture = texture

    def from_dict(self, d: dict) -> None:
        if self.NAME in d:
            self.name = d[self.NAME]
        if self.COLOR in d:
            self.color = d[self.COLOR]
        if self.TEXTURE in d:
            self.texture in d[self.TEXTURE]

    def to_dict(self) -> dict:
        return {
            self.NAME: self.name,
            self.COLOR: self.color,
            self.TEXTURE: self.texture
        }

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def color(self) -> List:
        return self._color

    @color.setter
    def color(self, color: List) -> None:
        if color:
            assert isinstance(color, List), (
                f'Material color must be a list of floats.'
                f'Received {color}')
            assert len(color) == 4, (
                f'Material color must be a list of 4 floats, representing RGBA.'
                f'Received list of length {len(color)}')
        self._color = color

    @property
    def texture(self) -> PackagePath:
        return self._texture

    @texture.setter
    def texture(self, texture: PackagePath | dict):
        if texture:
            if isinstance(texture, PackagePath):
                self._texture = texture
            if isinstance(texture, dict):
                self._texture = PackagePath()
                self._texture.from_dict(dict)
        self._texture = None
