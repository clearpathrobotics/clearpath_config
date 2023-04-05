# GENX Generic Robot Platform Configuration
from clearpath_config.common import Platform
from clearpath_config.platform.base import BaseDecorationsConfig


# GENX Generic Decorations Configuration
class GENERICDecorationsConfig(BaseDecorationsConfig):
    def __init__(self) -> None:
        super().__init__(model=Platform.GENERIC)
