from clearpath_config.common import Accessory, OrderedListConfig
from clearpath_config.sensors.base import BaseSensor
from clearpath_config.sensors.cameras import (
    BaseCamera,
    FlirBlackfly,
    IntelRealsense,
)
from clearpath_config.sensors.lidars_2d import (
    BaseLidar2D,
    HokuyoUST10,
    SickLMS1XX,
)
from typing import List


class Camera():
    FLIR_BLACKFLY = FlirBlackfly.SENSOR_MODEL
    INTEL_REALSENSE = IntelRealsense.SENSOR_MODEL

    MODEL = {
        FLIR_BLACKFLY: FlirBlackfly,
        INTEL_REALSENSE: IntelRealsense
    }

    @classmethod
    def assert_model(cls, model: str) -> None:
        assert model in Camera.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                Camera.MODEL.keys()
            )
        )

    def __new__(cls, model: str) -> BaseCamera:
        cls.assert_model(model)
        return Camera.MODEL[model]()


class Lidar2D():
    HOKUYO_UST10 = HokuyoUST10.SENSOR_MODEL
    SICK_LMS1XX = SickLMS1XX.SENSOR_MODEL

    MODEL = {
        HOKUYO_UST10: HokuyoUST10,
        SICK_LMS1XX: SickLMS1XX
    }

    @classmethod
    def assert_model(cls, model: str) -> None:
        assert model in Lidar2D.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                Lidar2D.MODEL.keys()
            )
        )

    def __new__(cls, model: str) -> BaseLidar2D:
        cls.assert_model(model)
        return Lidar2D.MODEL[model]()


class Sensor():
    CAMERA = BaseCamera.SENSOR_TYPE
    LIDAR2D = BaseLidar2D.SENSOR_TYPE

    TYPE = {
        CAMERA: Camera,
        LIDAR2D: Lidar2D
    }

    @classmethod
    def assert_type(cls, _type: str) -> None:
        assert _type in Sensor.TYPE, (
            "Sensor type '%s' must be one of: '%s'" % (
                _type,
                Sensor.TYPE.keys()
            )
        )

    def __new__(cls, _type: str, _model: str) -> BaseLidar2D:
        cls.assert_sensor_type(_type)
        return Sensor.TYPE[_type](_model)


# Sensor Config
class SensorConfig:
    LIDAR2D_INDEX = 0
    CAMERA_INDEX = 0

    def __init__(self) -> None:
        # 2D Lidars
        self.__lidars_2d = OrderedListConfig[BaseLidar2D](
            SensorConfig.LIDAR2D_INDEX
        )
        # Cameras
        self.__cameras = OrderedListConfig[BaseCamera](
            SensorConfig.CAMERA_INDEX
        )

    # Get All Sensors
    def get_all_sensors(self) -> List[BaseSensor]:
        sensors = []
        # Lidar2D
        sensors.extend(self.get_all_lidar_2d())
        # Cameras
        sensors.extend(self.get_all_cameras())
        return sensors

    # Lidar2D: Add Lidar2D by Object or Common Lidar2D Parameters
    def add_lidar2d(
            self,
            # By Object
            lidar2d: BaseLidar2D = None,
            # By Model and Paramters
            model: str = None,
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
            lidar2d.set_ip(ip)
            lidar2d.set_port(port)
            lidar2d.set_min_angle(min_angle)
            lidar2d.set_max_angle(max_angle)
            lidar2d.set_urdf_enabled(urdf_enabled)
            lidar2d.set_launch_enabled(launch_enabled)
            lidar2d.set_parent(parent)
            lidar2d.set_xyz(xyz)
            lidar2d.set_rpy(rpy)
        self.__lidars_2d.add(lidar2d)

    # Lidar2D: Add UST10
    def add_ust10(
            self,
            # By Object
            ust10: HokuyoUST10 = None,
            # By Parameters
            ip: str = BaseLidar2D.IP_ADDRESS,
            port: int = BaseLidar2D.IP_PORT,
            min_angle: float = HokuyoUST10.MIN_ANGLE,
            max_angle: float = HokuyoUST10.MAX_ANGLE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if ust10 is None:
            ust10 = HokuyoUST10(
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
        assert isinstance(ust10, HokuyoUST10), (
            "Lidar2D object must be of type UST10"
        )
        self.__lidars_2d.add(ust10)

    # Lidar2D: Add LMS1xx
    def add_lms1xx(
            self,
            # By Object
            lms1xx: SickLMS1XX = None,
            # By Parameters
            ip: str = BaseLidar2D.IP_ADDRESS,
            port: int = BaseLidar2D.IP_PORT,
            min_angle: float = SickLMS1XX.MIN_ANGLE,
            max_angle: float = SickLMS1XX.MAX_ANGLE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if lms1xx is None:
            lms1xx = SickLMS1XX(
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
        self.__lidars_2d.add(lms1xx)

    # Lidar2D: Remove Lidar2D by passing object or index
    def remove_lidar_2d(self, lidar_2d: BaseLidar2D | int) -> None:
        self.__lidars_2d.remove(lidar_2d)

    # Lidar2D: Get Single Object
    def get_lidar_2d(self, idx: int) -> BaseLidar2D:
        return self.__lidars_2d.get(idx)

    # Lidar2D: Get All Objects
    def get_all_lidar_2d(self) -> List[BaseLidar2D]:
        return self.__lidars_2d.get_all()

    # Lidar2D: Get All Objects of a Specified Model
    def get_all_lidar_2d_by_model(self, model: str) -> List[BaseLidar2D]:
        Lidar2D.assert_model(model)
        all_model_lidar_2d = []
        for lidar_2d in self.get_all_lidar_2d():
            if lidar_2d.SENSOR_MODEL == model:
                all_model_lidar_2d.append(lidar_2d)
        return all_model_lidar_2d

    # Lidar2D: Get All Objects of Model UST10
    def get_all_ust10(self) -> List[HokuyoUST10]:
        return self.get_all_lidar_2d_by_model(Lidar2D.UST10)

    # Lidar2D: Get All Objects of Model LMS1XX
    def get_all_lms1xx(self) -> List[SickLMS1XX]:
        return self.get_all_lidar_2d_by_model(Lidar2D.LMS1XX)

    # Lidar2D: Set Lidar2D Object
    def set_lidar_2d(self, lidar_2d: BaseLidar2D) -> None:
        self.__lidars_2d.set(lidar_2d)

    # Lidar2D: Set All Lidar2D Objects
    def set_all_lidar_2d(self, all_lidar_2d: List[BaseLidar2D]) -> None:
        self.__lidars_2d.set_all(all_lidar_2d)

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
            camera.set_parent(parent)
            camera.set_xyz(xyz)
            camera.set_rpy(rpy)
        self.__cameras.add(camera)

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
        self.__cameras.add(blackfly)

    # Camera: Add Realsense
    def add_realsense(
            self,
            # By Object
            realsense: IntelRealsense = None,
            # By Parameters
            fps: int = IntelRealsense.FPS,
            serial: str = BaseCamera.SERIAL,
            width: int = IntelRealsense.WIDTH,
            height: int = IntelRealsense.HEIGHT,
            depth_enabled: bool = IntelRealsense.DEPTH_ENABLED,
            depth_fps: int = IntelRealsense.DEPTH_FPS,
            depth_width: int = IntelRealsense.DEPTH_WIDTH,
            depth_height: int = IntelRealsense.DEPTH_HEIGHT,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if realsense is None:
            realsense = IntelRealsense(
                fps=fps,
                serial=serial,
                width=width,
                height=height,
                depth_enabled=depth_enabled,
                depth_fps=depth_fps,
                depth_width=depth_width,
                depth_height=depth_height,
                urdf_enabled=urdf_enabled,
                launch_enabled=launch_enabled,
                parent=parent,
                xyz=xyz,
                rpy=rpy,
            )
        assert isinstance(realsense, IntelRealsense), (
            "Realsense object must be of type Realsense"
        )
        self.__cameras.add(realsense)

    # Camera: Remove
    def remove_camera(self, camera: BaseCamera | int) -> None:
        self.__cameras.remove(camera)

    # Camera: Get
    def get_camera(self, idx: int) -> BaseCamera:
        return self.__cameras.get(idx)

    # Camera: Get All
    def get_all_cameras(self) -> List[BaseCamera]:
        return self.__cameras.get_all()

    # Camera: Set
    def set_camera(self, camera: BaseCamera) -> None:
        self.__cameras.set(camera)

    # Camera: Set All
    def set_all_camera(self, cameras: List[BaseCamera]) -> None:
        self.__cameras.set_all(cameras)
