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
from clearpath_config.common.types.ip import IP
from clearpath_config.common.types.port import Port
from clearpath_config.common.utils.dictionary import extend_flat_dict, is_in_dict
from clearpath_config.sensors.types.sensor import BaseSensor


class BaseLidar3D(BaseSensor):
    SENSOR_TYPE = 'lidar3d'
    SENSOR_MODEL = 'base'
    TOPIC = 'points'

    FRAME_ID = 'laser'
    IP_ADDRESS = '192.168.131.25'
    IP_PORT = '2368'

    class ROS_PARAMETER_KEYS:
        FRAME_ID = 'node_name.frame_id'
        IP_ADDRESS = 'node_name.ip_address'
        IP_PORT = 'node_name.ip_port'

    class TOPICS:
        SCAN = 'scan'
        POINTS = 'points'
        NAME = {
            SCAN: 'scan',
            POINTS: 'points',
        }
        TYPE = {
            SCAN: 'sensor_msgs/msg/LaserScan',
            POINTS: 'sensor_msgs/msg/PointCloud2',
        }

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
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # Frame ID
        self.frame_id = frame_id
        # IP Address
        self.ip = ip
        # IP Port
        self.port = port
        # ROS Parameter Template
        template = {
            self.ROS_PARAMETER_KEYS.FRAME_ID: BaseLidar3D.frame_id,
            self.ROS_PARAMETER_KEYS.IP_ADDRESS: BaseLidar3D.ip,
            self.ROS_PARAMETER_KEYS.IP_PORT: BaseLidar3D.port,
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
            rpy
        )
        self.rates = {
            # TODO: Be able to configure the expected update rate using the robot.yaml
            BaseLidar3D.TOPICS.SCAN: 20,
            BaseLidar3D.TOPICS.POINTS: 20
        }

    @classmethod
    def get_frame_id_from_idx(cls, idx: int) -> str:
        return '%s_%s' % (
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
        self.frame_id = self.get_frame_id_from_idx(idx)
        # Set IP
        if not is_in_dict(
                self._ros_parameters,
                self.ROS_PARAMETER_KEYS.IP_ADDRESS.split('.')):
            self.ip = self.get_ip_from_idx(idx)

    @property
    def frame_id(self) -> str:
        return self._frame_id

    @frame_id.setter
    def frame_id(self, link: str) -> None:
        Accessory.assert_valid_link(link)
        self._frame_id = link

    @property
    def ip(self) -> str:
        return str(self._ip)

    @ip.setter
    def ip(self, ip: str) -> None:
        self._ip = IP(str(ip))

    @property
    def port(self) -> int:
        return int(self._port)

    @port.setter
    def port(self, port: int) -> None:
        self._port = Port(int(port))


class VelodyneLidar(BaseLidar3D):
    SENSOR_MODEL = 'velodyne_lidar'

    FRAME_ID = 'laser'
    IP_PORT = 2368

    HDL_32E = '32E'
    HDL_64E = '64E'
    HDL_64E_S2 = '64E_S2'
    HDL_64E_S3 = '64E_S3'
    VLP_16 = 'VLP16'
    VLP_32C = '32C'
    DEVICE_TYPE = VLP_16
    DEVICE_TYPES = (
        HDL_32E,
        HDL_64E,
        HDL_64E_S2,
        HDL_64E_S3,
        VLP_16,
        VLP_32C
    )

    class ROS_PARAMETER_KEYS:
        FRAME_ID = 'velodyne_driver_node.frame_id'
        IP_ADDRESS = 'velodyne_driver_node.device_ip'
        IP_PORT = 'velodyne_driver_node.port'
        DRIVER_NODE_MODEL = 'velodyne_driver_node.model'
        TRANSFORM_NODE_MODEL = 'velodyne_transform_node.model'
        FIXED_FRAME = 'velodyne_transform_node.fixed_frame'
        TARGET_FRAME = 'velodyne_transform_node.target_frame'

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseLidar3D.TOPIC,
            frame_id: str = FRAME_ID,
            ip: str = BaseLidar3D.IP_ADDRESS,
            port: int = IP_PORT,
            device_type: str = DEVICE_TYPE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # Device Type:
        self.device_type = device_type
        # ROS Parameter Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.DRIVER_NODE_MODEL: VelodyneLidar.device_type,
            self.ROS_PARAMETER_KEYS.TRANSFORM_NODE_MODEL: VelodyneLidar.device_type,
            self.ROS_PARAMETER_KEYS.FIXED_FRAME: VelodyneLidar.frame_id,
            self.ROS_PARAMETER_KEYS.TARGET_FRAME: VelodyneLidar.frame_id,
        }
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
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )

    @property
    def device_type(self) -> str:
        return self._device_type

    @device_type.setter
    def device_type(self, device_type) -> None:
        if device_type not in self.DEVICE_TYPES:
            raise ValueError(
                f'Device type "{device_type}" must be one of {self.DEVICE_TYPES}'
            )
        self._device_type = device_type


class OusterOS1(BaseLidar3D):
    SENSOR_MODEL = 'ouster_os1'

    FRAME_ID = 'sensor_link'
    IP_PORT = 7502
    IP_COMPUTER_ADDRESS = '192.168.131.1'

    BASE_TYPE_NONE = 'none'
    BASE_TYPE_BASE = 'base'
    BASE_TYPES = [
        BASE_TYPE_NONE,
        BASE_TYPE_BASE,
    ]

    CAP_TYPE_HALO = 'halo'
    CAP_TYPE_FINS = 'fins'
    CAP_TYPES = [
        CAP_TYPE_HALO,
        CAP_TYPE_FINS,
    ]

    class ROS_PARAMETER_KEYS:
        FRAME_ID = 'ouster_driver.lidar_frame'
        SENSOR_FRAME_ID = 'ouster_driver.sensor_frame'
        IMU_FRAME_ID = 'ouster_driver.imu_frame'
        PCL_FRAME_ID = 'ouster_driver.point_cloud_frame'
        IP_PORT = 'ouster_driver.lidar_port'
        IP_ADDRESS = 'ouster_driver.sensor_hostname'
        IP_COMPUTER = 'ouster_driver.udp_dest'
        BASE_TYPE = 'ouster_driver.base_type'
        CAP_TYPE = 'ouster_driver.cap_type'

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseLidar3D.TOPIC,
            frame_id: str = FRAME_ID,
            ip: str = BaseLidar3D.IP_ADDRESS,
            port: int = IP_PORT,
            computer_ip: str = IP_COMPUTER_ADDRESS,
            base_type: str = BASE_TYPE_BASE,
            cap_type: str = CAP_TYPE_HALO,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.IP_COMPUTER: OusterOS1.computer_ip,
            self.ROS_PARAMETER_KEYS.IMU_FRAME_ID: OusterOS1.frame_id,
            self.ROS_PARAMETER_KEYS.SENSOR_FRAME_ID: OusterOS1.frame_id,
            self.ROS_PARAMETER_KEYS.PCL_FRAME_ID: OusterOS1.frame_id,
            self.ROS_PARAMETER_KEYS.BASE_TYPE: OusterOS1.base_type,
            self.ROS_PARAMETER_KEYS.CAP_TYPE: OusterOS1.cap_type,
        }
        self.computer_ip = computer_ip
        self.base_type = base_type
        self.cap_type = cap_type
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
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )

    @property
    def computer_ip(self) -> str:
        return str(self._computer_ip)

    @computer_ip.setter
    def computer_ip(self, ip: str) -> None:
        self._computer_ip = IP(str(ip))

    @property
    def base_type(self) -> str:
        return self._base_type

    @base_type.setter
    def base_type(self, base: str) -> None:
        if base not in self.BASE_TYPES:
            raise ValueError(f'Base type {base} must be one of {self.BASE_TYPES}')
        self._base_type = base

    @property
    def cap_type(self) -> str:
        return self._cap_type

    @cap_type.setter
    def cap_type(self, cap):
        if cap not in self.CAP_TYPES:
            raise ValueError(f'Cap type {cap} must be one of {self.CAP_TYPES}')
        self._cap_type = cap


class SeyondLidar(BaseLidar3D):
    """
    The Seyond Robin W.

    At present this lidar us URDF-only; launch files are handled by OutdoorNav
    """

    SENSOR_MODEL = 'seyond_lidar'

    FRAME_ID = 'seyond'
    IP_PORT = 0  # not used at present

    ROBIN_W = 'robin_w'
    DEVICE_TYPE = ROBIN_W
    DEVICE_TYPES = (
        ROBIN_W
    )

    class ROS_PARAMETER_KEYS:
        FRAME_ID = 'seyond_driver.frame_id'
        IP_ADDRESS = 'seyond_driver.device_ip'
        IP_PORT = 'seyond_driver.port'

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseLidar3D.TOPIC,
            frame_id: str = FRAME_ID,
            ip: str = BaseLidar3D.IP_ADDRESS,  # not used
            port: int = IP_PORT,  # not used
            device_type: str = DEVICE_TYPE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = False,  # URDF-only for now
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # Device Type:
        self.device_type = device_type
        # ROS Parameter Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.FRAME_ID: SeyondLidar.frame_id,
            self.ROS_PARAMETER_KEYS.IP_ADDRESS: SeyondLidar.ip,
            self.ROS_PARAMETER_KEYS.IP_PORT: SeyondLidar.port,
        }
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
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )

    @property
    def device_type(self) -> str:
        return self._device_type

    @device_type.setter
    def device_type(self, device_type: str) -> None:
        if device_type not in self.DEVICE_TYPES:
            raise ValueError(
                f'Device type "{device_type}" is not one of "{self.DEVICE_TYPES}"'
            )
        self._device_type = device_type
