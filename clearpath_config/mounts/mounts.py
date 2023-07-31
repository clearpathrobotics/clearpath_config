# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
# @copyright (c) 2023, Clearpath Robotics, Inc., All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Clearpath Robotics nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.list import OrderedListConfig
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.mounts.types.mount import BaseMount
from clearpath_config.mounts.types.fath_pivot import FathPivot
from clearpath_config.mounts.types.flir_ptu import FlirPTU
from clearpath_config.mounts.types.sick import SICKStand
from clearpath_config.mounts.types.tower import Tower
from clearpath_config.mounts.types.pacs import PACS
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


class MountListConfig(OrderedListConfig[BaseMount]):
    def __init__(self) -> None:
        super().__init__(obj_type=BaseMount)

    def to_dict(self) -> List[dict]:
        d = []
        for accessory in self.get_all():
            d.append(accessory.to_dict())
        return d


class MountsConfig(BaseConfig):

    MOUNTS = "mounts"
    BRACKET = PACS.Bracket.MOUNT_MODEL
    FATH_PIVOT = FathPivot.MOUNT_MODEL
    RISER = PACS.Riser.MOUNT_MODEL
    SICK = SICKStand.MOUNT_MODEL
    TOWER = Tower.MOUNT_MODEL

    TEMPLATE = {
        MOUNTS: {
            BRACKET: BRACKET,
            FATH_PIVOT: FATH_PIVOT,
            RISER: RISER,
            SICK: SICK,
            TOWER: TOWER,
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        BRACKET: [],
        FATH_PIVOT: [],
        RISER: [],
        SICK: [],
        TOWER: [],
    }

    def __init__(
            self,
            config: dict = {},
            bracket: List[PACS.Bracket] = DEFAULTS[BRACKET],
            fath_pivot: List[FathPivot] = DEFAULTS[FATH_PIVOT],
            riser: List[PACS.Riser] = DEFAULTS[RISER],
            sick_stand: List[SICKStand] = DEFAULTS[SICK],
            tower: List[Tower] = DEFAULTS[TOWER],
            ) -> None:
        # Initialization
        self.bracket = bracket
        self.fath_pivot = fath_pivot
        self.riser = riser
        self.sick_stand = sick_stand
        self.tower = tower
        # Template
        template = {
            self.KEYS[self.BRACKET]: MountsConfig.bracket,
            self.KEYS[self.FATH_PIVOT]: MountsConfig.fath_pivot,
            self.KEYS[self.RISER]: MountsConfig.riser,
            self.KEYS[self.SICK]: MountsConfig.sick_stand,
            self.KEYS[self.TOWER]: MountsConfig.tower,
        }
        super().__init__(template, config, self.MOUNTS)

    @property
    def bracket(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.BRACKET],
            value=self._bracket.to_dict()
        )
        return self._bracket

    @bracket.setter
    def bracket(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Mounts must be list of 'dict'")
        assert all([isinstance(i, dict) for i in value]), (
            "Mounts must be list of 'dict'")
        mounts = MountListConfig()
        mount_list = []
        for d in value:
            mount = PACS.Bracket()
            mount.from_dict(d)
            mount_list.append(mount)
        mounts.set_all(mount_list)
        self._bracket = mounts

    @property
    def riser(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.RISER],
            value=self._riser.to_dict()
        )
        return self._riser

    @riser.setter
    def riser(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Mounts must be list of 'dict'")
        assert all([isinstance(i, dict) for i in value]), (
            "Mounts must be list of 'dict'")
        mounts = MountListConfig()
        mount_list = []
        for d in value:
            mount = PACS.Riser(rows=1, columns=1)
            mount.from_dict(d)
            mount_list.append(mount)
        mounts.set_all(mount_list)
        self._riser = mounts

    @property
    def fath_pivot(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.FATH_PIVOT],
            value=self._fath_pivot.to_dict()
        )
        return self._fath_pivot

    @fath_pivot.setter
    def fath_pivot(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Mounts must be list of 'dict'")
        assert all([isinstance(i, dict) for i in value]), (
            "Mounts must be list of 'dict'")
        mounts = MountListConfig()
        mount_list = []
        for d in value:
            mount = FathPivot()
            mount.from_dict(d)
            mount_list.append(mount)
        mounts.set_all(mount_list)
        self._fath_pivot = mounts

    @property
    def sick_stand(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.SICK],
            value=self._sick.to_dict()
        )
        return self._sick

    @sick_stand.setter
    def sick_stand(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Mounts must be list of 'dict'")
        assert all([isinstance(i, dict) for i in value]), (
            "Mounts must be list of 'dict'")
        mounts = MountListConfig()
        mount_list = []
        for d in value:
            mount = SICKStand()
            mount.from_dict(d)
            mount_list.append(mount)
        mounts.set_all(mount_list)
        self._sick = mounts

    @property
    def tower(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.TOWER],
            value=self._tower.to_dict()
        )
        return self._tower

    @tower.setter
    def tower(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Mounts must be list of 'dict'")
        assert all([isinstance(i, dict) for i in value]), (
            "Mounts must be list of 'dict'")
        mounts = MountListConfig()
        mount_list = []
        for d in value:
            mount = Tower()
            mount.from_dict(d)
            mount_list.append(mount)
        mounts.set_all(mount_list)
        self._tower = mounts

    # Get All Mounts
    def get_all_mounts(self) -> List[BaseMount]:
        mounts = []
        mounts.extend(self.get_fath_pivots())
        mounts.extend(self.get_risers())
        mounts.extend(self.get_brackets())
        mounts.extend(self.get_sick_stands())
        mounts.extend(self.get_towers())
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
        self._fath_pivot.add(fath_pivot)

    # FathPivot: Remove
    def remove_fath_pivot(
            self,
            # By Object or Index
            fath_pivot: FathPivot | int,
            ) -> None:
        self._fath_pivot.remove(fath_pivot)

    # FathPivot: Get
    def get_fath_pivot(
            self,
            idx: int
            ) -> FathPivot:
        return self._fath_pivot.get(idx)

    # FathPivot: Get All
    def get_fath_pivots(
            self,
            ) -> List[FathPivot]:
        return self._fath_pivot.get_all()

    # FathPivot: Set
    def set_fath_pivot(
            self,
            fath_pivot: FathPivot
            ) -> None:
        self._fath_pivot.set(fath_pivot)

    # FathPivot: Set All
    def set_fath_pivots(
            self,
            fath_pivots: List[FathPivot],
            ) -> None:
        self._fath_pivot.set_all(fath_pivots)

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
        self._riser.add(riser)

    # Risers: Remove
    def remove_riser(
            self,
            # By Object or Index
            riser: PACS.Riser | int,
            ) -> None:
        self._riser.remove(riser)

    # Risers: Get
    def get_riser(
            self,
            idx: int
            ) -> PACS.Riser:
        return self._riser.get(idx)

    # Risers: Get All
    def get_risers(
            self
            ) -> List[PACS.Riser]:
        return self._riser.get_all()

    # Risers: Set
    def set_riser(
            self,
            riser: PACS.Riser
            ) -> None:
        self._riser.set(riser)

    # Risers: Set All
    def set_risers(
            self,
            risers: List[PACS.Riser]
            ) -> None:
        self._riser.set_all(risers)

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
        self._bracket.add(bracket)

    # Brackets: Remove
    def remove_bracket(
            self,
            # By Object or Name
            bracket: PACS.Bracket | int,
            ) -> None:
        self._bracket.remove(bracket)

    # Bracket: Get
    def get_bracket(
            self,
            idx: int,
            ) -> PACS.Bracket:
        return self._bracket.get(idx)

    # Brackets: Get All
    def get_brackets(
            self,
            ) -> List[PACS.Bracket]:
        return self._bracket.get_all()

    # Bracket: Set
    def set_bracket(
            self,
            bracket: PACS.Bracket,
            ) -> None:
        self._bracket.set(bracket)

    # Brackets: Set All
    def set_brackets(
            self,
            brackets: List[PACS.Bracket],
            ) -> None:
        self._bracket.set_all(brackets)

    # Sick Stand: Add
    def add_sick_stand(
            self,
            # By Object
            sick_stand: SICKStand = None,
            # By Parameters
            parent: str = "base_link",
            model: str = SICKStand.INVERTED,
            xyz: List[float] = [0.0, 0.0, 0.0],
            rpy: List[float] = [0.0, 0.0, 0.0]
            ) -> None:
        if not sick_stand:
            sick_stand = SICKStand(
                parent=parent,
                model=model,
                xyz=xyz,
                rpy=rpy
            )
        self._sick.add(sick_stand)

    # Sick Stand: Remove
    def remove_sick_stand(
            self,
            # By Object or Name
            sick_stand: SICKStand | int,
            ) -> None:
        self._sick.remove(sick_stand)

    # Sick Stand: Get
    def get_sick_stand(
            self,
            idx: int,
            ) -> SICKStand:
        return self._sick.get(idx)

    # Sick Stand: Get All
    def get_sick_stands(
            self,
            ) -> List[SICKStand]:
        return self._sick.get_all()

    # Sick Stand: Set
    def set_sick_stand(
            self,
            sick_stand: SICKStand,
            ) -> None:
        self._sick.set(sick_stand)

    # Sick Stand: Set All
    def set_sick_stands(
            self,
            sick_stands: List[SICKStand],
            ) -> None:
        self._sick.set_all(sick_stands)

    # Tower: Add
    def add_tower(
            self,
            # By Object
            tower: Tower = None,
            # By Parameters
            parent: str = "base_link",
            model: str = Tower.SINGLE,
            xyz: List[float] = [0.0, 0.0, 0.0],
            rpy: List[float] = [0.0, 0.0, 0.0]
            ) -> None:
        if not tower:
            tower = Tower(
                parent=parent,
                model=model,
                xyz=xyz,
                rpy=rpy
            )
        self._tower.add(tower)

    # Tower: Remove
    def remove_tower(
            self,
            # By Object or Name
            tower: Tower | int,
            ) -> None:
        self._tower.remove(tower)

    # Tower: Get
    def get_tower(
            self,
            idx: int,
            ) -> Tower:
        return self._tower.get(idx)

    # Tower: Get All
    def get_towers(
            self,
            ) -> List[Tower]:
        return self._tower.get_all()

    # Tower: Set
    def set_tower(
            self,
            tower: Tower,
            ) -> None:
        self._tower.set(tower)

    # Tower: Set All
    def set_towers(
            self,
            towers: List[Tower],
            ) -> None:
        self._tower.set_all(towers)
