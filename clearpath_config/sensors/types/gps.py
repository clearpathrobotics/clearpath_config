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
from clearpath_config.sensors.types.sensor import BaseSensor
from typing import List


class BaseGPS(BaseSensor):
    SENSOR_TYPE = "gps"
    SENSOR_MODEL = "base"
    TOPIC = "fix"

    FRAME_ID = "link"
    IP_ADDRESS = "192.168.131.30"
    IP_PORT = 55555

    class ROS_PARAMETER_KEYS:
        FRAME_ID = "frame_id"
        IP_ADDRESS = "ip_address"
        IP_PORT = "ip_port"

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = TOPIC,
            frame_id: str = FRAME_ID,
            ip: str = IP_ADDRESS,
            port: int = IP_PORT,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
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
        super().__init__(
            idx,
            name,
            topic,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )
        # ROS Parameter Keys
        pairs = {
            # Frame ID
            BaseGPS.ROS_PARAMETER_KEYS.FRAME_ID: (
                BaseSensor.ROSParameter(
                    key=BaseGPS.ROS_PARAMETER_KEYS.FRAME_ID,
                    get=lambda obj: obj.get_frame_id(),
                    set=lambda obj, val: obj.set_frame_id(val)
                )
            ),
            # IP Address
            BaseGPS.ROS_PARAMETER_KEYS.IP_ADDRESS: (
                BaseSensor.ROSParameter(
                    key=BaseGPS.ROS_PARAMETER_KEYS.IP_ADDRESS,
                    get=lambda obj: obj.get_ip(),
                    set=lambda obj, val: obj.set_ip(val))),
            # IP Port
            BaseGPS.ROS_PARAMETER_KEYS.IP_PORT: (
                BaseSensor.ROSParameter(
                    key=BaseGPS.ROS_PARAMETER_KEYS.IP_PORT,
                    get=lambda obj: obj.get_port(),
                    set=lambda obj, val: obj.set_port(val))),
        }
        self.ros_parameter_pairs.update(pairs)
        self.set_ros_parameters(ros_parameters)

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
        self.set_ip(self.get_ip_from_idx(idx))

    def get_frame_id(self) -> str:
        return self.frame_id

    def set_frame_id(self, link: str) -> None:
        Accessory.assert_valid_link(link)
        self.frame_id = link

    def get_ip(self) -> str:
        return str(self.ip)

    def set_ip(self, ip: str) -> None:
        self.ip = IP(ip)

    def get_port(self) -> int:
        return int(self.port)

    def set_port(self, port: int) -> None:
        self.port = Port(port)


class SwiftNavDuro(BaseGPS):
    SENSOR_MODEL = "swiftnav_duro"

    FRAME_ID = "link"
    IP_PORT = 55555

    class ROS_PARAMETER_KEYS:
        GPS_FRAME = "gps_receiver_frame_id"
        IMU_FRAME = "imu_frame_id"

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseGPS.TOPIC,
            frame_id: str = FRAME_ID,
            ip: str = BaseGPS.IP_ADDRESS,
            port: int = IP_PORT,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            ip,
            port,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )
        # ROS Parameter Keys
        self.ros_parameter_pairs[
            BaseGPS.ROS_PARAMETER_KEYS.FRAME_ID].key = (
                SwiftNavDuro.ROS_PARAMETER_KEYS.GPS_FRAME
            )
        pairs = {
            # Frame ID
            SwiftNavDuro.ROS_PARAMETER_KEYS.IMU_FRAME: (
                BaseSensor.ROSParameter(
                    key=SwiftNavDuro.ROS_PARAMETER_KEYS.IMU_FRAME,
                    get=lambda obj: obj.get_frame_id(),
                    set=lambda obj, val: obj.set_frame_id(val)
                )
            ),
        }
        self.ros_parameter_pairs.update(pairs)
        self.set_ros_parameters(ros_parameters)
