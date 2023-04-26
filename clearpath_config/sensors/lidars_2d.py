from clearpath_config.common import IP, Port
from clearpath_config.sensors.base import BaseSensor, Accessory, List
from math import pi


class BaseLidar2D(BaseSensor):
    """
    Base 2D Lidar Class
        - contains all common laser scan parameters:
            - frame_id: to publish LaserScan data
            - ip_address: to connect to lidar
            - ip_port: to connect to lidar
            - min_angle: starting angle
            - max_angle: end angle
        - all 2d lidars must be of type BaseLidar2d
    """
    SENSOR_TYPE = "lidar2d"
    SENSOR_MODEL = "base"
    TOPIC = "scan"

    FRAME_ID = "laser"
    IP_ADDRESS = "192.168.131.20"
    IP_PORT = 6000
    MIN_ANGLE = -pi
    MAX_ANGLE = pi

    class ROS_PARAMETER_KEYS:
        FRAME_ID = "frame_id"
        IP_ADDRESS = "ip_address"
        IP_PORT = "ip_port"
        MIN_ANGLE = "min_angle"
        MAX_ANGLE = "max_angle"

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = TOPIC,
            frame_id: str = FRAME_ID,
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
        # Frame ID
        self.frame_id: str = self.FRAME_ID
        self.set_frame_id(frame_id)
        # IP Address
        self.ip: IP = IP(self.IP_ADDRESS)
        self.set_ip(ip)
        # IP Port
        self.port: Port = Port(self.IP_PORT)
        self.set_port(port)
        # Min Angle
        self.min_angle: float = float(self.MIN_ANGLE)
        self.set_min_angle(min_angle)
        # Max Angle
        self.max_angle: float = float(self.MAX_ANGLE)
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
        # ROS Parameter Keys
        pairs = {
            # Frame ID
            self.ROS_PARAMETER_KEYS.FRAME_ID: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.FRAME_ID,
                    get=lambda obj: obj.get_frame_id(),
                    set=lambda obj, val: obj.set_frame_id(val)
                )
            ),
            # IP Address
            self.ROS_PARAMETER_KEYS.IP_ADDRESS: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.IP_ADDRESS,
                    get=lambda obj: obj.get_ip(),
                    set=lambda obj, val: obj.set_ip(val))),
            # IP Port
            self.ROS_PARAMETER_KEYS.IP_PORT: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.IP_PORT,
                    get=lambda obj: obj.get_port(),
                    set=lambda obj, val: obj.set_port(val))),
            # Min. Angle
            self.ROS_PARAMETER_KEYS.MIN_ANGLE: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.MIN_ANGLE,
                    get=lambda obj: obj.get_min_angle(),
                    set=lambda obj, val: obj.set_min_angle(val))),
            # Max. Angle
            self.ROS_PARAMETER_KEYS.MAX_ANGLE: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.MIN_ANGLE,
                    get=lambda obj: obj.get_max_angle(),
                    set=lambda obj, val: obj.set_max_angle(val))),
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
        self.max_angle = angle


class HokuyoUST10(BaseLidar2D):
    SENSOR_MODEL = "hokuyo_ust10"

    FRAME_ID = "laser"
    IP_PORT = 10940
    MIN_ANGLE = -pi
    MAX_ANGLE = pi

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseLidar2D.TOPIC,
            frame_id: str = BaseLidar2D.FRAME_ID,
            ip: str = BaseLidar2D.IP_ADDRESS,
            port: int = IP_PORT,
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
            frame_id,
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
        # ROS Parameter Keys
        self.ros_parameter_pairs[
            BaseLidar2D.ROS_PARAMETER_KEYS.FRAME_ID].key = "laser_frame_id"
        self.ros_parameter_pairs[
            BaseLidar2D.ROS_PARAMETER_KEYS.IP_ADDRESS].key = "ip_address"
        self.ros_parameter_pairs[
            BaseLidar2D.ROS_PARAMETER_KEYS.IP_PORT].key = "ip_port"
        self.ros_parameter_pairs[
            BaseLidar2D.ROS_PARAMETER_KEYS.MIN_ANGLE].key = "angle_min"
        self.ros_parameter_pairs[
            BaseLidar2D.ROS_PARAMETER_KEYS.MAX_ANGLE].key = "angle_max"


class SickLMS1XX(BaseLidar2D):
    SENSOR_MODEL = "sick_lms1xx"

    FRAME_ID = "laser"
    IP_PORT = 2112
    MIN_ANGLE = -2.391
    MAX_ANGLE = 2.391

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseLidar2D.TOPIC,
            frame_id: str = FRAME_ID,
            ip: str = BaseLidar2D.IP_ADDRESS,
            port: int = IP_PORT,
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
            frame_id,
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
        # ROS Parameter Keys
        self.ros_parameter_pairs[
            BaseLidar2D.ROS_PARAMETER_KEYS.FRAME_ID].key = "frame_id"
        self.ros_parameter_pairs[
            BaseLidar2D.ROS_PARAMETER_KEYS.IP_ADDRESS].key = "hostname"
        self.ros_parameter_pairs[
            BaseLidar2D.ROS_PARAMETER_KEYS.IP_PORT].key = "port"
        self.ros_parameter_pairs[
            BaseLidar2D.ROS_PARAMETER_KEYS.MIN_ANGLE].key = "min_ang"
        self.ros_parameter_pairs[
            BaseLidar2D.ROS_PARAMETER_KEYS.MAX_ANGLE].key = "max_ang"
