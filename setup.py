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
from setuptools import setup
import os

package_name = "clearpath_config"

setup(
    name=package_name,
    version="0.2.9",
    packages=[
        package_name,
        package_name + ".common",
        package_name + ".common.types",
        package_name + ".common.utils",
        package_name + ".links",
        package_name + ".links.types",
        package_name + ".mounts",
        package_name + ".mounts.types",
        package_name + ".platform",
        package_name + ".platform.attachments",
        package_name + ".platform.types",
        package_name + ".sensors",
        package_name + ".sensors.types",
        package_name + ".system",
    ],
    data_files=[
        # Install marker file in the package index
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        # Include the package.xml file
        (os.path.join("share", package_name), ["package.xml"]),
        (os.path.join("share", package_name, "sample"), [
            package_name + "/sample/a200/a200_default.yaml",
            package_name + "/sample/a200/a200_dual_laser.yaml",
            package_name + "/sample/a200/a200_sample.yaml",
            package_name + "/sample/a200/a200_velodyne.yaml",
            package_name + "/sample/j100/j100_default.yaml",
            package_name + "/sample/j100/j100_dual_laser.yaml",
            package_name + "/sample/j100/j100_sample.yaml",
            package_name + "/sample/j100/j100_velodyne.yaml",
            package_name + "/sample/w200/w200_default.yaml",
            package_name + "/sample/w200/w200_dual_laser.yaml",
            package_name + "/sample/w200/w200_velodyne.yaml",
            ]),
    ],
    install_requires=[
        "setuptools",
        "requests",
        'importlib-metadata; python_version == "3.8"',
    ],
    zip_safe=True,
    maintainer="Luis Camero",
    maintainer_email="lcamero@clearpathrobotics.com",
    description="Clearpath Configuration YAML Parser and Writer",
    license="BSD-3",
    tests_require=['pytest']
)
