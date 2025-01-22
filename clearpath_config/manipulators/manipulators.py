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
from clearpath_config.manipulators.types.lifts import (
    BaseLift,
    Lift,
)
from clearpath_config.manipulators.types.manipulator import BaseManipulator


class ManipulatorListConfig(OrderedListConfig[BaseManipulator]):

    def __init__(self) -> None:
        super().__init__(obj_type=BaseManipulator)

    def to_dict(self) -> List[dict]:
        d = []
        for manipulator in self.get_all():
            d.append(manipulator.to_dict())
        return d


class ManipulatorConfig(BaseConfig):
    MANIPULATORS = 'manipulators'
    ARMS = 'arms'
    LIFTS = 'lifts'
    TEMPLATE = {
        MANIPULATORS: {
            ARMS: ARMS,
            LIFTS: LIFTS
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        ARMS: [],
        LIFTS: [],
    }

    def __init__(
            self,
            config: dict = {},
            ) -> None:
        # List Initialization
        self._arms = ManipulatorListConfig()
        self._lifts = ManipulatorListConfig()
        template = {
            self.KEYS[self.ARMS]: ManipulatorConfig.arms,
            self.KEYS[self.LIFTS]: ManipulatorConfig.lifts
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
        assert isinstance(value, list), 'Manipulators must be of type "dict"'
        assert all([isinstance(i, dict) for i in value]), 'Manipulators must be of type "dict"'  # noqa:C419, E501
        arms_list = []
        for d in value:
            arm = Arm(d['model'])
            arm.from_dict(d)
            arms_list.append(arm)
        self._arms.set_all(arms_list)

    @property
    def lifts(self) -> OrderedListConfig:
        self.set_config_param(
            key=self.KEYS[self.LIFTS],
            value=self._lifts.to_dict()
        )
        return self._lifts

    @lifts.setter
    def lifts(self, value: List[dict]) -> None:
        assert isinstance(value, list), (
            "Manipulators must be list of 'dict'")
        assert all(isinstance(i, dict) for i in value), (
            "Manipulators must be list of 'dict'")
        lifts_list = []
        for d in value:
            lift = Lift(d['model'])
            lift.from_dict(d)
            lifts_list.append(lift)
        self._lifts.set_all(lifts_list)

    def get_all_manipulators(self) -> List[BaseManipulator]:
        manipulators = []
        # Arms
        manipulators.extend(self.get_all_arms())
        manipulators.extend(self.get_all_lifts())
        return manipulators

    def get_all_arms(self) -> List[BaseArm]:
        return self._arms.get_all()

    def get_all_lifts(self) -> List[BaseLift]:
        return self._lifts.get_all()
