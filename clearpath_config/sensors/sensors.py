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
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.list import OrderedListConfig
from clearpath_config.common.types.platform import Platform
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.sensors.types.sensor import BaseSensor
from clearpath_config.sensors.types.cameras import (
    BaseCamera,
    FlirBlackfly,
    IntelRealsense,
    StereolabsZed,
)
from clearpath_config.sensors.types.gps import (
    BaseGPS,
    SwiftNavDuro,
    Garmin18x,
    NovatelSmart6,
    NovatelSmart7,
)
from clearpath_config.sensors.types.imu import (
    BaseIMU,
    Microstrain,
    CHRoboticsUM6,
    RedshiftUM7,
)
from clearpath_config.sensors.types.lidars_2d import (
    BaseLidar2D,
    HokuyoUST,
    SickLMS1XX,
)
from clearpath_config.sensors.types.lidars_3d import (
    BaseLidar3D,
    VelodyneLidar,
)

from typing import List


class InertialMeasurementUnit():
    MICROSTRAIN_IMU = Microstrain.SENSOR_MODEL
    CHROBOTICS_UM6 = CHRoboticsUM6.SENSOR_MODEL
    REDSHIFT_UM7 = RedshiftUM7.SENSOR_MODEL
    MODEL = {
        MICROSTRAIN_IMU: Microstrain,
        CHROBOTICS_UM6: CHRoboticsUM6,
        REDSHIFT_UM7: RedshiftUM7,
    }

    @classmethod
    def assert_model(cls, model: str) -> None:
        assert model in cls.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                cls.MODEL.keys()
            )
        )

    def __new__(cls, model: str) -> BaseIMU:
        cls.assert_model(model)
        return cls.MODEL[model]()


class Camera():
    FLIR_BLACKFLY = FlirBlackfly.SENSOR_MODEL
    INTEL_REALSENSE = IntelRealsense.SENSOR_MODEL
    STEREOLABS_ZED = StereolabsZed.SENSOR_MODEL

    MODEL = {
        FLIR_BLACKFLY: FlirBlackfly,
        INTEL_REALSENSE: IntelRealsense,
        STEREOLABS_ZED: StereolabsZed,
    }

    @classmethod
    def assert_model(cls, model: str) -> None:
        assert model in cls.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                cls.MODEL.keys()
            )
        )

    def __new__(cls, model: str) -> BaseCamera:
        cls.assert_model(model)
        return cls.MODEL[model]()


class GlobalPositioningSystem():
    SWIFTNAV_DURO = SwiftNavDuro.SENSOR_MODEL
    GARMIN_18X = Garmin18x.SENSOR_MODEL
    NOVATEL_SMART6 = NovatelSmart6.SENSOR_MODEL
    NOVATEL_SMART7 = NovatelSmart7.SENSOR_MODEL

    MODEL = {
        SWIFTNAV_DURO: SwiftNavDuro,
        GARMIN_18X: Garmin18x,
        NOVATEL_SMART6: NovatelSmart6,
        NOVATEL_SMART7: NovatelSmart7,
    }

    @classmethod
    def assert_model(cls, model: str) -> None:
        assert model in cls.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                cls.MODEL.keys()
            )
        )

    def __new__(cls, model: str) -> BaseGPS:
        cls.assert_model(model)
        return cls.MODEL[model]()


class Lidar2D():
    HOKUYO_UST = HokuyoUST.SENSOR_MODEL
    SICK_LMS1XX = SickLMS1XX.SENSOR_MODEL

    MODEL = {
        HOKUYO_UST: HokuyoUST,
        SICK_LMS1XX: SickLMS1XX
    }

    @classmethod
    def assert_model(cls, model: str) -> None:
        assert model in cls.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                cls.MODEL.keys()
            )
        )

    def __new__(cls, model: str) -> BaseLidar2D:
        cls.assert_model(model)
        return cls.MODEL[model]()


class Lidar3D():
    VELODYNE_LIDAR = VelodyneLidar.SENSOR_MODEL

    MODEL = {
        VELODYNE_LIDAR: VelodyneLidar
    }

    @classmethod
    def assert_model(cls, model: str) -> None:
        assert model in cls.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                cls.MODEL.keys()
            )
        )

    def __new__(cls, model: str) -> BaseLidar3D:
        cls.assert_model(model)
        return cls.MODEL[model]()


class Sensor():
    CAMERA = BaseCamera.SENSOR_TYPE
    LIDAR2D = BaseLidar2D.SENSOR_TYPE
    LIDAR3D = BaseLidar3D.SENSOR_TYPE
    IMU = BaseIMU.SENSOR_TYPE
    GPS = BaseGPS.SENSOR_TYPE

    TYPE = {
        CAMERA: Camera,
        LIDAR2D: Lidar2D,
        LIDAR3D: Lidar3D,
        IMU: InertialMeasurementUnit,
        GPS: GlobalPositioningSystem,
    }

    @classmethod
    def assert_type(cls, _type: str) -> None:
        assert _type in cls.TYPE, (
            "Sensor type '%s' must be one of: '%s'" % (
                _type,
                cls.TYPE.keys()
            )
        )

    def __new__(cls, _type: str, _model: str) -> BaseSensor:
        cls.assert_type(_type)
        return cls.TYPE[_type](_model)


class SensorListConfig(OrderedListConfig[BaseSensor]):
    def __init__(self) -> None:
        super().__init__(obj_type=BaseSensor)

    def to_dict(self) -> List[dict]:
        d = []
        for accessory in self.get_all():
            d.append(accessory.to_dict())
        return d


# Sensor Config
class SensorConfig(BaseConfig):
    LIDAR2D_INDEX = 0
    LIDAR3D_INDEX = 0
    CAMERA_INDEX = 0
    IMU_INDEX = 0
    GPS_INDEX = 0

    SENSORS = "sensors"
    CAMERA = BaseCamera.SENSOR_TYPE
    IMU = BaseIMU.SENSOR_TYPE
    GPS = BaseGPS.SENSOR_TYPE
    LIDAR2D = BaseLidar2D.SENSOR_TYPE
    LIDAR3D = BaseLidar3D.SENSOR_TYPE

    TEMPLATE = {
        SENSORS: {
            CAMERA: CAMERA,
            IMU: IMU,
            GPS: GPS,
            LIDAR2D: LIDAR2D,
            LIDAR3D: LIDAR3D
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        CAMERA: [],
        GPS: [],
        IMU: [],
        LIDAR2D: [],
        LIDAR3D: []
    }

    def __init__(
            self,
            config: dict = {},
            camera: List[BaseCamera] = DEFAULTS[CAMERA],
            gps: List[BaseGPS] = DEFAULTS[GPS],
            imu: List[BaseIMU] = DEFAULTS[IMU],
            lidar2d: List[BaseLidar2D] = DEFAULTS[LIDAR2D],
            lidar3d: List[BaseLidar3D] = DEFAULTS[LIDAR3D]
            ) -> None:
        # List Initialization
        self._camera = SensorListConfig()
        self._gps = SensorListConfig()
        self._imu = SensorListConfig()
        self._lidar2d = SensorListConfig()
        self._lidar3d = SensorListConfig()
        # Initialization
        self.camera = camera
        self.gps = gps
        self.imu = imu
        self.lidar2d = lidar2d
        self.lidar3d = lidar3d
        # Template
        template = {
            self.KEYS[self.CAMERA]: SensorConfig.camera,
            self.KEYS[self.GPS]: SensorConfig.gps,
            self.KEYS[self.IMU]: SensorConfig.imu,
            self.KEYS[self.LIDAR2D]: SensorConfig.lidar2d,
            self.KEYS[self.LIDAR3D]: SensorConfig.lidar3d,
        }
        super().__init__(template, config, self.SENSORS)

    def update(self, serial_number=False) -> None:
        if serial_number:
            platform = self.get_platform_model()
            index = Platform.INDEX[platform]
            self._camera.set_index_offset(index.camera)
            self._gps.set_index_offset(index.gps)
            self._imu.set_index_offset(index.imu)
            self._lidar2d.set_index_offset(index.lidar2d)
            self._lidar3d.set_index_offset(index.lidar3d)

    @property
    def camera(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.CAMERA],
            value=self._camera.to_dict()
        )
        return self._camera

    @camera.setter
    def camera(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Sensors must be list of 'dict'")
        assert all([isinstance(d, dict) for d in value]), (
            "Sensors must be list of 'dict'")
        assert all(['model' in d for d in value]), (
            "Sensor 'dict' must have 'model' key")
        sensor_list = []
        for d in value:
            sensor = Camera(d['model'])
            sensor.from_dict(d)
            sensor_list.append(sensor)
        self._camera.set_all(sensor_list)

    @property
    def gps(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.GPS],
            value=self._gps.to_dict()
        )
        return self._gps

    @gps.setter
    def gps(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Sensors must be list of 'dict'")
        assert all([isinstance(d, dict) for d in value]), (
            "Sensors must be list of 'dict'")
        assert all(['model' in d for d in value]), (
            "Sensor 'dict' must have 'model' key")
        sensor_list = []
        for d in value:
            sensor = GlobalPositioningSystem(d['model'])
            sensor.from_dict(d)
            sensor_list.append(sensor)
        self._gps.set_all(sensor_list)

    @property
    def imu(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.IMU],
            value=self._imu.to_dict()
        )
        return self._imu

    @imu.setter
    def imu(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Sensors must be list of 'dict'")
        assert all([isinstance(d, dict) for d in value]), (
            "Sensors must be list of 'dict'")
        assert all(['model' in d for d in value]), (
            "Sensor 'dict' must have 'model' key")
        sensor_list = []
        for d in value:
            sensor = InertialMeasurementUnit(d['model'])
            sensor.from_dict(d)
            sensor_list.append(sensor)
        self._imu.set_all(sensor_list)

    @property
    def lidar2d(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.LIDAR2D],
            value=self._lidar2d.to_dict()
        )
        return self._lidar2d

    @lidar2d.setter
    def lidar2d(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Sensors must be list of 'dict'")
        assert all([isinstance(d, dict) for d in value]), (
            "Sensors must be list of 'dict'")
        assert all(['model' in d for d in value]), (
            "Sensor 'dict' must have 'model' key")
        sensor_list = []
        for d in value:
            sensor = Lidar2D(d['model'])
            sensor.from_dict(d)
            sensor_list.append(sensor)
        self._lidar2d.set_all(sensor_list)

    @property
    def lidar3d(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.LIDAR3D],
            value=self._lidar3d.to_dict()
        )
        return self._lidar3d

    @lidar3d.setter
    def lidar3d(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Sensors must be list of 'dict'")
        assert all([isinstance(d, dict) for d in value]), (
            "Sensors must be list of 'dict'")
        assert all(['model' in d for d in value]), (
            "Sensor 'dict' must have 'model' key")
        sensor_list = []
        for d in value:
            sensor = Lidar3D(d['model'])
            sensor.from_dict(d)
            sensor_list.append(sensor)
        self._lidar3d.set_all(sensor_list)

    # Get All Sensors
    def get_all_sensors(self) -> List[BaseSensor]:
        sensors = []
        # Lidar2D
        sensors.extend(self.get_all_lidar_2d())
        # Lidar3D
        sensors.extend(self.get_all_lidar_3d())
        # Cameras
        sensors.extend(self.get_all_cameras())
        # IMU
        sensors.extend(self.get_all_imu())
        # GPS
        sensors.extend(self.get_all_gps())
        return sensors

    # Lidar2D: Add Lidar2D by Object or Common Lidar2D Parameters
    def add_lidar2d(
            self,
            # By Object
            lidar2d: BaseLidar2D = None,
            # By Model and Paramters
            model: str = None,
            frame_id: str = BaseLidar2D.FRAME_ID,
            ip: str = BaseLidar2D.IP_ADDRESS,
            port: int = BaseLidar2D.IP_PORT,
            min_angle: float = BaseLidar2D.MIN_ANGLE,
            max_angle: float = BaseLidar2D.MAX_ANGLE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        assert lidar2d or model, (
            "Lidar2D object or model must be passed."
        )
        if not lidar2d and model:
            lidar2d = Lidar2D(model)
            lidar2d.set_frame_id(frame_id)
            lidar2d.set_ip(ip)
            lidar2d.set_port(port)
            lidar2d.set_min_angle(min_angle)
            lidar2d.set_max_angle(max_angle)
            lidar2d.set_urdf_enabled(urdf_enabled)
            lidar2d.set_launch_enabled(launch_enabled)
            lidar2d.set_parent(parent)
            lidar2d.set_xyz(xyz)
            lidar2d.set_rpy(rpy)
        self._lidar2d.add(lidar2d)

    # Lidar2D: Add UST
    def add_ust(
            self,
            # By Object
            ust: HokuyoUST = None,
            # By Parameters
            frame_id: str = HokuyoUST.FRAME_ID,
            ip: str = HokuyoUST.IP_ADDRESS,
            port: int = HokuyoUST.IP_PORT,
            min_angle: float = HokuyoUST.MIN_ANGLE,
            max_angle: float = HokuyoUST.MAX_ANGLE,
            urdf_enabled: bool = HokuyoUST.URDF_ENABLED,
            launch_enabled: bool = HokuyoUST.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if ust is None:
            ust = HokuyoUST(
                frame_id=frame_id,
                ip=ip,
                port=port,
                min_angle=min_angle,
                max_angle=max_angle,
                urdf_enabled=urdf_enabled,
                launch_enabled=launch_enabled,
                parent=parent,
                xyz=xyz,
                rpy=rpy
            )
        assert isinstance(ust, HokuyoUST), (
            "Lidar2D object must be of type UST"
        )
        self._lidar2d.add(ust)

    # Lidar2D: Add LMS1xx
    def add_lms1xx(
            self,
            # By Object
            lms1xx: SickLMS1XX = None,
            # By Parameters
            frame_id: str = SickLMS1XX.FRAME_ID,
            ip: str = SickLMS1XX.IP_ADDRESS,
            port: int = SickLMS1XX.IP_PORT,
            min_angle: float = SickLMS1XX.MIN_ANGLE,
            max_angle: float = SickLMS1XX.MAX_ANGLE,
            urdf_enabled: bool = SickLMS1XX.URDF_ENABLED,
            launch_enabled: bool = SickLMS1XX.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if lms1xx is None:
            lms1xx = SickLMS1XX(
                frame_id=frame_id,
                ip=ip,
                port=port,
                min_angle=min_angle,
                max_angle=max_angle,
                urdf_enabled=urdf_enabled,
                launch_enabled=launch_enabled,
                parent=parent,
                xyz=xyz,
                rpy=rpy
            )
        assert isinstance(lms1xx, SickLMS1XX), (
            "Lidar2D object must be of type LMS1XX"
        )
        self._lidar2d.add(lms1xx)

    # Lidar2D: Remove Lidar2D by passing object or index
    def remove_lidar_2d(self, lidar_2d: BaseLidar2D | int) -> None:
        self._lidar2d.remove(lidar_2d)

    # Lidar2D: Get Single Object
    def get_lidar_2d(self, idx: int) -> BaseLidar2D:
        return self._lidar2d.get(idx)

    # Lidar2D: Get All Objects
    def get_all_lidar_2d(self) -> List[BaseLidar2D]:
        return self._lidar2d.get_all()

    # Lidar2D: Get All Objects of a Specified Model
    def get_all_lidar_2d_by_model(self, model: str) -> List[BaseLidar2D]:
        Lidar2D.assert_model(model)
        all_model_lidar_2d = []
        for lidar_2d in self.get_all_lidar_2d():
            if lidar_2d.SENSOR_MODEL == model:
                all_model_lidar_2d.append(lidar_2d)
        return all_model_lidar_2d

    # Lidar2D: Get All Objects of Model UST
    def get_all_ust(self) -> List[HokuyoUST]:
        return self.get_all_lidar_2d_by_model(Lidar2D.UST)

    # Lidar2D: Get All Objects of Model LMS1XX
    def get_all_lms1xx(self) -> List[SickLMS1XX]:
        return self.get_all_lidar_2d_by_model(Lidar2D.LMS1XX)

    # Lidar2D: Set Lidar2D Object
    def set_lidar_2d(self, lidar_2d: BaseLidar2D) -> None:
        self._lidar2d.set(lidar_2d)

    # Lidar2D: Set All Lidar2D Objects
    def set_all_lidar_2d(self, all_lidar_2d: List[BaseLidar2D]) -> None:
        self._lidar2d.set_all(all_lidar_2d)

    # Lidar3D: Add Lidar3D by Object or Common Lidar3D Parameters
    def add_lidar3d(
            self,
            # By Object
            lidar3d: BaseLidar3D = None,
            # By Model and Parameters
            model: str = None,
            frame_id: str = BaseLidar3D.FRAME_ID,
            ip: str = BaseLidar3D.IP_ADDRESS,
            port: int = BaseLidar3D.IP_PORT,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        assert lidar3d or model, (
            "Lidar3D object or model must be passed."
        )
        if not lidar3d and model:
            lidar3d = Lidar3D(model)
            lidar3d.set_frame_id(frame_id)
            lidar3d.set_ip(ip)
            lidar3d.set_port(port)
            lidar3d.set_urdf_enabled(urdf_enabled)
            lidar3d.set_launch_enabled(launch_enabled)
            lidar3d.set_parent(parent)
            lidar3d.set_xyz(xyz)
            lidar3d.set_rpy(rpy)
        self._lidar3d.add(lidar3d)

    # Lidar3D: Add Velodyne
    def add_velodyne(
            self,
            # By Object
            velodyne: VelodyneLidar = None,
            # By Parameters
            frame_id: str = VelodyneLidar.FRAME_ID,
            ip: str = VelodyneLidar.IP_ADDRESS,
            port: int = VelodyneLidar.IP_PORT,
            device_type: str = VelodyneLidar.DEVICE_TYPE,
            urdf_enabled: bool = VelodyneLidar.URDF_ENABLED,
            launch_enabled: bool = VelodyneLidar.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if velodyne is None:
            velodyne = VelodyneLidar(
                frame_id=frame_id,
                ip=ip,
                port=port,
                device_type=device_type,
                urdf_enabled=urdf_enabled,
                launch_enabled=launch_enabled,
                parent=parent,
                xyz=xyz,
                rpy=rpy
            )
        assert isinstance(velodyne, VelodyneLidar), (
            "Lidar3D object must be of type VelodyneLidar"
        )
        self._lidar3d.add(velodyne)

    # Lidar3D: Remove Lidar3D by passing object or index
    def remove_lidar_3d(self, lidar_3d: BaseLidar3D | int) -> None:
        self._lidar3d.remove(lidar_3d)

    # Lidar3D: Get Single Object
    def get_lidar_3d(self, idx: int) -> BaseLidar3D:
        return self._lidar3d.get(idx)

    # Lidar3D: Get All Objects
    def get_all_lidar_3d(self) -> List[BaseLidar3D]:
        return self._lidar3d.get_all()

    # Lidar3D: Get All Objects of a Specified Model
    def get_all_lidar_3d_by_model(self, model: str) -> List[BaseLidar3D]:
        Lidar3D.assert_model(model)
        all_model_lidar_3d = []
        for lidar_3d in self.get_all_lidar_3d():
            if lidar_3d.SENSOR_MODEL == model:
                all_model_lidar_3d.append(lidar_3d)
        return all_model_lidar_3d

    # Lidar3D: Get All Objects of Model UST
    def get_all_velodyne(self) -> List[VelodyneLidar]:
        return self.get_all_lidar_3d_by_model(Lidar3D.VELODYNE_LIDAR)

    # Lidar3D: Set Lidar3D Object
    def set_lidar_3d(self, lidar_3d: BaseLidar3D) -> None:
        self._lidar3d.set(lidar_3d)

    # Lidar3D: Set All Lidar3D Objects
    def set_all_lidar_3d(self, all_lidar_3d: List[BaseLidar3D]) -> None:
        self._lidar3d.set_all(all_lidar_3d)

    # Camera: Add Camera
    def add_camera(
            self,
            # By Object
            camera: BaseCamera = None,
            # By Model and Parameters
            model: str = None,
            fps: int = BaseCamera.FPS,
            serial: str = BaseCamera.SERIAL,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        assert camera or model, (
            "Camera object or model must be passed."
        )
        if not camera and model:
            camera = Camera(model)
            camera.set_fps(fps)
            camera.set_serial(serial)
            camera.set_urdf_enabled(urdf_enabled)
            camera.set_launch_enabled(launch_enabled)
            camera.set_ros_parameters(ros_parameters)
            camera.set_parent(parent)
            camera.set_xyz(xyz)
            camera.set_rpy(rpy)
        self._camera.add(camera)

    # Camera: Add Blackfly
    def add_blackfly(
            self,
            # By Object
            blackfly: FlirBlackfly = None,
            # By Parameters
            connection_type: str = FlirBlackfly.CONNECTION_TYPE,
            encoding: str = FlirBlackfly.BAYER_RG8,
            fps: int = BaseCamera.FPS,
            serial: str = BaseCamera.SERIAL,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if blackfly is None:
            blackfly = FlirBlackfly(
                connection_type=connection_type,
                encoding=encoding,
                fps=fps,
                serial=serial,
                urdf_enabled=urdf_enabled,
                launch_enabled=launch_enabled,
                parent=parent,
                xyz=xyz,
                rpy=rpy,
            )
        assert isinstance(blackfly, FlirBlackfly), (
            "Blackfly object must be of type Blackfly"
        )
        self._camera.add(blackfly)

    # Camera: Add Realsense
    def add_realsense(
            self,
            # By Object
            realsense: IntelRealsense = None,
            # By Parameters
            serial: str = BaseCamera.SERIAL,
            device_type: str = IntelRealsense.DEVICE_TYPE,
            color_enabled: bool = IntelRealsense.COLOR_ENABLED,
            color_fps: bool = IntelRealsense.COLOR_FPS,
            color_width: int = IntelRealsense.COLOR_WIDTH,
            color_height: int = IntelRealsense.COLOR_HEIGHT,
            depth_enabled: bool = IntelRealsense.DEPTH_ENABLED,
            depth_fps: int = IntelRealsense.DEPTH_FPS,
            depth_width: int = IntelRealsense.DEPTH_WIDTH,
            depth_height: int = IntelRealsense.DEPTH_HEIGHT,
            pointcloud_enabled: bool = IntelRealsense.POINTCLOUD_ENABLED,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if realsense is None:
            realsense = IntelRealsense(
                serial=serial,
                device_type=device_type,
                color_enabled=color_enabled,
                color_fps=color_fps,
                color_width=color_width,
                color_height=color_height,
                depth_enabled=depth_enabled,
                depth_fps=depth_fps,
                depth_width=depth_width,
                depth_height=depth_height,
                pointcloud_enabled=pointcloud_enabled,
                urdf_enabled=urdf_enabled,
                launch_enabled=launch_enabled,
                ros_parameters=ros_parameters,
                parent=parent,
                xyz=xyz,
                rpy=rpy,
            )
        assert isinstance(realsense, IntelRealsense), (
            "Realsense object must be of type Realsense"
        )
        self._camera.add(realsense)

    # Camera: Remove
    def remove_camera(self, camera: BaseCamera | int) -> None:
        self._camera.remove(camera)

    # Camera: Get
    def get_camera(self, idx: int) -> BaseCamera:
        return self._camera.get(idx)

    # Camera: Get All
    def get_all_cameras(self) -> List[BaseCamera]:
        return self._camera.get_all()

    # Camera: Set
    def set_camera(self, camera: BaseCamera) -> None:
        self._camera.set(camera)

    # Camera: Set All
    def set_all_camera(self, cameras: List[BaseCamera]) -> None:
        self._camera.set_all(cameras)

    # Camera: Get All Objects of a Specified Model
    def get_all_cameras_by_model(self, model: str) -> List[BaseCamera]:
        Camera.assert_model(model)
        all_model_camera = []
        for camera in self.get_all_cameras():
            if camera.SENSOR_MODEL == model:
                all_model_camera.append(camera)
        return all_model_camera

    # Camera: Get All Objects of Model UST
    def get_all_realsense(self) -> List[IntelRealsense]:
        return self.get_all_cameras_by_model(Camera.INTEL_REALSENSE)

    # Camera: Get All Objects of Model LMS1XX
    def get_all_blackfly(self) -> List[FlirBlackfly]:
        return self.get_all_cameras_by_model(Camera.FLIR_BLACKFLY)

    # IMU: Add IMU by Object or Common IMU Parameters
    def add_imu(
            self,
            # By Object
            imu: BaseIMU = None,
            # By Model and Parameters
            model: str = None,
            frame_id: str = BaseIMU.FRAME_ID,
            port: str = BaseIMU.PORT,
            use_enu: bool = BaseIMU.USE_ENU,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        assert imu or model, (
            "IMU object or model must be passed."
        )
        if not imu and model:
            imu = InertialMeasurementUnit(model)
            imu.set_frame_id(frame_id)
            imu.set_port(port)
            imu.set_use_enu(use_enu)
            imu.set_urdf_enabled(urdf_enabled)
            imu.set_launch_enabled(launch_enabled)
            imu.set_parent(parent)
            imu.set_xyz(xyz)
            imu.set_rpy(rpy)
        self._imu.add(imu)

    # IMU: Add Microstrain
    def add_microstrain(
            self,
            # By Object
            imu: Microstrain = None,
            # By Parameters
            frame_id: str = Microstrain.FRAME_ID,
            port: str = Microstrain.PORT,
            use_enu: bool = Microstrain.USE_ENU,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if imu is None:
            imu = Microstrain(
                frame_id=frame_id,
                port=port,
                use_enu=use_enu,
                urdf_enabled=urdf_enabled,
                launch_enabled=launch_enabled,
                parent=parent,
                xyz=xyz,
                rpy=rpy
            )
        assert isinstance(imu, Microstrain), (
            "IMU object must be of type Microstrain"
        )
        self._imu.add(imu)

    # IMU: Remove IMU by passing object or index
    def remove_imu(self, imu: BaseIMU | int) -> None:
        self._imu.remove(imu)

    # IMU: Get Single Object
    def get_imu(self, idx: int) -> BaseIMU:
        return self._imu.get(idx)

    # IMU: Get All Objects
    def get_all_imu(self) -> List[BaseIMU]:
        return self._imu.get_all()

    # IMU: Get All Objects of a Specified Model
    def get_all_imu_by_model(self, model: str) -> List[BaseIMU]:
        InertialMeasurementUnit.assert_model(model)
        all_model_imu = []
        for imu in self.get_all_imu():
            if imu.SENSOR_MODEL == model:
                all_model_imu.append(imu)
        return all_model_imu

    # IMU: Get All Objects of Model Microstrain
    def get_all_microstrain(self) -> List[Microstrain]:
        return self.get_all_imu_by_model(
            InertialMeasurementUnit.MICROSTRAIN_IMU)

    # IMU: Set IMU Object
    def set_imu(self, imu: BaseIMU) -> None:
        self._imu.set(imu)

    # IMU: Set All IMU
    def set_all_imu(self, all_imu: List[BaseIMU]) -> None:
        self._imu.set_all(all_imu)

    # GPS: Add GPS by Object or Common GPS Parameters
    def add_gps(
            self,
            # By Object
            gps:  BaseGPS = None,
            # By Model and Paramters
            model: str = None,
            frame_id: str = BaseGPS.FRAME_ID,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        assert gps or model, (
            "GPS object or model must be passed."
        )
        if not gps and model:
            gps = GlobalPositioningSystem(model)
            gps.set_frame_id(frame_id)
            gps.set_urdf_enabled(urdf_enabled)
            gps.set_launch_enabled(launch_enabled)
            gps.set_parent(parent)
            gps.set_xyz(xyz)
            gps.set_rpy(rpy)
        self._gps.add(gps)

    # GPS: Add SwiftNav Duro
    def add_duro(
            self,
            # By Object
            duro: SwiftNavDuro = None,
            # By Parameters
            frame_id: str = SwiftNavDuro.FRAME_ID,
            ip: str = SwiftNavDuro.IP_ADDRESS,
            port: int = SwiftNavDuro.IP_PORT,
            urdf_enabled: bool = SwiftNavDuro.URDF_ENABLED,
            launch_enabled: bool = SwiftNavDuro.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if duro is None:
            duro = SwiftNavDuro(
                frame_id=frame_id,
                ip=ip,
                port=port,
                urdf_enabled=urdf_enabled,
                launch_enabled=launch_enabled,
                parent=parent,
                xyz=xyz,
                rpy=rpy
            )
        assert isinstance(duro, SwiftNavDuro), (
            "GPS object must be of type UST"
        )
        self._gps.add(duro)

    # GPS: Remove GPS by passing object or index
    def remove_gps(self, gps:  BaseGPS | int) -> None:
        self._gps.remove(gps)

    # GPS: Get Single Object
    def get_gps(self, idx: int) -> BaseGPS:
        return self._gps.get(idx)

    # GPS: Get All Objects
    def get_all_gps(self) -> List[BaseGPS]:
        return self._gps.get_all()

    # GPS: Get All Objects of a Specified Model
    def get_all_gps_by_model(self, model: str) -> List[BaseGPS]:
        GlobalPositioningSystem.assert_model(model)
        all_model_gps = []
        for gps in self.get_all_gps():
            if gps.SENSOR_MODEL == model:
                all_model_gps.append(gps)
        return all_model_gps

    # GPS: Get All Objects of Model UST
    def get_all_duro(self) -> List[SwiftNavDuro]:
        return self.get_all_gps_by_model(
            GlobalPositioningSystem.SWIFTNAV_DURO)

    # GPS: Set GPS Object
    def set_gps(self, gps:  BaseGPS) -> None:
        self._gps.set(gps)

    # GPS: Set All GPS Objects
    def set_all_gps(self, all_gps: List[BaseGPS]) -> None:
        self._gps.set_all(all_gps)
