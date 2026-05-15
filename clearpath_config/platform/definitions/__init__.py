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

# Import all concrete platform definitions so they auto-register
from clearpath_config.platform.definitions.a200 import A200PlatformConfig  # noqa: F401
from clearpath_config.platform.definitions.a300 import A300PlatformConfig  # noqa: F401
from clearpath_config.platform.definitions.dd100 import DD100PlatformConfig  # noqa: F401
from clearpath_config.platform.definitions.dd150 import DD150PlatformConfig  # noqa: F401
from clearpath_config.platform.definitions.do100 import DO100PlatformConfig  # noqa: F401
from clearpath_config.platform.definitions.do150 import DO150PlatformConfig  # noqa: F401
from clearpath_config.platform.definitions.generic import GenericPlatformConfig  # noqa: F401
from clearpath_config.platform.definitions.j100 import J100PlatformConfig  # noqa: F401
from clearpath_config.platform.definitions.r100 import R100PlatformConfig  # noqa: F401
from clearpath_config.platform.definitions.w200 import W200PlatformConfig  # noqa: F401
