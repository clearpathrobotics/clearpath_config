# Software License Agreement (BSD)
#
# @author    Tony Baltovski <tbaltovski@clearpathrobotics.com>
# @copyright (c) 2026, Clearpath Robotics, Inc., All rights reserved.
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
from clearpath_config.common.types.namespace import Namespace
import pytest


class TestNamespace:

    def test_empty_namespace_is_valid(self):
        assert Namespace.is_valid("")

    def test_empty_namespace_construction(self):
        ns = Namespace("")
        assert str(ns) == ""

    def test_empty_namespace_equality(self):
        ns = Namespace("")
        assert ns == ""

    def test_default_namespace(self):
        ns = Namespace()
        assert str(ns) == "/"

    def test_valid_namespaces(self):
        valid = ["my_robot", "a0", "robot/sensor", "/"]
        for name in valid:
            ns = Namespace(name)
            assert str(ns) == name

    def test_invalid_namespaces(self):
        invalid = ["0bad", "bad//path", "bad__name", "bad@char"]
        for name in invalid:
            with pytest.raises(ValueError):
                Namespace(name)

    def test_set_namespace_empty_string(self):
        BaseConfig.set_namespace("test_ns")
        assert BaseConfig.get_namespace() == "test_ns"
        BaseConfig.set_namespace("")
        assert BaseConfig.get_namespace() == ""
        # Reset to default
        BaseConfig.set_namespace("/")

    def test_set_namespace_object(self):
        ns = Namespace("robot_1")
        BaseConfig.set_namespace(ns)
        assert BaseConfig.get_namespace() == "robot_1"
        # Reset to default
        BaseConfig.set_namespace("/")
