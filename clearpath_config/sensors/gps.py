from clearpath_config.common import Accessory, IP, Port
from clearpath_config.sensors.base import BaseSensor
from typing import List


class BaseGPS(BaseSensor):
    """
    Base GPS Class
        - contains all common gps parameters:
            - frame_id: to publish Fix
            - ip_address: to connect to GPS
            - ip_port: to connect to GPS
    """
    SENSOR_TYPE = "gps"
    SENSOR_MODEL = "base"
    TOPIC = "fix"

    FRAME_ID = "link"
    IP_ADDRESS = "192.168.131.30"
    IP_PORT = 55555

    class ROS_PARAMETER_KEYS:
        FRAME_ID = "frame_id"
        IP_ADDRESS = "ip_address"
        IP_PORT = "ip_port"

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
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # Frame ID
        self.frame_id: str = self.FRAME_ID
        self.set_frame_id(frame_id)
        # IP Address
        self.ip: IP = IP(self.IP_ADDRESS)
        self.set_ip(ip)
        # IP Port
        self.port: Port = Port(self.IP_PORT)
        self.set_port(port)
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
            BaseGPS.ROS_PARAMETER_KEYS.FRAME_ID: (
                BaseSensor.ROSParameter(
                    key=BaseGPS.ROS_PARAMETER_KEYS.FRAME_ID,
                    get=lambda obj: obj.get_frame_id(),
                    set=lambda obj, val: obj.set_frame_id(val)
                )
            ),
            # IP Address
            BaseGPS.ROS_PARAMETER_KEYS.IP_ADDRESS: (
                BaseSensor.ROSParameter(
                    key=BaseGPS.ROS_PARAMETER_KEYS.IP_ADDRESS,
                    get=lambda obj: obj.get_ip(),
                    set=lambda obj, val: obj.set_ip(val))),
            # IP Port
            BaseGPS.ROS_PARAMETER_KEYS.IP_PORT: (
                BaseSensor.ROSParameter(
                    key=BaseGPS.ROS_PARAMETER_KEYS.IP_PORT,
                    get=lambda obj: obj.get_port(),
                    set=lambda obj, val: obj.set_port(val))),
        }
        self.ros_parameter_pairs.update(pairs)
        self.set_ros_parameters(ros_parameters)

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
        # Set IP
        self.set_ip(self.get_ip_from_idx(idx))

    def get_frame_id(self) -> str:
        return self.frame_id

    def set_frame_id(self, link: str) -> None:
        Accessory.assert_valid_link(link)
        self.frame_id = link

    def get_ip(self) -> str:
        return str(self.ip)

    def set_ip(self, ip: str) -> None:
        self.ip = IP(ip)

    def get_port(self) -> int:
        return int(self.port)

    def set_port(self, port: int) -> None:
        self.port = Port(port)


class SwiftNavDuro(BaseGPS):
    """
    Swift Navigation Duro Class:
        - extra ros_parameters:
            - gps_receiver_frame: same as frame_id
            - imu_frame: same as frame_id
    """
    SENSOR_MODEL = "swiftnav_duro"

    FRAME_ID = "link"
    IP_PORT = 55555

    class ROS_PARAMETER_KEYS:
        GPS_FRAME = "gps_receiver_frame_id"
        IMU_FRAME = "imu_frame_id"

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseGPS.TOPIC,
            frame_id: str = FRAME_ID,
            ip: str = BaseGPS.IP_ADDRESS,
            port: int = IP_PORT,
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
            ip,
            port,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )
        # ROS Parameter Keys
        self.ros_parameter_pairs[
            BaseGPS.ROS_PARAMETER_KEYS.FRAME_ID].key = (
                SwiftNavDuro.ROS_PARAMETER_KEYS.GPS_FRAME
            )
        pairs = {
            # Frame ID
            SwiftNavDuro.ROS_PARAMETER_KEYS.IMU_FRAME: (
                BaseSensor.ROSParameter(
                    key=SwiftNavDuro.ROS_PARAMETER_KEYS.IMU_FRAME,
                    get=lambda obj: obj.get_frame_id(),
                    set=lambda obj, val: obj.set_frame_id(val)
                )
            ),
        }
        self.ros_parameter_pairs.update(pairs)
        self.set_ros_parameters(ros_parameters)
