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

class PACSProfile:
    def __init__(
            self,
            rows: int,
            columns: int
            ) -> None:
        self.rows = rows
        self.columns = columns


class IndexingProfile:
    def __init__(
            self,
            camera: int = 0,
            gps: int = 0,
            imu: int = 0,
            lidar2d: int = 0,
            lidar3d: int = 0,
            ins: int = 0,
            ptu: int = 0,
            ) -> None:
        self.camera = camera
        self.gps = gps
        self.imu = imu
        self.lidar2d = lidar2d
        self.lidar3d = lidar3d
        self.ins = ins
        self.ptu = ptu


# Platform
# - registry of platform configurations
# - concrete platform data is defined in BasePlatformConfig subclasses
#   under clearpath_config.platform.definitions
class Platform:
    _REGISTRY = {}
    _LOADED = False

    @classmethod
    def register(cls, platform_config_cls) -> None:
        """Register a concrete BasePlatformConfig subclass."""
        cls._REGISTRY[platform_config_cls.NAME] = platform_config_cls

    @classmethod
    def get(cls, name: str):
        """Return the registered BasePlatformConfig subclass for the given name."""
        cls._ensure_loaded()
        if name not in cls._REGISTRY:
            raise KeyError(
                f'No platform registered for "{name}". '
                f'Available: {list(cls._REGISTRY.keys())}'
            )
        return cls._REGISTRY[name]

    @classmethod
    def all_names(cls) -> list:
        """Return list of all registered platform names."""
        cls._ensure_loaded()
        return list(cls._REGISTRY.keys())

    @classmethod
    def _ensure_loaded(cls):
        """Lazily import built-in platform definitions on first access."""
        if cls._LOADED:
            return
        cls._LOADED = True
        import clearpath_config.platform.definitions  # noqa: F401

    @staticmethod
    def assert_is_supported(platform):
        """
        Raise an exception if the platform is not presently supported/usable.

        @param platform  The platform-identifying serial number prefix (e.g. 'a200', 'j100')

        @exception UnsupportedPlatformException if the platform is not supported
        """
        # currently all platforms are supported, nothing to do
        pass

    @staticmethod
    def notify_if_deprecated(platform):
        """
        Print a notification that the selected platform is deprecated.

        @param platform  The platform-identifying serial number prefix (e.g. 'a200', 'j100')
        """
        # currently nothing is deprecated, so nothing to do here (yet)
        pass
