# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
# @copyright (c) 2024, Clearpath Robotics, Inc., All rights reserved.
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
from typing import List

from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.list import OrderedListConfig
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.manipulators.types.arms import (
    Arm,
    BaseArm,
)
from clearpath_config.manipulators.types.manipulator import BaseManipulator


class ArmListConfig(OrderedListConfig[BaseArm]):

    def __init__(self) -> None:
        super().__init__(obj_type=BaseArm)

    def to_dict(self) -> List[dict]:
        d = []
        for arm in self.get_all():
            d.append(arm.to_dict())
        return d


class ManipulatorConfig(BaseConfig):
    MANIPULATORS = "manipulators"
    ARMS = "arms"
    LIFTS = "lifts"
    TEMPLATE = {
        MANIPULATORS: {
            ARMS: ARMS,
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        ARMS: [],
    }

    def __init__(
            self,
            config: dict = {},
            ) -> None:
        # List Initialization
        self._arms = ArmListConfig()
        template = {
            self.KEYS[self.ARMS]: ManipulatorConfig.arms,
        }
        super().__init__(template, config, self.MANIPULATORS)

    @property
    def arms(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.ARMS],
            value=self._arms.to_dict()
        )
        return self._arms

    @arms.setter
    def arms(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Manipulators must be list of 'dict'")
        assert all([isinstance(i, dict) for i in value]), (
            "Manipulators must be list of 'dict'")
        arms_list = []
        for d in value:
            arm = Arm(d['model'])
            arm.from_dict(d)
            arms_list.append(arm)
        self._arms.set_all(arms_list)

    def get_all_manipulators(self) -> List[BaseManipulator]:
        manipulators = []
        # Arms
        manipulators.extend(self.get_all_arms())
        return manipulators

    def get_all_arms(self) -> List[BaseArm]:
        return self._arms.get_all()
