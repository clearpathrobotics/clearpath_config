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
from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.ip import IP
from clearpath_config.common.types.port import Port
from clearpath_config.common.utils.dictionary import extend_flat_dict, is_in_dict
from clearpath_config.sensors.types.sensor import BaseSensor
from typing import List
from math import pi


class BaseLidar2D(BaseSensor):
    SENSOR_TYPE = "lidar2d"
    SENSOR_MODEL = "base"
    TOPIC = "scan"

    FRAME_ID = "laser"
    IP_ADDRESS = "192.168.131.20"
    IP_PORT = 6000
    MIN_ANGLE = -pi
    MAX_ANGLE = pi

    class ROS_PARAMETER_KEYS:
        FRAME_ID = "node_name.frame_id"
        IP_ADDRESS = "node_name.ip_address"
        IP_PORT = "node_name.ip_port"
        MIN_ANGLE = "node_name.min_angle"
        MAX_ANGLE = "node_name.max_angle"

    class TOPICS:
        SCAN = "scan"
        NAME = {
            SCAN: "scan",
        }
        RATE = {
            SCAN: 10,
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = TOPIC,
            frame_id: str = FRAME_ID,
            ip: str = IP_ADDRESS,
            port: int = IP_PORT,
            min_angle: float = MIN_ANGLE,
            max_angle: float = MAX_ANGLE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ) -> None:
        # Frame ID
        self.frame_id: str = self.FRAME_ID
        self.set_frame_id(frame_id)
        # IP Address
        self.ip: IP = IP(self.IP_ADDRESS)
        self.set_ip(ip)
        # IP Port
        self.port: Port = Port(self.IP_PORT)
        self.set_port(port)
        # Min Angle
        self.min_angle: float = float(self.MIN_ANGLE)
        self.set_min_angle(min_angle)
        # Max Angle
        self.max_angle: float = float(self.MAX_ANGLE)
        self.set_max_angle(max_angle)
        # ROS Parameters Template
        template = {
            self.ROS_PARAMETER_KEYS.FRAME_ID: BaseLidar2D.frame_id,
            self.ROS_PARAMETER_KEYS.IP_ADDRESS: BaseLidar2D.ip,
            self.ROS_PARAMETER_KEYS.IP_PORT: BaseLidar2D.port,
            self.ROS_PARAMETER_KEYS.MIN_ANGLE: BaseLidar2D.min_angle,
            self.ROS_PARAMETER_KEYS.MAX_ANGLE: BaseLidar2D.max_angle,
        }
        ros_parameters_template = extend_flat_dict(template, ros_parameters_template)
        # Initialize Base
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

    @classmethod
    def get_frame_id_from_idx(cls, idx: int) -> str:
        return "%s_%s" % (
            cls.get_name_from_idx(idx),
            cls.FRAME_ID
        )

    @classmethod
    def get_ip_from_idx(cls, idx: int) -> str:
        ip = cls.IP_ADDRESS.split('.')
        network_id = ip[0:3]
        host_id = int(ip[-1]) + idx
        return '.'.join(network_id) + '.' + str(host_id)

    def set_idx(self, idx: int) -> None:
        # Set Base: Name and Topic
        super().set_idx(idx)
        # Set Frame ID
        self.set_frame_id(self.get_frame_id_from_idx(idx))
        # Set IP
        if not is_in_dict(
                self._ros_parameters,
                self.ROS_PARAMETER_KEYS.IP_ADDRESS.split(".")):
            self.set_ip(self.get_ip_from_idx(idx))

    @property
    def frame_id(self) -> str:
        return self._frame_id

    @frame_id.setter
    def frame_id(self, link: str) -> None:
        Accessory.assert_valid_link(link)
        self._frame_id = link

    def get_frame_id(self) -> str:
        return self.frame_id

    def set_frame_id(self, link: str) -> None:
        self.frame_id = link

    @property
    def ip(self) -> str:
        return str(self._ip)

    @ip.setter
    def ip(self, ip: str) -> None:
        self._ip = IP(str(ip))

    def get_ip(self) -> str:
        return str(self.ip)

    def set_ip(self, ip: str) -> None:
        self.ip = ip

    @property
    def port(self) -> int:
        return int(self._port)

    @port.setter
    def port(self, port: int) -> None:
        self._port = Port(int(port))

    def get_port(self) -> int:
        return int(self.port)

    def set_port(self, port: int) -> None:
        self.port = port

    @property
    def min_angle(self) -> float:
        return self._min_angle

    @min_angle.setter
    def min_angle(self, angle: float):
        if angle < self.MIN_ANGLE:
            angle = self.MIN_ANGLE
        self._min_angle = angle

    def get_min_angle(self) -> float:
        return self.min_angle

    def set_min_angle(self, angle: float) -> None:
        self.min_angle = angle

    @property
    def max_angle(self) -> float:
        return self._max_angle

    @max_angle.setter
    def max_angle(self, angle: float) -> None:
        if angle > self.MAX_ANGLE:
            angle = self.MAX_ANGLE
        self._max_angle = angle

    def get_max_angle(self) -> float:
        return self.max_angle

    def set_max_angle(self, angle: float) -> None:
        self.max_angle = angle


class HokuyoUST(BaseLidar2D):
    SENSOR_MODEL = "hokuyo_ust"

    FRAME_ID = "laser"
    IP_PORT = 10940
    MIN_ANGLE = -pi
    MAX_ANGLE = pi

    class ROS_PARAMETER_KEYS:
        FRAME_ID = "urg_node.laser_frame_id"
        IP_ADDRESS = "urg_node.ip_address"
        IP_PORT = "urg_node.ip_port"
        MIN_ANGLE = "urg_node.angle_min"
        MAX_ANGLE = "urg_node.angle_max"

    class TOPICS:
        SCAN = "scan"
        NAME = {
            SCAN: "scan",
        }
        RATE = {
            SCAN: 10,
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseLidar2D.TOPIC,
            frame_id: str = BaseLidar2D.FRAME_ID,
            ip: str = BaseLidar2D.IP_ADDRESS,
            port: int = IP_PORT,
            min_angle: float = MIN_ANGLE,
            max_angle: float = MAX_ANGLE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        ros_parameters_template = BaseSensor.ROS_PARAMETERS_TEMPLATE
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            ip,
            port,
            min_angle,
            max_angle,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )


class SickLMS1XX(BaseLidar2D):
    SENSOR_MODEL = "sick_lms1xx"

    FRAME_ID = "laser"
    IP_PORT = 2111
    MIN_ANGLE = -2.391
    MAX_ANGLE = 2.391

    class ROS_PARAMETER_KEYS:
        FRAME_ID = "lms1xx.frame_id"
        IP_ADDRESS = "lms1xx.host"
        IP_PORT = "lms1xx.port"
        MIN_ANGLE = "lms1xx.min_ang"
        MAX_ANGLE = "lms1xx.max_ang"

    class TOPICS:
        SCAN = "scan"
        NAME = {
            SCAN: "scan",
        }
        RATE = {
            SCAN: 10,
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseLidar2D.TOPIC,
            frame_id: str = FRAME_ID,
            ip: str = BaseLidar2D.IP_ADDRESS,
            port: int = IP_PORT,
            min_angle: float = MIN_ANGLE,
            max_angle: float = MAX_ANGLE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        ros_parameters_template = BaseSensor.ROS_PARAMETERS_TEMPLATE
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            ip,
            port,
            min_angle,
            max_angle,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )
