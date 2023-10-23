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
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.platform import Platform
from clearpath_config.common.utils.dictionary import flip_dict


class BatteryConfig(BaseConfig):
    BATTERY = "battery"

    # Models
    MODEL = "model"
    UNKNOWN = "unknown"
    # Husky Lead Acid
    ES20_12C = "ES20-12C"
    # Husky/Jackal Li_ION
    HE2613 = "HE2613"
    # Warthog Lead Acid
    U1_35 = "U1-35"
    # Warthog LiFEPO4
    ALM12V35 = "ALM12V35"
    U24_12XP = "U24-12XP"
    U27_12XP = "U27-12XP"

    # Configurations
    CONFIGURATION = "configuration"
    S2P1 = "S2P1"
    S1P3 = "S1P3"
    S1P4 = "S1P4"
    S1P1 = "S1P1"
    S4P3 = "S4P3"
    S4P1 = "S4P1"

    VALID = {
        Platform.GENERIC: {
            UNKNOWN: [UNKNOWN]
        },
        Platform.A200: {
            ES20_12C: [S2P1],
            HE2613: [S1P3, S1P4],
        },
        Platform.J100: {
            HE2613: [S1P1],
        },
        Platform.W200: {
            U1_35: [S4P3],
            ALM12V35: [S4P3],
            U24_12XP: [S4P1],
            U27_12XP: [S4P1],
        },
    }

    TEMPLATE = {
        BATTERY: {
            MODEL: MODEL,
            CONFIGURATION: CONFIGURATION
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        MODEL: UNKNOWN,
        CONFIGURATION: UNKNOWN
    }

    def __init__(
            self,
            config: dict = {},
            model: str = DEFAULTS[MODEL],
            configuration: str = DEFAULTS[CONFIGURATION],
            ) -> None:
        # Initialization
        self._config = {}
        self.model = model
        self.configuration = configuration
        # Setter Template
        setters = {
            self.KEYS[self.MODEL]: BatteryConfig.model,
            self.KEYS[self.CONFIGURATION]: BatteryConfig.configuration,
        }
        super().__init__(setters, config, self.BATTERY)

    def update(self, serial_number: bool = False) -> None:
        if serial_number:
            platform = BaseConfig.get_platform_model()
            self.model = list(self.VALID[platform])[0]
            self.configuration = list(self.VALID[platform][self.model])[0]

    @property
    def model(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.MODEL],
            value=self._model
        )
        return self._model

    @model.setter
    def model(self, value: str) -> None:
        platform = BaseConfig.get_platform_model()
        assert platform in self.VALID, (
            "Platform must be one of: %s" % list(self.VALID)
        )
        assert value in self.VALID[platform], (
            "Battery model for platform '%s' must be one of: %s" % (
                platform, list(self.VALID[platform]))
        )
        self._model = value

    @property
    def configuration(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.CONFIGURATION],
            value=self._configuration
        )
        return self._configuration

    @configuration.setter
    def configuration(self, value: str) -> None:
        platform = BaseConfig.get_platform_model()
        assert platform in self.VALID, (
            "Platform must be one of: %s" % list(self.VALID)
        )
        assert self.model in self.VALID[platform], (
            "Battery model for platform '%s' must be one of: %s" % (
                platform, list(self.VALID[platform]))
        )
        assert value in self.VALID[platform][self.model], (
            "Battery configuration for platform '%s', and battery model '%s' must be one of: %s" % (
                platform, self.model, list(self.VALID[platform][self.model]))
        )
        self._configuration = value
