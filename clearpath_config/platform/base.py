from clearpath_config.common import ListConfig, Platform
from clearpath_config.platform.decorations import Decorations
from typing import List


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
        self.__bumpers = ListConfig[
            Decorations.Bumper, str](
                uid=ListConfig.uid_name)
        self.__top_plates = ListConfig[
            Decorations.TopPlate, str](
                uid=ListConfig.uid_name)

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
