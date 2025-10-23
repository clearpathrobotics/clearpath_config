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
from clearpath_config.common.utils.dictionary import extend_flat_dict
from clearpath_config.sensors.types.sensor import BaseSensor


class IMUFilter():
    TYPE = 'type'

    class Base():
        TYPE = 'base'
        INPUT_RAW = 'input_raw'
        INPUT_MAG = 'input_mag'
        OUTPUT = 'output'

        INPUT_RAW_DEFAULT = 'data_raw'
        INPUT_MAG_DEFAULT = 'mag'
        OUTPUT_DEFAULT = 'data'

        def __init__(self, config: dict) -> None:
            self.from_dict(config)

        def from_dict(self, config: dict) -> None:
            self.input_raw = config.get(self.INPUT_RAW, self.INPUT_RAW_DEFAULT)
            self.input_mag = config.get(self.INPUT_MAG, self.INPUT_MAG_DEFAULT)
            self.output = config.get(self.OUTPUT, self.OUTPUT_DEFAULT)

        def to_dict(self) -> dict:
            return {
                IMUFilter.TYPE: self.TYPE,
                self.INPUT_RAW: self.input_raw,
                self.INPUT_MAG: self.input_mag,
                self.OUTPUT: self.output
            }

        @property
        def input_raw(self) -> str:
            return self._input_raw

        @input_raw.setter
        def input_raw(self, value: str) -> None:
            self._input_raw = value

        @property
        def input_mag(self) -> str:
            return self._input_mag

        @input_mag.setter
        def input_mag(self, value: str) -> None:
            self._input_mag = value

        @property
        def output(self) -> str:
            return self._output

        @output.setter
        def output(self, value: str) -> None:
            self._output = value

    class NoFilter(Base):
        TYPE = 'none'

    class Madgwick(Base):
        TYPE = 'madgwick'

    TYPES = {
        NoFilter.TYPE: NoFilter,
        Madgwick.TYPE: Madgwick
    }

    def __new__(self, config: dict) -> None:
        if self.TYPE not in config:
            raise ValueError(f'IMU filter {config} does not have parameter "{self.TYPE}"')
        if config[self.TYPE] not in self.TYPES:
            raise ValueError(f'IMU filter {config} "{self.TYPE}" must be one of: "{self.TYPES}"')
        return self.TYPES[config[self.TYPE]](config)


class BaseIMU(BaseSensor):
    SENSOR_TYPE = 'imu'
    SENSOR_MODEL = 'base'
    TOPIC = 'imu'

    PORT = '/dev/clearpath/imu'
    FRAME_ID = 'link'
    USE_ENU = True
    UPDATE_RATE = 20

    IMU_FILTER = 'filter'
    IMU_FILTER_DEFAULT = {'type': IMUFilter.NoFilter.TYPE}

    class ROS_PARAMETER_KEYS:
        FRAME_ID = 'node_name.frame_id'

    class TOPICS:
        DATA = 'data'
        MAG = 'mag'
        NAME = {
            DATA: 'data',
            MAG: 'mag'
        }
        TYPE = {
            DATA: 'sensor_msgs/msg/Imu',
            MAG: 'sensor_msgs/msg/MagneticField'
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            use_enu: bool = USE_ENU,
            update_rate: int = UPDATE_RATE,
            imu_filter: IMUFilter = IMU_FILTER_DEFAULT,
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
        # Port
        self.port = port
        # Use ENU
        self.use_enu = use_enu
        # Update Rate
        self.update_rate = update_rate
        # Filter
        self.imu_filter = imu_filter
        # ROS Parameter Template
        template = {
            self.ROS_PARAMETER_KEYS.FRAME_ID: BaseIMU.frame_id,
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
            BaseIMU.TOPICS.DATA: 20,
            BaseIMU.TOPICS.MAG: 20
        }

    @classmethod
    def get_frame_id_from_idx(cls, idx: int) -> str:
        return '%s_%s' % (
            cls.get_name_from_idx(idx),
            cls.FRAME_ID
        )

    def set_idx(self, idx: int) -> None:
        super().set_idx(idx)
        # Update Frame ID
        self.frame_id = ('%s_%s' % (
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

    @property
    def port(self) -> str:
        return str(self._port)

    @port.setter
    def port(self, file: str) -> None:
        self._port = File(file)

    @property
    def use_enu(self) -> bool:
        return self._use_enu

    @use_enu.setter
    def use_enu(self, enu: bool) -> None:
        self._use_enu = bool(enu)

    @property
    def update_rate(self) -> int:
        return self._update_rate

    @update_rate.setter
    def update_rate(self, rate: int) -> None:
        BaseSensor.assert_valid_rate(rate)
        self._update_rate = int(rate)

    @property
    def imu_filter(self) -> IMUFilter:
        return self._imu_filter

    @imu_filter.setter
    def imu_filter(self, imu_filter: dict) -> None:
        self._imu_filter = IMUFilter(imu_filter)

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['filter'] = self.imu_filter.to_dict()
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if self.IMU_FILTER in d:
            self.imu_filter = d[self.IMU_FILTER]


class Microstrain(BaseIMU):
    SENSOR_MODEL = 'microstrain_imu'

    PORT = '/dev/microstrain_main'
    FRAME_ID = 'link'
    USE_ENU = True
    IMU_RATE = 100
    MAG_RATE = 0

    class ROS_PARAMETER_KEYS:
        PORT = 'microstrain_inertial_driver.port'
        FRAME_ID = 'microstrain_inertial_driver.frame_id'
        USE_ENU = 'microstrain_inertial_driver.use_enu_frame'
        IMU_RATE = 'microstrain_inertial_driver.imu_data_rate'
        MAG_RATE = 'microstrain_inertial_driver.imu_mag_data_rate'

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseIMU.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            use_enu: bool = USE_ENU,
            imu_rate: int = IMU_RATE,
            mag_rate: int = MAG_RATE,
            imu_filter: str = BaseIMU.IMU_FILTER_DEFAULT,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # Initialization
        self.mag_rate = mag_rate
        # ROS Parameters Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.FRAME_ID: Microstrain.frame_id,
            self.ROS_PARAMETER_KEYS.PORT: Microstrain.port,
            self.ROS_PARAMETER_KEYS.USE_ENU: Microstrain.use_enu,
            self.ROS_PARAMETER_KEYS.IMU_RATE: Microstrain.imu_rate,
            self.ROS_PARAMETER_KEYS.MAG_RATE: Microstrain.mag_rate
        }
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            port,
            use_enu,
            imu_rate,
            imu_filter,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )
        self.rates = {
            Microstrain.TOPICS.DATA: Microstrain.imu_rate,
            Microstrain.TOPICS.MAG: Microstrain.mag_rate
        }

    @property
    def imu_rate(self) -> int:
        return self.update_rate

    @imu_rate.setter
    def imu_rate(self, rate: int) -> None:
        self.update_rate = int(rate)

    @property
    def mag_rate(self) -> int:
        return self._mag_rate

    @mag_rate.setter
    def mag_rate(self, rate: int) -> None:
        self._mag_rate = int(rate)


class CHRoboticsUM6(BaseIMU):
    SENSOR_MODEL = 'chrobotics_um6'

    PORT = '/dev/clearpath/imu'
    FRAME_ID = 'link'
    USE_ENU = True
    UPDATE_RATE = 20

    class ROS_PARAMETER_KEYS:
        PORT = 'um6_driver.port'
        FRAME_ID = 'um6_driver.frame_id'
        USE_ENU = 'um6_driver.tf_ned_to_enu'
        UPDATE_RATE = 'um6_driver.update_rate'

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseIMU.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            use_enu: bool = USE_ENU,
            update_rate: int = UPDATE_RATE,
            imu_filter: str = BaseIMU.IMU_FILTER_DEFAULT,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.FRAME_ID: CHRoboticsUM6.frame_id,
            self.ROS_PARAMETER_KEYS.PORT: CHRoboticsUM6.port,
            self.ROS_PARAMETER_KEYS.USE_ENU: CHRoboticsUM6.use_enu,
            self.ROS_PARAMETER_KEYS.UPDATE_RATE: CHRoboticsUM6.update_rate
        }
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            port,
            use_enu,
            update_rate,
            imu_filter,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )
        self.rates = {
            CHRoboticsUM6.TOPICS.DATA: CHRoboticsUM6.update_rate,
            CHRoboticsUM6.TOPICS.MAG: CHRoboticsUM6.update_rate,
        }


class RedshiftUM7(BaseIMU):
    SENSOR_MODEL = 'redshift_um7'

    PORT = '/dev/clearpath/um7'
    FRAME_ID = 'link'
    USE_ENU = True
    UPDATE_RATE = 20

    class ROS_PARAMETER_KEYS:
        PORT = 'um7_driver.port'
        FRAME_ID = 'um7_driver.frame_id'
        USE_ENU = 'um7_driver.tf_ned_to_enu'
        UPDATE_RATE = 'um7_driver.update_rate'

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseIMU.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            use_enu: bool = USE_ENU,
            update_rate: int = UPDATE_RATE,
            imu_filter: str = BaseIMU.IMU_FILTER_DEFAULT,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.FRAME_ID: RedshiftUM7.frame_id,
            self.ROS_PARAMETER_KEYS.PORT: RedshiftUM7.port,
            self.ROS_PARAMETER_KEYS.USE_ENU: RedshiftUM7.use_enu,
            self.ROS_PARAMETER_KEYS.UPDATE_RATE: RedshiftUM7.update_rate
        }
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            port,
            use_enu,
            update_rate,
            imu_filter,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )
        self.rates = {
            RedshiftUM7.TOPICS.DATA: RedshiftUM7.update_rate,
            RedshiftUM7.TOPICS.MAG: RedshiftUM7.update_rate,
        }


class PhidgetsSpatial(BaseIMU):
    SENSOR_MODEL = 'phidgets_spatial'

    PORT = None
    FRAME_ID = 'link'
    USE_ENU = True
    USE_MAG = True
    DATA_INTERVAL = 20

    IMU_FILTER_DEFAULT = {'type': IMUFilter.Madgwick.TYPE}

    class ROS_PARAMETER_KEYS:
        FRAME_ID = 'phidgets_spatial.frame_id'
        DATA_INTERVAL = 'phidgets_spatial.data_interval_ms'
        USE_MAG = 'imu_filter_madgwick.use_mag'

    class TOPICS:
        DATA = 'data'
        RAW_DATA = 'raw'
        MAG = 'mag'
        CALIB = 'calibrated'
        NAME = {
            DATA: 'data',
            RAW_DATA: 'data_raw',
            MAG: 'mag',
            CALIB: 'is_calibrated'
        }
        TYPE = {
            DATA: 'sensor_msgs/msg/Imu',
            RAW_DATA: 'sensor_msgs/msg/Imu',
            MAG: 'sensor_msgs/msg/MagneticField',
            CALIB: 'std_msgs/msg/Bool',
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseIMU.TOPIC,
            frame_id: str = FRAME_ID,
            port: str = PORT,
            use_enu: bool = USE_ENU,
            data_interval: int = DATA_INTERVAL,
            imu_filter: str = IMU_FILTER_DEFAULT,
            use_mag: bool = USE_MAG,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # Initializations
        self.data_interval = data_interval
        self.use_mag = use_mag
        # ROS Parameters Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.FRAME_ID: PhidgetsSpatial.frame_id,
            self.ROS_PARAMETER_KEYS.DATA_INTERVAL: PhidgetsSpatial.data_interval,
            self.ROS_PARAMETER_KEYS.USE_MAG: PhidgetsSpatial.use_mag,
        }
        super().__init__(
            idx,
            name,
            topic,
            frame_id,
            port,
            use_enu,
            round(1000 / data_interval),
            imu_filter,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )
        self.rates = {
            PhidgetsSpatial.TOPICS.DATA: PhidgetsSpatial.update_rate,
            PhidgetsSpatial.TOPICS.RAW_DATA: PhidgetsSpatial.update_rate,
            PhidgetsSpatial.TOPICS.MAG: PhidgetsSpatial.update_rate,
            PhidgetsSpatial.TOPICS.CALIB: PhidgetsSpatial.update_rate
        }

    @property
    def data_interval(self) -> int:
        return self._data_interval

    @data_interval.setter
    def data_interval(self, interval: int) -> None:
        BaseSensor.assert_valid_rate(interval)
        self._data_interval = int(interval)
        self.update_rate = round(1000 / interval)

    @property
    def use_mag(self) -> bool:
        return self._use_mag

    @use_mag.setter
    def use_mag(self, value: bool) -> None:
        self._use_mag = value
