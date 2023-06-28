from clearpath_config.common.types.platform import Platform
from clearpath_config.platform.decorations.a200 import A200DecorationsConfig
from clearpath_config.platform.decorations.config import BaseDecorationsConfig
from clearpath_config.platform.decorations.generic import (
    GENERICDecorationsConfig)
from clearpath_config.platform.decorations.j100 import J100DecorationsConfig


class DecorationsConfigMux:
    PLATFORM = {
        Platform.A200: A200DecorationsConfig(),
        Platform.J100: J100DecorationsConfig(),
        Platform.GENERIC: GENERICDecorationsConfig()
    }

    def __new__(
            cls,
            platform: str,
            config: dict = None
            ) -> BaseDecorationsConfig:
        assert platform in cls.PLATFORM, (
            "Platform '%s' must be one of: '%s'" % (
                platform,
                cls.PLATFORM.keys()
            )
        )
        if config is not None:
            cls.PLATFORM[platform].config = config
            return cls.PLATFORM[platform]
        else:
            return cls.PLATFORM[platform]
