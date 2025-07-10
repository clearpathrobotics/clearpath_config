# Software License Agreement (BSD)
#
# @author    Roni Kreinin <rkreinin@clearpathrobotics.com>
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
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.platform import Platform
from clearpath_config.common.utils.dictionary import flip_dict


class DrivetrainConfig(BaseConfig):
    DRIVETRAIN = 'drivetrain'
    TYPE = 'type'
    WHEELS = 'wheels'

    # Types
    DIFF_FWD = 'diff_fwd'
    DIFF_RWD = 'diff_rwd'
    DIFF_4WD = 'diff_4wd'
    OMNI_4WD = 'omni_4wd'

    # Wheels
    OUTDOOR = 'outdoor'
    INDOOR = 'indoor'
    MECANUM = 'mecanum'
    TRACK = 'track'

    # Configurations
    CONFIGURATION = 'configuration'
    LAUNCH_ARGS = 'launch_args'

    # Valid drivetrain type and wheels given a platform
    VALID = {
        TYPE: {
            Platform.GENERIC: [DIFF_FWD, DIFF_RWD, DIFF_4WD, OMNI_4WD],
            Platform.A200: [DIFF_FWD],
            Platform.A300: [DIFF_4WD, DIFF_FWD, DIFF_RWD, OMNI_4WD],
            Platform.DD100: [DIFF_FWD],
            Platform.DO100: [OMNI_4WD, DIFF_4WD, DIFF_FWD, DIFF_RWD],
            Platform.DD150: [DIFF_FWD],
            Platform.DO150: [OMNI_4WD, DIFF_4WD, DIFF_FWD, DIFF_RWD],
            Platform.J100: [DIFF_FWD],
            Platform.R100: [OMNI_4WD, DIFF_4WD, DIFF_FWD, DIFF_RWD],
            Platform.W200: [DIFF_FWD],
        },
        WHEELS: {
            Platform.GENERIC: [OUTDOOR, INDOOR, MECANUM, TRACK],
            Platform.A200: [OUTDOOR, INDOOR],
            Platform.A300: [OUTDOOR, MECANUM],
            Platform.DD100: [INDOOR],
            Platform.DO100: [MECANUM],
            Platform.DD150: [INDOOR],
            Platform.DO150: [MECANUM],
            Platform.J100: [OUTDOOR],
            Platform.R100: [MECANUM],
            Platform.W200: [OUTDOOR, TRACK],
        }
    }

    # Valid wheels given a drivetrain type
    VALID_WHEELS = {
        DIFF_FWD: [OUTDOOR, INDOOR, MECANUM, TRACK],
        DIFF_RWD: [OUTDOOR, INDOOR, MECANUM, TRACK],
        DIFF_4WD: [OUTDOOR, INDOOR, MECANUM, TRACK],
        OMNI_4WD: [MECANUM]
    }

    # Config template
    TEMPLATE = {
      DRIVETRAIN: {
          TYPE: TYPE,
          WHEELS: WHEELS
      }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        TYPE: DIFF_FWD,
        WHEELS: OUTDOOR
    }

    def __init__(
        self, config: dict = {}, dt_type: str = DEFAULTS[TYPE], wheels: str = DEFAULTS[WHEELS]
    ) -> None:
        # Initialization
        self._config = {}
        self._wheels = self.DEFAULTS[self.WHEELS]
        self._dt_type = self.DEFAULTS[self.TYPE]

        if dt_type == self.DEFAULTS[self.TYPE] and wheels == self.DEFAULTS[self.WHEELS]:
            self.update_defaults()
            self.wheels = self.DEFAULTS[self.WHEELS]
            self.dt_type = self.DEFAULTS[self.TYPE]
        elif dt_type == self.DEFAULTS[self.TYPE]:
            self.update_defaults()
            self.wheels = wheels
            self.dt_type = self.DEFAULTS[self.TYPE]
        elif wheels == self.DEFAULTS[self.WHEELS]:
            self.update_defaults()
            self.dt_type = dt_type
            self.wheels = self.DEFAULTS[self.WHEELS]
        else:
            self.wheels = wheels
            self.dt_type = dt_type

        # Setter Template
        setters = {
            self.KEYS[self.TYPE]: DrivetrainConfig.dt_type,
            self.KEYS[self.WHEELS]: DrivetrainConfig.wheels,
        }
        super().__init__(setters, config, self.DRIVETRAIN)

    def update_defaults(self) -> None:
        platform = BaseConfig.get_platform_model()
        self.DEFAULTS[self.TYPE] = list(self.VALID[self.TYPE][platform])[0]
        self.DEFAULTS[self.WHEELS] = list(self.VALID[self.WHEELS][platform])[0]

    def update(self, serial_number: bool = False) -> None:
        if serial_number:
            self.update_defaults()
            self.dt_type = self.DEFAULTS[self.TYPE]
            self.wheels = self.DEFAULTS[self.WHEELS]

    @property
    def dt_type(self) -> str:
        self.set_config_param(key=self.KEYS[self.TYPE], value=self._dt_type)
        return self._dt_type

    @dt_type.setter
    def dt_type(self, value: str) -> None:
        platform = BaseConfig.get_platform_model()
        assert platform in self.VALID[self.TYPE], (
            f'Platform "{platform}" is invalid. Must be one of "{list(self.VALID[self.TYPE])}"'
        )  # noqa:E501
        assert value in self.VALID[self.TYPE][platform], (
            f'Drivetrain type "{value}" is invalid. Drivetrain type for platform "{platform}" must be one of "{list(self.VALID[self.TYPE][platform])}"'
        )  # noqa:E501
        self._dt_type = value
        # Check that wheels are valid with updated type
        if self.wheels not in list(set(self.VALID[self.WHEELS][platform]).intersection(self.VALID_WHEELS[self.dt_type])):
            self.wheels = list(set(self.VALID[self.WHEELS][platform]).intersection(self.VALID_WHEELS[self.dt_type]))[0]

    @property
    def wheels(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.WHEELS], value=self._wheels
        )
        return self._wheels

    @wheels.setter
    def wheels(self, value: str) -> None:
        platform = BaseConfig.get_platform_model()
        assert platform in self.VALID[self.TYPE], (
            f'Platform "{platform}" is invalid. Must be one of "{list(self.VALID[self.WHEELS])}"'
        )  # noqa:E501
        assert self.dt_type in self.VALID[self.TYPE][platform], (
            f'Drivetrain type "{self.dt_type}" is invalid. Drivetrain type for platform "{platform}" must be one of "{list(self.VALID[self.TYPE][platform])}"'
        )  # noqa:E501
        assert value in self.VALID[self.WHEELS][platform] and value in self.VALID_WHEELS[self.dt_type], (
            f'Wheel type "{value}" is invalid. For platform "{platform}" and drivetrain "{self.dt_type}" it must be one of "{list(set(self.VALID[self.WHEELS][platform]).intersection(self.VALID_WHEELS[self.dt_type]))}"'
        )  # noqa:E501
        self._wheels = value
