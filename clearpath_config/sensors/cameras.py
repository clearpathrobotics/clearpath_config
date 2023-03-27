from clearpath_config.sensors.base import BaseSensor, Accessory, List


class Camera:

    class Common(BaseSensor):
        """
        Common Camera Class.
         - contains all common camera parameters
         - all cameras must be of type Camera.Common
        """
        FPS = 30
        SERIAL = "0"

        def __init__(
                self,
                name: str,
                topic: str,
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
            self.assert_valid_fps()
            self.fps = fps

        @staticmethod
        def assert_valid_fps(self, fps: int) -> None:
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

    class Realsense(Common):
        """
        Realsense Camera Class.
        Parameters:
        - URDF Enable:
        - Launch Enable:
        - Topic : [realsense] : ROS Topic to publish camera scan.
        - Serial : [0] : Serial number of camera. Must be specified if using 2.

        - Depth Enable : [True] : Toggle for depth data acquisition.
            - Depth FPS: [30] : Framerate of depth camera.
            - Depth Width: [640] : Width of depth image.
            - Depth Height: [480] : Height of depth image.

        - Color Enable: [True] : Toggle for color data acquisition
            - Color FPS: [30] : Framerate of color camera.
            - Color Width: [640] : Width of color image
            - Color Height: [480] : Height of color image

        - Prefix: [camera] : URDF link prefix of camera
        - Parent: [base_link] : parent link to attach realsense to
        - XYZ
        - RPY
        """
        def __init__(
            self,
            name: str,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
        ) -> None:
            super().__init__(name, parent, xyz, rpy)

    class Blackfly(Common):
        """
        Blackfly Camera Class
        Parameters:
        - URDF Enable
        - Launch Enable
        - Serial: [0] : Serial number of camera. Must be specified if using 2.
        - Device: [USB3 or GigE] : Device connection type.
        - Encoding: [BayerRG8] : Image encoding.
                     Must use BayerRG8 encoding to get more than 15 FPS.
        - FPS: [30] : Camera framerate
        - Prefix:
        - Parent:
        - XYZ:
        - RPY:
        """

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
            BAYER_GR12,
            BAYER_RG12,
            BAYER_GB12,
            BAYER_BG12,
            BAYER_GR12_PACKED,
            BAYER_RG12_PACKED,
            BAYER_GB12_PACKED,
            BAYER_BG12_PACKED,
        ]
        pass
