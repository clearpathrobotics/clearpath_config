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
from clearpath_config.manipulators.types.manipulator import BaseManipulator


class BaseGripper(BaseManipulator):
    MANIPULATOR_MODEL = "base"
    MANIPULATOR_TYPE = "gripper"


class FrankaGripper(BaseGripper):
    MANIPULATOR_MODEL = 'franka_gripper'
    JOINT_COUNT = 1

    @property
    def arm_id(self) -> str:
        return self._arm_id

    @arm_id.setter
    def arm_id(self, value: str) -> None:
        self._arm_id = value


class Kinova2FLite(BaseGripper):
    MANIPULATOR_MODEL = "kinova_2f_lite"
    JOINT_COUNT = 1


class Robotiq2F85(BaseGripper):
    MANIPULATOR_MODEL = "robotiq_2f_85"
    JOINT_COUNT = 1
    URDF_PARAMETERS = {
        'com_port': ''
    }


class Robotiq2F140(BaseGripper):
    MANIPULATOR_MODEL = "robotiq_2f_140"
    JOINT_COUNT = 1
    URDF_PARAMETERS = {
        'com_port': ''
    }


class Gripper():
    FRANKA_GRIPPER = FrankaGripper.MANIPULATOR_MODEL
    KINOVA_2F_LITE = Kinova2FLite.MANIPULATOR_MODEL
    ROBOTIQ_2F_140 = Robotiq2F140.MANIPULATOR_MODEL
    ROBOTIQ_2F_85 = Robotiq2F85.MANIPULATOR_MODEL

    MODEL = {
        FRANKA_GRIPPER: FrankaGripper,
        KINOVA_2F_LITE: Kinova2FLite,
        ROBOTIQ_2F_140: Robotiq2F140,
        ROBOTIQ_2F_85: Robotiq2F85,
    }

    @classmethod
    def assert_model(cls, model: str) -> None:
        assert model in cls.MODEL, (
            "Gripper model '%s' must be one of: '%s'" % (
                model,
                cls.MODEL.keys()
            )
        )

    def __new__(cls, model: str) -> BaseGripper:
        cls.assert_model(model)
        return cls.MODEL[model]()
