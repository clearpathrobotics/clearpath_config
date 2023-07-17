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
from clearpath_config.common.types.file import File
from clearpath_config.common.utils.dictionary import flip_dict


# ExtrasConfig:
# - URDF extras: urdf.xacro with custom links and joints
# - Control extras: YAML with overwrites or extra ROS parameters
class ExtrasConfig(BaseConfig):

    EXTRAS = "extras"
    URDF = "urdf"
    CONTROL = "control"

    TEMPLATE = {
        EXTRAS: {
            URDF: URDF,
            CONTROL: CONTROL
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        URDF: "empty.urdf.xacro",
        CONTROL: "empty.yaml"
    }

    def __init__(
            self,
            config: dict = {},
            urdf: str = DEFAULTS[URDF],
            control: str = DEFAULTS[CONTROL]
            ) -> None:
        # Initialization
        self._config = {}
        self.urdf = urdf
        self.control = control
        # Setter Template
        setters = {
            self.KEYS[self.URDF]: ExtrasConfig.urdf,
            self.KEYS[self.CONTROL]: ExtrasConfig.control
        }
        # Set from Config
        super().__init__(setters, config, self.EXTRAS)

    @property
    def urdf(self) -> str:
        urdf = None if self._is_default(self._urdf, self.URDF) else str(self._urdf)
        self.set_config_param(
            key=self.KEYS[self.URDF],
            value=urdf
        )
        return urdf

    @urdf.setter
    def urdf(self, value: str) -> None:
        if value is None or value == "None":
            return
        self._urdf = File(path=str(value))

    @property
    def control(self) -> str:
        control = None if self._is_default(self._control, self.CONTROL) else str(self._control)
        self.set_config_param(
            key=self.KEYS[self.CONTROL],
            value=control
        )
        return control

    @control.setter
    def control(self, value: str) -> None:
        if value is None or value == "None":
            return
        self._control = File(path=str(value))

    def _is_default(self, curr: str, key: str) -> bool:
        return curr == str(File(self.DEFAULTS[key]))
