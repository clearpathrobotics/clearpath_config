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
from clearpath_config.common.types.ip import IP
from clearpath_config.common.types.port import Port
from clearpath_config.manipulators.types.grippers import Gripper
from clearpath_config.manipulators.types.manipulator import BaseManipulator


class BaseArm(BaseManipulator):
    MANIPULATOR_MODEL = "base"
    MANIPULATOR_TYPE = "arm"

    IP_ADDRESS = "192.168.131.40"
    IP_PORT = 10000

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            ip: str = IP_ADDRESS,
            port: int = IP_PORT,
            ros_parameters: dict = BaseManipulator.ROS_PARAMETERS,
            ros_parameters_template: dict = BaseManipulator.ROS_PARAMETERS_TEMPLATE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(
            idx, name, ros_parameters, ros_parameters_template, parent, xyz, rpy)
        self.config = {}
        self.gripper = None
        # IP Address
        self.ip = IP(ip)
        # IP Port
        self.port = Port(port)

    @classmethod
    def get_ip_from_idx(cls, idx: int) -> str:
        ip = cls.IP_ADDRESS.split('.')
        network_id = ip[0:3]
        host_id = int(ip[-1]) + idx
        return '.'.join(network_id) + '.' + str(host_id)

    def set_idx(self, idx: int) -> None:
        super().set_idx(idx)
        if 'ip' not in self.config:
            self.ip = self.get_ip_from_idx(idx)
        if self.gripper:
            self.gripper.name = self.name + '_gripper'
            self.gripper.parent = self.name + '_end_effector_link'

    @property
    def ip(self) -> str:
        return str(self._ip)

    @ip.setter
    def ip(self, ip: str) -> None:
        self._ip = IP(str(ip))

    @property
    def port(self) -> int:
        return int(self._port)

    @port.setter
    def port(self, port: int) -> None:
        self._port = Port(int(port))

    def to_dict(self) -> dict:
        d = super().to_dict()
        d['ip'] = self.ip
        d['port'] = self.port
        if self.gripper:
            d['gripper'] = self.gripper.to_dict()
        else:
            d['gripper'] = None
        return d

    def from_dict(self, d: dict) -> None:
        self.config = d
        super().from_dict(d)
        if 'gripper' in d:
            self.gripper = Gripper(d['gripper']['model'])
            self.gripper.from_dict(d['gripper'])
            self.gripper.set_name('%s_gripper' % self.get_name())
            if 'parent' not in d['gripper']:
                self.gripper.set_parent('%s_end_effector_link' % self.get_name())
        if 'ip' in d:
            self.ip = d['ip']
        if 'port' in d:
            self.port = d['port']


class KinovaGen3Dof6(BaseArm):
    MANIPULATOR_MODEL = "kinova_gen3_6dof"


class KinovaGen3Dof7(BaseArm):
    MANIPULATOR_MODEL = "kinova_gen3_7dof"


class KinovaGen3Lite(BaseArm):
    MANIPULATOR_MODEL = "kinova_gen3_lite"


class Arm():
    KINOVA_GEN3_6DOF = KinovaGen3Dof6.MANIPULATOR_MODEL
    KINOVA_GEN3_7DOF = KinovaGen3Dof7.MANIPULATOR_MODEL
    KINOVA_GEN3_LITE = KinovaGen3Lite.MANIPULATOR_MODEL

    MODEL = {
        KINOVA_GEN3_6DOF: KinovaGen3Dof6,
        KINOVA_GEN3_7DOF: KinovaGen3Dof7,
        KINOVA_GEN3_LITE: KinovaGen3Lite,
    }

    @classmethod
    def assert_model(cls, model: str) -> None:
        assert model in cls.MODEL, (
            "Arm model '%s' must be one of: '%s'" % (
                model,
                cls.MODEL.keys()
            )
        )

    def __new__(cls, model: str) -> BaseArm:
        cls.assert_model(model)
        return cls.MODEL[model]()
