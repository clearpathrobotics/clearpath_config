from clearpath_config.common import Accessory
from copy import deepcopy
from typing import List


# PACS
# - all PACS structures
class PACS:
    # PACS Components
    class FullRiser:
        """
        Full Riser:
            - spans the entire platorm
            - acts as another plate
            - creates a grid of mounting locations
            - can be added at levels that correspond to 10 cm increments
        """

        def __init__(self, level: int, height: float = None) -> None:
            # Level of riser (i.e. first floor, second floor, etc.)
            self.level = int()
            self.set_level(level)
            # Height in meters from top plate to top of riser.
            self.height = float()
            if height is not None:
                self.set_height(height)
            else:
                self.set_height(0.1 * self.level)

        def get_level(self) -> int:
            return self.level

        def set_level(self, level: int) -> None:
            if isinstance(level, float):
                assert level.is_integer(), "Riser level must be an integer"
            try:
                level = int(level)
            except ValueError as e:
                raise AssertionError(e.args[0])
            assert level > 0, "Riser level must be greater than 0"
            self.level = level

        def get_height(self) -> float:
            return self.height

        def set_height(self, height: float) -> None:
            try:
                height = float(height)
            except ValueError as e:
                raise AssertionError(e.args[0])
            assert height >= 0, "Height must be greater than or equal to 0.0"
            self.height = height

    class RowRiser:
        """
        Row Riser:
            - spans one row of the full riser
            - can be added at levels that correspond to 10 cm increments
        """

        def __init__(self, level: int, row: int, height: float = None) -> None:
            # Level of riser (i.e. first floor, second floor, etc.)
            self.level = int()
            self.set_level(level)
            # Row of row riser (i.e. frist row, ..., last row: robot specifc)
            self.row = int()
            self.set_row(row)
            # Height in meters from top plate to top of riser.
            self.height = float()
            if height is not None:
                self.set_height(height)
            else:
                self.set_height(0.1 * self.level)

        def get_level(self) -> int:
            return self.level

        def set_level(self, level: int) -> None:
            if isinstance(level, float):
                assert level.is_integer(), "Riser level must be an integer"
            try:
                level = int(level)
            except ValueError as e:
                raise AssertionError(e.args[0])
            assert level > 0, "Riser level must be greater than 0"
            self.level = level

        def get_row(self) -> int:
            return self.row

        def set_row(self, row: int) -> None:
            if isinstance(row, float):
                assert row.is_integer(), "Riser row must be an integer"
            try:
                row = int(row)
            except ValueError as e:
                raise AssertionError(e.args[0])
            assert row > 0, "Riser row must be greater than 0"
            self.row = row

        def get_height(self) -> float:
            return self.height

        def set_height(self, height: float) -> None:
            try:
                height = float(height)
            except ValueError as e:
                raise AssertionError(e.args[0])
            assert height >= 0, "Height must be greater than or equal to 0.0"
            self.height = height

    class Bracket(Accessory):
        """
        Bracket:
            - small apapter plate
            - allows multiple sensors to be mounted
            - should be added to any
        """

        HORIZONTAL = "horizontal"
        HORIZONTAL_LARGE = "large"
        VERTICAL = "vertical"
        DEFAULT = HORIZONTAL
        MODELS = [HORIZONTAL, HORIZONTAL_LARGE, VERTICAL]

        def __init__(
            self,
            name: str,
            parent: str = "base_link",
            model: str = DEFAULT,
            extension: float = 0.0,
            xyz: List[float] = [0.0, 0.0, 0.0],
            rpy: List[float] = [0.0, 0.0, 0.0],
        ) -> None:
            # Initialize Accessory
            super().__init__(parent=parent, name=name, xyz=xyz, rpy=rpy)
            # Model: type of bracket
            self.model = PACS.Bracket.DEFAULT
            if model:
                self.set_model(model)
            # Extension: length of standoffs in meters
            self.extension = 0.0
            if extension:
                self.set_extension(extension)

        def get_model(self) -> str:
            return self.model

        def set_model(self, model: str) -> None:
            assert (
                model in self.MODELS
            ), "Unexpected Bracket model '%s', it must be one of the following: %s" % (
                model,
                self.MODELS,
            )
            self.model = model

        def get_extension(self) -> float:
            return self.extension

        def set_extension(self, extension) -> None:
            try:
                extension = float(extension)
            except ValueError as e:
                raise AssertionError(e.args[0])
            assert extension >= 0, "Bracket extension must be a positive value"
            self.extension = extension


# Base PACS Config
# - enable and disable PACS
class BasePACSConfig:
    def __init__(self, enabled: bool = True) -> None:
        self.enabled = bool(enabled)

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False


# Full Risers Config
# - list of full risers
class FullRisersConfig(BasePACSConfig):
    def __init__(
        self, enabled: bool = True, full_risers: List[PACS.FullRiser] = []
    ) -> None:
        super().__init__(enabled)
        self.full_risers = []
        if full_risers:
            self.set_full_risers(full_risers)

    def get_full_risers(self) -> list:
        return self.full_risers

    def set_full_risers(self, full_risers: List[PACS.FullRiser]) -> None:
        temp = deepcopy(self.get_full_risers())
        self.full_risers.clear()
        for full_riser in full_risers:
            try:
                self.add_full_riser(riser=full_riser)
            except AssertionError as e:
                self.full_risers = temp
                raise e

    def add_full_riser(
        self, riser: PACS.FullRiser, level: int = None, height: float = None
    ) -> None:
        assert riser or level, "FullRiser or level of riser must be passed."
        levels = [fr.level for fr in self.full_risers]
        if riser:
            assert isinstance(riser, PACS.FullRiser), "Riser must be of type FullRiser"
            assert riser.level not in levels, (
                "Riser of level %s already exists" % riser.level
            )
            self.full_risers.append(riser)
        else:
            assert level not in levels, "Riser of level %s already exists" % level
            if height is not None:
                self.full_risers.append(PACS.FullRiser(level, height))
            else:
                self.full_risers.append(PACS.FullRiser(level))

    def remove_full_riser(self, riser: PACS.FullRiser, level: int = None) -> bool:
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
    def __init__(
        self, enabled: bool = True, row_risers: List[PACS.RowRiser] = []
    ) -> None:
        super().__init__(enabled)
        self.row_risers = []
        if row_risers:
            self.set_row_risers(row_risers)

    def get_row_risers(self) -> list:
        return self.row_risers

    def set_row_risers(self, row_risers: List[PACS.RowRiser]) -> None:
        temp = deepcopy(self.get_row_risers())
        self.row_risers.clear()
        for row_riser in row_risers:
            try:
                self.add_row_riser(riser=row_riser)
            except AssertionError as e:
                self.full_risers = temp
                raise e

    def add_row_riser(
        self, riser: PACS.RowRiser, level: int = None, row: int = None
    ) -> None:
        assert riser or (level and row), "RowRiser or (level and row) must be passed."
        levels = [rr.level for rr in self.row_risers]
        rows = [rr.row for rr in self.row_risers]
        if riser:
            assert isinstance(riser, PACS.RowRiser), "Riser must be of type RowRiser"
            assert (riser.level not in levels) or (
                riser.row not in rows
            ), "Row riser at level %s and row %s already exists" % (
                riser.level,
                riser.row,
            )
            self.row_risers.append(riser)
        else:
            assert (level not in levels) or (
                row not in rows
            ), "Row riser at level %s and row %s already exists" % (level, row)

    def remove_row_riser(
        self, riser: PACS.RowRiser, level: int = None, row: int = None
    ) -> None:
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
class BracketsConfig:
    def __init__(self, brackets: List[PACS.Bracket] = []) -> None:
        self.brackets = []
        if brackets:
            self.set_brackets(brackets)

    def get_brackets(self) -> list:
        return self.brackets

    def set_brackets(self, brackets: List[PACS.Bracket] = []) -> None:
        temp = deepcopy(self.get_brackets())
        self.brackets.clear()
        for bracket in brackets:
            try:
                self.add_bracket(bracket)
            except AssertionError as e:
                self.brackets = temp
                raise e

    def add_bracket(
        self,
        bracket: PACS.Bracket,
        name: str = None,
        parent: str = None,
        model: str = None,
        extension: int = 0,
        xyz: List[float] = [0.0, 0.0, 0.0],
        rpy: List[float] = [0.0, 0.0, 0.0],
    ) -> None:
        assert bracket or (
            parent and name
        ), "Bracket or (parent and name) must be passed."
        names = [b.name for b in self.brackets]
        if bracket:
            assert isinstance(
                bracket, PACS.Bracket
            ), "Bracket must be of type PACSConfig.Bracket"
            assert bracket.name not in names, (
                "Bracket with name: '%s' already exists." % bracket.name
            )
            self.brackets.append(bracket)
        else:
            assert name not in names, "Bracket with name: '%s' already exists." % name
            if not model:
                model = PACS.Bracket.DEFAULT
            self.brackets.append(
                PACS.Bracket(
                    name=name,
                    parent=parent,
                    model=model,
                    extension=extension,
                    xyz=xyz,
                    rpy=rpy,
                )
            )

    def remove_bracket(self, bracket: PACS.Bracket, name: str = None) -> bool:
        assert bracket or name, "Bracket or name must be passed."
        if bracket:
            name = bracket.name
        for bracket in self.brackets:
            if bracket.name == name:
                self.brackets.remove(bracket)
                return True
        return False
