from clearpath_config.common import (
    ListConfig,
    Platform,
)
from clearpath_config.platform.decorations import (
    BaseDecoration,
    Bumper,
    TopPlate,
    Structure,
)
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
        self.__structures = ListConfig[
            Structure, str](
                uid=ListConfig.uid_name)

    # Decorations: Get All
    def get_all_decorations(self) -> List[BaseDecoration]:
        decorations = []
        decorations.extend(self.get_bumpers())
        decorations.extend(self.get_top_plates())
        decorations.extend(self.get_structures())
        return decorations

    # Bumper: Add
    def add_bumper(
            self,
            # By Object
            bumper: Bumper = None,
            # By Parameters
            name: str = None,
            enabled: bool = Bumper.ENABLED,
            model: str = Bumper.DEFAULT,
            extension: float = Bumper.EXTENSION,
            parent: str = Bumper.PARENT,
            xyz: List[float] = Bumper.XYZ,
            rpy: List[float] = Bumper.RPY
            ) -> None:
        assert bumper or name, "Bumper object or name must be passed"
        # Create Object
        if name and not bumper:
            bumper = Bumper(
                name=name,
                enabled=enabled,
                model=model,
                extension=extension,
                parent=parent,
                xyz=xyz,
                rpy=rpy,
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
            parent: str = TopPlate.PARENT,
            xyz: List[float] = TopPlate.XYZ,
            rpy: List[float] = TopPlate.RPY
            ) -> None:
        assert top_plate or name, "Top plate object or name must be passed."
        if name and not top_plate:
            top_plate = TopPlate(
                name=name,
                enabled=enabled,
                model=model,
                parent=parent,
                xyz=xyz,
                rpy=rpy
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

    # Structure: Add
    def add_structure(
            self,
            # By Object
            structure: Structure = None,
            # By Parameters
            name: str = None,
            enabled: bool = Structure.ENABLED,
            model: str = Structure.DEFAULT,
            parent: str = Structure.PARENT,
            xyz: List[float] = Structure.XYZ,
            rpy: List[float] = Structure.RPY
            ) -> None:
        assert structure or name, (
            "Structure object or name must be passed")
        # Create Object
        if name and not structure:
            structure = Structure(
                name=name,
                enabled=enabled,
                model=model,
                parent=parent,
                xyz=xyz,
                rpy=rpy
            )
        self.__structures.add(structure)

    # Structure: Remove
    def remove_structure(
            self,
            # By Object or Name
            structure: Structure | str,
            ) -> None:
        self.__structures.remove(structure)

    # Structure: Get
    def get_structure(
            self,
            name: str
            ) -> Structure:
        return self.__structures.get(name)

    # Structure: Get All
    def get_structures(
            self
            ) -> List[Structure]:
        return self.__structures.get_all()

    # Structure: Set
    def set_structure(
            self,
            structure: Structure
            ) -> None:
        self.__structures.set(structure)

    # Structure: Set All
    def set_structures(
            self,
            structures: List[Structure]
            ) -> None:
        self.__structures.set_all(structures)
