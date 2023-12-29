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


# File
# - file class
class File:
    def __init__(self, path: str, creatable=False, exists=False, make_abs=True) -> None:
        if creatable:
            assert File.is_creatable(path)
        if exists:
            assert File.is_exists(path)
        self.path = File.clean(path, make_abs)

    def __str__(self) -> str:
        return self.path

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.path == other
        elif isinstance(other, File):
            return self.path == other.path
        else:
            return False

    @staticmethod
    def clean(path: str, make_abs=True) -> str:
        if not path:
            return ""
        path = os.path.expanduser(path)
        path = os.path.normpath(path)
        if make_abs:
            path = os.path.abspath(path)
        return path

    @staticmethod
    def is_creatable(path: str, make_abs=True) -> bool:
        path = File.clean(path, make_abs)
        dirname = os.path.dirname(path) or os.getcwd()
        return os.access(dirname, os.W_OK)

    @staticmethod
    def is_exists(path: str, make_abs=True) -> bool:
        path = File.clean(path, make_abs)
        return os.path.exists(path)

    def get_path(self) -> str:
        return self.path
