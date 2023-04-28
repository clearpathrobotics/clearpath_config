from clearpath_config.common import IP, Port
from clearpath_config.sensors.base import BaseSensor, Accessory, List


class BaseLidar3D(BaseSensor):
    """
    Base 3D Lidar Class
        - contains all common 3d lidar parameters:
            - frame_id: to publish PointCloud data
            - ip_address: to connect to lidar
            - ip_port: to connect to lidar
    """
    SENSOR_TYPE = "lidar3d"
    SENSOR_MODEL = "base"
    TOPIC = "points"

    FRAME_ID = "laser"
    IP_ADDRESS = "192.168.131.25"
    IP_PORT = "2368"

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
            BaseLidar3D.ROS_PARAMETER_KEYS.FRAME_ID: (
                BaseSensor.ROSParameter(
                    key=BaseLidar3D.ROS_PARAMETER_KEYS.FRAME_ID,
                    get=lambda obj: obj.get_frame_id(),
                    set=lambda obj, val: obj.set_frame_id(val)
                )
            ),
            # IP Address
            BaseLidar3D.ROS_PARAMETER_KEYS.IP_ADDRESS: (
                BaseSensor.ROSParameter(
                    key=BaseLidar3D.ROS_PARAMETER_KEYS.IP_ADDRESS,
                    get=lambda obj: obj.get_ip(),
                    set=lambda obj, val: obj.set_ip(val))),
            # IP Port
            BaseLidar3D.ROS_PARAMETER_KEYS.IP_PORT: (
                BaseSensor.ROSParameter(
                    key=BaseLidar3D.ROS_PARAMETER_KEYS.IP_PORT,
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


class VelodyneLidar(BaseLidar3D):
    """
    Velodyne Lidar Class
        - extra ros_parameters:
            - device_type: model of the lidar:
                - '64E'
                - '64E_S3'
                - '32E'
                - '32C'
                - 'VLP16'
    """
    SENSOR_MODEL = "velodyne_lidar"

    FRAME_ID = "laser"
    IP_PORT = 2368

    HDL_32E = "32E"
    HDL_64E = "64E"
    HDL_64E_S2 = "64E_S2"
    HDL_64E_S3 = "64E_S3"
    VLP_16 = "VLP16"
    VLP_32C = "32C"
    DEVICE_TYPE = VLP_16
    DEVICE_TYPES = [
        HDL_32E,
        HDL_64E,
        HDL_64E_S2,
        HDL_64E_S3,
        VLP_16,
        VLP_32C
    ]

    class ROS_PARAMETER_KEYS:
        DEVICE_TYPE = "model"
        FIXED_FRAME = "fixed_frame"
        TARGET_FRAME = "target_frame"

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseLidar3D.TOPIC,
            frame_id: str = FRAME_ID,
            ip: str = BaseLidar3D.IP_ADDRESS,
            port: int = IP_PORT,
            device_type: str = DEVICE_TYPE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # Device Type:
        self.device_type: str = self.DEVICE_TYPE
        self.set_device_type(device_type)
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
            BaseLidar3D.ROS_PARAMETER_KEYS.FRAME_ID].key = "frame_id"
        self.ros_parameter_pairs[
            BaseLidar3D.ROS_PARAMETER_KEYS.IP_ADDRESS].key = "device_ip"
        self.ros_parameter_pairs[
            BaseLidar3D.ROS_PARAMETER_KEYS.IP_PORT].key = "port"
        pairs = {
            # Device Type
            self.ROS_PARAMETER_KEYS.DEVICE_TYPE: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.DEVICE_TYPE,
                    get=lambda obj: obj.get_device_type(),
                    set=lambda obj, val: obj.set_device_type(val)
                )
            ),
            # Fixed Frame
            self.ROS_PARAMETER_KEYS.FIXED_FRAME: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.FIXED_FRAME,
                    get=lambda obj: obj.get_frame_id(),
                    set=lambda obj, val: obj.set_frame_id(val),
                )
            ),
            # Target Frame
            self.ROS_PARAMETER_KEYS.TARGET_FRAME: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.TARGET_FRAME,
                    get=lambda obj: obj.get_frame_id(),
                    set=lambda obj, val: obj.set_frame_id(val),
                )
            ),
        }
        self.ros_parameter_pairs.update(pairs)
        self.set_ros_parameters(ros_parameters)

    def get_device_type(self) -> str:
        return self.device_type

    def set_device_type(self, device_type: str) -> None:
        assert device_type in self.DEVICE_TYPES, (
            "Device type '%s' is not one of '%s'" % (
                device_type,
                self.DEVICE_TYPES
            )
        )
        self.device_type = device_type
