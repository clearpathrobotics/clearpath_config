# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
# @copyright (c) 2026, Clearpath Robotics, Inc., All rights reserved.
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
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.package_path import PackagePath
from clearpath_config.common.utils.dictionary import flip_dict


class MCUConfig(BaseConfig):
    MCU = 'mcu'

    PROTOCOL = 'protocol'
    UROS = 'uros'
    PROTON = 'proton'
    PROTOCOLS = [UROS, PROTON]

    PROFILE = 'profile'

    TEMPLATE = {
        MCU: {
            PROTOCOL: PROTOCOL,
            PROFILE: PROFILE
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        PROTOCOL: UROS,
        PROFILE: '',
    }

    def __init__(
            self,
            config: dict = {},
            protocol: str = DEFAULTS[PROTOCOL],
            profile: dict = DEFAULTS[PROFILE]
            ) -> None:
        self._config = {}
        self.protocol = protocol
        self.profile = profile
        setters = {
            self.KEYS[self.PROTOCOL]: MCUConfig.protocol,
            self.KEYS[self.PROFILE]: MCUConfig.profile
        }
        super().__init__(setters, config, self.MCU)

    @property
    def protocol(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.PROTOCOL],
            value=self._protocol
        )
        return self._protocol

    @protocol.setter
    def protocol(self, value: str) -> None:
        if value.lower() not in self.PROTOCOLS:
            raise ValueError(
                f'"{value.lower()}" protocol is invalid. Must be one of "{self.PROTOCOLS}"')
        self._protocol = value.lower()

    @property
    def profile(self) -> dict:
        if self.KEYS[self.PROFILE] not in self.template:
            return self._profile.to_dict()
        self.set_config_param(
            key=self.KEYS[self.PROFILE],
            value=self._profile.to_dict()
        )
        return self._profile.to_dict()

    @profile.setter
    def profile(self, value: dict) -> None:
        self._profile = PackagePath()
        self._profile.from_dict(value)
