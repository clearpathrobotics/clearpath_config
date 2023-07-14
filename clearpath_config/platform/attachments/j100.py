# J100 Jackal Platform Configuration
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.platform import Platform
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.platform.attachments.config import BaseAttachmentsConfig
from clearpath_config.platform.types.bumper import Bumper


# J100 Jackal Attachments Configuration
class J100AttachmentsConfig(BaseConfig, BaseAttachmentsConfig):
    PLATFORM = Platform.J100

    ATTACHMENTS = "attachments"
    FRONT_BUMPER = "front_bumper"
    REAR_BUMPER = "rear_bumper"

    TEMPLATE = {
        ATTACHMENTS: {
            FRONT_BUMPER: FRONT_BUMPER,
            REAR_BUMPER: REAR_BUMPER,
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        FRONT_BUMPER: {
            'name': FRONT_BUMPER,
            'enabled': Bumper.ENABLED,
            'extension': Bumper.EXTENSION,
            'model': Bumper.DEFAULT},
        REAR_BUMPER: {
            'name': REAR_BUMPER,
            'enabled': Bumper.ENABLED,
            'extension': Bumper.EXTENSION,
            'model': Bumper.DEFAULT
            },
    }

    def __init__(
            self,
            config: dict = {}
            ) -> None:
        BaseAttachmentsConfig.__init__(self)
        # Initialization
        self._config = {}
        self.front_bumper = self.DEFAULTS[self.FRONT_BUMPER]
        self.rear_bumper = self.DEFAULTS[self.REAR_BUMPER]
        # Setter Template
        setters = {
            self.KEYS[self.FRONT_BUMPER]: J100AttachmentsConfig.front_bumper,
            self.KEYS[self.REAR_BUMPER]: J100AttachmentsConfig.rear_bumper,
        }
        # Set from Config
        BaseConfig.__init__(self, setters, config, self.ATTACHMENTS)

    @property
    def front_bumper(self):
        front_bumper = self.bumpers.get(self.FRONT_BUMPER)
        self.set_config_param(
            key=self.KEYS[self.FRONT_BUMPER],
            value=front_bumper.to_dict()[self.FRONT_BUMPER]
        )
        return front_bumper

    @front_bumper.setter
    def front_bumper(self, value: dict | Bumper):
        if isinstance(value, dict):
            new = Bumper(name=self.FRONT_BUMPER)
            new.from_dict(value)
            self.bumpers.set(new)
        elif isinstance(value, Bumper):
            assert value.get_name() == self.FRONT_BUMPER, (
                "Front bumper must be Bumper with name %s" % self.FRONT_BUMPER
            )
            self.bumpers.set(new)
        else:
            assert isinstance(value, dict) or isinstance(value, Bumper), (
                "Bumper must be of type 'dict' or 'Bumper'"
            )

    @property
    def rear_bumper(self):
        rear_bumper = self.bumpers.get(self.REAR_BUMPER)
        self.set_config_param(
            key=self.KEYS[self.REAR_BUMPER],
            value=rear_bumper.to_dict()[self.REAR_BUMPER]
        )
        return rear_bumper

    @rear_bumper.setter
    def rear_bumper(self, value: dict | Bumper):
        if isinstance(value, dict):
            new = Bumper(name=self.REAR_BUMPER)
            new.from_dict(value)
            self.bumpers.set(new)
        elif isinstance(value, Bumper):
            assert value.get_name() == self.REAR_BUMPER, (
                "Rear bumper must be Bumper with name %s" % self.REAR_BUMPER
            )
            self.bumpers.set(new)
        else:
            assert isinstance(value, dict) or isinstance(value, Bumper), (
                "Bumper must be of type 'dict' or 'Bumper'"
            )
