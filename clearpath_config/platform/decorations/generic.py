# Generic Robot Platform Configuration
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.platform import Platform
from clearpath_config.platform.decorations.config import BaseDecorationsConfig


# Generic Decorations Configuration
class GENERICDecorationsConfig(BaseDecorationsConfig, BaseConfig):
    PLATFORM = Platform.GENERIC
    DECORATIONS = "decorations"

    def __init__(
            self,
            config: dict = {}
            ) -> None:
        self._config = {}
        BaseDecorationsConfig.__init__(self)
        BaseConfig.__init__(self, {}, config, self.DECORATIONS)
