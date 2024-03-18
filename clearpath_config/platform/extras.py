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
from clearpath_config.common.types.package_path import PackagePath
from clearpath_config.common.types.platform import Platform
from clearpath_config.common.utils.dictionary import (
    flatten_dict,
    flip_dict,
    unflatten_dict,
)


class ROSParameterDefaults:
    A200 = {
        "platform_velocity_controller.wheel_radius": 0.1651,
        "platform_velocity_controller.linear.x.max_velocity": 1.0,
        "platform_velocity_controller.linear.x.min_velocity": -1.0,
        "platform_velocity_controller.linear.x.max_acceleration": 3.0,
        "platform_velocity_controller.linear.x.min_acceleration": -3.0,
        "platform_velocity_controller.angular.z.max_velocity": 2.0,
        "platform_velocity_controller.angular.z.min_velocity": -2.0,
        "platform_velocity_controller.angular.z.max_acceleration": 6.0,
        "platform_velocity_controller.angular.z.min_acceleration": -6.0,
    }

    DD100 = {
        "platform_velocity_controller.wheel_radius": 0.049,
        "platform_velocity_controller.linear.x.max_velocity": 1.3,
        "platform_velocity_controller.linear.x.min_velocity": -1.3,
        "platform_velocity_controller.linear.x.max_acceleration": 1.0,
        "platform_velocity_controller.linear.x.min_acceleration": -1.0,
        "platform_velocity_controller.angular.z.max_velocity": 4.0,
        "platform_velocity_controller.angular.z.min_velocity": -4.0,
        "platform_velocity_controller.angular.z.max_acceleration": 2.0,
        "platform_velocity_controller.angular.z.min_acceleration": -2.0,
    }

    DD150 = DD100

    DO100 = {
        "platform_velocity_controller.wheel_radius": 0.05,
        "platform_velocity_controller.linear.x.max_velocity": 1.3,
        "platform_velocity_controller.linear.x.min_velocity": -1.3,
        "platform_velocity_controller.linear.x.max_acceleration": 1.0,
        "platform_velocity_controller.linear.x.min_acceleration": -1.0,
        "platform_velocity_controller.linear.y.max_velocity": 1.3,
        "platform_velocity_controller.linear.y.min_velocity": -1.3,
        "platform_velocity_controller.linear.y.max_acceleration": 1.0,
        "platform_velocity_controller.linear.y.min_acceleration": -1.0,
        "platform_velocity_controller.angular.z.max_velocity": 4.0,
        "platform_velocity_controller.angular.z.min_velocity": -4.0,
        "platform_velocity_controller.angular.z.max_acceleration": 2.0,
        "platform_velocity_controller.angular.z.min_acceleration": -2.0,
    }

    DO150 = DO100

    GENERIC = {
        "platform_velocity_controller.wheel_radius": 0.1,
        "platform_velocity_controller.linear.x.max_velocity": 1.0,
        "platform_velocity_controller.linear.x.min_velocity": -1.0,
        "platform_velocity_controller.linear.x.max_acceleration": 1.0,
        "platform_velocity_controller.linear.x.min_acceleration": -1.0,
        "platform_velocity_controller.angular.z.max_velocity": 1.0,
        "platform_velocity_controller.angular.z.min_velocity": -1.0,
        "platform_velocity_controller.angular.z.max_acceleration": 1.0,
        "platform_velocity_controller.angular.z.min_acceleration": -1.0,
    }

    J100 = {
        "platform_velocity_controller.wheel_radius": 0.098,
        "platform_velocity_controller.linear.x.max_velocity": 2.0,
        "platform_velocity_controller.linear.x.min_velocity": -2.0,
        "platform_velocity_controller.linear.x.max_acceleration": 20.0,
        "platform_velocity_controller.linear.x.min_acceleration": -20.0,
        "platform_velocity_controller.angular.z.max_velocity": 4.0,
        "platform_velocity_controller.angular.z.min_velocity": -4.0,
        "platform_velocity_controller.angular.z.max_acceleration": 25.0,
        "platform_velocity_controller.angular.z.min_acceleration": -25.0,
    }

    W200 = {
        "platform_velocity_controller.wheel_radius": 0.3,
        "platform_velocity_controller.linear.x.max_velocity": 5.0,
        "platform_velocity_controller.linear.x.min_velocity": -5.0,
        "platform_velocity_controller.linear.x.max_acceleration": 50.0,
        "platform_velocity_controller.linear.x.min_acceleration": -50.0,
        "platform_velocity_controller.angular.z.max_velocity": 4.0,
        "platform_velocity_controller.angular.z.min_velocity": -4.0,
        "platform_velocity_controller.angular.z.max_acceleration": 40.0,
        "platform_velocity_controller.angular.z.min_acceleration": -40.0,
    }

    DEFAULTS = {
        Platform.A200: A200,
        Platform.DD100: DD100,
        Platform.DO100: DO100,
        Platform.DD150: DD150,
        Platform.DO150: DO150,
        Platform.J100: J100,
        Platform.GENERIC: GENERIC,
        Platform.W200: W200,
    }

    def __new__(cls, platform: str) -> dict:
        assert platform in Platform.ALL
        return cls.DEFAULTS[platform]


# ExtrasConfig:
# - URDF extras: urdf.xacro with custom links and joints
class ExtrasConfig(BaseConfig):

    EXTRAS = "extras"
    URDF = "urdf"
    LAUNCH = "launch"
    ROS_PARAMETERS = "ros_parameters"

    PLATFORM_VELOCITY_CONTROLLER = "platform_velocity_controller"
    WHEEL_RADIUS = "wheel_radius"
    LIN_MAX_VEL = "linear.x.max_velocity"
    LIN_MIN_VEL = "linear.x.min_velocity"
    LIN_MAX_ACC = "linear.x.max_acceleration"
    LIN_MIN_ACC = "linear.x.min_acceleration"
    ANG_MAX_VEL = "angular.z.max_velocity"
    ANG_MIN_VEL = "angular.z.min_velocity"
    ANG_MAX_ACC = "angular.z.max_acceleration"
    ANG_MIN_ACC = "angular.z.min_acceleration"

    TEMPLATE = {
        EXTRAS: {
            URDF: URDF,
            LAUNCH: LAUNCH,
            ROS_PARAMETERS: {
                PLATFORM_VELOCITY_CONTROLLER: {
                    WHEEL_RADIUS: WHEEL_RADIUS,
                    LIN_MAX_VEL: LIN_MAX_VEL,
                    LIN_MIN_VEL: LIN_MIN_VEL,
                    LIN_MAX_ACC: LIN_MAX_ACC,
                    LIN_MIN_ACC: LIN_MIN_ACC,
                    ANG_MAX_VEL: ANG_MAX_VEL,
                    ANG_MIN_VEL: ANG_MIN_VEL,
                    ANG_MAX_ACC: ANG_MAX_ACC,
                    ANG_MIN_ACC: ANG_MIN_ACC,
                }
            }
        }
    }

    KEYS = flip_dict(TEMPLATE)
    KEYS[ROS_PARAMETERS] = ".".join([EXTRAS, ROS_PARAMETERS])

    DEFAULTS = {
        URDF: None,
        LAUNCH: None,
        ROS_PARAMETERS: ROSParameterDefaults(BaseConfig.get_platform_model()),
    }

    def __init__(
            self,
            config: dict = {},
            urdf: dict = DEFAULTS[URDF],
            launch: dict = DEFAULTS[LAUNCH],
            ros_parameters: dict = {},
            ) -> None:
        # ROS Parameter Setter Template
        self._ros_parameters_setters = {
            self.KEYS[self.WHEEL_RADIUS]: ExtrasConfig.wheel_radius,
            self.KEYS[self.LIN_MAX_VEL]: ExtrasConfig.linear_max_velocity,
            self.KEYS[self.LIN_MIN_VEL]: ExtrasConfig.linear_min_velocity,
            self.KEYS[self.LIN_MAX_ACC]: ExtrasConfig.linear_max_acceleration,
            self.KEYS[self.LIN_MIN_ACC]: ExtrasConfig.linear_min_acceleration,
            self.KEYS[self.ANG_MAX_VEL]: ExtrasConfig.angular_max_velocity,
            self.KEYS[self.ANG_MIN_VEL]: ExtrasConfig.angular_min_velocity,
            self.KEYS[self.ANG_MAX_ACC]: ExtrasConfig.angular_max_acceleration,
            self.KEYS[self.ANG_MIN_ACC]: ExtrasConfig.angular_min_acceleration,
        }
        # Setter Template
        self.setters = {
            self.KEYS[self.URDF]: ExtrasConfig.urdf,
            self.KEYS[self.LAUNCH]: ExtrasConfig.launch,
            self.KEYS[self.ROS_PARAMETERS]: ExtrasConfig.ros_parameters,
        }
        # Initialization
        self._init_ros_parameter()
        self._config = {}
        self.urdf = urdf
        self.launch = launch
        self.ros_parameters = ros_parameters
        # Set from Config
        super().__init__(self.setters, config, self.EXTRAS)

    def update(self, serial_number: bool = False) -> None:
        if serial_number:
            self._update_ros_parameter()

    @property
    def urdf(self) -> dict:
        urdf = None if (self._urdf == self.DEFAULTS[self.URDF]) else dict(self._urdf.to_dict())
        self.set_config_param(
            key=self.KEYS[self.URDF],
            value=urdf,
        )
        return urdf

    @urdf.setter
    def urdf(self, value: dict | PackagePath) -> None:
        if isinstance(value, dict) and PackagePath.PATH in value and value[PackagePath.PATH]:
            self._urdf = PackagePath()
            self._urdf.from_dict(value)
        elif isinstance(value, PackagePath) and value.path:
            self._urdf = value
        else:
            self._urdf = self.DEFAULTS[self.URDF]
            assert not value or isinstance(value, dict) or (isinstance(value, PackagePath)), (
                "Extras URDF must be null or of type `dict` or `PackagePath`"
            )

    @property
    def launch(self) -> dict:
        if (self._launch == self.DEFAULTS[self.LAUNCH]):
            launch = None
        else:
            launch = dict(self._launch.to_dict())
        self.set_config_param(
            key=self.KEYS[self.LAUNCH],
            value=launch,
        )
        return launch

    @launch.setter
    def launch(self, value: dict | PackagePath) -> None:
        if isinstance(value, dict) and PackagePath.PATH in value and value[PackagePath.PATH]:
            self._launch = PackagePath()
            self._launch.from_dict(value)
        elif isinstance(value, PackagePath) and value.path:
            self._launch = value
        else:
            self._launch = self.DEFAULTS[self.LAUNCH]
            assert not value or isinstance(value, dict) or (isinstance(value, PackagePath)), (
                "Extras LAUNCH must be null or of type `dict` or `PackagePath`"
            )

    def _is_ros_parameter(self, key) -> bool:
        return any([key in i for i in self._ros_parameters_setters])

    def _is_ros_parameter_default(self, key) -> bool:
        default_parameters = self.DEFAULTS[self.ROS_PARAMETERS]
        current_val = self.getter(self._ros_parameters_setters[key])()
        default_val = flatten_dict(default_parameters)[".".join(key.split(".")[2:])]
        return current_val == default_val

    def _init_ros_parameter(self) -> None:
        default_parameters = self.DEFAULTS[self.ROS_PARAMETERS]
        for _, extended_key in self.KEYS.items():
            if extended_key in self._ros_parameters_setters:
                default_parameters_key = ".".join(extended_key.split(".")[2:])
                setter = self.setter(self._ros_parameters_setters[extended_key])
                setter(default_parameters[default_parameters_key])

    def _update_ros_parameter(self) -> None:
        default_parameters = ROSParameterDefaults(self.get_platform_model())
        for _, extended_key in self.KEYS.items():
            if extended_key in self._ros_parameters_setters:
                default_parameters_key = ".".join(extended_key.split(".")[2:])
                if not self._is_ros_parameter_default(extended_key):
                    continue
                setter = self.setter(self._ros_parameters_setters[extended_key])
                setter(default_parameters[default_parameters_key])
        self.DEFAULTS[self.ROS_PARAMETERS] = ROSParameterDefaults(self.get_platform_model())

    """ROS parameters with node names and flattened dictionaries"""
    @property
    def ros_parameters(self) -> dict:
        d = {}
        # Add non-default values
        for key, prop in self._ros_parameters_setters.items():
            if not self._is_ros_parameter_default(key):
                d[".".join(key.split(".")[2:])] = self.getter(prop)()
        # User parameters
        for key, val, in self._ros_parameters.items():
            if not self._is_ros_parameter(key):
                d[key] = val
        # Return flat
        d = unflatten_dict(d)
        for node_name in d:
            d[node_name] = flatten_dict(d[node_name])
        # Add to config
        self.set_config_param(
            key=self.KEYS[self.ROS_PARAMETERS],
            value=d
        )
        return d

    @ros_parameters.setter
    def ros_parameters(self, d: dict) -> None:
        # Keep a copy of exactly what the user passed in
        self._ros_parameters = d
        # Store Relevant Parameters
        for flatkey, value in flatten_dict(d).items():
            keys = flatkey.split(".")
            keys = ".".join(keys[1:])
            if keys not in self.KEYS:
                continue
            key = self.KEYS[keys]
            if key not in self._ros_parameters_setters:
                continue
            self.setter(self._ros_parameters_setters[key])(value)

    @property
    def wheel_radius(self) -> float:
        return self._wheel_radius

    @wheel_radius.setter
    def wheel_radius(self, r: float) -> None:
        self._wheel_radius = r

    @property
    def linear_max_velocity(self) -> float:
        return self._lin_max_vel

    @linear_max_velocity.setter
    def linear_max_velocity(self, vel: float) -> None:
        self._lin_max_vel = vel

    @property
    def linear_min_velocity(self) -> float:
        return self._lin_min_vel

    @linear_min_velocity.setter
    def linear_min_velocity(self, vel: float) -> None:
        self._lin_min_vel = vel

    @property
    def linear_max_acceleration(self) -> float:
        return self._lin_max_acc

    @linear_max_acceleration.setter
    def linear_max_acceleration(self, acc: float) -> None:
        self._lin_max_acc = acc

    @property
    def linear_min_acceleration(self) -> float:
        return self._lin_min_acc

    @linear_min_acceleration.setter
    def linear_min_acceleration(self, acc: float) -> None:
        self._lin_min_acc = acc

    @property
    def angular_max_velocity(self) -> float:
        return self._ang_max_vel

    @angular_max_velocity.setter
    def angular_max_velocity(self, vel: float) -> None:
        self._ang_max_vel = vel

    @property
    def angular_min_velocity(self) -> float:
        return self._ang_min_vel

    @angular_min_velocity.setter
    def angular_min_velocity(self, vel: float) -> None:
        self._ang_min_vel = vel

    @property
    def angular_max_acceleration(self) -> float:
        return self._ang_max_acc

    @angular_max_acceleration.setter
    def angular_max_acceleration(self, acc: float) -> None:
        self._ang_max_acc = acc

    @property
    def angular_min_acceleration(self) -> float:
        return self._ang_min_acc

    @angular_min_acceleration.setter
    def angular_min_acceleration(self, acc: float) -> None:
        self._ang_min_acc = acc
