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
from clearpath_config.common.utils.dictionary import flip_dict


class BatteryConfig(BaseConfig):
    BATTERY = 'battery'

    # Models
    MODEL = 'model'
    UNKNOWN = 'unknown'
    # User-defined battery: bypasses VALID_BATTERIES validation and requires
    # PARAM_FILE to point at a user-supplied parameter YAML.
    CUSTOM = 'custom'
    # D100 Lead Acid
    TLV1222 = 'TLV1222'
    # D100 LiION
    PH3054 = 'PH3054'
    # D150 LiION
    RB20 = 'RB20'
    # A200 Lead Acid
    ES20_12C = 'ES20_12C'
    # A200/J100 LiION
    HE2613 = 'HE2613'
    HE2411 = 'HE2411'
    HE2410 = 'HE2410'
    # A300 LiFEPO4
    S_24V20_U1 = 'S_24V20_U1'
    # R100 Lead Acid
    DTM8A31 = '8A31DTM'
    # W200 Lead Acid
    U1_35 = 'U1_35'
    # W200 LiFEPO4
    NEC_ALM12V35 = 'NEC_ALM12V35'
    VALENCE_U24_12XP = 'VALENCE_U24_12XP'
    VALENCE_U27_12XP = 'VALENCE_U27_12XP'

    # Configurations
    CONFIGURATION = 'configuration'
    LAUNCH_ARGS = 'launch_args'
    # External user-supplied parameter YAML (clearpath_config PackagePath).
    # Only valid when MODEL == CUSTOM.
    PARAM_FILE = 'param_file'
    # Inline node parameter overrides, namespaced by node name.
    # The battery_state_estimator block is forwarded to the node as-is.
    ROS_PARAMETERS = 'ros_parameters'
    BATTERY_STATE_ESTIMATOR = 'battery_state_estimator'
    S1P1 = 'S1P1'
    S1P2 = 'S1P2'
    S1P3 = 'S1P3'
    S1P4 = 'S1P4'
    S1P6 = 'S1P6'
    S2P1 = 'S2P1'
    S4P1 = 'S4P1'
    S4P3 = 'S4P3'

    VALID = {}  # Populated dynamically from platform registry

    @staticmethod
    def _get_valid_batteries(platform=None):
        if platform is None:
            platform = BaseConfig.get_platform_model()
        return Platform.get(platform).VALID_BATTERIES

    TEMPLATE = {
        BATTERY: {
            MODEL: MODEL,
            CONFIGURATION: CONFIGURATION,
            LAUNCH_ARGS: LAUNCH_ARGS,
            PARAM_FILE: PARAM_FILE,
            ROS_PARAMETERS: ROS_PARAMETERS,
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        MODEL: UNKNOWN,
        CONFIGURATION: UNKNOWN,
        LAUNCH_ARGS: {},
        PARAM_FILE: {},
        ROS_PARAMETERS: {},
    }

    def __init__(
            self,
            config: dict = {},
            model: str = DEFAULTS[MODEL],
            configuration: str = DEFAULTS[CONFIGURATION],
            launch_args: dict = DEFAULTS[LAUNCH_ARGS],
            param_file: dict = DEFAULTS[PARAM_FILE],
            ros_parameters: dict = DEFAULTS[ROS_PARAMETERS],
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
        if param_file == self.DEFAULTS[self.PARAM_FILE] or not param_file:
            self.param_file = self.DEFAULTS[self.PARAM_FILE]
        else:
            self.param_file = param_file
        if ros_parameters == self.DEFAULTS[self.ROS_PARAMETERS] or not ros_parameters:
            self.ros_parameters = self.DEFAULTS[self.ROS_PARAMETERS]
        else:
            self.ros_parameters = ros_parameters

        # Setter Template
        setters = {
            self.KEYS[self.MODEL]: BatteryConfig.model,
            self.KEYS[self.CONFIGURATION]: BatteryConfig.configuration,
            self.KEYS[self.LAUNCH_ARGS]: BatteryConfig.launch_args,
            self.KEYS[self.PARAM_FILE]: BatteryConfig.param_file,
            self.KEYS[self.ROS_PARAMETERS]: BatteryConfig.ros_parameters,
        }
        super().__init__(setters, config, self.BATTERY)

        self._validate_consistency()

    def update_defaults(self) -> None:
        platform = BaseConfig.get_platform_model()
        valid = self._get_valid_batteries(platform)
        self.DEFAULTS[self.MODEL] = list(valid)[0]
        self.DEFAULTS[self.CONFIGURATION] = list(
            valid[self.DEFAULTS[self.MODEL]])[0]

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
        # User-defined batteries bypass the per-platform VALID_BATTERIES table.
        if value == self.CUSTOM:
            self._model = value
            return
        platform = BaseConfig.get_platform_model()
        valid = self._get_valid_batteries(platform)
        if value not in valid:
            raise ValueError(
                f'Battery model "{value}" is invalid. Battery model for platform "{platform}" must be one of "{list(valid) + [self.CUSTOM]}"'  # noqa:E501
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
        # User-defined batteries do not require a configuration; the
        # configuration is supplied by the user's parameter file (and may be
        # overridden via ros_parameters).
        if self.model == self.CUSTOM:
            self._configuration = value
            return
        platform = BaseConfig.get_platform_model()
        valid = self._get_valid_batteries(platform)
        if self.model not in valid:
            raise ValueError(
                f'Battery model "{self.model}" is invalid. Battery model for platform "{platform}" it must be one of "{list(valid)}"'  # noqa:E501
            )
        if value not in valid[self.model]:
            raise ValueError(
                f'Battery configuration "{value}" is invalid. For platform "{platform}" and battery model "{self.model}" it must be one of "{list(valid[self.model])}"'  # noqa:E501
            )
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
        if not isinstance(value, dict):
            raise TypeError(f'Battery Launch args {value} must be of type "dict"')
        self._launch_args = value

    @property
    def param_file(self) -> dict:
        self.set_config_param(
            key=self.KEYS[self.PARAM_FILE],
            value=self._param_file.to_dict()
        )
        return self._param_file.to_dict()

    @param_file.setter
    def param_file(self, value) -> None:
        if value is None or value == {}:
            self._param_file = PackagePath()
            return
        if isinstance(value, PackagePath):
            self._param_file = value
            return
        if not isinstance(value, dict):
            raise TypeError(
                f'Battery param_file {value!r} must be a dict with keys '
                f'"{PackagePath.PACKAGE}" and "{PackagePath.PATH}"'
            )
        self._param_file = PackagePath()
        self._param_file.from_dict(value)

    @property
    def ros_parameters(self) -> dict:
        self.set_config_param(
            key=self.KEYS[self.ROS_PARAMETERS],
            value=self._ros_parameters
        )
        return self._ros_parameters

    @ros_parameters.setter
    def ros_parameters(self, value: dict) -> None:
        if not isinstance(value, dict):
            raise TypeError(f'Battery ros_parameters {value!r} must be of type "dict"')
        self._ros_parameters = value

    def _validate_consistency(self) -> None:
        """Enforce that param_file is set if and only if model == CUSTOM.

        PackagePath itself accepts either a (package, relative path) pair or
        an absolute path with no package; only the existence of a path entry
        is required here.
        """
        has_param_file = bool(self._param_file.package) or bool(self._param_file.path)
        if self._model == self.CUSTOM:
            if not has_param_file:
                raise ValueError(
                    f'Battery model "{self.CUSTOM}" requires "{self.PARAM_FILE}" to be set'
                )
        else:
            if has_param_file:
                raise ValueError(
                    f'Battery "{self.PARAM_FILE}" is only valid when model is "{self.CUSTOM}"; '
                    f'got model "{self._model}"'
                )
