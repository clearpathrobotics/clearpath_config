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
from clearpath_config.common.types.file import File
from clearpath_config.common.types.ip import IP
from clearpath_config.common.types.port import Port
from clearpath_config.common.utils.dictionary import extend_flat_dict
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
