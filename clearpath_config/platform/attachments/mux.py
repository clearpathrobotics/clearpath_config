from clearpath_config.common.types.platform import Platform
from clearpath_config.platform.attachments.a200 import A200AttachmentsConfig
from clearpath_config.platform.attachments.config import BaseAttachmentsConfig
from clearpath_config.platform.attachments.generic import GENERICAttachmentsConfig
from clearpath_config.platform.attachments.j100 import J100AttachmentsConfig


class AttachmentsConfigMux:
    PLATFORM = {
        Platform.A200: A200AttachmentsConfig(),
        Platform.J100: J100AttachmentsConfig(),
        Platform.GENERIC: GENERICAttachmentsConfig()
    }

    def __new__(
            cls,
            platform: str,
            config: dict = None
            ) -> BaseAttachmentsConfig:
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
