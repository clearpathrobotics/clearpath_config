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
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.list import OrderedListConfig
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.mounts.types.fath_pivot import FathPivot
from clearpath_config.mounts.types.flir_ptu import FlirPTU
from clearpath_config.mounts.types.mount import BaseMount
from clearpath_config.mounts.types.pacs import PACS
from clearpath_config.mounts.types.post import Post
from clearpath_config.mounts.types.sick import SICKStand
from clearpath_config.mounts.types.disk import Disk
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
    POST = Post.MOUNT_MODEL
    DISK = Disk.MOUNT_MODEL

    TEMPLATE = {
        MOUNTS: {
            BRACKET: BRACKET,
            FATH_PIVOT: FATH_PIVOT,
            RISER: RISER,
            SICK: SICK,
            POST: POST,
            DISK: DISK,
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        BRACKET: [],
        FATH_PIVOT: [],
        RISER: [],
        SICK: [],
        POST: [],
        DISK: [],
    }

    def __init__(
            self,
            config: dict = {},
            bracket: List[PACS.Bracket] = DEFAULTS[BRACKET],
            fath_pivot: List[FathPivot] = DEFAULTS[FATH_PIVOT],
            riser: List[PACS.Riser] = DEFAULTS[RISER],
            sick_stand: List[SICKStand] = DEFAULTS[SICK],
            post: List[Post] = DEFAULTS[POST],
            disk: List[Disk] = DEFAULTS[DISK],
            ) -> None:
        # Initialization
        self.bracket = bracket
        self.fath_pivot = fath_pivot
        self.riser = riser
        self.sick_stand = sick_stand
        self.post = post
        self.disk = disk
        # Template
        template = {
            self.KEYS[self.BRACKET]: MountsConfig.bracket,
            self.KEYS[self.FATH_PIVOT]: MountsConfig.fath_pivot,
            self.KEYS[self.RISER]: MountsConfig.riser,
            self.KEYS[self.SICK]: MountsConfig.sick_stand,
            self.KEYS[self.POST]: MountsConfig.post,
            self.KEYS[self.DISK]: MountsConfig.disk,
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
    def post(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.POST],
            value=self._post.to_dict()
        )
        return self._post

    @post.setter
    def post(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Mounts must be list of 'dict'")
        assert all([isinstance(i, dict) for i in value]), (
            "Mounts must be list of 'dict'")
        mounts = MountListConfig()
        mount_list = []
        for d in value:
            mount = Post()
            mount.from_dict(d)
            mount_list.append(mount)
        mounts.set_all(mount_list)
        self._post = mounts

    @property
    def disk(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.DISK],
            value=self._disk.to_dict()
        )
        return self._disk

    @disk.setter
    def disk(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Mounts must be list of 'dict'")
        assert all([isinstance(i, dict) for i in value]), (
            "Mounts must be list of 'dict'")
        mounts = MountListConfig()
        mount_list = []
        for d in value:
            mount = Disk()
            mount.from_dict(d)
            mount_list.append(mount)
        mounts.set_all(mount_list)
        self._disk = mounts

    # Get All Mounts
    def get_all_mounts(self) -> List[BaseMount]:
        mounts = []
        mounts.extend(self.fath_pivot.get_all())
        mounts.extend(self.riser.get_all())
        mounts.extend(self.bracket.get_all())
        mounts.extend(self.sick_stand.get_all())
        mounts.extend(self.post.get_all())
        mounts.extend(self.disk.get_all())
        return mounts
