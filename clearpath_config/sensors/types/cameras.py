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
from math import pi
from typing import List

from clearpath_config.common.ros import ROS_DISTRO

from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.exception import UnsupportedAccessoryException
from clearpath_config.common.utils.dictionary import extend_flat_dict
from clearpath_config.sensors.types.sensor import BaseSensor


class Republisher():
    TYPE = 'type'

    class Base():
        INPUT = 'input'
        OUTPUT = 'output'
        INPUT_DEFAULT = 'in'
        OUTPUT_DEFAULT = 'out'

        def __init__(self, config: dict) -> None:

            self.from_dict(config)

        def from_dict(self, config: dict) -> None:
            self.input = config.get(self.INPUT, self.INPUT_DEFAULT)
            self.output = config.get(self.OUTPUT, self.OUTPUT_DEFAULT)

        def to_dict(self) -> dict:
            return {
                self.INPUT: self.input,
                self.OUTPUT: self.output
            }

        @property
        def input(self) -> str:  # noqa:A003
            return self._input

        @input.setter
        def input(self, value: str) -> None:  # noqa:A003
            self._input = value

        @property
        def output(self) -> str:
            return self._output

        @output.setter
        def output(self, value: str) -> None:
            self._output = value

    class Compress(Base):
        TYPE = 'compress'
        INPUT_DEFAULT = 'color'
        OUTPUT_DEFAULT = 'compressed'

    class Rectify(Base):
        TYPE = 'rectify'
        INPUT_DEFAULT = 'color'
        OUTPUT_DEFAULT = 'rectified'

    class Resize(Base):
        TYPE = 'resize'
        INPUT_DEFAULT = 'color'
        OUTPUT_DEFAULT = 'resize'

    class Theora(Base):
        TYPE = 'theora'
        INPUT_DEFAULT = 'color'
        OUTPUT_DEFAULT = 'theora'

    TYPES = {
        Compress.TYPE: Compress,
        Rectify.TYPE: Rectify,
        Resize.TYPE: Resize,
        Theora.TYPE: Theora
    }

    def __new__(self, config: dict) -> None:
        assert self.TYPE in config, f'Republisher must have "{self.TYPE}" specified'
        assert config[self.TYPE] in self.TYPES, f'Republisher "{self.TYPE}" must be one of "{self.TYPES.keys()}"'  # noqa:E501
        return self.TYPES[config[self.TYPE]](config)


class BaseCamera(BaseSensor):
    SENSOR_TYPE = 'camera'
    SENSOR_MODEL = 'base'
    TOPIC = 'image'

    FPS = 30
    SERIAL = '0'

    class ROS_PARAMETER_KEYS:
        FPS = 'node_name.fps'
        SERIAL = 'node_name.serial'

    class TOPICS:
        COLOR_IMAGE = 'color_image'
        COLOR_CAMERA_INFO = 'color_camera_info'
        NAME = {
            COLOR_IMAGE: 'color/image',
            COLOR_CAMERA_INFO: 'color/camera_info'
        }
        TYPE = {
            COLOR_IMAGE: 'sensor_msgs/msg/Image',
            COLOR_CAMERA_INFO: 'sensor_msgs/msg/CameraInfo',
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = TOPIC,
            fps: int = FPS,
            serial: str = SERIAL,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        # FPS:
        # - camera frame rate
        # - default to 30
        # - certain sensors may only accept certain rates
        self.fps = fps
        # Serial Number:
        # - camera unique serial number for multi-camera setups
        # - usually an integer value
        self.serial = serial
        # ROS Parameter Template
        template = {
            self.ROS_PARAMETER_KEYS.FPS: BaseCamera.fps,
            self.ROS_PARAMETER_KEYS.SERIAL: BaseCamera.serial,
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
            rpy,
            )
        # Rates:
        # - should be a dictionary matching those in the TOPICS class
        # - should be updated as necessary to reflect current operation
        self.rates = {
            BaseCamera.TOPICS.COLOR_IMAGE: BaseCamera.fps,
            BaseCamera.TOPICS.COLOR_CAMERA_INFO: BaseCamera.fps,
        }

    @property
    def camera_name(self) -> str:
        return self.get_name()

    @camera_name.setter
    def camera_name(self, name: str) -> None:
        self.set_name(name)

    @property
    def fps(self) -> int:
        return self._fps

    @fps.setter
    def fps(self, fps: int) -> None:
        BaseSensor.assert_valid_rate(fps)
        self._fps = int(fps)

    @property
    def serial(self) -> str:
        return self._serial

    @serial.setter
    def serial(self, serial: str) -> None:
        self._serial = str(serial)

    @property
    def republishers(self) -> list:
        return [republisher.to_dict() for republisher in self._republishers]

    @republishers.setter
    def republishers(self, republishers: list) -> None:
        assert isinstance(republishers, list), (
            'Camera republishers must be a list of dictionaries')
        assert all([isinstance(i, dict) for i in republishers]), (  # noqa: C419
            'Camera republishers must be a list of dictionaries')
        self._republishers = []
        for republisher in republishers:
            self._republishers.append(Republisher(republisher))

    def to_dict(self) -> dict:
        config = super().to_dict()
        config['republishers'] = self.republishers
        return config

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        self.republishers = d.get('republishers', [])


class IntelRealsense(BaseCamera):
    SENSOR_MODEL = 'intel_realsense'

    D415 = 'd415'
    D435 = 'd435'
    D435i = 'd435i'
    D455 = 'd455'
    D456 = 'd456'
    DEVICE_TYPE = D435
    DEVICE_TYPES = (
        D415,
        D435,
        D435i,
        D455,
        D456,
    )

    COLOR_ENABLED = True
    COLOR_FPS = 30
    COLOR_WIDTH = 640
    COLOR_HEIGHT = 480

    DEPTH_ENABLED = True
    DEPTH_FPS = 30
    DEPTH_WIDTH = 640
    DEPTH_HEIGHT = 480

    POINTCLOUD_ENABLED = True

    class ROS_PARAMETER_KEYS:
        FPS = 'intel_realsense.rgb_camera.color_profile'
        SERIAL = 'intel_realsense.serial_no'
        CAMERA_NAME = 'intel_realsense.camera_name'
        DEVICE_TYPE = 'intel_realsense.device_type'
        DEPTH_PROFILE = 'intel_realsense.depth_module.depth_profile'
        DEPTH_ENABLE = 'intel_realsense.enable_depth'
        COLOR_ENABLE = 'intel_realsense.enable_color'
        POINTCLOUD_ENABLE = 'intel_realsense.pointcloud.enable'

    class TOPICS:
        COLOR_IMAGE = 'color_image'
        COLOR_CAMERA_INFO = 'color_camera_info'
        DEPTH_IMAGE = 'depth_image'
        DEPTH_CAMERA_INFO = 'depth_camera_info'
        POINTCLOUD = 'points'
        IMU = 'imu'
        NAME = {
            COLOR_IMAGE: 'color/image',
            COLOR_CAMERA_INFO: 'color/camera_info',
            DEPTH_IMAGE: 'depth/image',
            DEPTH_CAMERA_INFO: 'depth/camera_info',
            POINTCLOUD: 'points',
            IMU: 'imu'
        }
        TYPE = {
            COLOR_IMAGE: 'sensor_msgs/msg/Image',
            COLOR_CAMERA_INFO: 'sensor_msgs/msg/CameraInfo',
            DEPTH_IMAGE: 'sensor_msgs/msg/Image',
            DEPTH_CAMERA_INFO: 'sensor_msgs/msg/CameraInfo',
            POINTCLOUD: 'sensor_msgs/msg/PointCloud2',
            IMU: 'sensor_msgs/msg/Imu'
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseCamera.TOPIC,
            serial: str = BaseCamera.SERIAL,
            device_type: str = DEVICE_TYPE,
            color_enabled: bool = COLOR_ENABLED,
            color_fps: bool = COLOR_FPS,
            color_width: int = COLOR_WIDTH,
            color_height: int = COLOR_HEIGHT,
            depth_enabled: bool = DEPTH_ENABLED,
            depth_fps: int = DEPTH_FPS,
            depth_width: int = DEPTH_WIDTH,
            depth_height: int = DEPTH_HEIGHT,
            pointcloud_enabled: bool = POINTCLOUD_ENABLED,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:

        # Initialization
        self.device_type = device_type
        self.serial = serial
        # Color Image
        self.color_enabled = color_enabled
        self.color_width = color_width
        self.color_height = color_height
        self.color_fps = color_fps
        # Depth Image
        self.depth_enabled = depth_enabled
        self.depth_width = depth_width
        self.depth_height = depth_height
        self.depth_fps = depth_fps
        # Pointcloud
        self.pointcloud_enabled = pointcloud_enabled

        # ROS Parameter Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.FPS: IntelRealsense.color_profile,
            self.ROS_PARAMETER_KEYS.SERIAL: IntelRealsense.serial,
            self.ROS_PARAMETER_KEYS.CAMERA_NAME: IntelRealsense.camera_name,
            self.ROS_PARAMETER_KEYS.DEVICE_TYPE: IntelRealsense.device_type,
            self.ROS_PARAMETER_KEYS.DEPTH_PROFILE: IntelRealsense.depth_profile,
            self.ROS_PARAMETER_KEYS.DEPTH_ENABLE: IntelRealsense.depth_enabled,
            self.ROS_PARAMETER_KEYS.COLOR_ENABLE: IntelRealsense.color_enabled,
            self.ROS_PARAMETER_KEYS.POINTCLOUD_ENABLE: IntelRealsense.pointcloud_enabled,
        }
        super().__init__(
            idx,
            name,
            topic,
            color_fps,
            serial,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )

        # Topic Rates
        self.rates = {
            IntelRealsense.TOPICS.COLOR_IMAGE: IntelRealsense.color_fps,
            IntelRealsense.TOPICS.COLOR_CAMERA_INFO: IntelRealsense.color_fps,
            IntelRealsense.TOPICS.DEPTH_IMAGE: IntelRealsense.depth_fps,
            IntelRealsense.TOPICS.DEPTH_CAMERA_INFO: IntelRealsense.depth_fps,
            IntelRealsense.TOPICS.POINTCLOUD: IntelRealsense.depth_fps,
            # Tracking of the IMU rate is not currently supported
        }

    @staticmethod
    def clean_profile(profile: str | list) -> list:
        if isinstance(profile, str):
            profile = profile.split(',')
            assert len(profile) == 3, (
                'Profile "%s" is not three comma separated values')
            try:
                profile = [int(entry) for entry in profile]
            except ValueError:
                raise AssertionError(
                    'Profile "%s" cannot be cast to integer')
        else:
            assert len(profile) == 3, (
                'Profile "%s" is not three integer values')
            assert all([isinstance(entry, int) for entry in profile]), (  # noqa: C419
                'Profile "%s" is not three integer values')
        return profile

    def assert_pixel_length(
            self,
            length: int
            ) -> None:
        assert isinstance(length, int), (
            'Pixel value must be integer'
        )
        assert length >= 0, (
            'Pixel length must be positive'
        )

    @property
    def device_type(self) -> str:
        return self._device_type

    @device_type.setter
    def device_type(self, device_type: str) -> None:
        assert device_type in self.DEVICE_TYPES, (
            'Device type "%s" is not one of "%s"' % (
                device_type,
                self.DEVICE_TYPES
            )
        )
        self._device_type = device_type

    @property
    def color_enabled(self) -> bool:
        return self._color_enabled

    @color_enabled.setter
    def color_enabled(self, enabled: bool) -> None:
        self._color_enabled = bool(enabled)

    @property
    def color_fps(self) -> int:
        return self.fps

    @color_fps.setter
    def color_fps(self, fps: int) -> None:
        self.fps = int(fps)

    @property
    def color_height(self) -> int:
        return self._color_height

    @color_height.setter
    def color_height(self, height: int) -> None:
        self.assert_pixel_length(height)
        self._color_height = height

    @property
    def color_width(self) -> int:
        return self._color_width

    @color_width.setter
    def color_width(self, width: int) -> None:
        self.assert_pixel_length(width)
        self._color_width = width

    @property
    def color_profile(self) -> str:
        return '%s,%s,%s' % (
            self.color_width,
            self.color_height,
            self.color_fps
        )

    @color_profile.setter
    def color_profile(self, profile: str | list) -> None:
        profile = self.clean_profile(profile)
        self.color_width = profile[0]
        self.color_height = profile[1]
        self.color_fps = profile[2]

    @property
    def depth_enabled(self) -> bool:
        return self._depth_enabled

    @depth_enabled.setter
    def depth_enabled(self, enabled: bool) -> None:
        self._depth_enabled = bool(enabled)

    @property
    def depth_fps(self) -> int:
        return self._depth_fps

    @depth_fps.setter
    def depth_fps(self, fps: int) -> None:
        BaseSensor.assert_valid_rate(fps)
        self._depth_fps = int(fps)

    @property
    def depth_width(self) -> int:
        return self._depth_width

    @depth_width.setter
    def depth_width(self, width: int) -> None:
        self.assert_pixel_length(width)
        self._depth_width = width

    @property
    def depth_height(self) -> int:
        return self._depth_height

    @depth_height.setter
    def depth_height(self, height: int) -> None:
        self.assert_pixel_length(height)
        self._depth_height = height

    @property
    def depth_profile(self) -> str:
        return '%s,%s,%s' % (
            self.depth_width,
            self.depth_height,
            self.depth_fps
        )

    @depth_profile.setter
    def depth_profile(self, profile: str | list) -> None:
        profile = self.clean_profile(profile)
        self.depth_width = profile[0]
        self.depth_height = profile[1]
        self.depth_fps = profile[2]

    @property
    def pointcloud_enabled(self) -> bool:
        return self._pointcloud_enabled

    @pointcloud_enabled.setter
    def pointcloud_enabled(self, enabled: bool) -> None:
        self._pointcloud_enabled = bool(enabled)


class FlirBlackfly(BaseCamera):
    SENSOR_MODEL = 'flir_blackfly'

    USB3_CONNECTION = 'USB3'
    GIGE_CONNECTION = 'GigE'
    CONNECTION_TYPE = USB3_CONNECTION
    CONNECTION_TYPES = (USB3_CONNECTION, GIGE_CONNECTION)

    MONO_8 = 'Mono8'
    MONO_16 = 'Mono16'
    MONO_12 = 'Mono12p'
    MONO_12_PACKED = 'Mono12Packed'
    YUV_411_PACKED = 'YUV411Packed'
    YUV_422_PACKED = 'YUV422Packed'
    YUV_444_PACKED = 'YUV444Packed'
    YCBCR_8 = 'YCbCr8'
    YCBCR_422_8 = 'YCbCr422_8'
    YCBCR_411_8 = 'YCbCr411_8'
    BGR_8 = 'BGR8'
    BGRA_8 = 'BGRa8'
    RGB_8_PACKED = 'RGB8Packed'
    BAYER_GR8 = 'BayerGR8'
    BAYER_RG8 = 'BayerRG8'
    BAYER_GB8 = 'BayerGB8'
    BAYER_BG8 = 'BayerBG8'
    BAYER_GR16 = 'BayerGR16'
    BAYER_RG16 = 'BayerRG16'
    BAYER_GB16 = 'BayerGB16'
    BAYER_BG16 = 'BayerBG16'
    BAYER_GR12 = 'BayerGR12p'
    BAYER_RG12 = 'BayerRG12p'
    BAYER_GB12 = 'BayerGB12p'
    BAYER_BG12 = 'BayerBG12p'
    BAYER_GR12_PACKED = 'BayerGR12Packed'
    BAYER_RG12_PACKED = 'BayerRG12Packed'
    BAYER_GB12_PACKED = 'BayerGB12Packed'
    BAYER_BG12_PACKED = 'BayerBG12Packed'

    ENCODINGS = (
        MONO_8,
        MONO_16,
        MONO_12,
        MONO_12_PACKED,
        YUV_411_PACKED,
        YUV_422_PACKED,
        YUV_444_PACKED,
        YCBCR_8,
        YCBCR_422_8,
        YCBCR_411_8,
        BGR_8,
        BGRA_8,
        RGB_8_PACKED,
        BAYER_GR8,
        BAYER_RG8,
        BAYER_GB8,
        BAYER_BG8,
        BAYER_GR16,
        BAYER_RG16,
        BAYER_GB16,
        BAYER_BG16,
        BAYER_GR12,
        BAYER_RG12,
        BAYER_GB12,
        BAYER_BG12,
        BAYER_GR12_PACKED,
        BAYER_RG12_PACKED,
        BAYER_GB12_PACKED,
        BAYER_BG12_PACKED,
    )

    class ROS_PARAMETER_KEYS:
        FPS = 'flir_blackfly.frame_rate'
        SERIAL = 'flir_blackfly.serial_number'
        ENCODING = 'flir_blackfly.pixel_format'

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseCamera.TOPIC,
            fps: float = BaseCamera.FPS,
            serial: str = BaseCamera.SERIAL,
            connection_type: str = CONNECTION_TYPE,
            encoding: str = BAYER_RG8,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: str = BaseSensor.ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:

        # Initialization
        self.connection_type = connection_type
        self.encoding = encoding

        # ROS Parameter Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.FPS: FlirBlackfly.fps,
            self.ROS_PARAMETER_KEYS.SERIAL: FlirBlackfly.serial,
            self.ROS_PARAMETER_KEYS.ENCODING: FlirBlackfly.encoding,
        }
        super().__init__(
            idx,
            name,
            topic,
            fps,
            serial,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )

        # Topic Rates
        self.rates = {
            FlirBlackfly.TOPICS.COLOR_IMAGE: FlirBlackfly.fps,
            FlirBlackfly.TOPICS.COLOR_CAMERA_INFO: FlirBlackfly.fps,
        }

    @property
    def fps(self) -> float:
        return self._fps

    @fps.setter
    def fps(self, fps: float) -> None:
        BaseSensor.assert_valid_rate(fps)
        self._fps = float(fps)

    @property
    def connection_type(self) -> str:
        return self._connection_type

    @connection_type.setter
    def connection_type(self, _type: str) -> None:
        assert _type in FlirBlackfly.CONNECTION_TYPES
        self._connection_type = _type

    @property
    def encoding(self) -> str:
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: str) -> None:
        assert encoding in FlirBlackfly.ENCODINGS, (
            'Encoding "%s" not found in support encodings: "%s"' % (
                encoding, FlirBlackfly.ENCODINGS
            )
        )
        self._encoding = encoding


class StereolabsZed(BaseCamera):
    SENSOR_MODEL = 'stereolabs_zed'

    SERIAL = 0

    ZED = 'zed'
    ZEDM = 'zedm'
    ZED2 = 'zed2'
    ZED2I = 'zed2i'
    ZEDX = 'zedx'
    ZEDXM = 'zedxm'
    VIRTUAL = 'virtual'
    DEVICE_TYPE = ZED2
    DEVICE_TYPES = (
        ZED,
        ZEDM,
        ZED2,
        ZED2I,
        ZEDX,
        ZEDXM,
        VIRTUAL
    )

    RESOLUTION_DEFAULT = 'AUTO'
    RESOLUTION_PRESETS = (
        'AUTO',
        'HD2K',
        'HD1080',
        'HD720',
        'VGA'
    )

    class ROS_PARAMETER_KEYS:
        FPS = 'stereolabs_zed.general.grab_frame_rate'
        SERIAL = 'stereolabs_zed.general.serial_number'
        CAMERA_MODEL = 'stereolabs_zed.general.camera_model'
        CAMERA_NAME = 'stereolabs_zed.general.camera_name'
        RESOLUTION = 'stereolabs_zed.general.grab_resolution'

    class TOPICS:
        COLOR_IMAGE = 'color_image'
        COLOR_CAMERA_INFO = 'color_camera_info'
        DEPTH_IMAGE = 'depth_image'
        DEPTH_CAMERA_INFO = 'depth_camera_info'
        POINTCLOUD = 'points'
        IMU = 'imu'
        NAME = {
            COLOR_IMAGE: 'color/image',
            COLOR_CAMERA_INFO: 'color/camera_info',
            DEPTH_IMAGE: 'depth/image',
            DEPTH_CAMERA_INFO: 'depth/camera_info',
            POINTCLOUD: 'points',
            IMU: 'imu'
        }
        TYPE = {
            COLOR_IMAGE: 'sensor_msgs/msg/Image',
            COLOR_CAMERA_INFO: 'sensor_msgs/msg/CameraInfo',
            DEPTH_IMAGE: 'sensor_msgs/msg/Image',
            DEPTH_CAMERA_INFO: 'sensor_msgs/msg/CameraInfo',
            POINTCLOUD: 'sensor_msgs/msg/PointCloud2',
            IMU: 'sensor_msgs/msg/Imu'
        }

    @staticmethod
    def assert_is_supported():
        raise UnsupportedAccessoryException(f'Stereolabs Zed devices are not yet supported in {ROS_DISTRO}')  # noqa:E501

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseCamera.TOPIC,
            fps: int = BaseCamera.FPS,
            serial: str = BaseCamera.SERIAL,
            device_type: str = ZED2,
            resolution: str = RESOLUTION_DEFAULT,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:

        # Initialization
        self.device_type = device_type
        self.resolution = resolution

        # ROS Parameter Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.FPS: StereolabsZed.fps,
            self.ROS_PARAMETER_KEYS.SERIAL: StereolabsZed.serial,
            self.ROS_PARAMETER_KEYS.CAMERA_MODEL: StereolabsZed.device_type,
            self.ROS_PARAMETER_KEYS.CAMERA_NAME: StereolabsZed.camera_name,
            self.ROS_PARAMETER_KEYS.RESOLUTION: StereolabsZed.resolution,
        }
        super().__init__(
            idx,
            name,
            topic,
            fps,
            serial,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )

        # Topic Rates
        self.rates = {
            StereolabsZed.TOPICS.COLOR_IMAGE: StereolabsZed.fps,
            StereolabsZed.TOPICS.COLOR_CAMERA_INFO: StereolabsZed.fps,
            StereolabsZed.TOPICS.DEPTH_IMAGE: StereolabsZed.fps,
            StereolabsZed.TOPICS.DEPTH_CAMERA_INFO: StereolabsZed.fps,
            StereolabsZed.TOPICS.POINTCLOUD: StereolabsZed.fps,
            # Tracking of the IMU rate is not currently supported
        }

    @property
    def device_type(self) -> str:
        return self._device_type

    @device_type.setter
    def device_type(self, device_type: str) -> None:
        assert device_type in self.DEVICE_TYPES, (
            'Device type "%s" is not one of "%s"' % (
                device_type,
                self.DEVICE_TYPES
            )
        )
        self._device_type = device_type

    @property
    def resolution(self) -> str:
        return self._resolution

    @resolution.setter
    def resolution(self, resolution: str) -> None:
        assert resolution in self.RESOLUTION_PRESETS, (
            'Resolution preset "%s" is not one oserial_numberf "%s"' % (
                resolution,
                self.RESOLUTION_PRESETS
            )
        )
        self._resolution = resolution

    @property
    def serial(self) -> int:
        return self._serial

    @serial.setter
    def serial(self, serial: int) -> None:
        self._serial = int(serial)


class LuxonisOAKD(BaseCamera):
    SENSOR_MODEL = 'luxonis_oakd'

    SERIAL = None

    PRO = 'pro'
    LITE = 'lite'
    PRO_W_POE = 'pro_w_poe'
    DEVICE_TYPE = PRO
    DEVICE_TYPES = (
        PRO,
        LITE,
        PRO_W_POE,
    )

    HEIGHT = 720
    WIDTH = 1280

    FPS = 30.0

    class ROS_PARAMETER_KEYS:
        DEVICE_TYPE = 'oakd.device_type'

        # RGB parameters
        FPS = 'oakd.rgb.i_fps'
        HEIGHT = 'oakd.rgb.i_height'
        WIDTH = 'oakd.rgb.i_width'

        # Stereo parameters
        STEREO_FPS = 'oakd.stereo.i_fps'

        # General camera parameters
        IP_ADDRESS = 'oakd.camera.i_ip'
        MX_ID = 'oakd.camera.i_mx_id'
        SERIAL = 'oakd.camera.i_usb_port_id'

    class TOPICS:
        COLOR_IMAGE = 'color_image'
        COLOR_CAMERA_INFO = 'color_camera_info'
        STEREO_IMAGE = 'stereo_image'
        STEREO_CAMERA_INFO = 'stereo_camera_info'
        POINTCLOUD = 'points'
        IMU = 'imu'

        NAME = {
            COLOR_IMAGE: 'color/image',
            COLOR_CAMERA_INFO: 'color/camera_info',
            STEREO_IMAGE: 'stereo/image',
            STEREO_CAMERA_INFO: 'stereo/camera_info',
            POINTCLOUD: 'points',
            IMU: 'imu',
        }
        TYPE = {
            COLOR_IMAGE: 'sensor_msgs/msg/Image',
            COLOR_CAMERA_INFO: 'sensor_msgs/msg/CameraInfo',
            STEREO_IMAGE: 'sensor_msgs/msg/Image',
            STEREO_CAMERA_INFO: 'sensor_msgs/msg/CameraInfo',
            POINTCLOUD: 'sensor_msgs/msg/PointCloud2',
            IMU: 'sensor_msgs/msg/Imu'
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseCamera.TOPIC,
            fps: int = FPS,
            stereo_fps: int = FPS,
            serial: str = SERIAL,
            device_type: str = DEVICE_TYPE,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ip_address: str = None,  # only relevant for PoE models
            mx_id: str = None,  # optional ID for multiple cameras
            ) -> None:

        # Resolution
        self.height = LuxonisOAKD.HEIGHT
        self.width = LuxonisOAKD.WIDTH
        self.stereo_fps = stereo_fps

        self.device_type = device_type
        self.ip_address = ip_address
        self.mx_id = mx_id

        # ROS Parameter Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.DEVICE_TYPE: LuxonisOAKD.device_type,
            self.ROS_PARAMETER_KEYS.FPS: LuxonisOAKD.fps,
            self.ROS_PARAMETER_KEYS.STEREO_FPS: LuxonisOAKD.stereo_fps,
            self.ROS_PARAMETER_KEYS.SERIAL: LuxonisOAKD.serial,
            self.ROS_PARAMETER_KEYS.HEIGHT: LuxonisOAKD.height,
            self.ROS_PARAMETER_KEYS.WIDTH: LuxonisOAKD.width,
            self.ROS_PARAMETER_KEYS.IP_ADDRESS: LuxonisOAKD.ip_address
        }
        super().__init__(
            idx,
            name,
            topic,
            fps,
            serial,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )

        # Topic Rates
        self.rates = {
            LuxonisOAKD.TOPICS.COLOR_IMAGE: LuxonisOAKD.fps,
            LuxonisOAKD.TOPICS.COLOR_CAMERA_INFO: LuxonisOAKD.fps,
            LuxonisOAKD.TOPICS.STEREO_IMAGE: LuxonisOAKD.stereo_fps,
            LuxonisOAKD.TOPICS.STEREO_CAMERA_INFO: LuxonisOAKD.stereo_fps,
            LuxonisOAKD.TOPICS.POINTCLOUD: LuxonisOAKD.stereo_fps,
            # Tracking of the IMU rate is not currently supported
        }

    @property
    def device_type(self) -> str:
        return self._device_type

    @device_type.setter
    def device_type(self, device_type: str) -> None:
        assert device_type in self.DEVICE_TYPES, (
            'Device type "%s" is not one of "%s"' % (
                device_type,
                self.DEVICE_TYPES
            )
        )
        self._device_type = device_type

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        self._width = width

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, height: int) -> None:
        self._height = height

    @property
    def fps(self) -> float:
        return self._fps

    @fps.setter
    def fps(self, fps: float) -> None:
        BaseSensor.assert_valid_rate(fps)
        self._fps = float(fps)

    @property
    def stereo_fps(self) -> float:
        return self._stereo_fps

    @stereo_fps.setter
    def stereo_fps(self, fps: float) -> None:
        BaseSensor.assert_valid_rate(fps)
        self._stereo_fps = float(fps)

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @ip_address.setter
    def ip_address(self, addr: str) -> None:
        if addr is not None and len(addr) > 0:
            # non-PoE models should have None for their address
            # only validate the address if necessary
            BaseSensor.assert_is_ipv4_address(addr)
        self._ip_address = addr

    @property
    def mx_id(self) -> str:
        return self._mx_id

    @mx_id.setter
    def mx_id(self, mx_id: str) -> None:
        self._mx_id = mx_id


class AxisCamera(BaseCamera):
    """PTZ and fixed cameras that use the axis_camera driver."""

    SERIAL = ''

    SENSOR_MODEL = 'axis_camera'
    TF_PREFIX = 'axis'

    CAMERA_INFO_URL = ''

    DOME_FIXED = 'dome_fixed'
    DOME_PTZ = 'dome_ptz'
    Q62 = 'q62'

    DEVICE_TYPE = DOME_PTZ
    DEVICE_TYPES = (
        Q62,
        DOME_PTZ,
        DOME_FIXED,
    )

    DEFAULT = DOME_FIXED

    HOSTNAME = '192.168.10.0'
    HTTP_PORT = 80
    USERNAME = 'root'
    PASSWORD = ''
    USE_ENCRYPTED_PASSWORD = True

    CAMERA = 1
    WIDTH = 640
    HEIGHT = 480
    FPS = 20

    ENABLE_PTZ = True
    MIN_PAN = -pi
    MAX_PAN = pi
    MIN_TILT = -pi/2
    MAX_TILT = pi/2
    MIN_ZOOM = 1
    MAX_ZOOM = 24
    MAX_PAN_SPEED = 2.61
    MAX_TILT_SPEED = 2.61

    ENABLE_IR = False
    ENABLE_WPER = False
    ENABLE_DEFOG = False

    ENABLE_PTZ_TELEOP = False
    BUTTON_ENABLE_PAN_TILT = -1
    BUTTON_ENABLE_ZOOM = -1
    AXIS_PAN = -1
    AXIS_TILT = -1
    INVERT_TILT = False
    AXIS_ZOOM_IN = -1
    AXIS_ZOOM_OUT = -1
    ZOOM_IN_OFFSET = 0.0
    ZOOM_OUT_OFFSET = 0.0
    ZOOM_IN_SCALE = 1.0
    ZOOM_OUT_SCALE = 1.0
    SCALE_PAN = 1.0
    SCALE_TILT = 1.0
    SCALE_ZOOM = 1.0

    class ROS_PARAMETER_KEYS:
        SERIAL = 'axis_camera.serial'  # required by superclass, not used locally

        DEVICE_TYPE = 'axis_camera.device_type'
        TF_PREFIX = 'axis_camera.tf_prefix'

        HOSTNAME = 'axis_camera.hostname'
        HTTP_PORT = 'axis_camera.http_port'
        CAMERA_INFO_URL = 'axis_camera.camera_info_url'

        USERNAME = 'axis_camera.username'
        PASSWORD = 'axis_camera.password'
        USE_ENCRYPTED_PASSWORD = 'axis_camera.use_encrypted_password'

        CAMERA = 'axis_camera.camera'
        WIDTH = 'axis_camera.width'
        HEIGHT = 'axis_camera.height'
        FPS = 'axis_camera.fps'

        # PTZ
        ENABLE_PTZ = 'axis_camera.ptz'
        MIN_PAN = 'axis_camera.min_pan'
        MAX_PAN = 'axis_camera.max_pan'
        MIN_TILT = 'axis_camera.min_tilt'
        MAX_TILT = 'axis_camera.max_tilt'
        MIN_ZOOM = 'axis_camera.min_zoom'
        MAX_ZOOM = 'axis_camera.max_zoom'
        MAX_PAN_SPEED = 'axis_camera.max_pan_speed'
        MAX_TILT_SPEED = 'axis_camera.max_tilt_speed'

        # Q62 additional services
        ENABLE_IR = 'axis_camera.ir'
        ENABLE_WIPER = 'axis_camera.wiper'
        ENABLE_DEFOG = 'axis_camera.defog'

        # PTZ Teleop (see axis_camera/config/teleop_ps4.yaml)
        ENABLE_PTZ_TELEOP = 'axis_camera.ptz_teleop'
        BUTTON_ENABLE_PAN_TILT = 'axis_camera.button_enable_pan_tilt'
        BUTTON_ENABLE_ZOOM = 'axis_camera.button_enable_zoom'
        AXIS_PAN = 'axis_camera.axis_pan'
        AXIS_TILT = 'axis_camera.axis_tilt'
        INVERT_TILT = 'axis_camera.invert_tilt'
        AXIS_ZOOM_IN = 'axis_camera.axis_zoom_in'
        AXIS_ZOOM_OUT = 'axis_camera.axis_zoom_out'
        ZOOM_IN_OFFSET = 'axis_camera.zoom_in_offset'
        ZOOM_OUT_OFFSET = 'axis_camera.zoom_out_offset'
        ZOOM_IN_SCALE = 'axis_camera.zoom_in_scale'
        ZOOM_OUT_SCALE = 'axis_camera.zoom_out_scale'
        SCALE_PAN = 'axis_camera.scale_pan'
        SCALE_TILT = 'axis_camera.scale_tilt'
        SCALE_ZOOM = 'axis_camera.scale_zoom'

    class TOPICS:
        COLOR_IMAGE = 'color_image'
        COLOR_CAMERA_INFO = 'color_camera_info'
        AUTOFOCUS = 'autofocus'
        AUTOIRIS = 'autoiris'
        BRIGHTNESS = 'brightness'
        FOCUS = 'focus'
        IRIS = 'iris'
        JOINT_STATES = 'joint_states'
        PTZ_STATE = 'ptz_state'

        NAME = {
            COLOR_IMAGE: 'color/image/compressed',
            COLOR_CAMERA_INFO: 'color/camera_info',
        }
        TYPE = {
            COLOR_IMAGE: 'sensor_msgs/msg/CompressedImage',
            COLOR_CAMERA_INFO: 'sensor_msgs/msg/CameraInfo',
        }

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseCamera.TOPIC,
            fps: int = FPS,
            serial: str = SERIAL,
            device_type: str = DEFAULT,

            hostname: str = HOSTNAME,
            http_port: int = HTTP_PORT,
            username: str = USERNAME,
            password: str = PASSWORD,
            use_encrypted_password: bool = USE_ENCRYPTED_PASSWORD,
            camera_info_url: str = CAMERA_INFO_URL,

            camera: int = CAMERA,
            width: int = WIDTH,
            height: int = HEIGHT,

            enable_ptz: bool = ENABLE_PTZ,
            min_pan: float = MIN_PAN,
            max_pan: float = MAX_PAN,
            min_tilt: float = MIN_TILT,
            max_tilt: float = MAX_TILT,
            min_zoom: float = MIN_ZOOM,
            max_zoom: float = MAX_ZOOM,
            max_pan_speed: float = MAX_PAN_SPEED,
            max_tilt_speed: float = MAX_TILT_SPEED,

            enable_ir: bool = ENABLE_IR,
            enable_wiper: bool = ENABLE_WPER,
            enable_defog: bool = ENABLE_DEFOG,

            enable_ptz_teleop: bool = ENABLE_PTZ_TELEOP,
            button_enable_pan_tilt: int = BUTTON_ENABLE_PAN_TILT,
            button_enable_zoom: int = BUTTON_ENABLE_ZOOM,
            axis_pan: int = AXIS_PAN,
            axis_tilt: int = AXIS_TILT,
            invert_tilt: bool = INVERT_TILT,
            axis_zoom_in: int = AXIS_ZOOM_IN,
            axis_zoom_out: int = AXIS_ZOOM_OUT,
            zoom_in_offset: float = ZOOM_IN_OFFSET,
            zoom_out_offset: float = ZOOM_OUT_OFFSET,
            zoom_in_scale: float = ZOOM_IN_SCALE,
            zoom_out_scale: float = ZOOM_OUT_SCALE,
            scale_pan: float = SCALE_PAN,
            scale_tilt: float = SCALE_TILT,
            scale_zoom: float = SCALE_ZOOM,

            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            ros_parameters: dict = BaseSensor.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseSensor.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:

        # Initializations
        self.tf_prefix = name

        self.hostname = hostname
        self.http_port = http_port
        self.username = username
        self.password = password
        self.use_encrypted_password = use_encrypted_password
        self.camera_info_url = camera_info_url

        self.camera = camera
        self.width = width
        self.height = height

        self.enable_ptz = enable_ptz
        self.min_pan = min_pan
        self.max_pan = max_pan
        self.min_tilt = min_tilt
        self.max_tilt = max_tilt
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.max_pan_speed = max_pan_speed
        self.max_tilt_speed = max_tilt_speed

        self.enable_ir = enable_ir
        self.enable_wiper = enable_wiper
        self.enable_defog = enable_defog

        self.enable_ptz_teleop = enable_ptz_teleop
        self.button_enable_pan_tilt = button_enable_pan_tilt
        self.button_enable_zoom = button_enable_zoom
        self.axis_pan = axis_pan
        self.axis_tilt = axis_tilt
        self.invert_tilt = invert_tilt
        self.axis_zoom_in = axis_zoom_in
        self.axis_zoom_out = axis_zoom_out
        self.zoom_in_offset = zoom_in_offset
        self.zoom_out_offset = zoom_out_offset
        self.zoom_in_scale = zoom_in_scale
        self.zoom_out_scale = zoom_out_scale
        self.scale_pan = scale_pan
        self.scale_tilt = scale_tilt
        self.scale_zoom = scale_zoom

        # ROS Parameter Template
        ros_parameters_template = {
            self.ROS_PARAMETER_KEYS.SERIAL: AxisCamera.serial,

            self.ROS_PARAMETER_KEYS.DEVICE_TYPE: AxisCamera.device_type,

            self.ROS_PARAMETER_KEYS.TF_PREFIX: AxisCamera.tf_prefix,

            self.ROS_PARAMETER_KEYS.HOSTNAME: AxisCamera.hostname,
            self.ROS_PARAMETER_KEYS.HTTP_PORT: AxisCamera.http_port,
            self.ROS_PARAMETER_KEYS.CAMERA_INFO_URL: AxisCamera.camera_info_url,

            self.ROS_PARAMETER_KEYS.USERNAME: AxisCamera.username,
            self.ROS_PARAMETER_KEYS.PASSWORD: AxisCamera.password,
            self.ROS_PARAMETER_KEYS.USE_ENCRYPTED_PASSWORD: AxisCamera.use_encrypted_password,

            self.ROS_PARAMETER_KEYS.CAMERA: AxisCamera.camera,
            self.ROS_PARAMETER_KEYS.WIDTH: AxisCamera.width,
            self.ROS_PARAMETER_KEYS.HEIGHT: AxisCamera.height,
            self.ROS_PARAMETER_KEYS.FPS: AxisCamera.fps,

            # PTZ
            self.ROS_PARAMETER_KEYS.ENABLE_PTZ: AxisCamera.enable_ptz,
            self.ROS_PARAMETER_KEYS.MIN_PAN: AxisCamera.min_pan,
            self.ROS_PARAMETER_KEYS.MAX_PAN: AxisCamera.max_pan,
            self.ROS_PARAMETER_KEYS.MIN_TILT: AxisCamera.min_tilt,
            self.ROS_PARAMETER_KEYS.MAX_TILT: AxisCamera.max_tilt,
            self.ROS_PARAMETER_KEYS.MIN_ZOOM: AxisCamera.min_zoom,
            self.ROS_PARAMETER_KEYS.MAX_ZOOM: AxisCamera.max_zoom,
            self.ROS_PARAMETER_KEYS.MAX_PAN_SPEED: AxisCamera.max_pan_speed,
            self.ROS_PARAMETER_KEYS.MAX_TILT_SPEED: AxisCamera.max_tilt_speed,

            # Q62 additional services
            self.ROS_PARAMETER_KEYS.ENABLE_IR: AxisCamera.enable_ir,
            self.ROS_PARAMETER_KEYS.ENABLE_WIPER: AxisCamera.enable_wiper,
            self.ROS_PARAMETER_KEYS.ENABLE_DEFOG: AxisCamera.enable_defog,

            # PTZ Teleop (see axis_camera/config/teleop_ps4.yaml)
            self.ROS_PARAMETER_KEYS.ENABLE_PTZ_TELEOP: AxisCamera.enable_ptz_teleop,
            self.ROS_PARAMETER_KEYS.BUTTON_ENABLE_PAN_TILT: AxisCamera.button_enable_pan_tilt,
            self.ROS_PARAMETER_KEYS.BUTTON_ENABLE_ZOOM: AxisCamera.button_enable_zoom,
            self.ROS_PARAMETER_KEYS.AXIS_PAN: AxisCamera.axis_pan,
            self.ROS_PARAMETER_KEYS.AXIS_TILT: AxisCamera.axis_tilt,
            self.ROS_PARAMETER_KEYS.INVERT_TILT: AxisCamera.invert_tilt,
            self.ROS_PARAMETER_KEYS.AXIS_ZOOM_IN: AxisCamera.axis_zoom_in,
            self.ROS_PARAMETER_KEYS.AXIS_ZOOM_OUT: AxisCamera.axis_zoom_out,
            self.ROS_PARAMETER_KEYS.ZOOM_IN_OFFSET: AxisCamera.zoom_in_offset,
            self.ROS_PARAMETER_KEYS.ZOOM_OUT_OFFSET: AxisCamera.zoom_out_offset,
            self.ROS_PARAMETER_KEYS.ZOOM_IN_SCALE: AxisCamera.zoom_in_scale,
            self.ROS_PARAMETER_KEYS.ZOOM_OUT_SCALE: AxisCamera.zoom_out_scale,
            self.ROS_PARAMETER_KEYS.SCALE_PAN: AxisCamera.scale_pan,
            self.ROS_PARAMETER_KEYS.SCALE_TILT: AxisCamera.scale_tilt,
            self.ROS_PARAMETER_KEYS.SCALE_ZOOM: AxisCamera.scale_zoom,
        }
        # Initialization
        self.device_type: str = device_type
        super().__init__(
            idx,
            name,
            topic,
            fps,
            serial,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            ros_parameters_template,
            parent,
            xyz,
            rpy
        )
        # Topic Rates
        self.rates = {
            AxisCamera.TOPICS.COLOR_IMAGE: AxisCamera.fps,
            AxisCamera.TOPICS.COLOR_CAMERA_INFO: AxisCamera.fps,
        }

    @property
    def device_type(self) -> str:
        return self._device_type

    @device_type.setter
    def device_type(self, device_type: str) -> None:
        assert device_type in self.DEVICE_TYPES, (
            'Device type "%s" is not one of "%s"' % (
                device_type,
                self.DEVICE_TYPES
            )
        )
        self._device_type = device_type

    @property
    def tf_prefix(self) -> str:
        return self._tf_prefix

    @tf_prefix.setter
    def tf_prefix(self, prefix: str) -> None:
        self._tf_prefix = prefix

    @property
    def hostname(self) -> str:
        return self._hostname

    @hostname.setter
    def hostname(self, hostname: str) -> None:
        self._hostname = hostname

    @property
    def http_port(self) -> int:
        return self._http_port

    @http_port.setter
    def http_port(self, port: int) -> None:
        assert port >= 0 and port <= 65535, (
            f'Port {port} must be in range [0, 65535]'
        )
        self._http_port = port

    @property
    def camera_info_url(self) -> str:
        return self._camera_info_url

    @camera_info_url.setter
    def camera_info_url(self, url: str) -> None:
        self._camera_info_url = url

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str) -> None:
        assert len(username) > 0, 'Username cannot be empty'
        self._username = username

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        self._password = password

    @property
    def use_encrypted_password(self) -> bool:
        return self._use_encrypted_password

    @use_encrypted_password.setter
    def use_encrypted_password(self, encrypt: bool) -> None:
        self._use_encrypted_password = encrypt

    @property
    def camera(self) -> int:
        return self._camera

    @camera.setter
    def camera(self, num: int) -> None:
        assert num >= 0, f'Camera number {num} cannot be negative'
        self._camera = num

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int) -> None:
        assert width > 0, f'Frame width {width} must be positive'
        self._width = width

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, height: int) -> None:
        assert height > 0, f'Frame height {height} must be positive'
        self._height = height

    @property
    def enable_ptz(self) -> bool:
        return self._enable_ptz

    @enable_ptz.setter
    def enable_ptz(self, enable: bool) -> None:
        self._enable_ptz = enable

    @property
    def min_pan(self) -> float:
        return self._min_pan

    @min_pan.setter
    def min_pan(self, pan: float) -> None:
        assert pan >= -pi and pan <= pi, f'Min pan {pan} must be in range [-pi, pi]'
        self._min_pan = pan

    @property
    def max_pan(self) -> float:
        return self._max_pan

    @max_pan.setter
    def max_pan(self, pan: float) -> None:
        assert pan >= -pi and pan <= pi, f'Max pan {pan} must be in range [-pi, pi]'
        self._max_pan = pan

    @property
    def min_tilt(self) -> float:
        return self._min_tilt

    @min_tilt.setter
    def min_tilt(self, tilt: float) -> None:
        assert tilt >= -pi/2 and tilt <= pi/2, f'Min tilt {tilt} must be in range [-pi/2, pi/2]'
        self._min_tilt = tilt

    @property
    def max_tilt(self) -> float:
        return self._max_tilt

    @max_tilt.setter
    def max_tilt(self, tilt: float) -> None:
        assert tilt >= -pi/2 and tilt <= pi/2, f'Max tilt {tilt} must be in range [-pi/2, pi/2]'
        self._max_tilt = tilt

    @property
    def min_zoom(self) -> float:
        return self._min_zoom

    @min_zoom.setter
    def min_zoom(self, zoom: float) -> None:
        assert zoom > 0, f'Min zoom {zoom} must be positive'
        self._min_zoom = zoom

    @property
    def max_zoom(self) -> float:
        return self._max_zoom

    @max_zoom.setter
    def max_zoom(self, zoom: float) -> None:
        assert zoom > 0, f'Max zoom {zoom} must be positive'
        self._max_zoom = zoom

    @property
    def max_pan_speed(self) -> float:
        return self._max_pan_speed

    @max_pan_speed.setter
    def max_pan_speed(self, speed: float) -> None:
        assert speed > 0, f'Max pan speed {speed} must be positive'
        self._max_pan_speed = speed

    @property
    def max_tilt_speed(self) -> float:
        return self._max_tilt_speed

    @max_tilt_speed.setter
    def max_tilt_speed(self, speed: float) -> None:
        assert speed > 0, f'Max tilt speed {speed} must be positive'
        self._max_tilt_speed = speed

    @property
    def enable_ir(self) -> bool:
        return self._enable_ir

    @enable_ir.setter
    def enable_ir(self, enable: bool) -> None:
        self._enable_ir = enable

    @property
    def enable_wiper(self) -> bool:
        return self._enable_wiper

    @enable_wiper.setter
    def enable_wiper(self, enable: bool) -> None:
        self._enable_wiper = enable

    @property
    def enable_defog(self) -> bool:
        return self._enable_defog

    @enable_defog.setter
    def enable_defog(self, enable: bool) -> None:
        self._enable_defog = enable

    @property
    def enable_ptz_teleop(self) -> bool:
        return self._enable_ptz_teleop

    @enable_ptz_teleop.setter
    def enable_ptz_teleop(self, enable: bool) -> None:
        self._enable_ptz_teleop = enable

    @property
    def invert_tilt(self) -> bool:
        return self._invert_tilt

    @invert_tilt.setter
    def invert_tilt(self, enable: bool) -> None:
        self._invert_tilt = enable

    @property
    def button_enable_pan_tilt(self) -> int:
        return self._button_enable_pan_tilt

    @button_enable_pan_tilt.setter
    def button_enable_pan_tilt(self, button: int) -> None:
        self._button_enable_pan_tilt = button

    @property
    def button_enable_zoom(self) -> int:
        return self._button_enable_zoom

    @button_enable_zoom.setter
    def button_enable_zoom(self, button: int) -> None:
        self._button_enable_zoom = button

    @property
    def axis_pan(self) -> int:
        return self._axis_pan

    @axis_pan.setter
    def axis_pan(self, axis: int) -> None:
        self._axis_pan = axis

    @property
    def axis_tilt(self) -> int:
        return self._axis_tilt

    @axis_tilt.setter
    def axis_tilt(self, axis: int) -> None:
        self._axis_tilt = axis

    @property
    def axis_zoom_in(self) -> int:
        return self._axis_zoom_in

    @axis_zoom_in.setter
    def axis_zoom_in(self, axis: int) -> None:
        self._axis_zoom_in = axis

    @property
    def axis_zoom_out(self) -> int:
        return self._axis_zoom_out

    @axis_zoom_out.setter
    def axis_zoom_out(self, axis: int) -> None:
        self._axis_zoom_out = axis

    @property
    def zoom_in_offset(self) -> float:
        return self._zoom_in_offset

    @zoom_in_offset.setter
    def zoom_in_offset(self, offset: float) -> None:
        self._zoom_in_offset = offset

    @property
    def zoom_out_offset(self) -> float:
        return self._zoom_out_offset

    @zoom_out_offset.setter
    def zoom_out_offset(self, offset: float) -> None:
        self._zoom_out_offset = offset

    @property
    def zoom_in_scale(self) -> float:
        return self._zoom_in_scale

    @zoom_in_scale.setter
    def zoom_in_scale(self, scale: float) -> None:
        self._zoom_in_scale = scale

    @property
    def zoom_out_scale(self) -> float:
        return self._zoom_out_scale

    @zoom_out_scale.setter
    def zoom_out_scale(self, scale: float) -> None:
        self._zoom_out_scale = scale

    @property
    def scale_pan(self) -> float:
        return self._scale_pan

    @scale_pan.setter
    def scale_pan(self, scale: float) -> None:
        self._scale_pan = scale

    @property
    def scale_tilt(self) -> float:
        return self._scale_tilt

    @scale_tilt.setter
    def scale_tilt(self, scale: float) -> None:
        self._scale_tilt = scale

    @property
    def scale_zoom(self) -> float:
        return self._scale_zoom

    @scale_zoom.setter
    def scale_zoom(self, scale: float) -> None:
        self._scale_zoom = scale
