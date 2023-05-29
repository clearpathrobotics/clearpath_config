from clearpath_config.common import (
    Platform,
    Accessory,
    flatten_dict
)
from clearpath_config.clearpath_config import ClearpathConfig
from clearpath_config.mounts.mounts import (
    MountsConfig,
    Mount,
    BaseMount,
    FlirPTU,
    FathPivot
)
from clearpath_config.platform.base import (
    BaseDecorationsConfig,
    BaseDecoration
)
from clearpath_config.platform.decorations import (
    Decoration,
    Bumper,
    TopPlate,
    Structure
)
from clearpath_config.accessories.accessories import (
    AccessoryConfig,
    URDFAccessory,
    BaseAccessory,
    Link,
    Box,
    Cylinder,
    Sphere,
    Mesh
)
from clearpath_config.mounts.pacs import PACS
from clearpath_config.platform.platform import PlatformConfig
from clearpath_config.platform.a200 import A200DecorationsConfig
from clearpath_config.platform.j100 import J100DecorationsConfig
from clearpath_config.sensors.sensors import (
    Sensor,
    BaseSensor,
    SensorConfig,
    # Cameras
    Camera,
    BaseCamera,
    FlirBlackfly,
    IntelRealsense,
    # Lidar2D
    Lidar2D,
    BaseLidar2D,
    # Lidar3D
    Lidar3D,
    BaseLidar3D,
    # IMU
    InertialMeasurementUnit,
    BaseIMU,
    # GPS
    GlobalPositioningSystem,
    BaseGPS,
)
from clearpath_config.system.system import (
    SystemConfig,
    HostsConfig,
    Host,
    RMWImplementation
)
from typing import List
import os
import yaml


class BaseConfigParser:
    @staticmethod
    def is_nested_key(key: str) -> bool:
        return "." in key

    @staticmethod
    def get_nested_keys(key: str) -> list:
        return key.split(".")

    @staticmethod
    def check_key_exists(key: str, config: dict) -> bool:
        if BaseConfigParser.is_nested_key(key):
            keys = BaseConfigParser.get_nested_keys(key)
            key = keys.pop(0)
            if key in config:
                return False
            else:
                return BaseConfigParser.check_key_exists(
                    ".".join(keys), config
                )
        else:
            return key in config

    @staticmethod
    def assert_key_exists(key: str, config: dict) -> None:
        assert BaseConfigParser.check_key_exists(
            key, config
        ), "Key '%s' must be in YAML" % key

    @staticmethod
    def get_required_val(key: str, config: dict):
        BaseConfigParser.assert_key_exists(key, config)
        if BaseConfigParser.is_nested_key(key):
            keys = BaseConfigParser.get_nested_keys(key)
            key = keys.pop(0)
            return BaseConfigParser.get_required_val(
                key=".".join(keys),
                config=config[key]
            )
        return config[key]

    @staticmethod
    def get_optional_val(key: str, config: dict, default=None):
        if BaseConfigParser.check_key_exists(key, config):
            if BaseConfigParser.is_nested_key(key):
                keys = BaseConfigParser.get_nested_keys(key)
                key = keys.pop(0)
                return BaseConfigParser.get_optional_val(
                    key=".".join(keys),
                    config=config[key],
                    default=default
                )
            else:
                return config[key]
        else:
            return default


class HostsConfigParser(BaseConfigParser):
    # Key
    HOSTS = "hosts"
    # Host Keys
    PLATFORM = "platform"
    ONBOARD = "onboard"
    REMOTE = "remote"

    def __new__(cls, config: dict) -> HostsConfig:
        htsconfig = HostsConfig()
        # Hosts
        hosts = cls.get_required_val(cls.HOSTS, config)
        # Hosts.Platform
        platform = cls.get_platform_host(config=hosts)
        htsconfig.set_platform(platform)
        # Hosts.Onboard
        htsconfig.set_onboard(cls.get_hostlists(cls.ONBOARD, hosts))
        # Hosts.Remote
        htsconfig.set_remote(cls.get_hostlists(cls.REMOTE, hosts))
        return htsconfig

    @classmethod
    def get_platform_host(cls, config) -> Host:
        platform = cls.get_required_val(cls.PLATFORM, config)
        assert isinstance(platform, dict), "Platform host must be a dictionary"
        entries = list(platform.items())
        assert (
            len(entries) == 1
        ), "Platform must have exactly one ('hostname': 'ip') entry"
        hostname, ip = entries[0]
        return Host(hostname, ip)

    @classmethod
    def get_hostlists(cls, key, config) -> List[Host]:
        hostlist = cls.get_optional_val(key, config)
        if not hostlist:
            return []
        assert isinstance(hostlist, dict), (
            "%s host list must be a dictionary" % key.title()
        )
        hosts = []
        for hostname, value in hostlist.items():
            hosts.append(Host(hostname, value))
        return hosts


class SystemConfigParser(BaseConfigParser):
    # Key
    SYSTEM = "system"
    ROS2 = "ros2"
    # System Keys
    SELF = "self"
    HOSTS = "hosts"
    USERNAME = "username"
    NAMESPACE = "namespace"
    DOMAIN_ID = "domain_id"
    RMW = "rmw_implementation"
    WORKSPACES = "workspaces"

    def __new__(cls, config: dict) -> SystemConfig:
        sysconfig = SystemConfig()
        # System
        system = cls.get_required_val(cls.SYSTEM, config)
        ros2 = cls.get_required_val(cls.ROS2, system)
        # System.Self
        sysconfig.set_self(cls.get_required_val(cls.SELF, system))
        # System.Username
        sysconfig.set_username(cls.get_required_val(cls.USERNAME, ros2))
        # System.Namespace
        sysconfig.set_namespace(
            cls.get_optional_val(
                cls.NAMESPACE,
                ros2,
                "/"
            )
        )
        # System.DomainID
        sysconfig.set_domain_id(
            cls.get_optional_val(
                cls.DOMAIN_ID,
                ros2,
                0
            )
        )
        # System.RMW
        sysconfig.set_rmw_implementation(
            cls.get_optional_val(
                cls.RMW,
                ros2,
                RMWImplementation.FAST_RTPS
            )
        )
        # System.Workspaces
        sysconfig.set_workspaces(
            cls.get_optional_val(
                cls.WORKSPACES,
                ros2,
                []
            )
        )
        # System.Hosts
        sysconfig.set_hosts(HostsConfigParser(system))
        return sysconfig


class DecorationConfigParser(BaseConfigParser):
    # Keys
    ENABLED = "enabled"
    MODEL = "model"
    PARENT = "parent"
    XYZ = "xyz"
    RPY = "rpy"
    # Bumper
    EXTENSION = "extension"

    def __new__(cls, key: str, model: str, config: dict) -> BaseDecoration:
        dcrconfig = Decoration(model)
        dcrtype = Decoration.MODEL[model]
        # Decoration Name
        dcrconfig.set_name(key)
        # Get Keys
        decoration = cls.get_optional_val(key, config)
        if not decoration:
            return decoration
        # Base.Enable
        dcrconfig.set_enabled(
            cls.get_optional_val(cls.ENABLED, decoration, dcrtype.ENABLED)
        )
        # Base.Model
        dcrconfig.set_model(
            cls.get_optional_val(cls.MODEL, decoration, dcrtype.DEFAULT)
        )
        # Base.Parent
        dcrconfig.set_parent(
            cls.get_optional_val(cls.PARENT, decoration, dcrtype.PARENT)
        )
        # Base.XYZ
        dcrconfig.set_xyz(
            cls.get_optional_val(cls.XYZ, decoration, dcrtype.XYZ)
        )
        # Base.RPY
        dcrconfig.set_rpy(
            cls.get_optional_val(cls.RPY, decoration, dcrtype.RPY)
        )
        # Bumper.EXTENSION
        if model == Decoration.BUMPER:
            dcrconfig.set_extension(
                cls.get_optional_val(
                    cls.EXTENSION, decoration, dcrtype.EXTENSION
                )
            )
        return dcrconfig


class DecorationsConfigParser(BaseConfigParser):
    # Key
    DECORATIONS = "decorations"

    class A200:
        # A200 Husky Decoration Keys
        FRONT_BUMPER = "front_bumper"
        REAR_BUMPER = "rear_bumper"
        TOP_PLATE = "top_plate"
        STRUCTURE = "structure"
        PACS = "pacs"

        def __new__(cls, config: dict) -> A200DecorationsConfig:
            dcnconfig = A200DecorationsConfig()
            dcnparser = DecorationsConfigParser
            # Decorations
            decorations = (
                dcnparser.get_optional_val(dcnparser.DECORATIONS, config))
            if decorations is None:
                return dcnconfig
            # Decorations.Front_Bumper
            dcnconfig.set_bumper(
                DecorationConfigParser(
                    key=cls.FRONT_BUMPER,
                    model=Decoration.BUMPER,
                    config=decorations
                )
            )
            # Decorations.Rear_Bumper
            dcnconfig.set_bumper(
                DecorationConfigParser(
                    key=cls.REAR_BUMPER,
                    model=Decoration.BUMPER,
                    config=decorations
                )
            )
            # Decorations.Top_Plate
            dcnconfig.set_top_plate(
                DecorationConfigParser(
                    key=cls.TOP_PLATE,
                    model=Decoration.TOP_PLATE,
                    config=decorations,
                )
            )
            # Decorations.SensorArch
            dcnconfig.set_structure(
                DecorationConfigParser(
                    key=cls.STRUCTURE,
                    model=Decoration.STRUCTURE,
                    config=decorations
                )
            )
            return dcnconfig

    class J100:
        # J100 Jackal Decoration Keys
        FRONT_BUMPER = "front_bumper"
        REAR_BUMPER = "rear_bumper"

        def __new__(cls, config: dict) -> J100DecorationsConfig:
            dcnconfig = J100DecorationsConfig()
            dcnparser = DecorationsConfigParser
            # Decorations
            decorations = (
                dcnparser.get_optional_val(dcnparser.DECORATIONS, config))
            if decorations is None:
                return dcnconfig
            # Decorations.Front_Bumper
            dcnconfig.set_bumper(
                DecorationConfigParser(
                    key=cls.FRONT_BUMPER,
                    model=Decoration.BUMPER,
                    config=decorations
                )
            )
            # Decorations.Rear_Bumper
            dcnconfig.set_bumper(
                DecorationConfigParser(
                    key=cls.REAR_BUMPER,
                    model=Decoration.BUMPER,
                    config=decorations
                )
            )
            return dcnconfig

    MODEL_CONFIGS = {Platform.A200: A200, Platform.J100: J100}

    def __new__(cls, model: str, config: dict) -> BaseDecorationsConfig:
        assert model in Platform.ALL, "Model '%s' must be one of %s" % (
            model,
            Platform.ALL,
        )
        return DecorationsConfigParser.MODEL_CONFIGS[model](config)


class PlatformConfigParser(BaseConfigParser):
    # Key
    PLATFORM = "platform"
    # Platform Keys
    SERIAL_NUMBER = "serial_number"
    CONTROLLER = "controller"
    DECORATIONS = "decorations"
    EXTRAS = "extras"
    # Platform Extras KEys
    URDF = "urdf"
    CONTROL = "control"

    def __new__(cls, config: dict) -> PlatformConfig:
        pfmconfig = PlatformConfig()
        # Platform
        platform = cls.get_required_val(cls.PLATFORM, config)
        # Platform.SerialNumber
        pfmconfig.set_serial_number(
            cls.get_required_val(cls.SERIAL_NUMBER, platform))
        # Platform.Controller
        pfmconfig.set_controller(
            cls.get_optional_val(
                cls.CONTROLLER,
                platform,
                PlatformConfig.CONTROLLER))
        # Platform.Decorations
        pfmconfig.decorations = (
            DecorationsConfigParser(pfmconfig.get_model(), platform))
        # Platform.Extras
        extras = cls.get_optional_val(cls.EXTRAS, platform)
        if extras:
            pfmconfig.extras.set_urdf_extras(
                cls.get_optional_val(cls.URDF, extras, ""))
            pfmconfig.extras.set_control_extras(
                cls.get_optional_val(cls.CONTROL, extras, ""))
        return pfmconfig


class AccessoryParser(BaseConfigParser):
    # Keys
    NAME = "name"
    PARENT = "parent"
    XYZ = "xyz"
    RPY = "rpy"

    def __new__(cls, config: dict) -> Accessory:
        name = cls.get_required_val(
            AccessoryParser.NAME, config)
        parent = cls.get_optional_val(
            AccessoryParser.PARENT, config, Accessory.PARENT)
        xyz = cls.get_optional_val(
            AccessoryParser.XYZ, config, Accessory.XYZ)
        rpy = cls.get_optional_val(
            AccessoryParser.RPY, config, Accessory.RPY)
        return Accessory(name, parent, xyz, rpy)


class URDFAccessoryParser(BaseConfigParser):
    # Keys
    OFFSET_XYZ = "offset_xyz"
    OFFSET_RPY = "offset_rpy"
    SIZE = "size"
    RADIUS = "radius"
    LENGTH = "length"
    VISUAL = "visual"

    def __new__(cls, model: str, config: dict) -> BaseAccessory:
        acc = AccessoryParser(config)
        urdf = URDFAccessory(model, acc.get_name())
        # Set Common Parameters
        urdf.set_parent(acc.get_parent())
        urdf.set_xyz(acc.get_xyz())
        urdf.set_rpy(acc.get_rpy())
        # Set Individual Parameters
        if model == URDFAccessory.LINK:
            pass
        elif model == URDFAccessory.BOX:
            urdf.set_size(
                cls.get_optional_val(
                    URDFAccessoryParser.SIZE,
                    config,
                    Box.SIZE
                ))
        elif model == URDFAccessory.CYLINDER:
            urdf.set_radius(
                cls.get_optional_val(
                    URDFAccessoryParser.RADIUS,
                    config,
                    Cylinder.RADIUS
                ))
            urdf.set_length(
                cls.get_optional_val(
                    URDFAccessoryParser.LENGTH,
                    config,
                    Cylinder.LENGTH
                ))
        elif model == URDFAccessory.SPHERE:
            urdf.set_radius(
                cls.get_optional_val(
                    URDFAccessoryParser.RADIUS,
                    config,
                    Sphere.RADIUS
                ))
        elif model == URDFAccessory.MESH:
            urdf.set_visual(
                cls.get_optional_val(
                    URDFAccessoryParser.VISUAL,
                    config,
                    Mesh.VISUAL
                ))
        return urdf


class AccessoryConfigParser(BaseConfigParser):
    # Key
    ACCESSORIES = "accessories"
    ACCESSORIES_CONFIG = {}

    def __new__(cls, config: dict) -> AccessoryConfig:
        accconfig = AccessoryConfig()
        # Accessories
        accessories = cls.get_optional_val(cls.ACCESSORIES, config)
        if accessories is None:
            return accconfig
        accconfig.set_all_links(
            cls.get_accessories(accessories, URDFAccessory.LINK))
        accconfig.set_all_boxes(
            cls.get_accessories(accessories, URDFAccessory.BOX))
        accconfig.set_all_cylinders(
            cls.get_accessories(accessories, URDFAccessory.CYLINDER))
        accconfig.set_all_spheres(
            cls.get_accessories(accessories, URDFAccessory.SPHERE))
        accconfig.set_all_meshes(
            cls.get_accessories(accessories, URDFAccessory.MESH))
        return accconfig

    @classmethod
    def get_accessories(cls, config: dict, model: str) -> List[BaseAccessory]:
        # Assert Dictionary
        assert isinstance(config, dict), (
            "Accessories must be a dictionary"
        )
        entries = cls.get_optional_val(model, config, [])
        assert isinstance(entries, list), (
            "Model entries must be in a list"
        )
        models = []
        for entry in entries:
            models.append(URDFAccessoryParser(model, entry))
        return models


class MountParser(BaseConfigParser):

    class Base(BaseConfigParser):
        # Keys
        MODEL = "model"

        def __new__(cls, config: dict) -> BaseMount:
            parent = cls.get_optional_val(
                AccessoryParser.PARENT, config, Accessory.PARENT)
            xyz = cls.get_optional_val(
                AccessoryParser.XYZ, config, Accessory.XYZ)
            rpy = cls.get_optional_val(
                AccessoryParser.RPY, config, Accessory.RPY)
            return BaseMount(
                parent=parent,
                xyz=xyz,
                rpy=rpy,
                )

    class FathPivot(BaseConfigParser):
        # Keys
        ANGLE = "angle"

        def __new__(cls, config: dict) -> FathPivot:
            b = MountParser.Base(config)
            # Pivot Angle
            angle = cls.get_optional_val(
                MountParser.FathPivot.ANGLE,
                config,
                FathPivot.ANGLE,
            )
            return FathPivot(
                parent=b.get_parent(),
                xyz=b.get_xyz(),
                rpy=b.get_rpy(),
                angle=angle,
            )

    class FlirPTU(BaseConfigParser):
        # Keys
        TTY_PORT = "tty_port"
        TCP_PORT = "tcp_port"
        IP_ADDRESS = "ip"
        CONNECTION_TYPE = "connection_type"
        LIMITS_ENABLED = "limits_enabled"

        def __new__(cls, config: dict) -> FlirPTU:
            b = MountParser.Base(config)
            # TTY Port
            tty_port = cls.get_optional_val(
                MountParser.FlirPTU.TTY_PORT,
                config,
                FlirPTU.TTY_PORT,
            )
            # TCP Port
            tcp_port = cls.get_optional_val(
                MountParser.FlirPTU.TCP_PORT,
                config,
                FlirPTU.TCP_PORT,
            )
            # IP Address
            ip = cls.get_optional_val(
                MountParser.FlirPTU.IP_ADDRESS,
                config,
                FlirPTU.IP_ADDRESS,
            )
            # Connection Type
            connection_type = cls.get_optional_val(
                MountParser.FlirPTU.CONNECTION_TYPE,
                config,
                FlirPTU.CONNECTION_TYPE
            )
            # Limits Enabled
            limits_enabled = cls.get_optional_val(
                MountParser.FlirPTU.LIMITS_ENABLED,
                config,
                FlirPTU.LIMITS_ENABLED,
            )
            return FlirPTU(
                parent=b.get_parent(),
                xyz=b.get_xyz(),
                rpy=b.get_rpy(),
                tty_port=tty_port,
                tcp_port=tcp_port,
                ip=ip,
                connection_type=connection_type,
                limits_enabled=limits_enabled,
            )

    class PACSRiser(BaseConfigParser):
        # Keys
        ROWS = "rows"
        COLUMNS = "columns"
        THICKNESS = "thickness"

        def __new__(cls, config: dict) -> PACS.Riser:
            b = MountParser.Base(config)
            # Rows
            rows = cls.get_required_val(
                MountParser.PACSRiser.ROWS,
                config
            )
            # Columns
            columns = cls.get_required_val(
                MountParser.PACSRiser.COLUMNS,
                config
            )
            # Thickness
            thickness = cls.get_optional_val(
                MountParser.PACSRiser.THICKNESS,
                config,
                PACS.Riser.THICKNESS
            )
            return PACS.Riser(
                rows=rows,
                columns=columns,
                thickness=thickness,
                parent=b.get_parent(),
                xyz=b.get_xyz(),
                rpy=b.get_rpy(),
            )

    class PACSBracket(BaseConfigParser):
        # Keys
        MODEL = "model"

        def __new__(cls, config: dict) -> PACS.Riser:
            b = MountParser.Base(config)
            # Model
            model = cls.get_optional_val(
                MountParser.PACSBracket.MODEL,
                config,
                PACS.Bracket.DEFAULT
            )
            return PACS.Bracket(
                model=model,
                parent=b.get_parent(),
                xyz=b.get_xyz(),
                rpy=b.get_rpy(),
            )

    MODELS = {
        Mount.FATH_PIVOT: FathPivot,
        Mount.FLIR_PTU: FlirPTU,
        Mount.PACS_RISER: PACSRiser,
        Mount.PACS_BRACKET: PACSBracket
    }

    def __new__(cls, model, config: dict) -> BaseMount:
        assert model in MountParser.MODELS, (
            "Model '%s' must be one of '%s'" % (
                model,
                MountParser.MODELS
            )
        )
        return cls.MODELS[model](config)


class MountsConfigParser(BaseConfigParser):
    # Key
    MOUNTS = "mounts"
    MOUNT_CONFIG = {}

    def __new__(cls, config: dict) -> MountsConfig:
        mntconfig = MountsConfig()
        # Mounts
        mounts = cls.get_optional_val(cls.MOUNTS, config)
        if mounts is None:
            return mntconfig
        mntconfig.set_fath_pivots(cls.get_mounts(mounts, Mount.FATH_PIVOT))
        mntconfig.set_flir_ptus(cls.get_mounts(mounts, Mount.FLIR_PTU))
        mntconfig.set_risers(cls.get_mounts(mounts, Mount.PACS_RISER))
        mntconfig.set_brackets(cls.get_mounts(mounts, Mount.PACS_BRACKET))
        return mntconfig

    @classmethod
    def get_mounts(cls, config: dict, model: str) -> List[Mount]:
        # Assert Dictionary
        assert isinstance(config, dict), (
            "Mounts must be a dictionary of lists"
        )
        entries = cls.get_optional_val(model, config, [])
        # Assert List
        assert isinstance(entries, list), (
            "Model entries must be in a list"
        )
        models = []
        for entry in entries:
            models.append(MountParser(model, entry))
        return models


class BaseSensorParser(BaseConfigParser):
    # Keys
    URDF_ENABLED = "urdf_enabled"
    LAUNCH_ENABLED = "launch_enabled"
    ROS_PARAMETERS = "ros_parameters"

    def __new__(cls, config: dict) -> BaseSensor:
        parent = cls.get_optional_val(
            AccessoryParser.PARENT, config, AccessoryParser.PARENT)
        xyz = cls.get_optional_val(
            AccessoryParser.XYZ, config, Accessory.XYZ)
        rpy = cls.get_optional_val(
            AccessoryParser.RPY, config, Accessory.RPY)
        urdf_enabled = cls.get_optional_val(
            BaseSensorParser.URDF_ENABLED, config, BaseSensor.URDF_ENABLED)
        launch_enabled = cls.get_optional_val(
            BaseSensorParser.LAUNCH_ENABLED, config, BaseSensor.LAUNCH_ENABLED)
        ros_parameters = flatten_dict(cls.get_optional_val(
            BaseSensorParser.ROS_PARAMETERS,
            config,
            BaseSensor.ROS_PARAMETERS
            )
        )
        return BaseSensor(
            parent=parent,
            xyz=xyz, rpy=rpy,
            urdf_enabled=urdf_enabled,
            launch_enabled=launch_enabled,
            ros_parameters=ros_parameters
        )


class BaseLidar2DParser(BaseConfigParser):
    # Keys
    IP = "ip"
    PORT = "port"
    MIN_ANGLE = "min_angle"
    MAX_ANGLE = "max_angle"

    def __new__(cls, config: dict) -> BaseLidar2D:
        sensor = BaseSensorParser(config)
        ip = cls.get_optional_val(
            BaseLidar2DParser.IP, config, BaseLidar2D.IP_ADDRESS)
        port = cls.get_optional_val(
            BaseLidar2DParser.PORT, config, BaseLidar2D.IP_PORT)
        min_angle = cls.get_optional_val(
            BaseLidar2DParser.MIN_ANGLE, config, BaseLidar2D.MIN_ANGLE)
        max_angle = cls.get_optional_val(
            BaseLidar2DParser.MAX_ANGLE, config, BaseLidar2D.MAX_ANGLE)
        return BaseLidar2D(
            parent=sensor.get_parent(),
            xyz=sensor.get_xyz(),
            rpy=sensor.get_rpy(),
            urdf_enabled=sensor.get_urdf_enabled(),
            launch_enabled=sensor.get_launch_enabled(),
            ros_parameters=sensor.get_ros_parameters(),
            ip=ip,
            port=port,
            min_angle=min_angle,
            max_angle=max_angle
        )


class Lidar2DParser(BaseConfigParser):
    MODEL = "model"

    def __new__(cls, config: dict) -> BaseLidar2D:
        base = BaseLidar2DParser(config)
        model = cls.get_required_val(Lidar2DParser.MODEL, config)
        lidar2d = Lidar2D(model)
        # Set Base Parameters
        lidar2d.set_parent(base.get_parent())
        lidar2d.set_xyz(base.get_xyz())
        lidar2d.set_rpy(base.get_rpy())
        lidar2d.set_urdf_enabled(base.get_urdf_enabled())
        lidar2d.set_launch_enabled(base.get_launch_enabled())
        lidar2d.set_frame_id(base.get_frame_id())
        lidar2d.set_ip(base.get_ip())
        lidar2d.set_port(base.get_port())
        lidar2d.set_min_angle(base.get_min_angle())
        lidar2d.set_max_angle(base.get_max_angle())
        lidar2d.set_ros_parameters(base.get_ros_parameters())
        return lidar2d


class BaseLidar3DParser(BaseConfigParser):
    # Keys
    IP = "ip"
    PORT = "port"

    def __new__(cls, config: dict) -> BaseLidar3D:
        sensor = BaseSensorParser(config)
        ip = cls.get_optional_val(
            BaseLidar3DParser.IP, config, BaseLidar3D.IP_ADDRESS)
        port = cls.get_optional_val(
            BaseLidar3DParser.PORT, config, BaseLidar3D.IP_PORT)
        return BaseLidar3D(
            parent=sensor.get_parent(),
            xyz=sensor.get_xyz(),
            rpy=sensor.get_rpy(),
            urdf_enabled=sensor.get_urdf_enabled(),
            launch_enabled=sensor.get_launch_enabled(),
            ros_parameters=sensor.get_ros_parameters(),
            ip=ip,
            port=port,
        )


class Lidar3DParser(BaseConfigParser):
    MODEL = "model"

    def __new__(cls, config: dict) -> BaseLidar3D:
        base = BaseLidar3DParser(config)
        model = cls.get_required_val(Lidar3DParser.MODEL, config)
        lidar3d = Lidar3D(model)
        # Set Base Parameters
        lidar3d.set_parent(base.get_parent())
        lidar3d.set_xyz(base.get_xyz())
        lidar3d.set_rpy(base.get_rpy())
        lidar3d.set_urdf_enabled(base.get_urdf_enabled())
        lidar3d.set_launch_enabled(base.get_launch_enabled())
        lidar3d.set_frame_id(base.get_frame_id())
        lidar3d.set_ip(base.get_ip())
        lidar3d.set_port(base.get_port())
        lidar3d.set_ros_parameters(base.get_ros_parameters())
        return lidar3d


class BaseGPSParser(BaseConfigParser):
    # Keys
    IP = "ip"
    PORT = "port"
    FRAME_ID = "frame_id"

    def __new__(cls, config: dict) -> BaseGPS:
        sensor = BaseSensorParser(config)
        ip = cls.get_optional_val(
            BaseGPSParser.IP, config, BaseGPS.IP_ADDRESS)
        port = cls.get_optional_val(
            BaseGPSParser.PORT, config, BaseGPS.IP_PORT)
        frame_id = cls.get_optional_val(
            BaseGPSParser.FRAME_ID, config, BaseGPS.FRAME_ID)
        return BaseGPS(
            parent=sensor.get_parent(),
            xyz=sensor.get_xyz(),
            rpy=sensor.get_rpy(),
            urdf_enabled=sensor.get_urdf_enabled(),
            launch_enabled=sensor.get_launch_enabled(),
            ros_parameters=sensor.get_ros_parameters(),
            ip=ip,
            port=port,
            frame_id=frame_id
        )


class GPSParser(BaseConfigParser):
    MODEL = "model"

    def __new__(cls, config: dict) -> BaseGPS:
        base = BaseGPSParser(config)
        model = cls.get_required_val(GPSParser.MODEL, config)
        gps = GlobalPositioningSystem(model)
        # Set Base Parameters
        gps.set_parent(base.get_parent())
        gps.set_xyz(base.get_xyz())
        gps.set_rpy(base.get_rpy())
        gps.set_urdf_enabled(base.get_urdf_enabled())
        gps.set_launch_enabled(base.get_launch_enabled())
        gps.set_frame_id(base.get_frame_id())
        gps.set_ip(base.get_ip())
        gps.set_port(base.get_port())
        gps.set_ros_parameters(base.get_ros_parameters())
        return gps


class IMUParser(BaseConfigParser):
    MODEL = "model"

    def __new__(cls, config: dict) -> BaseIMU:
        base = BaseSensorParser(config)
        model = cls.get_required_val(IMUParser.MODEL, config)
        imu = InertialMeasurementUnit(model)
        # Set Base Parameters
        imu.set_parent(base.get_parent())
        imu.set_xyz(base.get_xyz())
        imu.set_rpy(base.get_rpy())
        imu.set_urdf_enabled(base.get_urdf_enabled())
        imu.set_launch_enabled(base.get_launch_enabled())
        imu.set_ros_parameters(base.get_ros_parameters())
        return imu


class BaseCameraParser(BaseConfigParser):
    FPS = "fps"
    SERIAL = "serial"

    def __new__(cls, config: dict) -> BaseCamera:
        sensor = BaseSensorParser(config)
        fps = cls.get_optional_val(
            BaseCameraParser.FPS, config, BaseCamera.FPS)
        serial = cls.get_optional_val(
            BaseCameraParser.SERIAL, config, BaseCamera.SERIAL)
        return BaseCamera(
            parent=sensor.get_parent(),
            xyz=sensor.get_xyz(),
            rpy=sensor.get_rpy(),
            urdf_enabled=sensor.get_urdf_enabled(),
            launch_enabled=sensor.get_launch_enabled(),
            ros_parameters=sensor.get_ros_parameters(),
            fps=fps,
            serial=serial
        )


class CameraParser(BaseConfigParser):
    MODEL = "model"

    # Blackfly Parameters
    CONNECTION_TYPE = "connection_type"
    ENCODING = "encoding"

    # Realsense Parameters
    COLOR_ENABLE = "color_enabled"
    COLOR_FPS = "color_fps"
    COLOR_WIDTH = "color_width"
    COLOR_HEIGHT = "color_height"
    DEPTH_ENABLED = "depth_enabled"
    DEPTH_FPS = "depth_fps"
    DEPTH_WIDTH = "depth_width"
    DEPTH_HEIGHT = "depth_height"
    POINTCLOUD_ENABLED = "pointcloud_enabled"

    # ROS Parameters
    ROS_PARAMETERS = "ros_parameters"

    def __new__(cls, config: dict) -> BaseCamera:
        base = BaseCameraParser(config)
        model = cls.get_required_val(CameraParser.MODEL, config)
        camera = Camera(model)
        # Set Specific Parameters
        if model == Camera.FLIR_BLACKFLY:
            camera.set_connection_type(
                cls.get_optional_val(
                    CameraParser.CONNECTION_TYPE,
                    config,
                    FlirBlackfly.CONNECTION_TYPE
                )
            )
            camera.set_encoding(
                cls.get_optional_val(
                    CameraParser.ENCODING,
                    config,
                    FlirBlackfly.BAYER_RG8
                )
            )
        elif model == Camera.INTEL_REALSENSE:
            camera.set_color_enabled(
                cls.get_optional_val(
                    CameraParser.COLOR_ENABLE,
                    config,
                    IntelRealsense.COLOR_ENABLED
                )
            )
            camera.set_color_fps(
                cls.get_optional_val(
                    CameraParser.COLOR_FPS,
                    config,
                    IntelRealsense.COLOR_FPS
                )
            )
            camera.set_color_width(
                cls.get_optional_val(
                    CameraParser.COLOR_WIDTH,
                    config,
                    IntelRealsense.COLOR_WIDTH
                )
            )
            camera.set_color_height(
                cls.get_optional_val(
                    CameraParser.COLOR_HEIGHT,
                    config,
                    IntelRealsense.COLOR_HEIGHT
                )
            )
            camera.set_depth_enabled(
                cls.get_optional_val(
                    CameraParser.DEPTH_ENABLED,
                    config,
                    IntelRealsense.DEPTH_ENABLED
                )
            )
            camera.set_depth_fps(
                cls.get_optional_val(
                    CameraParser.DEPTH_FPS,
                    config,
                    IntelRealsense.DEPTH_FPS
                )
            )
            camera.set_depth_width(
                cls.get_optional_val(
                    CameraParser.DEPTH_WIDTH,
                    config,
                    IntelRealsense.DEPTH_WIDTH
                )
            )
            camera.set_depth_height(
                cls.get_optional_val(
                    CameraParser.DEPTH_HEIGHT,
                    config,
                    IntelRealsense.DEPTH_HEIGHT
                )
            )
            camera.set_pointcloud_enabled(
                cls.get_optional_val(
                    CameraParser.POINTCLOUD_ENABLED,
                    config,
                    IntelRealsense.POINTCLOUD_ENABLED
                )
            )
        # Set Base Parameters
        camera.set_parent(base.get_parent())
        camera.set_xyz(base.get_xyz())
        camera.set_rpy(base.get_rpy())
        camera.set_urdf_enabled(base.get_urdf_enabled())
        camera.set_launch_enabled(base.get_launch_enabled())
        camera.set_fps(base.get_fps())
        camera.set_serial(base.get_serial())
        camera.set_ros_parameters(base.get_ros_parameters())
        return camera


class SensorParser(BaseConfigParser):

    def __new__(cls, model: str, config: dict) -> BaseSensor:
        Sensor.assert_type(model)
        if model == Sensor.LIDAR2D:
            return Lidar2DParser(config)
        elif model == Sensor.LIDAR3D:
            return Lidar3DParser(config)
        elif model == Sensor.CAMERA:
            return CameraParser(config)
        elif model == Sensor.IMU:
            return IMUParser(config)
        elif model == Sensor.GPS:
            return GPSParser(config)


class SensorConfigParser(BaseConfigParser):
    # Key
    SENSORS = "sensors"

    def __new__(cls, config: dict) -> SensorConfig:
        snrconfig = SensorConfig()
        # Sensors
        sensors = cls.get_optional_val(cls.SENSORS, config)
        if not sensors:
            return snrconfig
        # Lidar2D
        snrconfig.set_all_lidar_2d(cls.get_sensors(sensors, Sensor.LIDAR2D))
        # Lidar3D
        snrconfig.set_all_lidar_3d(cls.get_sensors(sensors, Sensor.LIDAR3D))
        # Camera
        snrconfig.set_all_camera(cls.get_sensors(sensors, Sensor.CAMERA))
        # IMU
        snrconfig.set_all_imu(cls.get_sensors(sensors, Sensor.IMU))
        # GPS
        snrconfig.set_all_gps(cls.get_sensors(sensors, Sensor.GPS))
        return snrconfig

    @classmethod
    def get_sensors(cls, config: dict, model: str) -> List[BaseSensor]:
        entries = cls.get_optional_val(model, config, [])
        models = []
        for entry in entries:
            models.append(SensorParser(model, entry))
        return models


# Clearpath Configuration Parser
class ClearpathConfigParser(BaseConfigParser):
    @staticmethod
    # Get Valid Path
    def find_valid_path(path, cwd=None):
        abspath = path
        if cwd:
            relpath = os.path.join(cwd, path)
        else:
            relpath = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), path)
        if not os.path.isfile(abspath) and not os.path.isfile(relpath):
            return None
        if os.path.isfile(abspath):
            path = abspath
        elif os.path.isfile(relpath):
            path = relpath
        return path

    @staticmethod
    def read_yaml(path: str) -> dict:
        # Check YAML Path
        path = ClearpathConfigParser.find_valid_path(path, os.getcwd())
        assert path, "YAML file '%s' could not be found" % path
        # Check YAML can be Opened
        try:
            config = yaml.load(open(path), Loader=yaml.SafeLoader)
        except yaml.scanner.ScannerError:
            raise AssertionError(
                "YAML file '%s' is not well formed" % path)
        except yaml.constructor.ConstructorError:
            raise AssertionError(
                "YAML file '%s' is attempting to create unsafe objects" % (
                    path))
        # Check contents are a Dictionary
        assert isinstance(config, dict), (
            "YAML file '%s' is not a dictionary" % path)
        return config

    @staticmethod
    def write_yaml(path: str, config: dict) -> None:
        yaml_file = open(path, "w+")
        yaml.dump(
            config,
            yaml_file,
            sort_keys=False,
            default_flow_style=None,
            allow_unicode=True,
        )

    """
    ConfigParser():
        - will take a config file path or a config and return a ClearpathConfig
    """

    def __new__(self, config):
        # Path: if config is path to config file, read YAML
        if isinstance(config, str):
            config = self.read_yaml(config)
        # Dict: if not path, it must be of type config
        assert isinstance(config, dict), "Configuration must be of type 'dict'"
        # ClearpathConfig
        cprconfig = ClearpathConfig()
        # SystemConfig
        cprconfig.system = SystemConfigParser(config)
        # AccessoryConfig
        cprconfig.accessories = AccessoryConfigParser(config)
        # PlatformConfig
        cprconfig.platform = PlatformConfigParser(config)
        # MountConfig
        cprconfig.mounts = MountsConfigParser(config)
        # SensorConfig
        cprconfig.sensors = SensorConfigParser(config)
        return cprconfig
