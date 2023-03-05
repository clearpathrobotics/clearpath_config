# GENX Generic Robot Platform Configuration
from clearpath_config.common import Platform
from clearpath_config.platform.decorations import BaseDecorationsConfig

# GENX Generic Decorations Configuration
class GENXDecorationsConfig(BaseDecorationsConfig):

    def __init__(self) -> None:
        super().__init__(model = Platform.GENX)
