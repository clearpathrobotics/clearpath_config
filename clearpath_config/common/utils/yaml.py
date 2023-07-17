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
import yaml


# Get Valid Path
def find_valid_path(path, cwd=None):
    abspath = path
    if cwd:
        relpath = os.path.join(cwd, path)
    else:
        relpath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), path)
    if not os.path.isfile(abspath) and not os.path.isfile(relpath):
        return None
    if os.path.isfile(abspath):
        path = abspath
    elif os.path.isfile(relpath):
        path = relpath
    return path


def read_yaml(path: str) -> dict:
    # Check YAML Path
    path = find_valid_path(path, os.getcwd())
    assert path, "YAML file '%s' could not be found" % path
    # Check YAML can be Opened
    try:
        config = yaml.load(open(path), Loader=yaml.SafeLoader)
    except yaml.scanner.ScannerError:
        raise AssertionError(
            "YAML file '%s' is not well formed" % path)
    except yaml.constructor.ConstructorError:
        raise AssertionError(
            "YAML file '%s' is attempting to create unsafe objects" % (
                path))
    # Check contents are a Dictionary
    assert isinstance(config, dict), (
        "YAML file '%s' is not a dictionary" % path)
    return config


def write_yaml(path: str, config: dict) -> None:
    yaml_file = open(path, "w+")
    yaml.Dumper.ignore_aliases = lambda *args: True
    yaml.dump(
        config,
        yaml_file,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )
