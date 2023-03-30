from clearpath_config.common import ListConfig, Platform
from clearpath_config.platform.decorations import Decorations
from clearpath_config.platform.pacs import PACS
from typing import List


# Unique Identifier: Name
def uid_name(T) -> str:
    return T.get_name()


# Unique Identifier: Level
def uid_level(T) -> int:
    return T.get_level()


# Unique Identifier: Level-Row
def uid_level_row(T) -> tuple:
    return (T.get_level(), T.get_row())


# Base Decorations Config
# - holds the model name for that config
# - to be used by all other configurations.
class BaseDecorationsConfig:

    def __init__(self, model) -> None:
        assert (
            model in Platform.ALL
        ), " ".join(
            "Model '%s' is invalid." % (
                model
            ),
            "Must be one of the following: %s." % (
                Platform.ALL
            )
        )
        # Standard Platform Decorations
        self.__bumpers = ListConfig[Decorations.Bumper, str](uid=uid_name)
        self.__top_plates = ListConfig[Decorations.TopPlate, str](uid=uid_name)
        # PACS Platform Decorations
        self.__full_risers = ListConfig[PACS.FullRiser, int](uid=uid_level)
        self.__row_risers = ListConfig[
                PACS.RowRiser, tuple[int, int]](
                    uid=uid_level_row)
        self.__brackets = ListConfig[PACS.Bracket, str](uid=uid_name)

    # Bumper: Add
    def add_bumper(
            self,
            # By Object
            bumper: Decorations.Bumper = None,
            # By Parameters
            name: str = None,
            enable: bool = True,
            extension: float = 0.0,
            model: str = Decorations.Bumper.DEFAULT,
            ) -> None:
        assert bumper or name, "Bumper object or name must be passed"
        # Create Object
        if name and not bumper:
            bumper = Decorations.Bumper(
                name=name,
                enable=enable,
                extension=extension,
                model=model
            )
        self.__bumpers.add(bumper)

    # Bumper: Remove
    def remove_bumper(
            self,
            # By Object or Name
            bumper: Decorations.Bumper | str,
            ) -> None:
        self.__bumpers.remove(bumper)

    # Bumper: Get
    def get_bumper(
            self,
            name: str,
            ) -> Decorations.Bumper:
        return self.__bumpers.get(name)

    # Bumper: Get All
    def get_bumpers(
            self
            ) -> List[Decorations.Bumper]:
        return self.__bumpers.get_all()

    # Bumper: Set
    def set_bumper(
            self,
            bumper: Decorations.Bumper,
            ) -> None:
        self.__bumpers.set(bumper)

    # Bumper: Set All
    def set_bumpers(
            self,
            bumpers: List[Decorations.Bumper],
            ) -> None:
        self.__bumpers.set_all(bumpers)

    # Top Plate: Add
    def add_top_plate(
            self,
            # By Object
            top_plate: Decorations.TopPlate = None,
            # By Parameters
            name: str = None,
            enable: bool = True,
            model: str = Decorations.TopPlate.DEFAULT,
            ) -> None:
        assert top_plate or name, "Top plate object or name must be passed."
        if name and not top_plate:
            top_plate = Decorations.TopPlate(
                name=name,
                enable=enable,
                model=model
            )
        self.__top_plates.add(top_plate)

    # Top Plate: Remove
    def remove_top_plate(
            self,
            # By Object or Name
            top_plate: Decorations.TopPlate | str,
            ) -> None:
        self.__top_plates.remove(top_plate)

    # Top Plate: Get
    def get_top_plate(
            self,
            name: str
            ) -> Decorations.TopPlate:
        return self.__top_plates.get(name)

    # Top Plate: Get All
    def get_top_plates(
            self
            ) -> List[Decorations.TopPlate]:
        return self.__top_plates.get_all()

    # Top Plate: Set
    def set_top_plate(
            self,
            top_plate: Decorations.TopPlate
            ) -> None:
        self.__top_plates.set(top_plate)

    # Top Plate: Set All
    def set_top_plates(
            self,
            top_plates: List[Decorations.TopPlate]
            ) -> None:
        self.__top_plates.set_all(top_plates)

    # Full Risers: Add
    def add_full_riser(
            self,
            # By Object
            full_riser: PACS.FullRiser = None,
            # By Parameters
            level: int = None,
            height: float = 0.0,
            ) -> None:
        assert full_riser or level, "Full riser object or level must be passed"
        if level and not full_riser:
            full_riser = PACS.FullRiser(
                level=level,
                height=height
            )
        self.__full_risers.add(full_riser)

    # Full Risers: Remove
    def remove_full_riser(
            self,
            # By Object or Level
            full_riser: PACS.FullRiser | int,
            ) -> None:
        self.__full_risers.remove(full_riser)

    # Full Riser: Get
    def get_full_riser(
            self,
            level: int
            ) -> PACS.FullRiser:
        return self.__full_risers.get(level)

    # Full Risers: Get All
    def get_full_risers(
            self,
            ) -> List[PACS.FullRiser]:
        return self.__full_risers.get_all()

    # Full Riser: Set
    def set_full_riser(
            self,
            full_riser: PACS.FullRiser
            ) -> None:
        self.__full_risers.set(full_riser)

    # Full Risers: Set All
    def set_full_risers(
            self,
            full_risers: List[PACS.FullRiser]
            ) -> None:
        self.__full_risers.set_all(full_risers)

    # Row Risers: Add
    def add_row_riser(
            self,
            # By Object
            row_riser: PACS.RowRiser = None,
            # By Parameters
            level: int = None,
            row: int = None,
            height: float = 0.0,
            ) -> None:
        assert row_riser or (level and row), (
            "Row riser object or level and row must be passed."
        )
        if (level and row) and not row_riser:
            row_riser = PACS.RowRiser(
                level=level,
                row=row,
                height=height
            )
        self.__row_risers.add(row_riser)

    # Row Risers: Remove
    def remove_row_riser(
            self,
            # By Object or (Level, Row)
            row_riser: PACS.RowRiser | tuple[int],
            ) -> None:
        self.__row_risers.remove(row_riser)

    # Row Riser: Get
    def get_row_riser(
            self,
            level: int,
            row: int,
            ) -> PACS.RowRiser:
        return self.__row_risers.get((level, row))

    # Row Risers: Get All
    def get_row_risers(
            self,
            ) -> List[PACS.RowRiser]:
        return self.__row_risers.get_all()

    # Row Risers: Set
    def set_row_riser(
            self,
            row_riser: PACS.RowRiser,
            ) -> None:
        self.__row_risers.set(row_riser)

    # Row Risers: Set All
    def set_row_risers(
            self,
            row_risers: List[PACS.RowRiser]
            ) -> None:
        self.__row_risers.set_all(row_risers)

    # Brackets: Add
    def add_bracket(
            self,
            # By Object
            bracket: PACS.Bracket = None,
            # By Parameters
            name: str = None,
            parent: str = "base_link",
            model: str = PACS.Bracket.DEFAULT,
            extension: float = 0.0,
            xyz: List[float] = [0.0, 0.0, 0.0],
            rpy: List[float] = [0.0, 0.0, 0.0]
            ) -> None:
        assert bracket or name, "Bracket object or name must be passed"
        if name and not bracket:
            bracket = PACS.Bracket(
                name=name,
                parent=parent,
                model=model,
                extension=extension,
                xyz=xyz,
                rpy=rpy
            )
        self.__brackets.add(bracket)

    # Brackets: Remove
    def remove_bracket(
            self,
            # By Object or Name
            bracket: PACS.Bracket | str,
            ) -> None:
        self.__brackets.remove(bracket)

    # Bracket: Get
    def get_bracket(
            self,
            name: str,
            ) -> PACS.Bracket:
        return self.__brackets.get(name)

    # Brackets: Get All
    def get_brackets(
            self,
            ) -> List[PACS.Bracket]:
        return self.__brackets.get_all()

    # Bracket: Set
    def set_bracket(
            self,
            bracket: PACS.Bracket,
            ) -> None:
        self.__brackets.set(bracket)

    # Brackets: Set All
    def set_brackets(
            self,
            brackets: List[PACS.Bracket],
            ) -> None:
        self.__brackets.set_all(brackets)
