# A200 Husky Platform Configuration
from clearpath_config.common import Platform
from clearpath_config.platform.decorations import BaseDecorationsConfig, Decorations
from clearpath_config.platform.pacs import (
    BracketsConfig,
    FullRisersConfig,
    RowRisersConfig,
)


# A200 Husky PACS Configuration
class A200PACSConfig(BracketsConfig, FullRisersConfig, RowRisersConfig):
    def __init__(self) -> None:
        super().__init__()


# A200 Husky Decorations Configuration
class A200DecorationsConfig(BaseDecorationsConfig):
    def __init__(self) -> None:
        super().__init__(model=Platform.A200)
        self.front_bumper = Decorations.Bumper(
            enable=True, extension=0.0, model=Decorations.Bumper.DEFAULT
        )
        self.rear_bumper = Decorations.Bumper(
            enable=True, extension=0.0, model=Decorations.Bumper.DEFAULT
        )
        self.top_plate = Decorations.A200.TopPlate()
        self.pacs = A200PACSConfig()
