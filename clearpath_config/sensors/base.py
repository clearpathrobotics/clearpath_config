from clearpath_config.common import Accessory, List


class BaseSensor(Accessory):
    """
    Base Sensor Class
     - inherits from Accessory.
     - contains all common parameters shared by all sensors.
    """
    URDF_ENABLED = True
    LAUNCH_ENABLED = True

    def __init__(
            self,
            name: str,
            topic: str,
            urdf_enabled: bool = URDF_ENABLED,
            launch_enabled: bool = LAUNCH_ENABLED,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ) -> None:
        super().__init__(name, parent, xyz, rpy)
        # Topic:
        # - should be automatically determined by the sensor's index
        # - should match the Clearpath API
        self.topic = str()
        # URDF Enable
        # - enables the sensor description in the generated URDF
        self.urdf_enabled = True
        # Launch Enable
        # - enables the sensor launch in the generated launch
        self.launch_enabled = True

    def get_topic(self) -> str:
        return self.topic

    def set_topic(self, topic: str) -> None:
        assert isinstance(topic, str), (
            "Topic '%s' of type '%s', expected 'str'" % (topic, type(topic))
        )
        assert " " not in topic, (
            "Topic '%s' contains empty spaces." % topic
        )
        self.topic = topic

    def enable_urdf(self) -> None:
        self.urdf_enabled = True

    def disable_urdf(self) -> None:
        self.urdf_enabled = False

    def enable_launch(self) -> None:
        self.launch_enabled = True

    def disable_launch(self) -> None:
        self.launch_enabled = False
