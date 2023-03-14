from clearpath_config.sensors.base import BaseSensor, List

# Sensor Config
class SensorConfig:

    def __init__(
            self,
            lidars_2d: List[BaseSensor],
            lidars_3d: List[BaseSensor],
            cameras: List[BaseSensor],
        ) -> None:
        # 2D Lidars
        self.lidars_2d = list()
        # 3D Lidars
        self.lidars_3d = []
        # Cameras
        self.cameras = []

    def get_sensors(self, ) -> List[BaseSensor]:
        return

    def add_sensor(self, sensor: BaseSensor) -> None:
        pass

    def remove_sensor(self, sensor: BaseSensor) -> None:
        pass
