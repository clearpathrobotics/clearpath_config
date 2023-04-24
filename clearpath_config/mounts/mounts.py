from clearpath_config.common import Accessory, OrderedListConfig
from clearpath_config.mounts.base import BaseMount
from clearpath_config.mounts.fath_pivot import FathPivot
from clearpath_config.mounts.flir_ptu import FlirPTU
from clearpath_config.mounts.pacs import PACS
from typing import List


class Mount():
    FATH_PIVOT = FathPivot.MOUNT_MODEL
    FLIR_PTU = FlirPTU.MOUNT_MODEL
    PACS_RISER = PACS.Riser.MOUNT_MODEL
    PACS_BRACKET = PACS.Bracket.MOUNT_MODEL

    MODEL = {
        FATH_PIVOT: FathPivot,
        FLIR_PTU: FlirPTU,
        PACS_RISER: PACS.Riser,
        PACS_BRACKET: PACS.Bracket
    }

    def __new__(cls, model: str) -> BaseMount:
        assert model in Mount.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                Mount.MODEL.keys()
            )
        )
        return Mount.MODEL[model]()


class MountsConfig:
    def __init__(self) -> None:
        # Fath Pivot
        self.__fath_pivots = OrderedListConfig[FathPivot]()
        # Flir PTU
        self.__flir_ptus = OrderedListConfig[FlirPTU]()
        # PACS Riser
        self.__pacs_risers = OrderedListConfig[PACS.Riser]()
        # PACS Brackets
        self.__pacs_brackets = OrderedListConfig[PACS.Bracket]()

    # Get All Mounts
    def get_all_mounts(self) -> List[BaseMount]:
        mounts = []
        mounts.extend(self.get_fath_pivots())
        mounts.extend(self.get_flir_ptus())
        mounts.extend(self.get_risers())
        mounts.extend(self.get_brackets())
        return mounts

    # FathPivot: Add
    def add_fath_pivot(
            self,
            # By Object
            fath_pivot: FathPivot = None,
            # By Parameters
            parent: str = "base_link",
            angle: float = FathPivot.ANGLE,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ):
        if not fath_pivot:
            fath_pivot = FathPivot(
                parent,
                angle,
                xyz,
                rpy
            )
        self.__fath_pivots.add(fath_pivot)

    # FathPivot: Remove
    def remove_fath_pivot(
            self,
            # By Object or Index
            fath_pivot: FathPivot | int,
            ) -> None:
        self.__fath_pivots.remove(fath_pivot)

    # FathPivot: Get
    def get_fath_pivot(
            self,
            idx: int
            ) -> FathPivot:
        return self.__fath_pivots.get(idx)

    # FathPivot: Get All
    def get_fath_pivots(
            self,
            ) -> List[FathPivot]:
        return self.__fath_pivots.get_all()

    # FathPivot: Set
    def set_fath_pivot(
            self,
            fath_pivot: FathPivot
            ) -> None:
        self.__fath_pivots.set(fath_pivot)

    # FathPivot: Set All
    def set_fath_pivots(
            self,
            fath_pivots: List[FathPivot],
            ) -> None:
        self.__fath_pivots.set_all(fath_pivots)

    # FlirPTU: Add
    def add_flir_ptu(
            self,
            # By Object
            flir_ptu: FlirPTU = None,
            # By Parameters
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            tty_port: str = FlirPTU.TTY_PORT,
            tcp_port: int = FlirPTU.TCP_PORT,
            ip: str = FlirPTU.IP_ADDRESS,
            connection_type: str = FlirPTU.CONNECTION_TYPE,
            limits_enabled: bool = FlirPTU.LIMITS_ENABLED,
            ) -> None:
        if not flir_ptu:
            flir_ptu = FlirPTU(
                parent,
                xyz,
                rpy,
                tty_port,
                tcp_port,
                ip,
                connection_type,
                limits_enabled,
            )
        self.__flir_ptus.add(flir_ptu)

    # FlirPTU: Remove
    def remove_flir_ptu(
            self,
            # By Object or Index
            flir_ptu: FlirPTU | int,
            ) -> None:
        self.__flir_ptus.remove(flir_ptu)

    # FlirPTU: Get
    def get_flir_ptu(
            self,
            idx: int
            ) -> FlirPTU:
        return self.__flir_ptus.get(idx)

    # FlirPTU: Get All
    def get_flir_ptus(
            self
            ) -> List[FlirPTU]:
        return self.__flir_ptus.get_all()

    # FlirPTU: Set
    def set_flir_ptu(
            self,
            flir_ptu: FlirPTU,
            ) -> None:
        self.__flir_ptus.set(flir_ptu)

    # FlirPTU: Set All
    def set_flir_ptus(
            self,
            flir_ptus: List[FlirPTU]
            ) -> None:
        self.__flir_ptus.set_all(flir_ptus)

    # Risers: Add
    def add_riser(
            self,
            # By Object
            riser: PACS.Riser = None,
            # By Parameters
            rows: int = None,
            columns: int = None,
            thickness: float = PACS.Riser.THICKNESS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ) -> None:
        assert riser or (
            rows is not None and (
                columns is not None)), (
            "Riser object or rows, columns, and height must be passed"
        )
        if not riser:
            riser = PACS.Riser(
                rows,
                columns,
                thickness,
                parent,
                xyz,
                rpy
            )
        self.__pacs_risers.add(riser)

    # Risers: Remove
    def remove_riser(
            self,
            # By Object or Index
            riser: PACS.Riser | int,
            ) -> None:
        self.__pacs_risers.remove(riser)

    # Risers: Get
    def get_riser(
            self,
            idx: int
            ) -> PACS.Riser:
        return self.__pacs_risers.get(idx)

    # Risers: Get All
    def get_risers(
            self
            ) -> List[PACS.Riser]:
        return self.__pacs_risers.get_all()

    # Risers: Set
    def set_riser(
            self,
            riser: PACS.Riser
            ) -> None:
        self.__pacs_risers.set(riser)

    # Risers: Set All
    def set_risers(
            self,
            risers: List[PACS.Riser]
            ) -> None:
        self.__pacs_risers.set_all(risers)

    # Brackets: Add
    def add_bracket(
            self,
            # By Object
            bracket: PACS.Bracket = None,
            # By Parameters
            parent: str = "base_link",
            model: str = PACS.Bracket.DEFAULT,
            xyz: List[float] = [0.0, 0.0, 0.0],
            rpy: List[float] = [0.0, 0.0, 0.0]
            ) -> None:
        if not bracket:
            bracket = PACS.Bracket(
                parent=parent,
                model=model,
                xyz=xyz,
                rpy=rpy
            )
        self.__pacs_brackets.add(bracket)

    # Brackets: Remove
    def remove_bracket(
            self,
            # By Object or Name
            bracket: PACS.Bracket | int,
            ) -> None:
        self.__pacs_brackets.remove(bracket)

    # Bracket: Get
    def get_bracket(
            self,
            idx: int,
            ) -> PACS.Bracket:
        return self.__pacs_brackets.get(idx)

    # Brackets: Get All
    def get_brackets(
            self,
            ) -> List[PACS.Bracket]:
        return self.__pacs_brackets.get_all()

    # Bracket: Set
    def set_bracket(
            self,
            bracket: PACS.Bracket,
            ) -> None:
        self.__pacs_brackets.set(bracket)

    # Brackets: Set All
    def set_brackets(
            self,
            brackets: List[PACS.Bracket],
            ) -> None:
        self.__pacs_brackets.set_all(brackets)
