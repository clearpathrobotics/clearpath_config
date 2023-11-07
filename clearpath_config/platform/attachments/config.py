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
from clearpath_config.common.types.list import ListConfig
from clearpath_config.common.utils.dictionary import merge_dict
from clearpath_config.platform.types.attachment import BaseAttachment
from typing import List


class AttachmentListConfig(ListConfig[BaseAttachment, str]):
    def __init__(self) -> None:
        super().__init__(
            uid=lambda obj: obj.get_name(),
            obj_type=BaseAttachment,
            uid_type=str
        )

    def to_dict(self) -> dict:
        d = {}
        for decoration in self.get_all():
            merge_dict(d, decoration.to_dict())
        return d


# Attachments Config
# - to be used by all platforms.
class AttachmentsConfig:
    def __init__(
            self,
            attachment,
            config: dict = {}
            ) -> None:
        self._attach_type = attachment
        self._attachments = AttachmentListConfig()
        self.config = config

    def __add__(self, other):
        self._attachments.extend(other.get_all())
        return self

    def get_all(self) -> List[BaseAttachment]:
        return self._attachments.get_all()

    @property
    def config(self):
        return [a.to_dict() for a in self.get_all()]

    @config.setter
    def config(self, attachments: list):
        # Clear Previous
        self._attachments.remove_all()
        # Load New
        for a in attachments:
            if self._attach_type.is_valid(a['type']):
                attachment = self._attach_type(a['type'])()
                attachment.from_dict(a)
                self._attachments.add(attachment)
