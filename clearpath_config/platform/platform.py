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
from clearpath_config.common.types.platform import Platform
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.package_path import PackagePath
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.platform.battery import BatteryConfig
from clearpath_config.platform.extras import ExtrasConfig
from clearpath_config.platform.attachments.config import AttachmentsConfig
from clearpath_config.platform.attachments.mux import AttachmentsConfigMux


class DescriptionPackagePath(PackagePath):
    MACRO = "macro"
    PARAMETERS = "parameters"

    def __init__(
            self,
            package: str = None,
            path: str = None,
            macro: str = None,
            parameters: dict = None
            ) -> None:
        super().__init__(package, path)
        self.macro = macro
        self.parameters = parameters

    def from_dict(self, config: dict) -> None:
        super().from_dict(config)
        if self.MACRO in config:
            self.macro = config[self.MACRO]
        if self.PARAMETERS in config:
            self.parameters = config[self.PARAMETERS]

    def to_dict(self) -> dict:
        d = super().to_dict()
        d[self.MACRO] = self.macro
        d[self.PARAMETERS] = self.parameters
        return d

    @property
    def macro(self) -> str:
        return self._macro

    @macro.setter
    def macro(self, value: str) -> None:
        self._macro = value

    @property
    def parameters(self) -> dict:
        return self._parameters

    @parameters.setter
    def parameters(self, value: dict) -> None:
        self._parameters = value


class PlatformConfig(BaseConfig):

    PLATFORM = "platform"
    # Controllers
    PS4 = "ps4"
    LOGITECH = "logitech"

    CONTROLLER = "controller"
    ATTACHMENTS = "attachments"
    # Extras
    EXTRAS = "extras"
    # Generic Robot
    DESCRIPTION = "description"
    LAUNCH = "launch"
    CONTROL = "control"
    # Battery
    BATTERY = "battery"
    # Wheel
    WHEEL = "wheel"

    TEMPLATE = {
        PLATFORM: {
            CONTROLLER: CONTROLLER,
            ATTACHMENTS: ATTACHMENTS,
            EXTRAS: EXTRAS,
            DESCRIPTION: DESCRIPTION,
            LAUNCH: LAUNCH,
            CONTROL: CONTROL,
            BATTERY: BATTERY,
            WHEEL: WHEEL,
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        # PLATFORM
        CONTROLLER: PS4,
        ATTACHMENTS: {},
        EXTRAS: ExtrasConfig.DEFAULTS,
        DESCRIPTION: "",
        LAUNCH: "",
        CONTROL: "",
        BATTERY: BatteryConfig.DEFAULTS,
        WHEEL: "default",
    }

    def __init__(
            self,
            config: dict = {},
            controller: str = DEFAULTS[CONTROLLER],
            attachments: str = DEFAULTS[ATTACHMENTS],
            battery: dict = DEFAULTS[BATTERY],
            extras: dict = DEFAULTS[EXTRAS],
            wheel: dict = DEFAULTS[WHEEL],
            ) -> None:
        # Initialization
        self._config = {}
        self.controller = controller
        self.attachments = attachments
        self._battery = BatteryConfig(battery)
        self._extras = ExtrasConfig(extras)
        self.description = self.DEFAULTS[self.DESCRIPTION]
        self.launch = self.DEFAULTS[self.LAUNCH]
        self.control = self.DEFAULTS[self.CONTROL]
        self.wheel = self.DEFAULTS[self.WHEEL]
        # Setter Template
        setters = {
            self.KEYS[self.CONTROLLER]: PlatformConfig.controller,
            self.KEYS[self.ATTACHMENTS]: PlatformConfig.attachments,
            self.KEYS[self.BATTERY]: PlatformConfig.battery,
            self.KEYS[self.EXTRAS]: PlatformConfig.extras,
            self.KEYS[self.WHEEL]: PlatformConfig.wheel,
        }
        super().__init__(setters, config, self.PLATFORM)

    def update(self, serial_number=False) -> None:
        if serial_number:
            # Reload attachments
            self.attachments = None
            # TODO: Set PACS Profile
            # Reload extras
            self.extras.update(serial_number=serial_number)
            # Generic Robot Launch and URDF
            if BaseConfig.get_platform_model() == Platform.GENERIC:
                # Add to Template
                template = self.template
                if self.KEYS[self.DESCRIPTION] not in template:
                    template[self.KEYS[self.DESCRIPTION]] = PlatformConfig.description
                if self.KEYS[self.LAUNCH] not in template:
                    template[self.KEYS[self.LAUNCH]] = PlatformConfig.launch
                if self.KEYS[self.CONTROL] not in template:
                    template[self.KEYS[self.CONTROL]] = PlatformConfig.control
                self.template = template
            else:
                template = self.template
                if self.KEYS[self.DESCRIPTION] in template:
                    del template[self.KEYS[self.DESCRIPTION]]
                if self.KEYS[self.LAUNCH] in template:
                    del template[self.KEYS[self.LAUNCH]]
                if self.KEYS[self.CONTROL] in template:
                    del template[self.KEYS[self.CONTROL]]
                self.template = template
            # Reload battery
            self.battery.update(serial_number=serial_number)

    @property
    def controller(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.CONTROLLER],
            value=self._controller
        )
        return self._controller

    @controller.setter
    def controller(self, value: str) -> None:
        assert value.lower() in [self.PS4, self.LOGITECH], (
            "'%s' controller is invalid. Must be one of: '%s'" % (
                value.lower(),
                [self.PS4, self.LOGITECH]))
        self._controller = value.lower()

    @property
    def attachments(self) -> AttachmentsConfig:
        self.set_config_param(
            key=self.KEYS[self.ATTACHMENTS],
            value=self._attachments.config
        )
        return self._attachments

    @attachments.setter
    def attachments(self, value: dict) -> None:
        self._attachments = AttachmentsConfigMux(
            self.get_platform_model(), value)

    @property
    def extras(self) -> ExtrasConfig:
        self.set_config_param(
            key=self.KEYS[self.EXTRAS],
            value=self._extras.config[self.EXTRAS]
        )
        return self._extras

    @extras.setter
    def extras(self, value: dict | ExtrasConfig) -> None:
        if isinstance(value, dict):
            self._extras.config = value
        elif isinstance(value, ExtrasConfig):
            self._extras = value
        else:
            assert isinstance(value, dict) or (
                    isinstance(value, ExtrasConfig)), (
                "Extras must be of type 'dict' or 'ExtrasConfig'"
            )

    def get_controller(self) -> str:
        return self.controller

    @property
    def description(self) -> dict:
        if self.KEYS[self.DESCRIPTION] not in self.template:
            return self._description.to_dict()
        self.set_config_param(
            key=self.KEYS[self.DESCRIPTION],
            value=self._description.to_dict()
        )
        return self._description.to_dict()

    @description.setter
    def description(self, value: dict) -> None:
        self._description = DescriptionPackagePath()
        self._description.from_dict(value)

    @property
    def launch(self) -> dict:
        if self.KEYS[self.LAUNCH] not in self.template:
            return self._launch.to_dict()
        self.set_config_param(
            key=self.KEYS[self.LAUNCH],
            value=self._launch.to_dict()
        )
        return self._launch.to_dict()

    @launch.setter
    def launch(self, value: dict) -> None:
        self._launch = PackagePath()
        self._launch.from_dict(value)

    @property
    def control(self) -> dict:
        if self.KEYS[self.CONTROL] not in self.template:
            return self._control.to_dict()
        self.set_config_param(
            key=self.KEYS[self.CONTROL],
            value=self._control.to_dict(),
        )
        return self._control.to_dict()

    @control.setter
    def control(self, value: dict) -> None:
        self._control = PackagePath()
        self._control.from_dict(value)

    @property
    def battery(self) -> BatteryConfig:
        self.set_config_param(
            key=self.KEYS[self.BATTERY],
            value=self._battery.config[self.BATTERY]
        )
        return self._battery

    @battery.setter
    def battery(self, value: dict | BatteryConfig) -> None:
        if isinstance(value, dict):
            self._battery.config = value
        elif isinstance(value, BatteryConfig):
            self._battery = value
        else:
            assert isinstance(value, dict) or (
                isinstance(value, BatteryConfig)), (
                "Battery configuration must be of type 'dict' or 'BatteryConfig'"
            )

    @property
    def wheel(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.WHEEL],
            value=self._wheel
        )
        return self._wheel

    @wheel.setter
    def wheel(self, value: str) -> None:
        self._wheel = value
