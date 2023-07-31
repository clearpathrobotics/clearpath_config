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
from clearpath_config.common.utils.yaml import read_yaml, write_yaml
from clearpath_config.system.system import SystemConfig
from clearpath_config.platform.platform import PlatformConfig
from clearpath_config.links.links import LinksConfig
from clearpath_config.mounts.mounts import MountsConfig
from clearpath_config.sensors.sensors import SensorConfig


# ClearpathConfig:
#  - top level configurator
#  - contains
class ClearpathConfig(BaseConfig):

    VERSION = "version"
    SERIAL_NUMBER = "serial_number"
    SYSTEM = "system"
    PLATFORM = "platform"
    LINKS = "links"
    MOUNTS = "mounts"
    SENSORS = "sensors"

    TEMPLATE = {
        SERIAL_NUMBER: SERIAL_NUMBER,
        VERSION: VERSION,
        SYSTEM: SYSTEM,
        PLATFORM: PLATFORM,
        LINKS: LINKS,
        MOUNTS: MOUNTS,
        SENSORS: SENSORS
    }

    KEYS = TEMPLATE

    DEFAULTS = {
        SERIAL_NUMBER: "generic",
        VERSION: 0,
        SYSTEM: SystemConfig.DEFAULTS,
        PLATFORM: PlatformConfig.DEFAULTS,
        LINKS: LinksConfig.DEFAULTS,
        MOUNTS: MountsConfig.DEFAULTS,
        SENSORS: SensorConfig.DEFAULTS,
    }

    def __init__(self, config: dict | str = None) -> None:
        # Read YAML
        if isinstance(config, str):
            config = self.read(config)
        # Initialization of Sub-Configs
        self._config = {}
        self._system = SystemConfig(self.DEFAULTS[self.SYSTEM])
        self._platform = PlatformConfig(self.DEFAULTS[self.PLATFORM])
        self._links = LinksConfig(self.DEFAULTS[self.LINKS])
        self._mounts = MountsConfig(self.DEFAULTS[self.MOUNTS])
        self._sensors = SensorConfig(self.DEFAULTS[self.SENSORS])
        # Initialization
        self.serial_number = self.DEFAULTS[self.SERIAL_NUMBER]
        self.version = self.DEFAULTS[self.VERSION]
        # Setter Template
        setters = {
            self.SERIAL_NUMBER: ClearpathConfig.serial_number,
            self.VERSION: ClearpathConfig.version,
            self.SYSTEM: ClearpathConfig.system,
            self.PLATFORM: ClearpathConfig.platform,
            self.LINKS: ClearpathConfig.links,
            self.MOUNTS: ClearpathConfig.mounts,
            self.SENSORS: ClearpathConfig.sensors,
        }
        # Set from Config
        super().__init__(setters, config)

    def read(self, file: str | dict) -> None:
        self._file = None
        if isinstance(file, dict):
            return file
        self._file = file
        return read_yaml(file)

    def write(self, file: str) -> None:
        write_yaml(file, self.config)

    @property
    def serial_number(self) -> str:
        self.set_config_param(
            self.SERIAL_NUMBER,
            str(self.get_serial_number())
        )
        return self.get_serial_number()

    @serial_number.setter
    def serial_number(self, sn: str) -> None:
        self.set_serial_number(sn)
        self._system.update(serial_number=True)
        self._platform.update(serial_number=True)
        self._links.update(serial_number=True)
        self._mounts.update(serial_number=True)
        self._sensors.update(serial_number=True)

    @property
    def version(self) -> int:
        self.set_config_param(self.VERSION, self._version)
        return self._version

    @version.setter
    def version(self, v: int) -> None:
        assert isinstance(v, int), (
            "version must be of type 'int'"
        )
        self._version = v
        # Add propagators here

    @property
    def system(self) -> SystemConfig:
        self.set_config_param(
            self.SYSTEM,
            self._system.config[self.SYSTEM])
        return self._system

    @system.setter
    def system(self, config: dict) -> None:
        self._system.config = config

    @property
    def platform(self) -> PlatformConfig:
        self.set_config_param(
            self.PLATFORM,
            self._platform.config[self.PLATFORM])
        return self._platform

    @platform.setter
    def platform(self, config: dict) -> None:
        self._platform.config = config

    @property
    def links(self) -> LinksConfig:
        self.set_config_param(
            self.LINKS,
            self._links.config[self.LINKS])
        return self._links

    @links.setter
    def links(self, config: dict) -> None:
        self._links.config = config

    @property
    def mounts(self) -> MountsConfig:
        self.set_config_param(
            self.MOUNTS,
            self._mounts.config[self.MOUNTS])
        return self._mounts

    @mounts.setter
    def mounts(self, config: dict) -> None:
        self._mounts.config = config

    @property
    def sensors(self) -> SensorConfig:
        self.set_config_param(
            self.SENSORS,
            self._sensors.config[self.SENSORS])
        return self._sensors

    @sensors.setter
    def sensors(self, config: dict) -> None:
        self._sensors.config = config
