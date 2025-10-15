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


# SerialNumber
# - Clearpath Robots Serial Number
# - ex. cpr-j100-0100
# - drop 'cpr' prefix as it is not required
class SerialNumber:
    SERIAL_NUMBER = 'serial_number'

    def __init__(self, sn: str) -> None:
        self.model, self.unit = SerialNumber.parse(sn)

    def __str__(self) -> str:
        return self.get_serial()

    def from_dict(self, config: dict) -> None:
        if not isinstance(config, dict):
            raise TypeError('Config must be of type "dict"')
        if self.SERIAL_NUMBER not in config:
            raise ValueError(f'Key "{self.SERIAL_NUMBER}" must be in config')
        self.model, self.unit = SerialNumber.parse(config[self.SERIAL_NUMBER])

    @staticmethod
    def parse(sn: str) -> tuple:
        if not isinstance(sn, str):
            raise TypeError(f'Serial Number "{sn}" must be string')
        sn_tokens = sn.lower().strip().split('-')
        if len(sn_tokens) <= 0 or len(sn_tokens) >= 4:
            raise ValueError(
                f'Serial number {sn}" must be delimited by hypens "-" and have 2 or 3 fields (e.g. cpr-a300-00001 or a300-00001), or 1 (generic) field'  # noqa: E501
            )
        # Remove CPR Prefix
        if len(sn_tokens) == 3:
            if sn_tokens[0] != 'cpr':
                raise ValueError(
                    f'Serial number with 3 fields must start with "cpr" not "{sn_tokens[0]}"'
                )
            sn_tokens = sn_tokens[1:]
        # Silently replace A201 prefix with A200
        # Mechanically both are effectively identical, and re-use the same options & payloads
        if sn_tokens[0] == 'a201':
            sn_tokens[0] = 'a200'
        # Match to Robot
        if sn_tokens[0] not in Platform.ALL:
            raise ValueError(
                f'Serial number model entry {sn_tokens[0]} must be one of {Platform.ALL}'
            )

        # Verify that the platform is well-supported and not deprecated
        Platform.assert_is_supported(sn_tokens[0])
        Platform.notify_if_deprecated(sn_tokens[0])

        # Generic Robot
        if sn_tokens[0] == Platform.GENERIC:
            if len(sn) > 1:
                return (sn_tokens[0], sn[1])
            else:
                return (sn_tokens[0], 'xxxx')
        # Check Number
        if not sn_tokens[1].isdecimal():
            raise ValueError(f'Serial number unit entry "{sn_tokens[1]}" must be an integer')
        return (sn_tokens[0], sn_tokens[1])

    def get_model(self) -> str:
        return self.model

    def get_unit(self) -> str:
        return self.unit

    def get_serial(self, prefix=False) -> str:
        if prefix:
            return '-'.join(['cpr', self.model, self.unit])
        else:
            return '-'.join([self.model, self.unit])
