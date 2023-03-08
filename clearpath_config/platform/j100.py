# J100 Jackal Platform Configuration
from clearpath_config.common import Platform
from clearpath_config.platform.decorations import BaseDecorationsConfig, Decorations


# J100 Jackal PACS Configuration
class J100PACSConfig:
    def __init__(self) -> None:
        super().__init__()


# J100 Jackal Decorations Configuration
class J100DecorationsConfig(BaseDecorationsConfig):
    def __init__(self) -> None:
        super().__init__(model=Platform.J100)
        self.front_bumper = Decorations.Bumper(
            enable=True, extension=0.0, model=Decorations.Bumper.DEFAULT
        )
        self.rear_bumper = Decorations.Bumper(
            enable=True, extension=0.0, model=Decorations.Bumper.DEFAULT
        )
        # No J100 Jackal PACS Config Yet
        # self.pacs = J100PACSConfig()
