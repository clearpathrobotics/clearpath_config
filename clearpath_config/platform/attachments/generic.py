# Generic Robot Platform Configuration
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.platform import Platform
from clearpath_config.platform.attachments.config import BaseAttachmentsConfig


# Generic Attachments Configuration
class GENERICAttachmentsConfig(BaseAttachmentsConfig, BaseConfig):
    PLATFORM = Platform.GENERIC
    ATTACHMENTS = "attachments"

    def __init__(
            self,
            config: dict = {}
            ) -> None:
        self._config = {}
        BaseAttachmentsConfig.__init__(self)
        BaseConfig.__init__(self, {}, config, self.ATTACHMENTS)
