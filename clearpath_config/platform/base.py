from clearpath_config.common import ListConfig, Platform
from clearpath_config.platform.decorations import Bumper, TopPlate
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
            Bumper, str](
                uid=ListConfig.uid_name)
        self.__top_plates = ListConfig[
            TopPlate, str](
                uid=ListConfig.uid_name)

    # Bumper: Add
    def add_bumper(
            self,
            # By Object
            bumper: Bumper = None,
            # By Parameters
            name: str = None,
            enabled: bool = True,
            extension: float = 0.0,
            model: str = Bumper.DEFAULT,
            ) -> None:
        assert bumper or name, "Bumper object or name must be passed"
        # Create Object
        if name and not bumper:
            bumper = Bumper(
                name=name,
                enabled=enabled,
                extension=extension,
                model=model
            )
        self.__bumpers.add(bumper)

    # Bumper: Remove
    def remove_bumper(
            self,
            # By Object or Name
            bumper: Bumper | str,
            ) -> None:
        self.__bumpers.remove(bumper)

    # Bumper: Get
    def get_bumper(
            self,
            name: str,
            ) -> Bumper:
        return self.__bumpers.get(name)

    # Bumper: Get All
    def get_bumpers(
            self
            ) -> List[Bumper]:
        return self.__bumpers.get_all()

    # Bumper: Set
    def set_bumper(
            self,
            bumper: Bumper,
            ) -> None:
        self.__bumpers.set(bumper)

    # Bumper: Set All
    def set_bumpers(
            self,
            bumpers: List[Bumper],
            ) -> None:
        self.__bumpers.set_all(bumpers)

    # Top Plate: Add
    def add_top_plate(
            self,
            # By Object
            top_plate: TopPlate = None,
            # By Parameters
            name: str = None,
            enabled: bool = True,
            model: str = TopPlate.DEFAULT,
            ) -> None:
        assert top_plate or name, "Top plate object or name must be passed."
        if name and not top_plate:
            top_plate = TopPlate(
                name=name,
                enabled=enabled,
                model=model
            )
        self.__top_plates.add(top_plate)

    # Top Plate: Remove
    def remove_top_plate(
            self,
            # By Object or Name
            top_plate: TopPlate | str,
            ) -> None:
        self.__top_plates.remove(top_plate)

    # Top Plate: Get
    def get_top_plate(
            self,
            name: str
            ) -> TopPlate:
        return self.__top_plates.get(name)

    # Top Plate: Get All
    def get_top_plates(
            self
            ) -> List[TopPlate]:
        return self.__top_plates.get_all()

    # Top Plate: Set
    def set_top_plate(
            self,
            top_plate: TopPlate
            ) -> None:
        self.__top_plates.set(top_plate)

    # Top Plate: Set All
    def set_top_plates(
            self,
            top_plates: List[TopPlate]
            ) -> None:
        self.__top_plates.set_all(top_plates)
