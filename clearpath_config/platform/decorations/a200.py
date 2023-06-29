# A200 Husky Platform Configuration
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.platform import Platform
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.platform.decorations.config import BaseDecorationsConfig
from clearpath_config.platform.types.bumper import Bumper
from clearpath_config.platform.types.top_plate import TopPlate
from clearpath_config.platform.types.structure import Structure


# A200 Husky Decorations Configuration
class A200DecorationsConfig(BaseConfig, BaseDecorationsConfig):
    PLATFORM = Platform.A200

    DECORATIONS = "decorations"
    FRONT_BUMPER = "front_bumper"
    REAR_BUMPER = "rear_bumper"
    TOP_PLATE = "top_plate"
    STRUCTURE = "structure"

    TEMPLATE = {
        DECORATIONS: {
            FRONT_BUMPER: FRONT_BUMPER,
            REAR_BUMPER: REAR_BUMPER,
            TOP_PLATE: TOP_PLATE,
            STRUCTURE: STRUCTURE,
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
        TOP_PLATE: {
            'name': TOP_PLATE,
            'enabled': TopPlate.ENABLED,
            'model': TopPlate.DEFAULT
            },
        STRUCTURE: {
            'name': STRUCTURE,
            'enabled': Structure.ENABLED,
            'model': Structure.DEFAULT
            },
    }

    def __init__(
            self,
            config: dict = {}
            ) -> None:
        BaseDecorationsConfig.__init__(self)
        # Initialization
        self._config = {}
        self.front_bumper = self.DEFAULTS[self.FRONT_BUMPER]
        self.rear_bumper = self.DEFAULTS[self.REAR_BUMPER]
        self.structure = self.DEFAULTS[self.STRUCTURE]
        self.top_plate = self.DEFAULTS[self.TOP_PLATE]
        # Setter Template
        setters = {
            self.KEYS[self.FRONT_BUMPER]: A200DecorationsConfig.front_bumper,
            self.KEYS[self.REAR_BUMPER]: A200DecorationsConfig.rear_bumper,
            self.KEYS[self.STRUCTURE]: A200DecorationsConfig.structure,
            self.KEYS[self.TOP_PLATE]: A200DecorationsConfig.top_plate
        }
        # Set from Config
        BaseConfig.__init__(self, setters, config, self.DECORATIONS)

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

    @property
    def top_plate(self) -> TopPlate:
        top_plate = self.top_plates.get(self.TOP_PLATE)
        self.set_config_param(
            key=self.KEYS[self.TOP_PLATE],
            value=top_plate.to_dict()[self.TOP_PLATE]
        )
        return top_plate

    @top_plate.setter
    def top_plate(self, value: dict | TopPlate):
        if isinstance(value, dict):
            new = TopPlate(name=self.TOP_PLATE)
            new.from_dict(value)
            self.top_plates.set(new)
        elif isinstance(value, TopPlate):
            assert value.get_name() == self.TOP_PLATE, (
                "Top plate must be TopPlate with name %s" % self.TOP_PLATE
            )
        else:
            assert isinstance(value, dict) or isinstance(value, TopPlate), (
                "Top plate must be of type 'dict' or 'TopPlate'"
            )

    @property
    def structure(self) -> Structure:
        structure = self.structures.get(self.STRUCTURE)
        self.set_config_param(
            key=self.KEYS[self.STRUCTURE],
            value=structure.to_dict()[self.STRUCTURE]
        )
        return structure

    @structure.setter
    def structure(self, value: dict | Structure) -> None:
        if isinstance(value, dict):
            new = Structure(name=self.STRUCTURE)
            new.from_dict(value)
            self.structures.set(new)
        elif isinstance(value, Structure):
            assert value.get_name() == self.STRUCTURE, (
                "Structure must be Structure with name %s" % self.STRUCTURE
            )
