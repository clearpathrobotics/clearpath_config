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
from typing import List

from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.file import File
from clearpath_config.common.types.ip import IP
from clearpath_config.common.utils.dictionary import extend_flat_dict
from clearpath_config.sensors.types.sensor import BaseSensor


class BasePTU(BaseSensor):
    SENSOR_TYPE = 'ptu'
    SENSOR_MODEL = 'base'
    TOPIC = 'state'

    class TOPICS:
        STATE = 'state'
        NAME = {
            STATE: 'state',
        }
        TYPE = {
            STATE: 'sensor_msgs/msg/JointState',
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = TOPIC,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ) -> None:
        super().__init__(
            idx,
            name,
            topic,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy,
        )
        self.rates = {
            BasePTU.TOPICS.STATE: 10,
        }


class FlirPTU(BasePTU):
    SENSOR_MODEL = 'flir_ptu'

    # Hardware models
    D46 = 'd46'
    PTU5 = 'ptu5'
    MODEL = D46
    MODELS = [D46, PTU5]

    # Connection types
    TTY = 'tty'
    TCP = 'tcp'
    CONNECTION_TYPE = TCP
    CONNECTION_TYPES = [TTY, TCP]

    # Defaults
    TTY_PORT = '/dev/ptu'
    TCP_PORT = 4000
    IP_ADDRESS = '192.168.131.70'
    LIMITS_ENABLED = False

    MIN_PORT = 1024
    MAX_PORT = 65535

    class ROS_PARAMETER_KEYS:
        CONNECTION_TYPE = 'ptu_driver.connection_type'
        TTY_PORT = 'ptu_driver.port'
        TCP_PORT = 'ptu_driver.tcp_port'
        IP_ADDRESS = 'ptu_driver.ip_addr'
        LIMITS_ENABLED = 'ptu_driver.limits_enabled'
        JOINT_NAME_PREFIX = 'ptu_driver.joint_name_prefix'

    JOINT_NAME_PREFIX = 'ptu_'

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BasePTU.TOPIC,
            ptu_model: str = MODEL,
            connection_type: str = CONNECTION_TYPE,
            tty_port: str = TTY_PORT,
            tcp_port: int = TCP_PORT,
            ip: str = IP_ADDRESS,
            limits_enabled: bool = LIMITS_ENABLED,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ) -> None:
        # Joint name prefix
        self.joint_name_prefix = self.JOINT_NAME_PREFIX
        # Hardware model
        self.ptu_model = ptu_model
        # Connection type
        self.connection_type = connection_type
        # Serial port
        self.tty_port = tty_port
        # TCP port
        self.tcp_port = tcp_port
        # IP address
        self.ip = ip
        # Software-enforced limits
        self.limits_enabled = limits_enabled
        # ROS Parameters Template
        template = {
            self.ROS_PARAMETER_KEYS.CONNECTION_TYPE: FlirPTU.connection_type,
            self.ROS_PARAMETER_KEYS.TTY_PORT: FlirPTU.tty_port,
            self.ROS_PARAMETER_KEYS.TCP_PORT: FlirPTU.tcp_port,
            self.ROS_PARAMETER_KEYS.IP_ADDRESS: FlirPTU.ip,
            self.ROS_PARAMETER_KEYS.LIMITS_ENABLED: FlirPTU.limits_enabled,
            self.ROS_PARAMETER_KEYS.JOINT_NAME_PREFIX: FlirPTU.joint_name_prefix,
        }
        ros_parameters_template = extend_flat_dict(template, ros_parameters_template)
        super().__init__(
            idx,
            name,
            topic,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy,
        )

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['ptu_model'] = self.ptu_model
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if 'ptu_model' in d:
            self.ptu_model = d['ptu_model']

    @property
    def ptu_model(self) -> str:
        return self._ptu_model

    @ptu_model.setter
    def ptu_model(self, value: str) -> None:
        if value not in self.MODELS:
            raise ValueError(
                f'Flir PTU model "{value}" must be one of "{self.MODELS}"'
            )
        self._ptu_model = value

    @property
    def connection_type(self) -> str:
        return self._connection_type

    @connection_type.setter
    def connection_type(self, value: str) -> None:
        if value not in self.CONNECTION_TYPES:
            raise ValueError(
                f'Connection type "{value}" must be one of "{self.CONNECTION_TYPES}"'
            )
        self._connection_type = value

    @property
    def tty_port(self) -> str:
        return self._tty_port.get_path()

    @tty_port.setter
    def tty_port(self, value: str) -> None:
        self._tty_port = File(value)

    @property
    def tcp_port(self) -> int:
        return self._tcp_port

    @tcp_port.setter
    def tcp_port(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f'TCP port {value} must be of type "int"')
        if value < self.MIN_PORT or value > self.MAX_PORT:
            raise ValueError(
                f'TCP port {value} must be in range {self.MIN_PORT} to {self.MAX_PORT}'
            )
        self._tcp_port = value

    @property
    def ip(self) -> str:
        return str(self._ip)

    @ip.setter
    def ip(self, value: str) -> None:
        self._ip = IP(value)

    @property
    def limits_enabled(self) -> bool:
        return self._limits_enabled

    @limits_enabled.setter
    def limits_enabled(self, value: bool) -> None:
        self._limits_enabled = bool(value)

    @classmethod
    def get_joint_name_prefix_from_idx(cls, idx: int) -> str:
        return f'ptu_{idx}_'

    def set_idx(self, idx: int) -> None:
        super().set_idx(idx)
        self.joint_name_prefix = self.get_joint_name_prefix_from_idx(idx)

    @property
    def joint_name_prefix(self) -> str:
        return self._joint_name_prefix

    @joint_name_prefix.setter
    def joint_name_prefix(self, prefix: str) -> None:
        self._joint_name_prefix = prefix
