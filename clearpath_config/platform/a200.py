# A200 Husky Platform Configuration
from clearpath_config.common import Platform
from clearpath_config.platform.base import BaseDecorationsConfig
from clearpath_config.platform.decorations import Decorations


# A200 Husky Decorations Configuration
class A200DecorationsConfig(BaseDecorationsConfig):

    def __init__(self) -> None:
        super().__init__(model=Platform.A200)
        # Front Bumper
        self.add_bumper(
            name="front_bumper",
            enable=True,
            extension=0.0,
            model=Decorations.Bumper.DEFAULT
        )
        # Rear Bumper
        self.add_bumper(
            name="rear_bumper",
            enable=True,
            extension=0.0,
            model=Decorations.Bumper.DEFAULT
        )
        # Top Plate
        self.add_top_plate(
            name="top_plate",
            enable=True,
            model=Decorations.TopPlate.DEFAULT
        )
