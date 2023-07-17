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
from clearpath_config.common.types.accessory import Accessory, IndexedAccessory
from typing import List, Callable


class BaseSensor(IndexedAccessory):
    SENSOR_TYPE = "generic"
    SENSOR_MODEL = "base"
    TOPIC = "base"
    URDF_ENABLED = True
    LAUNCH_ENABLED = True
    ROS_PARAMETERS = {}

    class ROSParameter:
        def __init__(
                self,
                key: str,
                get: Callable,
                set: Callable
                ) -> None:
            self.key = key
            self.get = get
            self.set = set

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            topic: str = TOPIC,
            urdf_enabled: bool = URDF_ENABLED,
            launch_enabled: bool = LAUNCH_ENABLED,
            ros_parameters: str = ROS_PARAMETERS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            ) -> None:
        # Topic:
        # - should be automatically determined by the sensor's index
        # - should match the Clearpath API
        self.topic = str()
        self.set_topic(topic)
        # URDF Enable
        # - enables the sensor description in the generated URDF
        self.urdf_enabled = True
        self.enable_urdf() if urdf_enabled else self.disable_urdf()
        # Launch Enable
        # - enables the sensor launch in the generated launch
        self.launch_enabled = True
        self.enable_launch if launch_enabled else self.disable_launch()
        # ROS Parameters
        # - dictionary with parameters for launch file
        self.ros_parameters = {}
        self.ros_parameter_pairs = {}
        self.set_ros_parameters(ros_parameters)
        super().__init__(idx, name, parent, xyz, rpy)

    def to_dict(self) -> dict:
        d = {}
        d['model'] = self.get_sensor_model()
        d['urdf_enabled'] = self.get_urdf_enabled()
        d['launch_enabled'] = self.get_launch_enabled()
        d['parent'] = self.get_parent()
        d['xyz'] = self.get_xyz()
        d['rpy'] = self.get_rpy()
        d['ros_parameters'] = self.get_ros_parameters()
        return d

    def from_dict(self, d: dict) -> None:
        if 'urdf_enabled' in d:
            self.set_urdf_enabled(d['urdf_enabled'])
        if 'launch_enabled' in d:
            self.set_launch_enabled(d['launch_enabled'])
        if 'parent' in d:
            self.set_parent(d['parent'])
        if 'xyz' in d:
            self.set_xyz(d['xyz'])
        if 'rpy' in d:
            self.set_rpy(d['rpy'])
        if 'ros_parameters' in d:
            self.set_ros_parameters(d['ros_parameters'])

    @classmethod
    def get_sensor_type(cls) -> str:
        return cls.SENSOR_TYPE

    @classmethod
    def get_sensor_model(cls) -> str:
        return cls.SENSOR_MODEL

    @classmethod
    def get_name_from_idx(cls, idx: int) -> str:
        return "%s_%s" % (
            cls.get_sensor_type(),
            idx
        )

    @classmethod
    def get_topic_from_idx(cls, idx: int) -> str:
        return "%s/%s" % (
            cls.get_name_from_idx(idx),
            cls.TOPIC
        )

    def set_idx(self, idx: int) -> None:
        super().set_idx(idx)
        self.topic = self.get_topic_from_idx(idx)

    def get_topic(self) -> str:
        return self.topic

    def set_topic(self, topic: str) -> None:
        assert isinstance(topic, str), (
            "Topic '%s' of type '%s', expected 'str'" % (topic, type(topic))
        )
        assert " " not in topic, (
            "Topic '%s' contains empty spaces." % topic
        )
        self.topic = topic

    def enable_urdf(self) -> None:
        self.urdf_enabled = True

    def disable_urdf(self) -> None:
        self.urdf_enabled = False

    def set_urdf_enabled(self, enabled: bool) -> None:
        self.enable_urdf() if enabled else self.disable_urdf()

    def get_urdf_enabled(self) -> bool:
        return self.urdf_enabled

    def enable_launch(self) -> None:
        self.launch_enabled = True

    def disable_launch(self) -> None:
        self.launch_enabled = False

    def set_launch_enabled(self, enabled: bool) -> None:
        self.enable_launch() if enabled else self.disable_launch()

    def get_launch_enabled(self) -> bool:
        return self.launch_enabled

    def set_ros_parameters(self, ros_parameters: dict) -> None:
        assert isinstance(ros_parameters, dict), (
            "ROS paramaters must be a dictionary")
        for key, val in ros_parameters.items():
            for _, param in self.ros_parameter_pairs.items():
                if key == param.key:
                    param.set(self, val)
        self.ros_parameters = ros_parameters

    def get_ros_parameters(self) -> dict:
        for _, param in self.ros_parameter_pairs.items():
            self.ros_parameters[param.key] = param.get(self)
        return self.ros_parameters
