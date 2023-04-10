from clearpath_config.sensors.base import BaseSensor, Accessory, List


class BaseCamera(BaseSensor):
    """
    Common Camera Class.
        - contains all common camera parameters
        - all cameras must be of type Camera.Common
    """
    SENSOR_MODEL = "camera"
    CAMERA_MODEL = "base"
    NAME = SENSOR_MODEL + "_0"
    TOPIC = NAME + "/image"

    FPS = 30
    SERIAL = "0"

    def __init__(
            self,
            name: str = NAME,
            topic: str = TOPIC,
            fps: int = FPS,
            serial: str = SERIAL,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(
            name,
            topic,
            urdf_enabled,
            launch_enabled,
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


class Realsense(BaseCamera):
    """
    Realsense Camera Class.
    - Width: [640] : Width of image image
    - Height: [480] : Height of color image
    - Depth Enable : [True] : Toggle for depth data acquisition.
        - Depth FPS: [30] : Framerate of depth camera.
        - Depth Width: [640] : Width of depth image.
        - Depth Height: [480] : Height of depth image.
    """
    CAMERA_MODEL = "realsense"

    FPS = 30
    WIDTH = 640
    HEIGHT = 480

    DEPTH_ENABLED = True
    DEPTH_FPS = 30
    DEPTH_WIDTH = 640
    DEPTH_HEIGHT = 480

    def __init__(
            self,
            name: str = BaseCamera.NAME,
            topic: str = BaseCamera.TOPIC,
            fps: int = FPS,
            serial: str = BaseCamera.SERIAL,
            width: int = WIDTH,
            height: int = HEIGHT,
            depth_enabled: bool = DEPTH_ENABLED,
            depth_fps: int = DEPTH_FPS,
            depth_width: int = DEPTH_WIDTH,
            depth_height: int = DEPTH_HEIGHT,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(
            name,
            topic,
            fps,
            serial,
            urdf_enabled,
            launch_enabled,
            parent,
            xyz,
            rpy
        )
        self.width: int = Realsense.WIDTH
        self.set_width(width)
        self.height: int = Realsense.HEIGHT
        self.set_height(height)
        self.depth_enabled: bool = Realsense.DEPTH_ENABLED
        self.enable_depth() if depth_enabled else self.disable_depth()
        self.depth_fps: int = Realsense.DEPTH_FPS
        self.set_depth_fps(depth_fps)
        self.depth_width: int = Realsense.DEPTH_WIDTH
        self.set_depth_width(depth_width)
        self.detph_height: int = Realsense.DEPTH_HEIGHT
        self.set_depth_height(depth_height)

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

    def set_height(self, height: int) -> None:
        self.assert_pixel_length(height)
        self.height = height

    def get_height(self) -> int:
        return self.get_height

    def set_width(self, width: int) -> None:
        self.assert_pixel_length(width)
        self.width = width

    def get_width(self) -> int:
        return self.get_width

    def enable_depth(self) -> None:
        self.depth_enabled = True

    def disable_depth(self) -> None:
        self.depth_enabled = False

    def is_depth_enabled(self) -> bool:
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


class Blackfly(BaseCamera):
    """
    Blackfly Camera Class
    Parameters:
    - Device: [USB3 or GigE] : Device connection type.
    - Encoding: [BayerRG8] : Image encoding.
                    Must use BayerRG8 encoding to get more than 15 FPS.
    """
    CAMERA_MODEL = "blackfly"

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
            name: str = BaseCamera.NAME,
            topic: str = BaseCamera.TOPIC,
            connection_type: str = CONNECTION_TYPE,
            encoding: str = BAYER_RG8,
            fps: int = BaseCamera.FPS,
            serial: str = BaseCamera.SERIAL,
            urdf_enabled: bool = BaseSensor.URDF_ENABLED,
            launch_enabled: bool = BaseSensor.LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(
            name,
            topic,
            fps,
            serial,
            urdf_enabled,
            launch_enabled,
            parent,
            xyz,
            rpy
        )
        self.connection_type: str = Blackfly.CONNECTION_TYPE
        self.set_connection_type(connection_type)
        self.encoding: str = Blackfly.BAYER_RG8
        self.set_encoding(encoding)

    def set_connection_type(self, connection_type: str) -> None:
        assert connection_type in Blackfly.CONNECTION_TYPES
        self.connection_type = connection_type

    def get_connection_type(self) -> str:
        return self.connection_type

    def set_encoding(self, encoding: str) -> None:
        assert encoding in Blackfly.ENCODINGS, (
            "Encoding '%s' not found in support encodings: '%s'" % (
                encoding, Blackfly.ENCODINGS
            )
        )
        self.encoding = encoding

    def get_encoding(self) -> str:
        return self.encoding
