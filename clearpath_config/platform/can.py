# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
# @copyright (c) 2024, Clearpath Robotics, Inc., All rights reserved.
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
from typing import List

from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.list import ListConfig
from clearpath_config.common.types.platform import Platform
from clearpath_config.common.types.port import Port


class PhysicalCANAdapter:
    TYPE = 'physical'
    CAN_DEV = 'can_dev'
    BAUD = 'baud'

    DEFAULT = {
        CAN_DEV: 'vcan0',
        BAUD: 's8'
    }

    def __init__(
            self,
            can_dev: str = DEFAULT[CAN_DEV],
            baud: str = DEFAULT[BAUD],
            ):
        self.can_dev = can_dev
        self.baud = baud

    def to_dict(self) -> dict:
        d = {}
        d['type'] = self.TYPE
        d[self.CAN_DEV] = self.can_dev
        d[self.BAUD] = self.baud
        return d

    def from_dict(self, d: dict) -> None:
        if self.CAN_DEV in d:
            self.can_dev = d[self.CAN_DEV]
        if self.BAUD in d:
            self.baud = d[self.BAUD]

    @property
    def can_dev(self) -> str:
        return self._can_dev

    @can_dev.setter
    def can_dev(self, value: str) -> None:
        self._can_dev = value

    @property
    def baud(self) -> str:
        return self._baud

    @baud.setter
    def baud(self, value: str) -> None:
        self._baud = value


class SerialCANAdapter(PhysicalCANAdapter):
    TYPE = 'serial'
    SERIAL_DEV = 'serial_dev'

    DEFAULT = {
        SERIAL_DEV: '/dev/ttycan0'
    }

    def __init__(
            self,
            can_dev: str = PhysicalCANAdapter.DEFAULT[PhysicalCANAdapter.CAN_DEV],
            baud: str = PhysicalCANAdapter.DEFAULT[PhysicalCANAdapter.BAUD],
            serial_dev: str = DEFAULT[SERIAL_DEV],
            ):
        super().__init__(can_dev, baud)
        self.serial_dev = serial_dev

    def to_dict(self) -> dict:
        d = super().to_dict()
        d[self.SERIAL_DEV] = self.serial_dev
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if self.SERIAL_DEV in d:
            self.serial_dev = d[self.SERIAL_DEV]

    @property
    def serial_dev(self) -> str:
        return self._serial_dev

    @serial_dev.setter
    def serial_dev(self, value: str) -> None:
        self._serial_dev = value


class VirtualCANAdapter(SerialCANAdapter):
    TYPE = 'virtual'
    PORT = 'port'

    DEFAULT = {
        PORT: 11412
    }

    def __init__(
            self,
            can_dev: str = PhysicalCANAdapter.DEFAULT[PhysicalCANAdapter.CAN_DEV],
            baud: str = PhysicalCANAdapter.DEFAULT[PhysicalCANAdapter.BAUD],
            serial_dev: str = SerialCANAdapter.DEFAULT[SerialCANAdapter.SERIAL_DEV],
            port: int = DEFAULT[PORT]
            ):
        super().__init__(can_dev, baud, serial_dev)
        self.port = port

    def to_dict(self) -> dict:
        d = super().to_dict()
        d[self.PORT] = self.port
        return d

    def from_dict(self, d: dict) -> None:
        super().from_dict(d)
        if self.PORT in d:
            self.port = d[self.PORT]

    @property
    def port(self) -> int:
        return int(self._port)

    @port.setter
    def port(self, value: int):
        self._port = Port(value)


class CANAdapter:

    TYPES = {
        PhysicalCANAdapter.TYPE: PhysicalCANAdapter,
        SerialCANAdapter.TYPE: SerialCANAdapter,
        VirtualCANAdapter.TYPE: VirtualCANAdapter,
    }

    def __new__(cls, type_: str) -> PhysicalCANAdapter:
        assert type_ in cls.TYPES, f'CANAdapter model, {type_}, not one of {cls.TYPES}'
        return cls.TYPES[type_]()


class CANAdapterListConfig(ListConfig[PhysicalCANAdapter, str]):

    def __init__(self) -> None:

        super().__init__(
            uid=lambda obj: obj.can_dev,
            obj_type=PhysicalCANAdapter,
            uid_type=str
        )


class CANAdapterConfig:
    VCAN0_DEFAULT = {
        'type': VirtualCANAdapter.TYPE,
        VirtualCANAdapter.CAN_DEV: 'vcan0',
        VirtualCANAdapter.BAUD: 's8',
        VirtualCANAdapter.SERIAL_DEV: '/dev/ttycan0',
        VirtualCANAdapter.PORT: 11412,
    }
    VCAN1_DEFAULT = {
        'type': VirtualCANAdapter.TYPE,
        VirtualCANAdapter.CAN_DEV: 'vcan1',
        VirtualCANAdapter.BAUD: 's5',
        VirtualCANAdapter.SERIAL_DEV: '/dev/ttycan1',
        VirtualCANAdapter.PORT: 11413
    }
    DEFAULTS = {
        Platform.A200: [],
        Platform.A300: [VCAN0_DEFAULT, VCAN1_DEFAULT],
        Platform.DD100: [VCAN0_DEFAULT],
        Platform.DD150: [VCAN0_DEFAULT],
        Platform.DO100: [VCAN0_DEFAULT],
        Platform.DO150: [VCAN0_DEFAULT],
        Platform.GENERIC: [],
        Platform.J100: [],
        Platform.R100: [VCAN0_DEFAULT],
        Platform.W200: [],
    }

    def __init__(
            self,
            config: dict = {}
            ) -> None:
        self._can_adapters = CANAdapterListConfig()
        self.config = config

    def __add__(self, other):
        self._can_adapters.extend(other.get_all())
        return self

    def get_all(self) -> List[PhysicalCANAdapter]:
        return self._can_adapters.get_all()

    @property
    def config(self):
        return [a.to_dict() for a in self.get_all()]

    @config.setter
    def config(self, can_adapters: list):
        for d in can_adapters:
            assert 'type' in d,  'CAN adapter must have "type" parameter defined'
            adapter = CANAdapter(d['type'])
            adapter.from_dict(d)
            self._can_adapters.set(adapter)

    def update(self, serial_number: bool = False) -> None:
        if serial_number:
            self.config = self.DEFAULTS[BaseConfig.get_platform_model()]


class CANBridge:
    INTERFACE = 'interface'
    ENABLE_CAN_FD = 'enable_can_fd'
    INTERVAL = 'interval'
    USE_BUS_TIME = 'use_bus_time'
    FILTERS = 'filters'
    AUTO_CONFIGURE = 'auto_configure'
    AUTO_ACTIVATE = 'auto_activate'
    TOPIC_RX = 'topic_rx'
    TOPIC_TX = 'topic_tx'

    DEFAULTS = {
        INTERFACE: 'can0',
        ENABLE_CAN_FD: False,
        INTERVAL: 0.01,
        USE_BUS_TIME: False,
        FILTERS: '0:0',
        AUTO_CONFIGURE: True,
        AUTO_ACTIVATE: True,
        TOPIC_RX: 'can0/rx',
        TOPIC_TX: 'can0/tx'
    }

    def __init__(
            self,
            interface: str = DEFAULTS[INTERFACE],
            enable_can_fd: bool = DEFAULTS[ENABLE_CAN_FD],
            interval: float = DEFAULTS[INTERVAL],
            use_bus_time: bool = DEFAULTS[USE_BUS_TIME],
            filters: str = DEFAULTS[FILTERS],
            auto_configure: bool = DEFAULTS[AUTO_CONFIGURE],
            auto_activate: bool = DEFAULTS[AUTO_ACTIVATE],
            topic_rx: str = DEFAULTS[TOPIC_RX],
            topic_tx: str = DEFAULTS[TOPIC_TX],
            ) -> None:
        self.topic_rx = topic_rx
        self.topic_tx = topic_tx
        self.interface = interface
        self.enaled_can_fd = enable_can_fd
        self.interval = interval
        self.use_bus_time = use_bus_time
        self.filters = filters
        self.auto_configure = auto_configure
        self.auto_activate = auto_activate

    def to_dict(self) -> dict:
        d = {}
        d[self.INTERFACE] = self.interface
        d[self.ENABLE_CAN_FD] = self.enaled_can_fd
        d[self.INTERVAL] = self.interval
        d[self.USE_BUS_TIME] = self.use_bus_time
        d[self.FILTERS] = self.filters
        d[self.AUTO_CONFIGURE] = self.auto_configure
        d[self.AUTO_ACTIVATE] = self.auto_activate
        d[self.TOPIC_RX] = self.topic_rx
        d[self.TOPIC_TX] = self.topic_tx
        return d

    def from_dict(self, d: dict) -> None:
        if self.INTERFACE in d:
            self.interface = d[self.INTERFACE]
        if self.ENABLE_CAN_FD in d:
            self.enaled_can_fd = d[self.ENABLE_CAN_FD]
        if self.INTERVAL in d:
            self.interval = d[self.INTERVAL]
        if self.USE_BUS_TIME in d:
            self.use_bus_time = d[self.USE_BUS_TIME]
        if self.FILTERS in d:
            self.filters = d[self.FILTERS]
        if self.AUTO_CONFIGURE in d:
            self.auto_configure = d[self.AUTO_CONFIGURE]
        if self.AUTO_ACTIVATE in d:
            self.auto_activate = d[self.AUTO_ACTIVATE]
        if self.TOPIC_RX in d:
            self.topic_rx = d[self.TOPIC_RX]
        if self.TOPIC_TX in d:
            self.topic_tx = d[self.TOPIC_TX]

    @property
    def interface(self) -> str:
        return self._interface

    @interface.setter
    def interface(self, interface: str) -> None:
        self._interface = interface
        if self.topic_rx == self.DEFAULTS[self.TOPIC_RX]:
            self.topic_rx = f'{interface}/rx'
        if self.topic_tx == self.DEFAULTS[self.TOPIC_TX]:
            self.topic_tx = f'{interface}/tx'


class CANBridgeListConfig(ListConfig[CANBridge, str]):

    def __init__(self) -> None:

        super().__init__(
            uid=lambda obj: obj.interface,
            obj_type=CANBridge,
            uid_type=str
        )


class CANBridgeConfig:
    SINGLE_VCAN_DEFAULT = [
        {
            CANBridge.INTERFACE: 'vcan0',
            CANBridge.ENABLE_CAN_FD: False,
            CANBridge.INTERVAL: 0.01,
            CANBridge.USE_BUS_TIME: False,
            CANBridge.FILTERS: '0:0',
            CANBridge.AUTO_CONFIGURE: True,
            CANBridge.AUTO_ACTIVATE: True,
        }
    ]

    A300_DEFAULT = [
        {
            CANBridge.INTERFACE: 'vcan0',
            CANBridge.ENABLE_CAN_FD: False,
            CANBridge.INTERVAL: 0.01,
            CANBridge.USE_BUS_TIME: False,
            CANBridge.FILTERS: '0:0',
            CANBridge.AUTO_CONFIGURE: True,
            CANBridge.AUTO_ACTIVATE: True,
        },
        # TODO: Re-enable when battery driver uses clearpath_ros2_socketcan_interface
        # {
        #     CANBridge.INTERFACE: 'vcan1',
        #     CANBridge.ENABLE_CAN_FD: False,
        #     CANBridge.INTERVAL: 0.01,
        #     CANBridge.USE_BUS_TIME: False,
        #     CANBridge.FILTERS: '0:0',
        #     CANBridge.AUTO_CONFIGURE: True,
        #     CANBridge.AUTO_ACTIVATE: True,
        # }
    ]

    DEFAULTS = {
        Platform.A200: [],
        Platform.A300: A300_DEFAULT,
        Platform.DD100: SINGLE_VCAN_DEFAULT,
        Platform.DD150: SINGLE_VCAN_DEFAULT,
        Platform.DO100: SINGLE_VCAN_DEFAULT,
        Platform.DO150: SINGLE_VCAN_DEFAULT,
        Platform.GENERIC: [],
        Platform.J100: [],
        Platform.R100: SINGLE_VCAN_DEFAULT,
        Platform.W200: [],
    }

    def __init__(
            self,
            config: dict = {}
            ) -> None:
        self._can_bridges = CANBridgeListConfig()
        self.config = config

    def __add__(self, other):
        self._can_bridges.extend(other.get_all())
        return self

    def get_all(self) -> List[CANBridge]:
        return self._can_bridges.get_all()

    @property
    def config(self):
        return [a.to_dict() for a in self.get_all()]

    @config.setter
    def config(self, can_bridges: list):
        for b in can_bridges:
            bridge = CANBridge()
            bridge.from_dict(b)
            self._can_bridges.set(bridge)

    def update(self, serial_number: bool = False) -> None:
        if serial_number:
            self.config = self.DEFAULTS[BaseConfig.get_platform_model()]
