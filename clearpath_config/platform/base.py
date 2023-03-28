from clearpath_config.common import Platform
from clearpath_config.platform.decorations import Decorations
from clearpath_config.platform.pacs import PACS
from copy import deepcopy
from typing import Callable, Generic, List, TypeVar

# Generic Type
T = TypeVar("T")


# Unique Identifier: Name
def uid_name(T) -> str:
    return T.get_name()


# Unique Identifier: Level
def uid_level(T) -> int:
    return T.get_level()


# Unique Identifier: Level-Row
def uid_level_row(T) -> tuple:
    return (T.get_level(), T.get_row())


# ListConfigs
# - holds a list of an object type
# - generic class
class ListConfig(Generic[T]):

    def __init__(self, uid: Callable) -> None:
        self.__list: List[T] = []
        self.__uid: Callable = uid

    def find(
            self,
            _obj: T,
            ) -> T:
        for obj in self.__list:
            if self.__uid(obj) == self.__uid(_obj):
                return obj
        return None

    def add(
            self,
            obj: T,
            ) -> None:
        assert isinstance(obj, self.__orig_class__.__args__[0]), (
            "Object must be of type %s" % T
        )
        assert self.find(obj) is None, (
            "Object with uid %s is not unique." % (
                self.__uid(obj)
            )
        )
        self.__list.append(obj)

    def remove(
            self,
            _obj: T,
            ) -> None:
        for obj in self.__list:
            if self.__uid(obj) == self.__uid(_obj):
                self.__list.remove(obj)
                return

    def get(self) -> List[T]:
        return self.__list

    def set(
            self,
            _list: List[T],
            ) -> None:
        # Copy and Clear
        tmp_list = deepcopy(self.__list)
        self.__list.clear()
        # Add One-by-One
        try:
            for obj in _list:
                self.add(obj)
        # Restore Save if Failure
        except AssertionError:
            self.__list = tmp_list


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
        self.__bumpers = ListConfig[Decorations.Bumper](uid=uid_name)
        self.__top_plates = ListConfig[Decorations.TopPlate](uid=uid_name)
        # PACS Platform Decorations
        self.__full_risers = ListConfig[PACS.FullRiser](uid=uid_level)
        self.__row_risers = ListConfig[PACS.RowRiser](uid=uid_level_row)
        self.__brackets = ListConfig[PACS.Bracket](uid=uid_name)

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
            # By Object
            bumper: Decorations.Bumper = None,
            # By Name
            name: str = None,
            ) -> None:
        assert bumper or name, "Bumper object or name must be passed"
        # Create Object
        if name and not bumper:
            bumper = Decorations.Bumper(name)
        self.__bumpers.remove(bumper)

    # Bumper: Get
    def get_bumpers(
            self
            ) -> List[Decorations.Bumper]:
        return self.__bumpers.get()

    # Bumper: Set
    def set_bumpers(
            self,
            bumpers: List[Decorations.Bumper],
            ) -> None:
        self.__bumpers.set(bumpers)

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
            # By Object
            top_plate: Decorations.TopPlate = None,
            # By Name
            name: str = None
            ) -> None:
        assert top_plate or name, "Top plate object or name must be passed."
        if name and not top_plate:
            top_plate = Decorations.TopPlate(name=name)
        self.__top_plates.remove(top_plate)

    # Top Plate: Get
    def get_top_plates(
            self
            ) -> List[Decorations.TopPlate]:
        return self.__top_plates.get()

    # Top Plate: Set
    def set_top_plates(
            self,
            top_plates: List[Decorations.TopPlate]
            ) -> None:
        self.__top_plates.set(top_plates)

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
            # By Object
            full_riser: PACS.FullRiser = None,
            # By Level
            level: int = None
            ) -> None:
        assert full_riser or level, "Full riser object or level must be passed"
        if level and not full_riser:
            full_riser = PACS.FullRiser(level=level)
        self.__full_risers.remove(full_riser)

    # Full Risers: Get
    def get_full_risers(
            self,
            ) -> List[PACS.FullRiser]:
        return self.__full_risers.get()

    # Full Risers: Set
    def set_full_risers(
            self,
            full_risers: List[PACS.FullRiser]
            ) -> None:
        self.__full_risers.set(full_risers)

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
            # By Object
            row_riser: PACS.RowRiser = None,
            # By Level and Row
            level: int = None,
            row: int = None,
            ) -> None:
        assert row_riser or (level and row), (
            "Row riser object or level and row must be passed."
        )
        if (level and row) and not row_riser:
            row_riser = PACS.RowRiser(
                level=level,
                row=row,
            )
        self.__row_risers.remove(row_riser)

    # Row Risers: Get
    def get_row_risers(
            self,
            ) -> List[PACS.RowRiser]:
        return self.__row_risers.get()

    # Row Risers: Set
    def set_row_risers(
            self,
            row_risers: List[PACS.RowRiser]
            ) -> None:
        self.__row_risers.set(row_risers)

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
            # By Object
            bracket: PACS.Bracket = None,
            # By Parameters
            name: str = None
            ) -> None:
        assert bracket or name, "Bracket object or name must be passed"
        if name and not bracket:
            bracket = PACS.Bracket(name=name)
        self.__brackets.remove(bracket)

    # Brackets: Get
    def get_brackets(
            self,
            ) -> List[PACS.Bracket]:
        return self.__brackets.get()

    # Brackets: Set
    def set_brackets(
            self,
            brackets: List[PACS.Bracket],
            ) -> None:
        self.__brackets.set(brackets)
