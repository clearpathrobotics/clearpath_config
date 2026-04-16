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
from clearpath_config.common.types.platform import Platform
from clearpath_config.platform.attachments.config import AttachmentsConfig
from clearpath_config.platform.types.attachment import BaseAttachment


class AttachmentsConfigMux:

    def __new__(cls, platform: str, attachments: dict = None) -> AttachmentsConfig:
        # Look up the platform's attachment class from the registry
        platform_cls = Platform.get(platform)
        attachment_cls = platform_cls.ATTACHMENT_CLASS
        if attachment_cls is None:
            return AttachmentsConfig(BaseAttachment)
        if not attachments:
            return AttachmentsConfig(attachment_cls)
        # Pre-Process Entries
        attachments = AttachmentsConfigMux.preprocess(platform, attachments)
        # Add All Attachments from all registered platforms
        attachments_config = AttachmentsConfig(BaseAttachment)
        for name in Platform.all_names():
            pcls = Platform.get(name)
            if pcls.ATTACHMENT_CLASS is not None:
                ac = AttachmentsConfig(pcls.ATTACHMENT_CLASS)
                ac.config = attachments
                attachments_config += ac
        return attachments_config

    @staticmethod
    def preprocess(platform: str, attachments: dict):
        for i, a in enumerate(attachments):
            if 'name' not in a:
                raise ValueError(f'Attachment {a} is missing parameter "name"')
            if 'type' not in a:
                raise ValueError(f'Attachment {a} is missing parameter "type"')
            if '.' not in a['type']:
                a['type'] = f'{platform}.{a["type"]}'
            attachments[i] = a
        return attachments
