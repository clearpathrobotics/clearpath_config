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
from clearpath_config.common.types.file import File
from clearpath_config.common.utils.dictionary import extend_flat_dict
from clearpath_config.sensors.types.sensor import BaseSensor
from typing import List


class BaseIMU(BaseSensor):
    SENSOR_TYPE = "imu"
    SENSOR_MODEL = "base"
    TOPIC = "imu"

    PORT = "/dev/clearpath/imu"
    FRAME_ID = "link"
    USE_ENU = True

    class ROS_PARAMETERS_KEYS:
        PORT = "node_name.port"
        FRAME_ID = "node_name.frame_id"
        USE_ENU = "node_name.use_enu"

    class TOPICS:
        RAW_DATA = "raw"
        DATA = "data"
        MAG = "mag"
        NAME = {
            RAW_DATA: "data_raw",
            DATA: "data",
            MAG: "mag"
        }
        RATE = {
            RAW_DATA: 60,
            DATA: 60,
            MAG: 60
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            use_enu: bool = USE_ENU,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # Frame ID
        self.frame_id: str = self.FRAME_ID
        self.set_frame_id(frame_id)
        # Port
        self.port: str = self.PORT
        self.set_port(port)
        # Use ENU
        self.use_enu: bool = self.USE_ENU
        self.set_use_enu(use_enu)
        # ROS Parameter Template
        template = {
            self.ROS_PARAMETERS_KEYS.FRAME_ID: BaseIMU.frame_id,
            self.ROS_PARAMETERS_KEYS.PORT: BaseIMU.port,
            self.ROS_PARAMETERS_KEYS.USE_ENU: BaseIMU.use_enu,
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

    def set_idx(self, idx: int) -> None:
        super().set_idx(idx)
        # Update Frame ID
        self.set_frame_id("%s_%s" % (
            self.get_name_from_idx(idx),
            self.FRAME_ID
        ))

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
    def port(self) -> str:
        return str(self._port)

    @port.setter
    def port(self, file: str) -> None:
        self._port = File(file)

    def get_port(self) -> str:
        return self.port

    def set_port(self, file: str) -> None:
        self.port = file

    @property
    def use_enu(self) -> bool:
        return self._use_enu

    @use_enu.setter
    def use_enu(self, enu: bool) -> None:
        self._use_enu = bool(enu)

    def get_use_enu(self) -> bool:
        return self.use_enu

    def set_use_enu(self, enu: bool) -> None:
        self.use_enu = bool(enu)


class Microstrain(BaseIMU):
    SENSOR_MODEL = "microstrain_imu"

    PORT = "/dev/microstrain_main"
    FRAME_ID = "link"
    USE_ENU = True

    class ROS_PARAMETERS_KEYS:
        PORT = "microstrain_inertial_driver.port"
        FRAME_ID = "microstrain_inertial_driver.imu_frame_id"
        USE_ENU = "microstrain_inertial_driver.use_enu_frame"

    class TOPICS:
        RAW_DATA = "raw"
        DATA = "data"
        MAG = "mag"
        NAME = {
            RAW_DATA: "data_raw",
            DATA: "data",
            MAG: "mag"
        }
        RATE = {
            RAW_DATA: 60,
            DATA: 60,
            MAG: 60
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseIMU.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            use_enu: bool = USE_ENU,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
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
            port,
            use_enu,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )


class CHRoboticsUM6(BaseIMU):
    SENSOR_MODEL = "chrobotics_um6"

    PORT = "/dev/clearpath/imu"
    FRAME_ID = "link"
    USE_ENU = True

    class ROS_PARAMETERS_KEYS:
        PORT = "um6_driver.port"
        FRAME_ID = "um6_driver.frame_id"
        USE_ENU = "um6_driver.tf_ned_to_enu"

    class TOPICS:
        RAW_DATA = "raw"
        DATA = "data"
        MAG = "mag"
        NAME = {
            RAW_DATA: "data_raw",
            DATA: "data",
            MAG: "mag"
        }
        RATE = {
            RAW_DATA: 60,
            DATA: 60,
            MAG: 60
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseIMU.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            use_enu: bool = USE_ENU,
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
            port,
            use_enu,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )


class RedshiftUM7(BaseIMU):
    SENSOR_MODEL = "redshift_um7"

    PORT = "/dev/clearpath/um7"
    FRAME_ID = "link"
    USE_ENU = True

    class ROS_PARAMETERS_KEYS:
        PORT = "um7_driver.port"
        FRAME_ID = "um7_driver.frame_id"
        USE_ENU = "um7_driver.tf_ned_to_enu"

    class TOPICS:
        RAW_DATA = "raw"
        DATA = "data"
        MAG = "mag"
        NAME = {
            RAW_DATA: "data_raw",
            DATA: "data",
            MAG: "mag"
        }
        RATE = {
            RAW_DATA: 60,
            DATA: 60,
            MAG: 60
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseIMU.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            use_enu: bool = USE_ENU,
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
            port,
            use_enu,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )
