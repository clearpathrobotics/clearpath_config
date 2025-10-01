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

from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.platform import Platform


class BaseAttachment(Accessory):
    PLATFORM = Platform.GENERIC
    ATTACHMENT_MODEL = '%s.attachment' % PLATFORM
    ENABLED = True
    # Models
    DEFAULT = 'default'
    MODELS = [DEFAULT]

    def __init__(
            self,
            name: str = ATTACHMENT_MODEL,
            model: str = DEFAULT,
            enabled: bool = ENABLED,
            parent: str = ...,
            xyz: List[float] = ...,
            rpy: List[float] = ...
            ) -> None:
        super().__init__(name, parent, xyz, rpy)
        self.platform = self.ATTACHMENT_MODEL.split('.')[0]
        self.file = self.ATTACHMENT_MODEL.split('.')[-1]
        self.model = self.DEFAULT
        self.enabled = self.ENABLED
        self.set_model(model)
        self.set_enabled(enabled)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['type'] = self.ATTACHMENT_MODEL
        d['model'] = self.get_model()
        d['enabled'] = self.get_enabled()
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'model' in d:
            self.set_model(d['model'])
        if 'enabled' in d:
            self.set_enabled(d['enabled'])

    def set_enabled(self, enable: bool) -> None:
        self.enabled = bool(enable)

    def get_enabled(self) -> bool:
        return self.enabled

    def get_model(self) -> str:
        return self.model

    def set_model(self, model: str) -> None:
        if model not in self.MODELS:
            raise ValueError(f'{self.ATTACHMENT_MODEL.title()} model "{model}" is not not of "{self.MODELS}"')  # noqa:E501
        self.model = model


class PlatformAttachment(BaseAttachment):
    PLATFORM = Platform.GENERIC
    TYPES = {}

    @classmethod
    def is_valid(cls, _type: str) -> bool:
        return _type in cls.TYPES

    def __new__(cls, _type: str) -> BaseAttachment:
        if not cls.is_valid(_type):
            raise ValueError(f'{cls.PLATFORM} does not have attachment "{_type}". Must be one of "{cls.TYPES}"')  # noqa:E501
        return cls.TYPES[_type]
