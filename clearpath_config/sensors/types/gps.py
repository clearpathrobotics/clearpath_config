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
from clearpath_config.common.types.file import File
from clearpath_config.common.utils.dictionary import extend_flat_dict
from clearpath_config.sensors.types.sensor import BaseSensor
from typing import List


class BaseGPS(BaseSensor):
    SENSOR_TYPE = "gps"
    SENSOR_MODEL = "base"
    TOPIC = "fix"

    FRAME_ID = "link"

    class ROS_PARAMETER_KEYS:
        FRAME_ID = "node_name.frame_id"

    class TOPICS:
        FIX = "fix"
        NAME = {
            FIX: "fix",
        }
        RATE = {
            FIX: 60,
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = TOPIC,
            frame_id: str = FRAME_ID,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # Frame ID
        self.frame_id: str = self.FRAME_ID
        self.set_frame_id(frame_id)
        # ROS Parameters Template
        template = {
            self.ROS_PARAMETER_KEYS.FRAME_ID: BaseGPS.frame_id,
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


class SwiftNavDuro(BaseGPS):
    SENSOR_MODEL = "swiftnav_duro"

    FRAME_ID = "link"
    IP_ADDRESS = "192.168.131.30"
    IP_PORT = 55555

    class ROS_PARAMETER_KEYS:
        FRAME_ID = "duro_node.imu_frame_id"
        GPS_FRAME = "duro_node.gps_receiver_frame_id"
        IP_ADDRESS = "duro_node.ip_address"
        IP_PORT = "duro_node.port"

    class TOPICS:
        FIX = "fix"
        NAME = {
            FIX: "fix",
        }
        RATE = {
            FIX: 60,
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseGPS.TOPIC,
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
        # IP Address
        self.ip: IP = IP(self.IP_ADDRESS)
        self.set_ip(ip)
        # IP Port
        self.port: Port = Port(self.IP_PORT)
        self.set_port(port)
        # ROS Parameter Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.IP_ADDRESS: SwiftNavDuro.ip,
            self.ROS_PARAMETER_KEYS.IP_PORT: SwiftNavDuro.port,
            self.ROS_PARAMETER_KEYS.FRAME_ID: SwiftNavDuro.frame_id,
            self.ROS_PARAMETER_KEYS.GPS_FRAME: SwiftNavDuro.frame_id,
        }
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )

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


class NMEA(BaseGPS):
    SENSOR_MODEL = "nmea_gps"

    FRAME_ID = "link"
    PORT = "/dev/ttyACM0"
    BAUD = 115200

    class ROS_PARAMETER_KEYS:
        FRAME_ID = "nmea_navsat_driver.frame_id"
        PORT = "nmea_navsat_driver.port"
        BAUD = "nmea_navsat_driver.baud"

    class TOPICS:
        FIX = "fix"
        NAME = {
            FIX: "fix",
        }
        RATE = {
            FIX: 60,
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseGPS.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            baud: int = BAUD,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # Port
        self.port = port
        # Baud
        self.baud = baud
        # ROS Paramater Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.PORT: NMEA.port,
            self.ROS_PARAMETER_KEYS.BAUD: NMEA.baud
        }
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )

    @property
    def port(self) -> str:
        return str(self._port)

    @port.setter
    def port(self, file: str) -> str:
        self._port = File(str(file))

    @property
    def baud(self) -> int:
        return self._baud

    @baud.setter
    def baud(self, baud: int) -> None:
        assert isinstance(baud, int), ("Baud must be of type 'int'.")
        assert baud >= 0, ("Baud must be positive integer.")
        self._baud = baud


class Garmin18x(NMEA):
    SENSOR_MODEL = "garmin_18x"

    FRAME_ID = "link"
    PORT = "/dev/ttyACM0"
    BAUD = 115200

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseGPS.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            baud: int = BAUD,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY) -> None:
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            port,
            baud,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )


class NovatelSmart6(NMEA):
    SENSOR_MODEL = "novatel_smart6"

    FRAME_ID = "link"
    PORT = "/dev/ttyACM0"
    BAUD = 115200

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseGPS.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            baud: int = BAUD,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY) -> None:
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            port,
            baud,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )


class NovatelSmart7(NMEA):
    SENSOR_MODEL = "novatel_smart7"

    FRAME_ID = "link"
    PORT = "/dev/ttyACM0"
    BAUD = 115200

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseGPS.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            baud: int = BAUD,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY) -> None:
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            port,
            baud,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )
