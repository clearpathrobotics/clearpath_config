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
from clearpath_config.sensors.types.sensor import BaseSensor
from clearpath_config.common.utils.dictionary import extend_flat_dict
from typing import List


class BaseCamera(BaseSensor):
    SENSOR_TYPE = "camera"
    SENSOR_MODEL = "base"
    TOPIC = "image"

    FPS = 30
    SERIAL = "0"

    class ROS_PARAMETER_KEYS:
        FPS = "node_name.fps"
        SERIAL = "node_name.serial"

    class TOPICS:
        COLOR_IMAGE = "color_image"
        COLOR_CAMERA_INFO = "color_camera_info"
        NAME = {
            COLOR_IMAGE: "color/image",
            COLOR_CAMERA_INFO: "color/camera_info"
        }
        RATE = {
            COLOR_IMAGE: 30,
            COLOR_CAMERA_INFO: 30,
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
        self.fps = int()
        self.set_fps(fps)
        # Serial Number:
        # - camera unique serial number for multi-camera setups
        # - usually an integer value
        self.serial = str()
        self.set_serial(serial)
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

    @property
    def fps(self) -> int:
        return self._fps

    @fps.setter
    def fps(self, fps: int) -> None:
        BaseCamera.assert_valid_fps(fps)
        self._fps = fps

    def get_fps(self) -> int:
        return self.fps

    def set_fps(self, fps: int) -> None:
        self.fps = fps

    @staticmethod
    def assert_valid_fps(fps: int) -> None:
        assert isinstance(fps, int), (
            "FPS '%s' is invalid, must be an integer." % fps
        )
        assert 0 <= fps, (
            "FPS '%s' must be a positive integer." % fps
        )

    @property
    def serial(self) -> str:
        return self._serial

    @serial.setter
    def serial(self, serial: str) -> None:
        self._serial = str(serial)

    def get_serial(self) -> str:
        return self.serial

    def set_serial(self, serial: str) -> None:
        self.serial = serial


class IntelRealsense(BaseCamera):
    SENSOR_MODEL = "intel_realsense"

    D415 = "d415"
    D435 = "d435"
    D435i = "d435i"
    DEVICE_TYPE = D435
    DEVICE_TYPES = [D415, D435, D435i]

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
        FPS = "camera.rgb_camera.profile"
        SERIAL = "camera.serial_no"
        CAMERA_NAME = "camera.camera_name"
        DEVICE_TYPE = "camera.device_type"
        DEPTH_PROFILE = "camera.depth_module.profile"
        DEPTH_ENABLE = "camera.enable_depth"
        COLOR_ENABLE = "camera.enable_color"
        POINTCLOUD_ENABLE = "camera.pointcloud.enable"

    class TOPICS:
        COLOR_IMAGE = "color_image"
        COLOR_CAMERA_INFO = "color_camera_info"
        DEPTH_IMAGE = "depth_image"
        DEPTH_CAMERA_INFO = "depth_camera_info"
        POINTCLOUD = "points"
        IMU = "imu"
        NAME = {
            COLOR_IMAGE: "color/image",
            COLOR_CAMERA_INFO: "color/camera_info",
            DEPTH_IMAGE: "depth/image",
            DEPTH_CAMERA_INFO: "depth/camera_info",
            POINTCLOUD: "points",
            IMU: "imu"
        }
        RATE = {
            COLOR_IMAGE: BaseCamera.FPS,
            COLOR_CAMERA_INFO: BaseCamera.FPS,
            DEPTH_IMAGE: BaseCamera.FPS,
            DEPTH_CAMERA_INFO: BaseCamera.FPS,
            POINTCLOUD: BaseCamera.FPS,
            IMU: BaseCamera.FPS
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
        self.TOPICS.RATE[self.TOPICS.COLOR_IMAGE] = self.fps
        self.TOPICS.RATE[self.TOPICS.COLOR_CAMERA_INFO] = self.fps
        self.TOPICS.RATE[self.TOPICS.DEPTH_IMAGE] = self.fps
        self.TOPICS.RATE[self.TOPICS.DEPTH_CAMERA_INFO] = self.fps
        self.TOPICS.RATE[self.TOPICS.POINTCLOUD] = self.fps
        self.TOPICS.RATE[self.TOPICS.IMU] = self.fps
        # Initialization
        self.device_type: str = IntelRealsense.DEVICE_TYPE
        self.set_device_type(device_type)
        # Color Image
        self.color_enabled: bool = IntelRealsense.COLOR_ENABLED
        self.color_width: int = IntelRealsense.COLOR_WIDTH
        self.color_height: int = IntelRealsense.COLOR_HEIGHT
        self.set_color_enabled(color_enabled)
        self.set_color_width(color_width)
        self.set_color_height(color_height)
        # Depth Image
        self.depth_enabled: bool = IntelRealsense.DEPTH_ENABLED
        self.depth_width: int = IntelRealsense.DEPTH_WIDTH
        self.depth_height: int = IntelRealsense.DEPTH_HEIGHT
        self.depth_fps: int = IntelRealsense.DEPTH_FPS
        self.set_depth_enabled(depth_enabled)
        self.set_depth_width(depth_width)
        self.set_depth_height(depth_height)
        self.set_depth_fps(depth_fps)
        # Pointcloud
        self.pointcloud_enabled: bool = IntelRealsense.POINTCLOUD_ENABLED
        self.set_pointcloud_enabled(pointcloud_enabled)

    @staticmethod
    def clean_profile(profile: str | list) -> list:
        if isinstance(profile, str):
            profile = profile.split(",")
            assert len(profile) == 3, (
                "Profile '%s' is not three comma separated values")
            try:
                profile = [int(entry) for entry in profile]
            except ValueError:
                raise AssertionError(
                    "Profile '%s' cannot be cast to integer")
        else:
            assert len(profile) == 3, (
                "Profile '%s' is not three integer values")
            assert all([isinstance(entry, int) for entry in profile]), (
                "Profile '%s' is not three integer values")
        return profile

    def assert_pixel_length(
            self,
            length: int
            ) -> None:
        assert isinstance(length, int), (
            "Pixel value must be integer"
        )
        assert length >= 0, (
            "Pixel length must be positive"
        )

    @property
    def camera_name(self) -> str:
        return self.get_name()

    @camera_name.setter
    def camera_name(self, name: str) -> None:
        self._camera_name = name

    @property
    def device_type(self) -> str:
        return self._device_type

    @device_type.setter
    def device_type(self, device_type: str) -> None:
        assert device_type in self.DEVICE_TYPES, (
            "Device type '%s' is not one of '%s'" % (
                device_type,
                self.DEVICE_TYPES
            )
        )
        self._device_type = device_type

    def get_device_type(self) -> str:
        return self.device_type

    def set_device_type(self, device_type: str) -> None:
        self.device_type = device_type

    @property
    def color_enabled(self) -> bool:
        return self._color_enabled

    @color_enabled.setter
    def color_enabled(self, enabled: bool) -> None:
        self._color_enabled = bool(enabled)

    def enable_color(self) -> None:
        self.color_enabled = True

    def disable_color(self) -> None:
        self.color_enabled = False

    def is_color_enabled(self) -> bool:
        return self.color_enabled

    def get_color_enabled(self) -> bool:
        return self.color_enabled

    def set_color_enabled(self, enable: bool) -> None:
        self.color_enabled = bool(enable)

    def set_color_fps(self, fps: int) -> None:
        self.set_fps(fps)

    def get_color_fps(self) -> int:
        return self.get_fps()

    @property
    def color_height(self) -> int:
        return self._color_height

    @color_height.setter
    def color_height(self, height: int) -> None:
        self.assert_pixel_length(height)
        self._color_height = height

    def set_color_height(self, height: int) -> None:
        self.color_height = height

    def get_color_height(self) -> int:
        return self.color_height

    @property
    def color_width(self) -> int:
        return self._color_width

    @color_width.setter
    def color_width(self, width: int) -> None:
        self.assert_pixel_length(width)
        self._color_width = width

    def set_color_width(self, width: int) -> None:
        self.color_width = width

    def get_color_width(self) -> int:
        return self.color_width

    @property
    def color_profile(self) -> str:
        return "%s,%s,%s" % (
            self.color_width,
            self.color_height,
            self.fps
        )

    @color_profile.setter
    def color_profile(self, profile: str | list) -> None:
        profile = self.clean_profile(profile)
        self.color_width = profile[0]
        self.color_height = profile[1]
        self.fps = profile[2]

    def set_color_profile(self, profile: str | list) -> None:
        self.color_profile = profile

    def get_color_profile(self) -> str:
        return self.color_profile

    @property
    def depth_enabled(self) -> bool:
        return self._depth_enabled

    @depth_enabled.setter
    def depth_enabled(self, enabled: bool) -> None:
        self._depth_enabled = bool(enabled)

    def enable_depth(self) -> None:
        self.depth_enabled = True

    def disable_depth(self) -> None:
        self.depth_enabled = False

    def is_depth_enabled(self) -> bool:
        return self.depth_enabled

    def get_depth_enabled(self) -> bool:
        return self.depth_enabled

    def set_depth_enabled(self, enable: bool) -> None:
        self.depth_enabled = bool(enable)

    @property
    def depth_fps(self) -> int:
        return self._depth_fps

    @depth_fps.setter
    def depth_fps(self, fps: int) -> None:
        self.assert_valid_fps(fps)
        self._depth_fps = fps

    def set_depth_fps(self, fps: int) -> None:
        self.depth_fps = fps

    def get_depth_fps(self) -> int:
        return self.depth_fps

    @property
    def depth_width(self) -> int:
        return self._depth_width

    @depth_width.setter
    def depth_width(self, width: int) -> None:
        self.assert_pixel_length(width)
        self._depth_width = width

    def set_depth_width(self, width: int) -> None:
        self.depth_width = width

    def get_depth_width(self) -> int:
        return self.depth_width

    @property
    def depth_height(self) -> int:
        return self._depth_height

    @depth_height.setter
    def depth_height(self, height: int) -> None:
        self.assert_pixel_length(height)
        self._depth_height = height

    def set_depth_height(self, height: int) -> None:
        self.depth_height = height

    def get_depth_height(self) -> int:
        return self.depth_height

    @property
    def depth_profile(self) -> str:
        return "%s,%s,%s" % (
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

    def set_depth_profile(self, profile: str | list) -> None:
        self.depth_profile = profile

    def get_depth_profile(self) -> str:
        return self.depth_profile

    @property
    def pointcloud_enabled(self) -> bool:
        return self._pointcloud_enabled

    @pointcloud_enabled.setter
    def pointcloud_enabled(self, enabled: bool) -> None:
        self._pointcloud_enabled = bool(enabled)

    def enable_pointcloud(self) -> None:
        self.pointcloud_enabled = True

    def disable_pointcloud(self) -> None:
        self.pointcloud_enabled = False

    def is_pointcloud_enabled(self) -> bool:
        return self.pointcloud_enabled

    def get_pointcloud_enabled(self) -> bool:
        return self.pointcloud_enabled

    def set_pointcloud_enabled(self, enable: bool) -> None:
        self.pointcloud_enabled = bool(enable)


class FlirBlackfly(BaseCamera):
    SENSOR_MODEL = "flir_blackfly"

    USB3_CONNECTION = "USB3"
    GIGE_CONNECTION = "GigE"
    CONNECTION_TYPE = USB3_CONNECTION
    CONNECTION_TYPES = [USB3_CONNECTION, GIGE_CONNECTION]

    MONO_8 = "Mono8"
    MONO_16 = "Mono16"
    MONO_12 = "Mono12p"
    MONO_12_PACKED = "Mono12Packed"
    YUV_411_PACKED = "YUV411Packed"
    YUV_422_PACKED = "YUV422Packed"
    YUV_444_PACKED = "YUV444Packed"
    YCBCR_8 = "YCbCr8"
    YCBCR_422_8 = "YCbCr422_8"
    YCBCR_411_8 = "YCbCr411_8"
    BGR_8 = "BGR8"
    BGRA_8 = "BGRa8"
    RGB_8_PACKED = "RGB8Packed"
    BAYER_GR8 = "BayerGR8"
    BAYER_RG8 = "BayerRG8"
    BAYER_GB8 = "BayerGB8"
    BAYER_BG8 = "BayerBG8"
    BAYER_GR16 = "BayerGR16"
    BAYER_RG16 = "BayerRG16"
    BAYER_GB16 = "BayerGB16"
    BAYER_BG16 = "BayerBG16"
    BAYER_GR12 = "BayerGR12p"
    BAYER_RG12 = "BayerRG12p"
    BAYER_GB12 = "BayerGB12p"
    BAYER_BG12 = "BayerBG12p"
    BAYER_GR12_PACKED = "BayerGR12Packed"
    BAYER_RG12_PACKED = "BayerRG12Packed"
    BAYER_GB12_PACKED = "BayerGB12Packed"
    BAYER_BG12_PACKED = "BayerBG12Packed"

    ENCODINGS = [
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
    ]

    class ROS_PARAMETER_KEYS:
        FPS = "flir_blackfly.frame_rate"
        SERIAL = "flir_blackfly.serial_number"
        ENCODING = "flir_blackfly.pixel_format"

    class TOPICS:
        COLOR_IMAGE = "color_image"
        COLOR_CAMERA_INFO = "color_camera_info"
        NAME = {
            COLOR_IMAGE: "color/image",
            COLOR_CAMERA_INFO: "color/camera_info"
        }
        RATE = {
            COLOR_IMAGE: BaseCamera.FPS,
            COLOR_CAMERA_INFO: BaseCamera.FPS,
        }

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
        self.TOPICS.RATE[self.TOPICS.COLOR_IMAGE] = self.fps
        self.TOPICS.RATE[self.TOPICS.COLOR_CAMERA_INFO] = self.fps
        # Initialization
        self.connection_type: str = FlirBlackfly.CONNECTION_TYPE
        self.set_connection_type(connection_type)
        self.encoding: str = FlirBlackfly.BAYER_RG8
        self.set_encoding(encoding)

    @property
    def connection_type(self) -> str:
        return self._connection_type

    @connection_type.setter
    def connection_type(self, type: str) -> None:
        assert type in FlirBlackfly.CONNECTION_TYPES
        self._connection_type = type

    def set_connection_type(self, connection_type: str) -> None:
        self.connection_type = connection_type

    def get_connection_type(self) -> str:
        return self.connection_type

    @property
    def encoding(self) -> str:
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: str) -> None:
        assert encoding in FlirBlackfly.ENCODINGS, (
            "Encoding '%s' not found in support encodings: '%s'" % (
                encoding, FlirBlackfly.ENCODINGS
            )
        )
        self._encoding = encoding

    def set_encoding(self, encoding: str) -> None:
        self.encoding = encoding

    def get_encoding(self) -> str:
        return self.encoding
