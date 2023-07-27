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
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.platform.extras import ExtrasConfig
from clearpath_config.platform.attachments.config import BaseAttachmentsConfig
from clearpath_config.platform.attachments.mux import AttachmentsConfigMux


class PlatformConfig(BaseConfig):

    PLATFORM = "platform"
    # Controllers
    PS4 = "ps4"
    LOGITECH = "logitech"
    CONTROLLER = "controller"
    ATTACHMENTS = "attachments"
    # Extras
    EXTRAS = "extras"

    TEMPLATE = {
        PLATFORM: {
            CONTROLLER: CONTROLLER,
            ATTACHMENTS: ATTACHMENTS,
            EXTRAS: EXTRAS
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        # PLATFORM
        CONTROLLER: PS4,
        ATTACHMENTS: {},
        EXTRAS: ExtrasConfig.DEFAULTS
    }

    def __init__(
            self,
            config: dict = {},
            controller: str = DEFAULTS[CONTROLLER],
            attachments: str = DEFAULTS[ATTACHMENTS],
            extras: str = DEFAULTS[EXTRAS]
            ) -> None:
        # Initialization
        self._config = {}
        self.controller = controller
        self.attachments = attachments
        self._extras = ExtrasConfig(extras)
        # Setter Template
        setters = {
            self.KEYS[self.CONTROLLER]: PlatformConfig.controller,
            self.KEYS[self.ATTACHMENTS]: PlatformConfig.attachments,
            self.KEYS[self.EXTRAS]: PlatformConfig.extras
        }
        super().__init__(setters, config, self.PLATFORM)

    def update(self, serial_number=False) -> None:
        if serial_number:
            # Reload attachments
            self.attachments = None
            # TODO: Set PACS Profile
            # Reload extras
            self.extras.update(serial_number=serial_number)

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
    def attachments(self) -> BaseAttachmentsConfig:
        self.set_config_param(
            key=self.KEYS[self.ATTACHMENTS],
            value=self._attachments.config[self.ATTACHMENTS]
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

