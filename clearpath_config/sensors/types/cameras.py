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
from typing import List


class BaseCamera(BaseSensor):
    SENSOR_TYPE = "camera"
    SENSOR_MODEL = "base"
    TOPIC = "image"

    FPS = 30
    SERIAL = "0"

    class ROS_PARAMETER_KEYS:
        FPS = "fps"
        SERIAL = "serial"

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
            rpy,
            )
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

    def get_fps(self) -> int:
        return self.fps

    def set_fps(self, fps: int) -> None:
        BaseCamera.assert_valid_fps(fps)
        self.fps = fps

    @staticmethod
    def assert_valid_fps(fps: int) -> None:
        assert isinstance(fps, int), (
            "FPS '%s' is invalid, must be an integer." % fps
        )
        assert 0 <= fps, (
            "FPS '%s' must be a positive integer." % fps
        )

    def get_serial(self) -> str:
        return self.serial

    def set_serial(self, serial: str) -> None:
        self.serial = str(serial)


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
        CAMERA_NAME = "camera_name"
        SERIAL = "serial_no"
        DEVICE_TYPE = "device_type"
        DEPTH_PROFILE = "depth_module.profile"
        DEPTH_ENABLE = "enable_depth"
        COLOR_PROFILE = "rgb_camera.profile"
        COLOR_ENABLE = "enable_color"
        POINTCLOUD_ENABLE = "pointcloud.enable"

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
        super().__init__(
            idx,
            name,
            topic,
            color_fps,
            serial,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )
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
        # ROS Parameter Keys
        pairs = {
            # Camera Name
            self.ROS_PARAMETER_KEYS.CAMERA_NAME: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.CAMERA_NAME,
                    get=lambda obj: obj.get_name(),
                    set=lambda obj, val: obj.set_name(val)
                )
            ),
            # Device Type
            self.ROS_PARAMETER_KEYS.DEVICE_TYPE: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.DEVICE_TYPE,
                    get=lambda obj: obj.get_device_type(),
                    set=lambda obj, val: obj.set_device_type(val)
                )
            ),
            # Device Serial
            self.ROS_PARAMETER_KEYS.SERIAL: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.SERIAL,
                    get=lambda obj: obj.get_serial(),
                    set=lambda obj, val: obj.set_serial(val)
                )
            ),
            # Color Enable
            self.ROS_PARAMETER_KEYS.COLOR_ENABLE: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.COLOR_ENABLE,
                    get=lambda obj: obj.get_color_enabled(),
                    set=lambda obj, val: obj.set_color_enabled(val)
                )
            ),
            # Color Profile
            self.ROS_PARAMETER_KEYS.COLOR_PROFILE: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.COLOR_PROFILE,
                    get=lambda obj: obj.get_color_profile(),
                    set=lambda obj, val: obj.set_color_profile(val)
                )
            ),
            # Depth Enable
            self.ROS_PARAMETER_KEYS.DEPTH_ENABLE: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.DEPTH_ENABLE,
                    get=lambda obj: obj.get_depth_enabled(),
                    set=lambda obj, val: obj.set_depth_enabled(val)
                )
            ),
            # Depth Profile
            self.ROS_PARAMETER_KEYS.DEPTH_PROFILE: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.DEPTH_PROFILE,
                    get=lambda obj: obj.get_depth_profile(),
                    set=lambda obj, val: obj.set_depth_profile(val)
                )
            ),
            # Pointcloud Enable
            self.ROS_PARAMETER_KEYS.POINTCLOUD_ENABLE: (
                BaseSensor.ROSParameter(
                    key=self.ROS_PARAMETER_KEYS.POINTCLOUD_ENABLE,
                    get=lambda obj: obj.get_pointcloud_enabled(),
                    set=lambda obj, val: obj.set_pointcloud_enabled(val)
                )
            ),
        }
        self.ros_parameter_pairs.update(pairs)
        self.set_ros_parameters(ros_parameters)

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
        assert length > 0, (
            "Pixel length must be positive"
        )

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

    def set_color_height(self, height: int) -> None:
        self.assert_pixel_length(height)
        self.height = height

    def get_color_height(self) -> int:
        return self.color_height

    def set_color_width(self, width: int) -> None:
        self.assert_pixel_length(width)
        self.width = width

    def get_color_width(self) -> int:
        return self.color_width

    def set_color_profile(self, profile: str | list) -> None:
        profile = self.clean_profile(profile)
        self.set_color_width(profile[0])
        self.set_color_height(profile[1])
        self.set_color_fps(profile[2])

    def get_color_profile(self) -> str:
        return "%s,%s,%s" % (
            self.get_color_width(),
            self.get_color_height(),
            self.get_color_fps()
        )

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

    def set_depth_fps(self, fps: int) -> None:
        self.assert_valid_fps(fps)
        self.depth_fps = fps

    def get_depth_fps(self) -> int:
        return self.depth_fps

    def set_depth_width(self, width: int) -> None:
        self.assert_pixel_length(width)
        self.depth_width = width

    def get_depth_width(self) -> int:
        return self.depth_width

    def set_depth_height(self, height: int) -> None:
        self.assert_pixel_length(height)
        self.depth_height = height

    def get_depth_height(self) -> int:
        return self.depth_height

    def set_depth_profile(self, profile: str | list) -> None:
        profile = self.clean_profile(profile)
        self.set_depth_width(profile[0])
        self.set_depth_height(profile[1])
        self.set_depth_fps(profile[2])

    def get_depth_profile(self) -> str:
        return "%s,%s,%s" % (
            self.get_depth_width(),
            self.get_depth_height(),
            self.get_depth_fps()
        )

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

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = BaseCamera.TOPIC,
            connection_type: str = CONNECTION_TYPE,
            encoding: str = BAYER_RG8,
            fps: int = BaseCamera.FPS,
            serial: str = BaseCamera.SERIAL,
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
            fps,
            serial,
            urdf_enabled,
            launch_enabled,
            ros_parameters,
            parent,
            xyz,
            rpy
        )
        self.connection_type: str = FlirBlackfly.CONNECTION_TYPE
        self.set_connection_type(connection_type)
        self.encoding: str = FlirBlackfly.BAYER_RG8
        self.set_encoding(encoding)

    def set_connection_type(self, connection_type: str) -> None:
        assert connection_type in FlirBlackfly.CONNECTION_TYPES
        self.connection_type = connection_type

    def get_connection_type(self) -> str:
        return self.connection_type

    def set_encoding(self, encoding: str) -> None:
        assert encoding in FlirBlackfly.ENCODINGS, (
            "Encoding '%s' not found in support encodings: '%s'" % (
                encoding, FlirBlackfly.ENCODINGS
            )
        )
        self.encoding = encoding

    def get_encoding(self) -> str:
        return self.encoding
