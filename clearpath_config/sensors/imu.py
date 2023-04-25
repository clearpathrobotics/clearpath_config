from clearpath_config.sensors.base import BaseSensor, Accessory, List


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
    FRAME_ID = "imu_link"
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
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )
