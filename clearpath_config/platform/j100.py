# J100 Jackal Platform Configuration
from clearpath_config.common import Platform
from clearpath_config.platform.base import BaseDecorationsConfig
from clearpath_config.platform.decorations import Decorations


# J100 Jackal Decorations Configuration
class J100DecorationsConfig(BaseDecorationsConfig):
    def __init__(self) -> None:
        super().__init__(model=Platform.J100)
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
