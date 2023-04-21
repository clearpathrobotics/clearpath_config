from clearpath_config.common import IP, Port
from clearpath_config.sensors.base import BaseSensor, Accessory, List
from math import pi


class BaseLidar2D(BaseSensor):
    """
    Base 2D Lidar Class
        - contains all common laser scan parameters
        - all 2d lidars must be of type Camera.Lidar2D
    """
    SENSOR_TYPE = "lidar2d"
    SENSOR_MODEL = "base"
    TOPIC = "scan"

    IP_ADDRESS = "192.168.131.20"
    IP_PORT = 6000
    MIN_ANGLE = -pi
    MAX_ANGLE = pi

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = TOPIC,
            ip: str = IP_ADDRESS,
            port: int = IP_PORT,
            min_angle: float = MIN_ANGLE,
            max_angle: float = MAX_ANGLE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ) -> None:
        # IP Address
        self.ip = IP(self.IP_ADDRESS)
        self.set_ip(ip)
        # IP Port
        self.port = Port(self.IP_PORT)
        self.set_port(port)
        # Min Angle
        self.min_angle = float(self.MIN_ANGLE)
        self.set_min_angle(min_angle)
        # Max Angle
        self.max_angle = float(self.MAX_ANGLE)
        self.set_max_angle(max_angle)
        # Initialize Base
        super().__init__(
            idx,
            name,
            topic,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy,
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
        # Set IP
        self.set_ip(self.get_ip_from_idx(idx))

    def get_ip(self) -> str:
        return str(self.ip)

    def set_ip(self, ip: str) -> None:
        self.ip = IP(ip)

    def get_port(self) -> int:
        return int(self.port)

    def set_port(self, port: int) -> None:
        self.port = Port(port)

    def get_min_angle(self) -> float:
        return self.min_angle

    def set_min_angle(self, angle: float) -> None:
        if angle < self.MIN_ANGLE:
            angle = self.MIN_ANGLE
        self.min_angle = angle

    def get_max_angle(self) -> float:
        return self.max_angle

    def set_max_angle(self, angle: float) -> None:
        if angle > self.MAX_ANGLE:
            angle = self.MAX_ANGLE
        self.min_angle = angle


class HokuyoUST10(BaseLidar2D):
    SENSOR_MODEL = "hokuyo_ust10"

    MIN_ANGLE = -pi
    MAX_ANGLE = pi

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseLidar2D.TOPIC,
            ip: str = BaseLidar2D.IP_ADDRESS,
            port: int = BaseLidar2D.IP_PORT,
            min_angle: float = MIN_ANGLE,
            max_angle: float = MAX_ANGLE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(
            idx,
            name,
            topic,
            ip,
            port,
            min_angle,
            max_angle,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )


class SickLMS1XX(BaseLidar2D):
    SENSOR_MODEL = "sick_lms1xx"

    MIN_ANGLE = -2.391
    MAX_ANGLE = 2.391

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseLidar2D.TOPIC,
            ip: str = BaseLidar2D.IP_ADDRESS,
            port: int = BaseLidar2D.IP_PORT,
            min_angle: float = MIN_ANGLE,
            max_angle: float = MAX_ANGLE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(
            idx,
            name,
            topic,
            ip,
            port,
            min_angle,
            max_angle,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )
