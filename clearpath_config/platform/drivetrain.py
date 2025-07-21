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
    CONTROL = 'control'
    WHEELS = 'wheels'
    FRONT = 'front'
    REAR = 'rear'

    # Types
    DIFF_FWD = 'diff_fwd'
    DIFF_RWD = 'diff_rwd'
    DIFF_4WD = 'diff_4wd'
    OMNI_4WD = 'omni_4wd'

    # Wheels
    OUTDOOR = 'outdoor'
    INDOOR = 'indoor'
    MECANUM = 'mecanum'
    TRACKS = 'tracks'
    CASTER = 'caster'

    # Configurations
    CONFIGURATION = 'configuration'
    LAUNCH_ARGS = 'launch_args'

    # Valid drivetrain type and wheels given a platform
    VALID = {
        Platform.GENERIC: {
            CONTROL: [DIFF_FWD, DIFF_RWD, DIFF_4WD, OMNI_4WD],
            WHEELS: {
                FRONT: [OUTDOOR, INDOOR, MECANUM, TRACKS, CASTER],
                REAR:  [OUTDOOR, INDOOR, MECANUM, TRACKS, CASTER],
            }
        },
        Platform.A200: {
            CONTROL: [DIFF_4WD],
            WHEELS: {
                FRONT: [OUTDOOR, INDOOR],
                REAR:  [OUTDOOR, INDOOR]
            }
        },
        Platform.A300: {
            CONTROL: [DIFF_4WD, DIFF_FWD, DIFF_RWD, OMNI_4WD],
            WHEELS: {
                FRONT: [OUTDOOR, CASTER, MECANUM],
                REAR:  [OUTDOOR, CASTER, MECANUM]
            }
        },
        Platform.DD100: {
            CONTROL: [DIFF_FWD],
            WHEELS: {
                FRONT: [INDOOR],
                REAR:  [CASTER]
            }
        },
        Platform.DO100: {
            CONTROL: [OMNI_4WD, DIFF_4WD],
            WHEELS: {
                FRONT: [MECANUM],
                REAR:  [MECANUM]
            }
        },
        Platform.DD150: {
            CONTROL: [DIFF_FWD],
            WHEELS: {
                FRONT: [INDOOR],
                REAR:  [CASTER]
            }
        },
        Platform.DO150: {
            CONTROL: [OMNI_4WD, DIFF_4WD],
            WHEELS: {
                FRONT: [MECANUM],
                REAR:  [MECANUM]
            }
        },
        Platform.J100: {
            CONTROL: [DIFF_4WD],
            WHEELS: {
                FRONT: [OUTDOOR],
                REAR:  [OUTDOOR]
            }
        },
        Platform.R100: {
            CONTROL: [OMNI_4WD, DIFF_4WD],
            WHEELS: {
                FRONT: [MECANUM],
                REAR:  [MECANUM]
            }
        },
        Platform.W200: {
            CONTROL: [DIFF_4WD],
            WHEELS: {
                FRONT: [OUTDOOR, TRACKS],
                REAR:  [OUTDOOR, TRACKS]
            }
        }
    }

    # Valid wheels given a drivetrain type
    VALID_WHEELS = {
        DIFF_FWD: {
            FRONT: [OUTDOOR, INDOOR, MECANUM, TRACKS],
            REAR:  [OUTDOOR, INDOOR, MECANUM, TRACKS, CASTER]
        },
        DIFF_RWD: {
            FRONT: [OUTDOOR, INDOOR, MECANUM, TRACKS, CASTER],
            REAR:  [OUTDOOR, INDOOR, MECANUM, TRACKS]
        },
        DIFF_4WD: {
            FRONT: [OUTDOOR, INDOOR, MECANUM, TRACKS],
            REAR:  [OUTDOOR, INDOOR, MECANUM, TRACKS]
        },
        OMNI_4WD: {
            FRONT: [MECANUM],
            REAR:  [MECANUM]
        }
    }

    # Config template
    TEMPLATE = {
        DRIVETRAIN: {
            CONTROL: CONTROL,
            WHEELS: {
                FRONT: FRONT,
                REAR: REAR
            }
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        CONTROL: DIFF_FWD,
        FRONT: OUTDOOR,
        REAR: OUTDOOR
    }

    def __init__(
        self, config: dict = {},
        control: str = DEFAULTS[CONTROL],
        front_wheels: str = DEFAULTS[FRONT],
        rear_wheels: str = DEFAULTS[REAR]
    ) -> None:
        # Initialization
        self._config = {}
        self._front_wheels = self.DEFAULTS[self.FRONT]
        self._rear_wheels = self.DEFAULTS[self.REAR]
        self._control = self.DEFAULTS[self.CONTROL]

        if control == self.DEFAULTS[self.CONTROL]:
            self.update_defaults()
            self.control = self.DEFAULTS[self.CONTROL]
        else:
            self.control = control

        if front_wheels == self.DEFAULTS[self.FRONT]:
            self.update_defaults()
            self.front_wheels = self.DEFAULTS[self.FRONT]
        else:
            self.front_wheels = front_wheels

        if rear_wheels == self.DEFAULTS[self.REAR]:
            self.update_defaults()
            self.rear_wheels = self.DEFAULTS[self.REAR]
        else:
            self.rear_wheels = rear_wheels

        # Setter Template
        setters = {
            self.KEYS[self.CONTROL]: DrivetrainConfig.control,
            self.KEYS[self.FRONT]: DrivetrainConfig.front_wheels,
            self.KEYS[self.REAR]: DrivetrainConfig.rear_wheels,
        }
        super().__init__(setters, config, self.DRIVETRAIN)

    def update_defaults(self) -> None:
        platform = BaseConfig.get_platform_model()
        self.DEFAULTS[self.CONTROL] = list(self.VALID[platform][self.CONTROL])[0]
        self.DEFAULTS[self.FRONT] = list(self.VALID[platform][self.WHEELS][self.FRONT])[0]
        self.DEFAULTS[self.REAR] = list(self.VALID[platform][self.WHEELS][self.REAR])[0]

    def update(self, serial_number: bool = False) -> None:
        if serial_number:
            self.update_defaults()
            self.control = self.DEFAULTS[self.CONTROL]
            self.front_wheels = self.DEFAULTS[self.FRONT]
            self.rear_wheels = self.DEFAULTS[self.REAR]

    @property
    def control(self) -> str:
        self.set_config_param(key=self.KEYS[self.CONTROL], value=self._control)
        return self._control

    @control.setter
    def control(self, value: str) -> None:
        platform = BaseConfig.get_platform_model()
        assert platform in self.VALID, (
            f'Platform "{platform}" is invalid. Must be one of "{list(self.VALID)}"'
        )  # noqa:E501
        assert value in self.VALID[platform][self.CONTROL], (
            f'Drivetrain control "{value}" is invalid. '
            f'Drivetrain control for platform "{platform}" must be '
            f'one of "{list(self.VALID[platform][self.CONTROL])}"'
        )  # noqa:E501
        self._control = value
        # Check that front wheels are valid with updated control
        if self.front_wheels not in list(
            set(self.VALID[platform][self.WHEELS][self.FRONT]).intersection(
                self.VALID_WHEELS[self.control][self.FRONT])):
            self.front_wheels = list(
                set(self.VALID[platform][self.WHEELS][self.FRONT]).intersection(
                    self.VALID_WHEELS[self.control][self.FRONT]))[0]
        # Check that rear wheels are valid with updated control
        if self.rear_wheels not in list(
            set(self.VALID[platform][self.WHEELS][self.REAR]).intersection(
                self.VALID_WHEELS[self.control][self.REAR])):
            self.rear_wheels = list(
                  set(self.VALID[platform][self.WHEELS][self.REAR]).intersection(
                      self.VALID_WHEELS[self.control][self.REAR]))[0]

    @property
    def front_wheels(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.FRONT], value=self._front_wheels
        )
        return self._front_wheels

    @front_wheels.setter
    def front_wheels(self, value: str) -> None:
        platform = BaseConfig.get_platform_model()
        assert platform in self.VALID, (
            f'Platform "{platform}" is invalid. Must be one of "{list(self.VALID[self.WHEELS])}"'
        )  # noqa:E501
        assert self.control in self.VALID[platform][self.CONTROL], (
            f'Drivetrain control "{self.control}" is invalid. '
            f'Drivetrain control for platform "{platform}" must be '
            f'one of "{list(self.VALID[self.CONTROL][platform])}"'
        )  # noqa:E501
        assert value in self.VALID[platform][self.WHEELS][self.FRONT] and \
               value in self.VALID_WHEELS[self.control][self.FRONT], (
            f'Front wheel type "{value}" is invalid. '
            f'For platform "{platform}" and drivetrain "{self.control}" it must be '
            f'one of "{list(set(self.VALID[platform][self.WHEELS][self.FRONT]).intersection(
                 self.VALID_WHEELS[self.control][self.FRONT]))}"'
        )  # noqa:E501
        self._front_wheels = value

    @property
    def rear_wheels(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.REAR], value=self._rear_wheels
        )
        return self._rear_wheels

    @rear_wheels.setter
    def rear_wheels(self, value: str) -> None:
        platform = BaseConfig.get_platform_model()
        assert platform in self.VALID, (
            f'Platform "{platform}" is invalid. Must be one of "{list(self.VALID[self.WHEELS])}"'
        )  # noqa:E501
        assert self.control in self.VALID[platform][self.CONTROL], (
            f'Drivetrain control "{self.control}" is invalid. '
            f'Drivetrain control for platform "{platform}" must be '
            f'one of "{list(self.VALID[self.CONTROL][platform])}"'
        )  # noqa:E501
        assert value in self.VALID[platform][self.WHEELS][self.REAR] and \
               value in self.VALID_WHEELS[self.control][self.REAR], (
            f'Rear wheel type "{value}" is invalid. '
            f'For platform "{platform}" and drivetrain "{self.control}" it must be '
            f'one of "{list(set(self.VALID[platform][self.WHEELS][self.REAR]).intersection(
                 self.VALID_WHEELS[self.control][self.REAR]))}"'
        )  # noqa:E501
        self._rear_wheels = value
