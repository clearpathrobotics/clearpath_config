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
from clearpath_config.platform.attachments.a200 import A200Attachment
from clearpath_config.platform.attachments.config import AttachmentsConfig
from clearpath_config.platform.attachments.dd100 import DD100Attachment
from clearpath_config.platform.attachments.do100 import DO100Attachment
from clearpath_config.platform.attachments.dd150 import DD150Attachment
from clearpath_config.platform.attachments.do150 import DO150Attachment
from clearpath_config.platform.attachments.generic import GENERICAttachment
from clearpath_config.platform.attachments.j100 import J100Attachment
from clearpath_config.platform.attachments.w200 import W200Attachment
from clearpath_config.platform.types.attachment import BaseAttachment


class AttachmentsConfigMux:
    PLATFORM = {
        Platform.A200: AttachmentsConfig(A200Attachment),
        Platform.DD100: AttachmentsConfig(DD100Attachment),
        Platform.DO100: AttachmentsConfig(DO100Attachment),
        Platform.DD150: AttachmentsConfig(DD150Attachment),
        Platform.DO150: AttachmentsConfig(DO150Attachment),
        Platform.GENERIC: AttachmentsConfig(GENERICAttachment),
        Platform.J100: AttachmentsConfig(J100Attachment),
        Platform.W200: AttachmentsConfig(W200Attachment),
    }

    def __new__(cls, platform: str, attachments: dict = None) -> AttachmentsConfig:
        # Check Platform is Supported
        assert platform in cls.PLATFORM, (
            "Platform '%s' must be one of: '%s'" % (
                platform,
                cls.PLATFORM.keys()
            )
        )
        if not attachments:
            return cls.PLATFORM[platform]
        # Pre-Process Entries
        attachments = AttachmentsConfigMux.preprocess(platform, attachments)
        # Add All Attachments
        attachments_config = AttachmentsConfig(BaseAttachment)
        for p in cls.PLATFORM:
            cls.PLATFORM[p].config = attachments
            attachments_config += cls.PLATFORM[p]
        return attachments_config

    @staticmethod
    def preprocess(platform: str, attachments: dict):
        for i, a in enumerate(attachments):
            assert 'name' in a, "An attachment is missing 'name'"
            assert 'type' in a, "An attachment is missing 'type'"
            if '.' not in a['type']:
                a['type'] = "%s.%s" % (platform, a['type'])
            attachments[i] = a
        return attachments
