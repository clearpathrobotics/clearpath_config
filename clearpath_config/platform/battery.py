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
    # D100 Lead Acid
    TLV1222 = "TLV1222"
    # D100 LiION
    PH3054 = "PH3054"
    # D150 LiION
    RB20 = "RB20"
    # A200 Lead Acid
    ES20_12C = "ES20_12C"
    # A200/J100 LiION
    HE2613 = "HE2613"
    # W200 Lead Acid
    U1_35 = "U1_35"
    # W200 LiFEPO4
    NEC_ALM12V35 = "NEC_ALM12V35"
    VALENCE_U24_12XP = "VALENCE_U24_12XP"
    VALENCE_U27_12XP = "VALENCE_U27_12XP"

    # Configurations
    CONFIGURATION = "configuration"
    LAUNCH_ARGS = 'launch_args'
    S1P1 = "S1P1"
    S1P2 = "S1P2"
    S1P3 = "S1P3"
    S1P4 = "S1P4"
    S2P1 = "S2P1"
    S4P1 = "S4P1"
    S4P3 = "S4P3"

    VALID = {
        Platform.GENERIC: {
            UNKNOWN: [UNKNOWN]
        },
        Platform.A200: {
            ES20_12C: [S2P1],
            HE2613: [S1P3, S1P4],
        },
        Platform.DD100: {
            TLV1222: [S1P1],
            PH3054: [S1P1],
        },
        Platform.DO100: {
            TLV1222: [S1P1, S1P2, S1P3],
            PH3054: [S1P1, S1P2, S1P3],
        },
        Platform.DD150: {
            TLV1222: [S1P1],
            RB20: [S1P1],
        },
        Platform.DO150: {
            TLV1222: [S1P1, S1P2, S1P3],
            RB20: [S1P1, S1P2, S1P3],
        },
        Platform.J100: {
            HE2613: [S1P1],
        },
        Platform.W200: {
            U1_35: [S4P3],
            NEC_ALM12V35: [S4P3],
            VALENCE_U24_12XP: [S4P1],
            VALENCE_U27_12XP: [S4P1],
        },
    }

    TEMPLATE = {
        BATTERY: {
            MODEL: MODEL,
            CONFIGURATION: CONFIGURATION,
            LAUNCH_ARGS: LAUNCH_ARGS
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        MODEL: UNKNOWN,
        CONFIGURATION: UNKNOWN,
        LAUNCH_ARGS: {}
    }

    def __init__(
            self,
            config: dict = {},
            model: str = DEFAULTS[MODEL],
            configuration: str = DEFAULTS[CONFIGURATION],
            launch_args: dict = DEFAULTS[LAUNCH_ARGS]
            ) -> None:
        # Initialization
        self._config = {}
        if model == self.DEFAULTS[self.MODEL] or model == self.UNKNOWN:
            self.update_defaults()
            self.model = self.DEFAULTS[self.MODEL]
        else:
            self.model = model
        if configuration == self.DEFAULTS[self.CONFIGURATION] or model == self.UNKNOWN:
            self.update_defaults()
            self.configuration = self.DEFAULTS[self.CONFIGURATION]
        else:
            self.configuration = configuration
        if launch_args == self.DEFAULTS[self.LAUNCH_ARGS] or not launch_args:
            self.launch_args = self.DEFAULTS[self.LAUNCH_ARGS]
        else:
            self.launch_args = launch_args

        # Setter Template
        setters = {
            self.KEYS[self.MODEL]: BatteryConfig.model,
            self.KEYS[self.CONFIGURATION]: BatteryConfig.configuration,
            self.KEYS[self.LAUNCH_ARGS]: BatteryConfig.launch_args,
        }
        super().__init__(setters, config, self.BATTERY)

    def update_defaults(self) -> None:
        platform = BaseConfig.get_platform_model()
        self.DEFAULTS[self.MODEL] = list(self.VALID[platform])[0]
        self.DEFAULTS[self.CONFIGURATION] = list(
            self.VALID[platform][self.DEFAULTS[self.MODEL]])[0]

    def update(self, serial_number: bool = False) -> None:
        if serial_number:
            self.update_defaults()
            self.model = self.DEFAULTS[self.MODEL]
            self.configuration = self.DEFAULTS[self.CONFIGURATION]

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
        assert platform in self.VALID, ((
            "Platform %s is invalid. " % platform +
            "Platform must be one of: %s" % list(self.VALID)
        ))
        assert value in self.VALID[platform], ((
            "Battery model %s is invalid. " % value +
            "Battery model for platform '%s' must be one of: %s" % (
                platform, list(self.VALID[platform]))
        ))
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
        assert platform in self.VALID, ((
            "Platform %s is invalid. " % platform +
            "Platform must be one of: %s" % list(self.VALID)
        ))
        assert self.model in self.VALID[platform], ((
            "Battery model %s in invalid. " % self.model +
            "Battery model for platform '%s' must be one of: %s" % (
                platform, list(self.VALID[platform]))
        ))
        assert value in self.VALID[platform][self.model], ((
            "Battery configuration %s invalid. " % value +
            "For platform '%s' and battery model '%s', it must be one of: %s" % (
                platform, self.model, list(self.VALID[platform][self.model]))
        ))
        self._configuration = value

    @property
    def launch_args(self) -> dict:
        self.set_config_param(
            key=self.KEYS[self.LAUNCH_ARGS],
            value=self._launch_args
        )
        return self._launch_args

    @launch_args.setter
    def launch_args(self, value: dict) -> None:
        assert isinstance(value, dict), ((
            "Battery Launch args %s are invalid. " % value +
            "They must be in the format of a dictionary."
        ))
        self._launch_args = value
