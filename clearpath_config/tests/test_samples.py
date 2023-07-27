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
import os
from clearpath_config.clearpath_config import ClearpathConfig
from clearpath_config.common.types.platform import Platform
from clearpath_config.tests.test_utils import assert_not_errors

sample = os.path.dirname(os.path.realpath(__file__)) + "/../sample"

A200_DEFAULT = sample + "/a200/a200_default.yaml"
A200_DUAL_LASER = sample + "/a200/a200_dual_laser.yaml"
A200_VELODYNE = sample + "/a200/a200_velodyne.yaml"

J100_DEFAULT = sample + "/j100/j100_default.yaml"
J100_DUAL_LASER = sample + "/j100/j100_dual_laser.yaml"
J100_VELODYNE = sample + "/j100/j100_velodyne.yaml"

A200_SAMPLES = [
    A200_DEFAULT,
    A200_DUAL_LASER,
    A200_VELODYNE
]

J100_SAMPLES = [
    J100_DEFAULT,
    J100_DUAL_LASER,
    J100_VELODYNE
]


class TestPlatformSamples:

    def test_a200_model(self):
        errors = []
        for sample in A200_SAMPLES:
            try:
                print(sample)
                cc = ClearpathConfig(sample)
            except AssertionError as ae:
                errors.append("A200 sample failed to load: %s" % ae.args[0])
            else:
                if cc.get_platform_model() != Platform.A200:
                    errors.append("Platform model does not match. %s =/= %s" % (
                        cc.get_platform_model(),
                        Platform.A200
                    ))
        assert_not_errors(errors)

    def test_j100_model(self):
        errors = []
        for sample in J100_SAMPLES:
            try:
                cc = ClearpathConfig(sample)
            except AssertionError as ae:
                errors.append("J100 sample failed to load: %s" % ae.args[0])
            else:
                if cc.get_platform_model() != Platform.J100:
                    errors.append("Platform model does not match. %s =/= %s" % (
                        cc.get_model(),
                        Platform.J100
                    ))
        assert_not_errors(errors)
