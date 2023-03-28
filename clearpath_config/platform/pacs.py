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
