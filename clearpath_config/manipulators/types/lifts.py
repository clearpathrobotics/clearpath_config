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

from clearpath_config.common.types.accessory import Accessory
from clearpath_config.manipulators.types.manipulator import BaseManipulator


class BaseLift(BaseManipulator):
    MANIPULATOR_MODEL = 'base'
    MANIPULATOR_TYPE = 'lift'

    URDF_PARAMETERS = {}

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            ros_parameters: dict = BaseManipulator.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseManipulator.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(
            idx, name, ros_parameters, ros_parameters_template, parent, xyz, rpy)
        self.urdf_parameters = dict(self.URDF_PARAMETERS)

    def to_dict(self) -> dict:
        d = super().to_dict()
        for k, v in self.urdf_parameters.items():
            if v:
                d[k] = v
        return d

    def from_dict(self, d: dict) -> None:
        self.config = d
        super().from_dict(d)
        for k in self.urdf_parameters:
            if k in d:
                self.urdf_parameters[k] = d[k]

    def get_urdf_parameters(self) -> dict:
        d = {}
        for k, v in self.urdf_parameters.items():
            if v:
                d[k] = v
        return d


class Ewellix(BaseLift):
    MANIPULATOR_MODEL = 'ewellix'

    EWELLIX_TYPE = 'ewellix_type'
    ADD_PLATE = 'add_plate'
    PARAMETERS_FILE = 'parameters_file'
    INITIAL_POSITIONS = 'initial_positions'
    INITIAL_POSITIONS_FILE = 'initial_positions_file'
    GENERATE_ROS2_CONTROL_TAG = 'generate_ros2_control_tag'
    USE_FAKE_HARDWARE = 'use_fake_hardware'
    SIM_IGNITION = 'sim_ignition'
    PORT = 'port'
    BAUD = 'baud'
    TIMEOUT = 'timeout'
    CONVERSION = 'conversion'
    RATED_EFFORT = 'rated_effort'
    TOLERANCE = 'tolerance'

    URDF_PARAMETERS = {
        EWELLIX_TYPE: '',
        ADD_PLATE: '',
        PARAMETERS_FILE: '',
        INITIAL_POSITIONS: '',
        INITIAL_POSITIONS_FILE: '',
        GENERATE_ROS2_CONTROL_TAG: '',
        USE_FAKE_HARDWARE: '',
        SIM_IGNITION: '',
        PORT: '',
        BAUD: '',
        TIMEOUT: '',
        CONVERSION: '',
        RATED_EFFORT: '',
        TOLERANCE: '',
    }


class Lift():
    EWELLIX = Ewellix.MANIPULATOR_MODEL

    MODEL = {
        EWELLIX: Ewellix
    }

    @classmethod
    def assert_model(cls, model: str) -> None:
        assert model in cls.MODEL, (
            f'Lift model {model} must be one of {cls.MODEL.keys()}')

    def __new__(cls, model: str) -> BaseLift:
        cls.assert_model(model)
        return cls.MODEL[model]()
