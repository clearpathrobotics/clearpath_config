from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.file import File
from clearpath_config.sensors.types.sensor import BaseSensor
from typing import List


class BaseIMU(BaseSensor):
    """
    Common IMU Class.
      - contains all common imu parameters:
        - port: device file path
        - frame_id: to publish IMU data
        - use_enu: transform data to ENU frame
      - all IMUs must be of type BaseIMU
    """
    SENSOR_TYPE = "imu"
    SENSOR_MODEL = "base"
    TOPIC = "imu"

    PORT = "/dev/clearpath/imu"
    FRAME_ID = "link"
    USE_ENU = True

    class ROS_PARAMETERS_KEYS:
        PORT = "port"
        FRAME_ID = "frame_id"
        USE_ENU = "use_enu"

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
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
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
            self.ROS_PARAMETERS_KEYS.FRAME_ID: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETERS_KEYS.FRAME_ID,
                    get=lambda obj: obj.get_frame_id(),
                    set=lambda obj, val: obj.set_frame_id(val)
                )
            ),
            # Port
            self.ROS_PARAMETERS_KEYS.PORT: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETERS_KEYS.PORT,
                    get=lambda obj: obj.get_port(),
                    set=lambda obj, val: obj.set_port(val)
                )
            ),
            # Use ENU
            self.ROS_PARAMETERS_KEYS.USE_ENU: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETERS_KEYS.USE_ENU,
                    get=lambda obj: obj.get_use_enu(),
                    set=lambda obj, val: obj.set_use_enu(val)
                )
            )
        }
        self.ros_parameter_pairs.update(pairs)
        self.set_ros_parameters(ros_parameters)

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

    def get_frame_id(self) -> str:
        return self.frame_id

    def set_frame_id(self, link: str) -> None:
        Accessory.assert_valid_link(link)
        self.frame_id = link

    def get_port(self) -> str:
        return str(self.port)

    def set_port(self, file: str) -> None:
        self.port = File(file)

    def get_use_enu(self) -> bool:
        return self.use_enu

    def set_use_enu(self, enu: bool) -> None:
        self.use_enu = bool(enu)


class Microstrain(BaseIMU):
    SENSOR_MODEL = "microstrain_imu"

    PORT = "/dev/microstrain_main"
    FRAME_ID = "link"
    USE_ENU = True

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
            parent,
            xyz,
            rpy
        )
        # ROS Parameter Keys
        self.ros_parameter_pairs[
            BaseIMU.ROS_PARAMETERS_KEYS.FRAME_ID].key = "imu_frame_id"
        self.ros_parameter_pairs[
            BaseIMU.ROS_PARAMETERS_KEYS.PORT].key = "port"
        self.ros_parameter_pairs[
            BaseIMU.ROS_PARAMETERS_KEYS.USE_ENU].key = "use_enu_frame"
