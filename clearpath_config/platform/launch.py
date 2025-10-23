# Software License Agreement (BSD)
#
# @author    Chris Iverach-Brereton <civerachb@clearpathrobotics.com>
# @copyright (c) 2025, Clearpath Robotics, Inc., All rights reserved.
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
from clearpath_config.common.utils.dictionary import (
    flip_dict,
)


class LaunchConfig(BaseConfig):
    """
    Parameters for user-defined additional launch files.

    These launch files may be specified by absolute path or relative path + package.

    Launch arguments may provided as a {str: Any} dict of key value pairs.
    """

    PACKAGE = 'package'
    PATH = 'path'
    ARGS = 'args'

    TEMPALTE = {
        PACKAGE: PACKAGE,
        PATH: PATH,
        ARGS: ARGS,
    }

    KEYS = flip_dict(TEMPALTE)

    DEFAULTS = {
        PATH: '',
        PACKAGE: None,
        ARGS: {}
    }

    def __init__(
        self,
        config: dict = {},
        path: str = DEFAULTS[PATH],
        package: str = DEFAULTS[PACKAGE],
        args: dict = DEFAULTS[ARGS],
    ):
        self._args = {}
        self._package = None
        self._path = ''

        setters = {
            self.KEYS[self.PACKAGE]: LaunchConfig.package,
            self.KEYS[self.PATH]: LaunchConfig.path,
            self.KEYS[self.ARGS]: LaunchConfig.args,
        }

        super().__init__(setters, config)

        self.path = path
        self.package = package
        self.args = args

    def from_dict(self, d: dict) -> None:
        self.path = d.get('path', '')
        self.package = d.get('package', None)
        self.args = d.get('args', {})

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        if not isinstance(path, str):
            raise TypeError(f'Path {path} must be a string')
        self._path = path

    @property
    def package(self) -> str:
        return self._package

    @package.setter
    def package(self, package: str) -> None:
        if (
            package is not None
            and not isinstance(package, str)
        ):
            raise TypeError(f'Package {package} must be null or a string')
        self._package = package

    @property
    def args(self) -> dict:
        return self._args

    @args.setter
    def args(self, args: dict) -> None:
        if args is None:
            args = {}

        if not isinstance(args, dict):
            raise TypeError(f'Arguments {args} must be of type "dict"')
        self._args = {}
        for arg in args:
            if not isinstance(arg, str):
                raise TypeError(f'Argument key {arg} must be of type "str"')
            self._args[arg] = args[arg]
