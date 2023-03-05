from clearpath_config.common import Accessory
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

# Base PACS Config
# - enable and disable PACS
class BasePACSConfig():

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = True

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False


# Full Risers Config
# - list of full risers
class FullRisersConfig(BasePACSConfig):

    def __init__(self, enabled: bool = True, full_risers = List[PACS.FullRiser]) -> None:
        super().__init__(enabled)
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

# Row Risers Config
# - list of row risers
class RowRisersConfig(BasePACSConfig):

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

# Brackets Config
# - list of brackets
class BracketsConfig():

    def __init__(self) -> None:
        self.brackets = []

    def get_brackets(self) -> list:
        return self.brackets

    def add_bracket(self, bracket = PACS.Bracket, 
                    name: str = None, parent: str = None, model: str = None, 
                    extension: int = 0, xyz: List[float] = [0.0, 0.0, 0.0], rpy: List[float] = [0.0, 0.0, 0.0]) -> None:
        assert bracket or (parent and name), "Bracket or (parent and name) must be passed."
        names = [b.name for b in self.brackets]
        if bracket:
            assert isinstance(bracket, PACS.Bracket), "Bracket must be of type PACSConfig.Bracket"
            assert bracket.name not in names,  "Bracket with name: '%s' already exists." % bracket.name
            self.brackets.append(bracket)
        else:
            assert name not in names, "Bracket with name: '%s' already exists." % name
            if not model:
                model = PACS.Bracket.DEFAULT
            self.brackets.append(PACS.Bracket(name=name, parent=parent, model=model, extension=extension, xyz=xyz, rpy=rpy))

    def remove_bracket(self, bracket = PACS.Bracket, name: str = None) -> bool:
        assert bracket or name, "Bracket or name must be passed."
        if bracket:
            name = bracket.name
        for bracket in self.brackets:
            if bracket.name == name:
                self.brackets.remove(bracket)
                return True
        return False
