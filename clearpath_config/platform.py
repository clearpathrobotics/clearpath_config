from clearpath_config.common import Accessory, File, Platform, SerialNumber
from typing import List

#PACS
# - all PACS structures
class PACS():


    # PACS Components
    class FullRiser():
        '''
        Full Riser:
            - spans the entire platorm
            - acts as another plate
            - creates a grid of mounting locations
            - can be added at levels that correspond to 10 cm increments
        '''
        def __init__(self, level: int, height: float = None) -> None:
            # Level of riser (i.e. first floor, second floor, etc.)
            self.level = level
            # Height in meters from top plate to top of riser.
            self.height = height if height else 0.1 * level


    class RowRiser():
        '''
        Row Riser:
            - spans one row of the full riser
            - can be added at levels that correspond to 10 cm increments
        '''
        def __init__(self, level: int, row: int, height: float = None) -> None:
            # Level of row riser (i.e. first level, second level, etc.)
            self.level = level
            # Row of row riser (i.e. frist row, ..., last row: robot specifc)
            self.row = row
            # Height in meters from top plate to top of riser.
            self.height = height if height else 0.1 * level


    class Bracket(Accessory):
        '''
        Bracket:
            - small apapter plate
            - allows multiple sensors to be mounted
            - should be added to any 
        '''
        HORIZONTAL = "horizontal"
        HORIZONTAL_LARGE = "large"
        VERTICAL = "vertical"
        DEFAULT = HORIZONTAL
        MODELS = [HORIZONTAL, HORIZONTAL_LARGE, VERTICAL]

        def __init__(self,
                     name: str,
                     parent: str,
                     model: str = DEFAULT,
                     extension: str = 0.0,
                     xyz: List[float] = [0.0, 0.0, 0.0],
                     rpy: List[float] = [0.0, 0.0, 0.0]) -> None:
            # Initialize Accessory
            super().__init__(parent=parent, name=name, xyz=xyz, rpy=rpy)
            # Model: type of bracket
            assert model in self.MODELS, "Unexpected Bracket model '%s', it must be one of the following: %s" % (model, self.MODELS)
            self.model = model
            # Extension: length of standoffs in meters
            self.extension = extension


# PACSConfig:
# - platform specific grid based structures
# - each platform will have its own PACS config
class PACSConfig():

    # Base PACSConfig
    class Base():

        def __init__(self) -> None:
            self.enabled = True

        def enable(self) -> None:
            self.enabled = True

        def disable(self) -> None:
            self.enabled = False


    class BaseFullRisers(Base):
        def __init__(self) -> None:
            self.full_risers = []

        def get_full_risers(self) -> list:
            return self.full_risers

        def add_full_riser(self, riser = PACS.FullRiser, level: int = None) -> None:
            assert riser or level, "FullRiser or level of riser must be passed."
            levels = [fr.level for fr in self.full_risers]
            if riser:
                assert isinstance(riser, PACS.FullRiser), "Riser must be of type FullRiser"
                assert riser.level not in levels, "Riser of level %s already exists" % riser.level
                self.full_risers.append(riser)
            else:
                assert level not in levels, "Riser of level %s already exists" % level
                self.full_risers.append(PACS.FullRiser(level))

        def remove_full_riser(self, riser = PACS.FullRiser, level: int = None) -> bool:
            assert riser or level, "FullRiser or level of riser must be passed."
            if riser:
                level = riser.level
            for riser in self.full_risers:
                if riser.level == level:
                    self.full_risers.remove(riser)
                    return True
            return False


    # Base Row Risers
    class BaseRowRisers(Base):

        def __init__(self) -> None:
            self.row_risers = []

        def get_row_risers(self) -> list:
            return self.row_risers

        def add_row_riser(self, riser = PACS.RowRiser, level: int = None, row: int = None) -> None:
            assert riser or (level and row), "RowRiser or (level and row) must be passed."
            levels = [rr.level for rr in self.row_risers]
            rows = [rr.row for rr in self.row_risers]
            if riser:
                assert isinstance(riser, PACS.RowRiser), "Riser must be of type RowRiser"
                assert (riser.level not in levels) and (riser.row not in rows), "Row riser at level %s and row %s already exists" % (riser.level, riser.row)
                self.row_risers.append(riser)
            else:
                assert (level not in levels) and (row not in rows), "Row riser at level %s and row %s already exists" % (level, row)

        def remove_row_riser(self, riser = PACS.RowRiser, level: int = None, row: int = None) -> None:
            assert riser or (level and row), "RowRiser or (level and row) must be passed."
            if riser:
                level = riser.level
                row = riser.row
            for riser in self.row_risers:
                if riser.level == level:
                    self.row_risers.remove(riser)
                    return True
            return False


    # Base Brackets
    class BaseBrackets(Base):

        def __init__(self) -> None:
            self.brackets = []

        def get_brackets(self) -> list:
            return self.brackets

        def add_bracket(self, bracket = PACS.Bracket, 
                        prefix: str = None, parent: str = None, model: str = None, 
                        extension: int = 0, xyz: List[float] = [0.0, 0.0, 0.0], rpy: List[float] = [0.0, 0.0, 0.0]) -> None:
            assert bracket or (parent and prefix), "Bracket or (parent and prefix) must be passed."
            prefixes = [b.prefix for b in self.brackets]
            if bracket:
                assert isinstance(bracket, PACS.Bracket), "Bracket must be of type PACSConfig.Bracket"
                assert bracket.prefix not in prefixes,  "Bracket with prefix: '%s' already exists." % bracket.prefix
                self.brackets.append(bracket)
            else:
                assert prefix not in prefixes, "Bracket with prefix: '%s' already exists." % prefix
                if not model:
                    model = PACS.Bracket.DEFAULT
                self.brackets.append(PACS.Bracket(prefix=prefix, parent=parent, model=model, extension=extension, xyz=xyz, rpy=rpy))

        def remove_bracket(self, bracket = PACS.Bracket, prefix: str = None) -> bool:
            assert bracket or prefix, "Bracket or prefix must be passed."
            if bracket:
                prefix = bracket.prefix
            for bracket in self.brackets:
                if bracket.prefix == prefix:
                    self.brackets.remove(bracket)
                    return True
            return False


    # Dingo Differential
    class DingoD():
        pass


    # Dingo Omnidirectional
    class DingoO():
        pass


    # Husky
    class Husky(BaseFullRisers, BaseRowRisers, BaseBrackets):

        def __init__(self) -> None:
            super().__init__()


    # Jackal
    class Jackal(Base):

        def __init__(self) -> None:
            super().__init__()


    # Ridgeback
    class Ridgeback():
        pass


    # Warthog
    class Warthog():
        pass


    # Generic
    class Generic():
        pass


    '''
    PACS Configuration:
        - top level configuration for all PACS robots
        - not all robots have PACS configurations
        - return the configuration for each robot
    '''
    MODEL_CONFIGS = {Platform.DINGO_DIFF: DingoD(),
                     Platform.DINGO_OMNI: DingoO(),
                     Platform.HUSKY: Husky(),
                     Platform.JACKAL: Jackal(),
                     Platform.RIDGEBACK: Ridgeback(),
                     Platform.WARTHOG: Warthog(),
                     Platform.GENERIC: Generic()}

    def __new__(self, model) -> None:
        assert model in Platform.ALL, "Model passed '%s' is not expected. must be one of the following: %s" % (model, Platform.ALL)
        return self.MODEL_CONFIGS[model]


# DecorationAccessories
class Decorations():

    # General Decorations
    class Bumper():
        '''
        Bumpers on the Husky can be:
            - toggled on/off
            - extended
            - swapped for a Wibotic charger bumper
        '''
        DEFAULT = "default"
        WIBOTIC = "wibotic"
        MODELS = [DEFAULT, WIBOTIC]

        def __init__(self,
                        enable: bool = True,
                        extension: float = 0.0,
                        model: str = DEFAULT) -> None:
            self.enabled = True
            self.extension = 0.0
            self.model = self.DEFAULT
            if enable:
                self.enable()
            if extension:
                self.set_extension(extension)
            if model:
                self.set_model(model)

        def enable(self) -> None:
            self.enabled = True

        def disable(self) -> None:
            self.enabled = False

        def get_extension(self) -> float:
            return self.extension

        def set_extension(self, extension) -> None:
            assert isinstance(extension, float), "Bumper extension must be of type float, unexpected type '%s'" % type(extension)
            self.extension = extension

        def get_model(self) -> str:
            return self.model

        def set_model(self, model: str) -> None:
            assert model in self.MODELS, "Bumper model '%s' is not one of: %s" % (model, self.MODELS)
            self.model = model


    # Husky Specific Decorations
    class Husky():
        class TopPlate():
            '''
            Top Plate on the Husky can be:
                - toggled on/off
                - swapped for larger plate and pacs plate
                - PACS plate is required
            '''
            DEFAULT = "default"
            LARGE = "large"
            PACS = "pacs"
            MODELS = [DEFAULT, LARGE, PACS]

            def __init__(self,
                         enable: bool = True,
                         model: str = DEFAULT) -> None:
                self.enabled = True
                self.extension = 0.0
                self.model = self.DEFAULT
                if enable:
                    self.enable()
                if model:
                    self.set_model(model)

            def enable(self) -> None:
                self.enabled = True

            def disable(self) -> None:
                self.enabled = False

            def get_model(self) -> str:
                return self.model

            def set_model(self, model: str) -> None:
                assert model in self.MODELS, "Top plate model '%s' is not one of: %s" % (model, self.MODELS)
                self.model = model


# DecorationsConfig:
# - platform specific structures
# - each platform should have its own DecorationsConfig
class DecorationsConfig():

    # Base Platofrm Configuration
    class Base():

        def __init__(self, model) -> None:
            assert model in Platform.ALL, "Model passed '%s' is not expected. must be one of the following: %s" % (model, Platform.ALL)
            self.model = model


    # Dingo Differential
    class DingoD(Base):

        def __init__(self) -> None:
            super().__init__(model = Platform.DINGO_DIFF)


    # Dingo Omnidirectional
    class DingoO(Base):

        def __init__(self) -> None:
            super().__init__(model = Platform.DINGO_OMNI)


    # Husky
    # - Bumper
    # - TopPlate
    # - PACS
    class Husky(Base):

        def __init__(self) -> None:
            super().__init__(model = Platform.HUSKY)
            Bumper = Decorations.Bumper
            TopPlate = Decorations.Husky.TopPlate
            self.front_bumper = Bumper(enable=True, extension=0.0, model=Bumper.DEFAULT)
            self.rear_bumper = Bumper(enable=True, extension=0.0, model=Bumper.DEFAULT)
            self.top_plate = TopPlate(enable=True, model=TopPlate.DEFAULT)
            self.pacs = PACSConfig(model = Platform.HUSKY)


    # Jackal
    # - Bumper (Wibotic)
    # - AccessoryFender
    class Jackal(Base):

        def __init__(self) -> None:
            super().__init__(model = Platform.JACKAL)
            Bumper = Decorations.Bumper
            self.front_bumper = Bumper(enable=True, extension=0.0, model=Bumper.DEFAULT)
            self.rear_bumper = Bumper(enable=True, extension=0.0, model=Bumper.DEFAULT)
            self.front_accessory_fender = False
            self.rear_accessory_fender = False


    # Ridgeback
    class Ridgeback(Base):

        def __init__(self) -> None:
            super().__init__(model = Platform.RIDGEBACK)


    # Warthog
    class Warthog(Base):

        def __init__(self) -> None:
            super().__init__(model = Platform.WARTHOG)


    # Genric
    class Generic(Base):

        def __init__(self) -> None:
            super().__init__(model = Platform.GENERIC)


    '''
    DecorationsConfig
        - top level configuration for all models
        - returns appropriate config from sub-classes
    '''
    MODEL_CONFIGS = {Platform.DINGO_DIFF: DingoD(),
                     Platform.DINGO_OMNI: DingoO(),
                     Platform.HUSKY: Husky(),
                     Platform.JACKAL: Jackal(),
                     Platform.RIDGEBACK: Ridgeback(),
                     Platform.WARTHOG: Warthog(),
                     Platform.GENERIC: Generic()}

    def __new__(self, model) -> None:
        assert model in Platform.ALL, "Model passed '%s' is not expected. must be one of the following: %s" % (model, Platform.ALL)
        return self.MODEL_CONFIGS[model]


# ExtrasConfig:
# - URDF extras: urdf.xacro with custom links and joints
# - Control extras: YAML with overwrites or extra ROS parameters
class ExtrasConfig():

    def __init__(self, urdf: str = None, control: str = None) -> None:
        self.urdf = File(path=urdf)
        self.control = File(path=control)

    def get_urdf_extras(self) -> str:
        return str(self.urdf)

    def set_urdf_extras(self, path: str) -> None:
        self.urdf = File(path=path)

    def get_control_extras(self) -> str:
        return str(self.control)

    def set_control_extras(self, path: str) -> None:
        self.control = File(path=path)


# PlatformConfig:
# - platform level configuration options
class PlatformConfig():

    def __init__(self, 
                 serial: str = "generic-0000",
                 decorations: DecorationsConfig.Base = None,
                 extras: ExtrasConfig = None) -> None:
        self.serial = SerialNumber(sn = serial)
        self.model = self.serial.get_model()
        self.decorations = DecorationsConfig(model=self.get_model_name())
        self.extras = ExtrasConfig()
        if decorations:
            assert isinstance(decorations, DecorationsConfig.Base), "Decorations must be of type DecorationsConfig, unexpected type: '%s'" % type(decorations)
            assert decorations.model == self.model, "Decorations do not match the model of the serial number"
            self.decorations = decorations
        if extras:
            assert isinstance(extras, ExtrasConfig), "Extras must be of type ExtrasConfig, unexpected type: '%s'" % type(extras)
            self.extras = extras

    def set_serial_number(self, serial_number: str) -> None:
        self.serial = SerialNumber(serial_number)
        self.decorations = DecorationsConfig(model=self.get_model_name())

    def get_serial_number(self, prefix: bool = False) -> str:
        return self.serial.get_serial(prefix)

    def get_unit_number(self) -> str:
        return self.serial.get_unit()

    def get_model(self) -> str:
        return self.serial.get_model()

    def get_model_name(self) -> str:
        return self.serial.get_model_name()

