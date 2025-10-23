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
import os
from typing import List

from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.utils.dictionary import flip_dict


class BashConfig(BaseConfig):
    """
    Contains additional BASH sources and envars.

    These are passed to the generator for inclusion in setup.bash.
    """

    SOURCE = 'source'
    ENV = 'env'

    TEMPLATE = {
        SOURCE: SOURCE,
        ENV: ENV,
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        SOURCE: [],
        ENV: {},
    }

    def __init__(
        self,
        config: dict = {},
        source: List[str] = DEFAULTS[SOURCE],
        env: dict = DEFAULTS[ENV],
    ) -> None:
        self._env = {}
        self._source = []

        setters = {
            self.KEYS[self.SOURCE]: BashConfig.additional_sources,
            self.KEYS[self.ENV]: BashConfig.additional_envars,
        }

        super().__init__(setters, config)

        self.additional_envars = env
        self.additional_sources = source

    @property
    def additional_sources(self) -> List[str]:
        return self._source

    @additional_sources.setter
    def additional_sources(self, sources: List[str]) -> None:
        self._source.clear()
        for f in sources:
            if not isinstance(f, str):
                raise TypeError(f'Bash source {f} must be a string')
            if not os.path.exists(f):
                raise FileNotFoundError(f'Bash source {f} does not exist')
            self._source.append(f)

    @property
    def additional_envars(self) -> dict:
        return self._env

    @additional_envars.setter
    def additional_envars(self, envars: dict) -> None:
        self._env.clear()
        for env in envars:
            if not isinstance(env, str):
                raise TypeError(f'Environment variable {env}={envars[env]} must be a string')
            self._env[env] = str(envars[env])
