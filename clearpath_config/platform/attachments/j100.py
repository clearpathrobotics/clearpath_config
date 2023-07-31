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
# J100 Jackal Platform Configuration
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.platform import Platform
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.platform.attachments.config import BaseAttachmentsConfig
from clearpath_config.platform.types.bumper import Bumper
from clearpath_config.platform.types.fender import Fender


# J100 Jackal Attachments Configuration
class J100AttachmentsConfig(BaseConfig, BaseAttachmentsConfig):
    PLATFORM = Platform.J100

    ATTACHMENTS = "attachments"
    FRONT_BUMPER = "front_bumper"
    REAR_BUMPER = "rear_bumper"
    FRONT_FENDER = "front_fender"
    REAR_FENDER = "rear_fender"

    TEMPLATE = {
        ATTACHMENTS: {
            FRONT_BUMPER: FRONT_BUMPER,
            REAR_BUMPER: REAR_BUMPER,
            FRONT_FENDER: FRONT_FENDER,
            REAR_FENDER: REAR_FENDER
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        FRONT_BUMPER: {
            'name': FRONT_BUMPER,
            'enabled': Bumper.ENABLED,
            'extension': Bumper.EXTENSION,
            'model': Bumper.DEFAULT},
        REAR_BUMPER: {
            'name': REAR_BUMPER,
            'enabled': Bumper.ENABLED,
            'extension': Bumper.EXTENSION,
            'model': Bumper.DEFAULT
            },
        FRONT_FENDER: {
            'name': FRONT_FENDER,
            'enabled': Fender.ENABLED,
            'model': Fender.DEFAULT
        },
        REAR_FENDER: {
            'name': REAR_FENDER,
            'enabled': Fender.ENABLED,
            'model': Fender.DEFAULT
        },
    }

    def __init__(
            self,
            config: dict = {}
            ) -> None:
        BaseAttachmentsConfig.__init__(self)
        # Initialization
        self._config = {}
        self.front_bumper = self.DEFAULTS[self.FRONT_BUMPER]
        self.rear_bumper = self.DEFAULTS[self.REAR_BUMPER]
        self.front_fender = self.DEFAULTS[self.FRONT_FENDER]
        self.rear_fender = self.DEFAULTS[self.REAR_FENDER]
        # Setter Template
        setters = {
            self.KEYS[self.FRONT_BUMPER]: J100AttachmentsConfig.front_bumper,
            self.KEYS[self.REAR_BUMPER]: J100AttachmentsConfig.rear_bumper,
            self.KEYS[self.FRONT_FENDER]: J100AttachmentsConfig.front_fender,
            self.KEYS[self.REAR_FENDER]: J100AttachmentsConfig.rear_fender,
        }
        # Set from Config
        BaseConfig.__init__(self, setters, config, self.ATTACHMENTS)

    @property
    def front_bumper(self):
        front_bumper = self.bumpers.get(self.FRONT_BUMPER)
        self.set_config_param(
            key=self.KEYS[self.FRONT_BUMPER],
            value=front_bumper.to_dict()[self.FRONT_BUMPER]
        )
        return front_bumper

    @front_bumper.setter
    def front_bumper(self, value: dict | Bumper):
        if isinstance(value, dict):
            new = Bumper(name=self.FRONT_BUMPER)
            new.from_dict(value)
            self.bumpers.set(new)
        elif isinstance(value, Bumper):
            assert value.get_name() == self.FRONT_BUMPER, (
                "Front bumper must be Bumper with name %s" % self.FRONT_BUMPER
            )
            self.bumpers.set(new)
        else:
            assert isinstance(value, dict) or isinstance(value, Bumper), (
                "Bumper must be of type 'dict' or 'Bumper'"
            )

    @property
    def rear_bumper(self):
        rear_bumper = self.bumpers.get(self.REAR_BUMPER)
        self.set_config_param(
            key=self.KEYS[self.REAR_BUMPER],
            value=rear_bumper.to_dict()[self.REAR_BUMPER]
        )
        return rear_bumper

    @rear_bumper.setter
    def rear_bumper(self, value: dict | Bumper):
        if isinstance(value, dict):
            new = Bumper(name=self.REAR_BUMPER)
            new.from_dict(value)
            self.bumpers.set(new)
        elif isinstance(value, Bumper):
            assert value.get_name() == self.REAR_BUMPER, (
                "Rear bumper must be Bumper with name %s" % self.REAR_BUMPER
            )
            self.bumpers.set(new)
        else:
            assert isinstance(value, dict) or isinstance(value, Bumper), (
                "Bumper must be of type 'dict' or 'Bumper'"
            )

    @property
    def front_fender(self):
        front_fender = self.fenders.get(self.FRONT_FENDER)
        self.set_config_param(
            key=self.KEYS[self.FRONT_FENDER],
            value=front_fender.to_dict()[self.FRONT_FENDER]
        )
        return front_fender

    @front_fender.setter
    def front_fender(self, value: dict | Fender):
        if isinstance(value, dict):
            new = Fender(name=self.FRONT_FENDER)
            new.from_dict(value)
            self.fenders.set(new)
        elif isinstance(value, Fender):
            assert value.get_name() == self.FRONT_FENDER, (
                "Front fender must be Fender with name %s" % self.FRONT_FENDER
            )
            self.fenders.set(new)
        else:
            assert isinstance(value, dict) or isinstance(value, Fender), (
                "Fender must be of type 'dict' or 'Fender'"
            )

    @property
    def rear_fender(self):
        rear_fender = self.fenders.get(self.REAR_FENDER)
        self.set_config_param(
            key=self.KEYS[self.REAR_FENDER],
            value=rear_fender.to_dict()[self.REAR_FENDER]
        )
        return rear_fender

    @rear_fender.setter
    def rear_fender(self, value: dict | Fender):
        if isinstance(value, dict):
            new = Fender(name=self.REAR_FENDER)
            new.from_dict(value)
            self.fenders.set(new)
        elif isinstance(value, Fender):
            assert value.get_name() == self.REAR_FENDER, (
                "Rear fender must be Fender with name %s" % self.FRONT_FENDER
            )
            self.fenders.set(new)
        else:
            assert isinstance(value, dict) or isinstance(value, Fender), (
                "Fender must be of type 'dict' or 'Fender'"
            )
