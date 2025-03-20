# Software License Agreement (BSD)
#
# @author    Chris Iverach-Brereton <civerachb@clearpathrobotics.com>
# @copyright (c) 2025, Clearpath Robotics, Inc., All rights reserved.
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
from clearpath_config.sensors.types.sensor import BaseSensor


class InsAntenna(Accessory):
    """
    Container class for the GNSS antenna(s) used by the INS sensor

    Supports 3 types
    """
    # antenna type
    TYPE_HELICAL = 'helical'
    TYPE_PATCH = 'patch'
    TYPE_SPHERICAL = 'spherical'
    DEFAULT_TYPE = TYPE_SPHERICAL
    TYPES = (
        TYPE_HELICAL,
        TYPE_PATCH,
        TYPE_SPHERICAL,
    )

    def __init__(
        self,
        idx: int = 0,
        prefix: str = 'ins_0',
        parent: str = 'base_link',
        type: str = DEFAULT_TYPE,
        xyz: List[float] = [0.0, 0.0, 0.0],
        rpy: List[float] = [0.0, 0.0, 0.0],
    ):
        self.antenna_type = type

        super().__init__(
            name=f'{prefix}_gps_{idx}_frame',
            parent=parent,
            xyz=xyz,
            rpy=rpy,
        )

    @property
    def antenna_type(self) -> str:
        return self._antenna_type

    @antenna_type.setter
    def antenna_type(self, antenna_type: str) -> None:
        assert antenna_type in InsAntenna.TYPES, f'{antenna_type} is not one of ({InsAntenna.TYPES})' # noqa: E501
        self._antenna_type = antenna_type


class BaseINS(BaseSensor):
    """
    Base class for all INS sensors

    INS sensors have 2-3 relevant frames:
    - primary sensor frame
    - 1-2 GPS antenna frames

    These sensors output the following topics in the sensors/ins_N namespace:
    - gps_0/fix (NavSatFix)
    - gps_0/vel (Twist)
    - gps_1/fix (NavSatFix) (if 2 GPS frames, otherwise skipped)
    - gps_1/vel (Twist) (as above)
    - imu/data (Imu)
    - odom (Odometry)
    """
    SENSOR_TYPE = 'ins'
    SENSOR_MODEL = 'base'

    FRAME_ID = 'link'

    # GPS fix topics (1-2)
    FIX_TOPICS = [
        'gps_0/fix'
    ]
    VEL_TOPICS = [
        'gps_0/vel'
    ]
    IMU_TOPIC = 'imu/data'
    ODOM_TOPIC = 'odom'

    DEFAULT_ANTENNAS = [
        InsAntenna()
    ]

    def __init__(
        self,
        idx: int = None,
        name: str = None,
        topic: str = ODOM_TOPIC,
        frame_id: str = FRAME_ID,
        urdf_enabled: bool = BaseSensor.URDF_ENABLED,
        launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
        ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
        ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
        parent: str = Accessory.PARENT,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
        antennas: List[InsAntenna] = DEFAULT_ANTENNAS
    ) -> None:
        self.antennas = antennas
        self.frame_id = frame_id

        super().__init__(
            idx=idx,
            name=name,
            topic=topic,
            urdf_enabled=urdf_enabled,
            launch_enabled=launch_enabled,
            ros_parameters=ros_parameters,
            ros_parameters_template=ros_parameters_template,
            parent=parent,
            xyz=xyz,
            rpy=rpy,
        )

    def from_dict(self, d):
        super().from_dict(d)

        if 'antennas' in d:
            antennas = []
            i = 0
            for antenna_dict in d['antennas']:
                antennas.append(InsAntenna(
                    idx=i,
                    prefix=f'ins_{self.idx}',
                    **antenna_dict
                ))
                i += 1
            self.antennas = antennas

    @property
    def antennas(self) -> List[InsAntenna]:
        return self._antennas

    @antennas.setter
    def antennas(self, antennas: List[InsAntenna]) -> None:
        self._antennas = []
        for a in antennas:
            self._antennas.append(a)
        assert len(self.antennas) >= 1, 'Must include at least 1 antenna'
        assert len(self.antennas) <= 2, 'Cannot have more than 2 antennas'

    @property
    def frame_id(self) -> str:
        return self._frame_id

    @frame_id.setter
    def frame_id(self, link: str) -> None:
        Accessory.assert_valid_link(link)
        self._frame_id = link


class Fixposition(BaseINS):
    SENSOR_MODEL = 'fixposition'

    XVN = 'xvn'
    DEVICE_TYPE = XVN
    DEVICE_TYPES = (
        XVN
    )

    XVN_IP = '192.168.131.35'
    XVN_IP_TYPE = 'tcp'
    XVN_PORT = 21001
    XVN_RATE = 200
    XVN_RECONNECT = 5
    XVN_FORMATS = [
        'ODOMETRY',
        'LLH',
        'RAWIMU',
        'CORRIMU'
    ]

    # These topics are optional and not supported by default on Clearpath platforms
    # eventually we may have defaults, but for now they're blank and customers can
    # configure them if desired
    XVN_WHEEL_SPEED_TOPIC = ''
    XVN_RTCM_TOPIC = ''

    class ROS_PARAMETER_KEYS:
        IP_ADDRESS = 'xvn.fp_output.ip'
        IP_TYPE = 'xvn.fp_output.type'
        PORT = 'xvn.fp_output.port'
        RATE = 'xvn.fp_output.rate'
        RECONNECT = 'xvn.fp_output.reconnect'
        FORMATS = 'xvn.fp_output.formats'

        WHEEL_SPEED_TOPIC = 'xvn.customer_input.speed_topic'
        RTCM_TOPIC = 'xvn.customer_input.rtcm_topic'


    def __init__(
        self,
        idx: int = None,
        name: str = None,
        topic: str = BaseINS.ODOM_TOPIC,
        frame_id: str = BaseINS.FRAME_ID,
        urdf_enabled: bool = BaseSensor.URDF_ENABLED,
        launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
        ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
        ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
        parent: str = Accessory.PARENT,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
        antennas: List[InsAntenna] = BaseINS.DEFAULT_ANTENNAS,
        device_type: str = DEVICE_TYPE,
    ):
        self.device_type = device_type
        self.ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.IP_ADDRESS: Fixposition.ip_address,
            self.ROS_PARAMETER_KEYS.IP_TYPE: Fixposition.ip_type,
            self.ROS_PARAMETER_KEYS.PORT: Fixposition.port,
            self.ROS_PARAMETER_KEYS.RATE: Fixposition.rate,
            self.ROS_PARAMETER_KEYS.RECONNECT: Fixposition.reconnect,
            self.ROS_PARAMETER_KEYS.FORMATS: Fixposition.formats,
            self.ROS_PARAMETER_KEYS.WHEEL_SPEED_TOPIC: Fixposition.wheel_speed_topic,
            self.ROS_PARAMETER_KEYS.RTCM_TOPIC: Fixposition.rtcm_topic,
        }
        super().__init__(
            idx=idx,
            name=name,
            topic=topic,
            frame_id=frame_id,
            urdf_enabled=urdf_enabled,
            launch_enabled=launch_enabled,
            ros_parameters=ros_parameters,
            ros_parameters_template=ros_parameters_template,
            parent=parent,
            xyz=xyz,
            rpy=rpy,
            antennas=antennas,
        )

    @property
    def device_type(self) -> str:
        return self._device_type

    @device_type.setter
    def device_type(self, device_type: str) -> None:
        assert device_type in self.DEVICE_TYPES, (
            f'Device type "{device_type}" is not one of "{self.DEVICE_TYPES}"'
        )
        self._device_type = device_type

    @property
    def ip_address(self) -> str:
        return str(self._ip_address)

    @ip_address.setter
    def ip_address(self, ip: str) -> None:
        BaseSensor.assert_is_ipv4_address(ip)
        self._ip_address = IP(ip)

    @property
    def ip_type(self) -> str:
        return self._ip_type

    @ip_type.setter
    def ip_type(self, ip_type: str) -> None:
        assert ip_type.lower() in ('tcp', 'udp'), f'"{ip_type}" is not one of ["tcp", "udp"]'
        self._ip_type = ip_type

    @property
    def port(self) -> int:
        return int(self._port)

    @port.setter
    def port(self, port: int) -> None:
        assert (port >= 0 and port <= 65535), f'Port {port} is invalid: 0-65536'
        self._port = Port(port)

    @property
    def rate(self) -> int:
        return self._rate

    @rate.setter
    def rate(self, rate: int) -> None:
        assert rate >= 0, 'Rate cannot be negative'
        self._rate = rate

    @property
    def reconnect(self) -> int:
        return self._reconnect

    @reconnect.setter
    def reconnect(self, reconnect: int) -> None:
        assert reconnect >= 0, 'Reconnect timeout cannot be negative'
        self._reconnect = reconnect

    @property
    def formats(self) -> List[str]:
        return self._formats

    @formats.setter
    def formats(self, formats: List[str]) -> None:
        self._formats = formats

    @property
    def wheel_speed_topic(self) -> str:
        return self._wheel_speed_topic

    @wheel_speed_topic.setter
    def wheel_speed_topic(self, wheel_speed_topic: str) -> None:
        self._wheel_speed_topic = wheel_speed_topic

    @property
    def rtcm_topic(self) -> str:
        return self._rtcm_topic

    @rtcm_topic.setter
    def rtcm_topic(self, rtcm_topic: str) -> None:
        self._rtcm_topic = rtcm_topic
