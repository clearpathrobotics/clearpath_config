# Software License Agreement (BSD)
#
# @author    Chris Iverach-Brereton (civerachb@clearpathrobotics.com)
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
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.sensors.types.sensor import BaseSensor


class BaseRouter():
    """
    Generic configuration parameters for a router we can install on the robot.

    Must be sub-typed as appropriate.
    """

    IP_ADDRESS = 'ip_address'
    LAUNCH_ENABLED = 'launch_enabled'

    def __init__(
        self,
        ip_address: str = None,
        launch_enabled: bool = True,
    ):
        self.ip_address = ip_address
        self.launch_enabled = launch_enabled

    def from_dict(self, d: dict):
        self.ip_address = d.get(self.IP_ADDRESS, self.ip_address)
        self.launch_enabled = d.get(self.LAUNCH_ENABLED, self.launch_enabled)

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @ip_address.setter
    def ip_address(self, value: str) -> None:
        BaseSensor.assert_is_ipv4_address(value)
        self._ip_address = value

    @property
    def launch_enabled(self) -> bool:
        return self._launch_enabled

    @launch_enabled.setter
    def launch_enabled(self, value: bool):
        self._launch_enabled = value


class PeplinkRouter(BaseRouter):
    """
    Configuration object for Peplink routers.

    These use the peplink_router_driver package to run the actual node
    """

    MODEL = 'peplink'

    USERNAME = 'username'
    PASSWORD = 'password'
    ENABLE_GPS = 'enable_gps'
    PUBLISH_PASSWORDS = 'publish_passwords'

    DEFAULTS = {
        BaseRouter.IP_ADDRESS: '192.168.131.51',
        USERNAME: 'admin',
        PASSWORD: 'admin',
        ENABLE_GPS: False,
        PUBLISH_PASSWORDS: False,
    }

    def __init__(
        self,
        ip_address: str = DEFAULTS[BaseRouter.IP_ADDRESS],
        username: str = DEFAULTS[USERNAME],
        password: str = DEFAULTS[PASSWORD],
        enable_gps: bool = DEFAULTS[ENABLE_GPS],
        publish_passwords: bool = DEFAULTS[PUBLISH_PASSWORDS]
    ) -> None:
        super().__init__(ip_address=ip_address)
        self.username = username
        self.password = password
        self.enable_gps = enable_gps
        self.publish_passwords = publish_passwords

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        self.username = d.get(self.USERNAME, self.username)
        self.password = d.get(self.PASSWORD, self.password)
        self.enable_gps = d.get(self.ENABLE_GPS, self.enable_gps)
        self.publish_passwords = d.get(self.PUBLISH_PASSWORDS, self.publish_passwords)

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f'Username {value} must be of type "str"')
        if len(value) <= 0:
            raise ValueError('Username cannot be empty')
        self._username = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f'Password {value} must be of type "str"')
        if len(value) <= 0:
            raise ValueError('Password cannot be empty')
        self._password = value

    @property
    def enable_gps(self) -> bool:
        return self._enable_gps

    @enable_gps.setter
    def enable_gps(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f'Enable GPS flag {value} must be of type "bool"')
        self._enable_gps = value

    @property
    def publish_passwords(self) -> bool:
        return self._publish_passwords

    @publish_passwords.setter
    def publish_passwords(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f'Publish passwords flag {value} must be of type "bool"')
        self._publish_passwords = value


class Router:
    MODELS = {
        PeplinkRouter.MODEL: PeplinkRouter,
    }

    def __new__(cls, model: str) -> BaseRouter:
        if model not in Router.MODELS:
            raise TypeError(f'Router model {model} must be one of {Router.MODELS}')
        return Router.MODELS[model]()


class WirelessConfig(BaseConfig):
    """
    Contains additional wireless networking nodes we can enable/disable.

    Currently only peplink devices are supported here, but this may expand in the future.
    """

    WIRELESS = 'wireless'
    ROUTER = 'router'
    BASE_STATION = 'base_station'
    ENABLE_WIRELESS_WATCHER = 'enable_wireless_watcher'

    TEMPLATE = {
        ROUTER: ROUTER,
        BASE_STATION: BASE_STATION,
        ENABLE_WIRELESS_WATCHER: ENABLE_WIRELESS_WATCHER,
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        ROUTER: None,
        BASE_STATION: None,
        ENABLE_WIRELESS_WATCHER: True
    }

    def __init__(
        self, config: dict = {},
        router: str = DEFAULTS[ROUTER],
        base_station: str = DEFAULTS[BASE_STATION],
        enable_wireless_watcher: str = DEFAULTS[ENABLE_WIRELESS_WATCHER]
    ) -> None:
        self._router = self.DEFAULTS[self.ROUTER]
        self._base_station = self.DEFAULTS[self.BASE_STATION]
        self._enable_wireless_watcher = self.DEFAULTS[self.ENABLE_WIRELESS_WATCHER]

        setters = {
            self.KEYS[self.ROUTER]: WirelessConfig.router,
            self.KEYS[self.BASE_STATION]: WirelessConfig.base_station,
            self.KEYS[self.ENABLE_WIRELESS_WATCHER]: WirelessConfig.enable_wireless_watcher,
        }
        super().__init__(setters, config)

        self.router = router
        self.base_station = base_station
        self.enable_wireless_watcher = enable_wireless_watcher

    def from_dict(self, value: dict):
        if self.ROUTER in value:
            router_cfg = value[self.ROUTER]
            if 'model' not in router_cfg:
                raise ValueError(f'Router configuration {router_cfg} must contain a "model" key')
            self.router = Router(router_cfg['model'])
            self.router.from_dict(router_cfg)

        if self.BASE_STATION in value:
            router_cfg = value[self.BASE_STATION]
            if 'model' not in router_cfg:
                raise ValueError(f'Base station configuration {router_cfg} must contain a "model" key')  # noqa: E501
            self.base_station = Router(router_cfg['model'])
            self.base_station.from_dict(router_cfg)

        if self.ENABLE_WIRELESS_WATCHER in value:
            self.enable_wireless_watcher = value[self.ENABLE_WIRELESS_WATCHER]

    @property
    def router(self) -> BaseRouter:
        return self._router

    @router.setter
    def router(self, value: dict | BaseRouter) -> None:
        if value is None:
            # no router; that's fine
            pass
        elif isinstance(value, dict):
            if 'model' not in value:
                raise ValueError(f'Router configuration {value} must contain a "model" key')
            self._router = Router(value['model'])
            self._router.from_dict(value)
        elif isinstance(value, BaseRouter):
            self._router = value
        else:
            raise TypeError(f'Router configuration must be of type "dict" or "BaseRouter". Got {value}')  # noqa: E501

    @property
    def base_station(self) -> BaseRouter:
        return self._base_station

    @base_station.setter
    def base_station(self, value: dict | BaseRouter) -> None:
        if value is None:
            # no base station; that's fine
            pass
        elif isinstance(value, dict):
            if 'model' not in value:
                raise ValueError(f'Base station configuration {value} must contain a "model" key')
            self._base_station = Router(value['model'])
            self._base_station.from_dict(value)
        elif isinstance(value, BaseRouter):
            self._base_station = value
        else:
            raise TypeError(f'Base station configuration must be of type "dict" or "BaseRouter". Got {value}')  # noqa: E501

    @property
    def enable_wireless_watcher(self) -> bool:
        return self._enable_wireless_watcher

    @enable_wireless_watcher.setter
    def enable_wireless_watcher(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError(f'Enable wireless watcher {value} must be of type "bool"')
        self._enable_wireless_watcher = value
