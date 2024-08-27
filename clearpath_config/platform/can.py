from clearpath_config.common.types.list import ListConfig
from typing import List


class CANBridge:
    INTERFACE = "interface"
    ENABLE_CAN_FD = "enable_can_fd"
    INTERVAL = "interval"
    USE_BUS_TIME = "use_bus_time"
    FILTERS = "filters"
    AUTO_CONFIGURE = "auto_configure"
    AUTO_ACTIVATE = "auto_activate"
    TOPIC = "topic"

    DEFAULTS = {
        INTERFACE: "can0",
        ENABLE_CAN_FD: False,
        INTERVAL: 0.01,
        USE_BUS_TIME: False,
        FILTERS: "0:0",
        AUTO_CONFIGURE: True,
        AUTO_ACTIVATE: True,
        TOPIC: "from_can0_bus"
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
            topic: str = DEFAULTS[TOPIC],
            ) -> None:
        self.interface = interface
        self.enaled_can_fd = enable_can_fd
        self.interval = interval
        self.use_bus_time = use_bus_time
        self.filters = filters
        self.auto_configure = auto_configure
        self.auto_activate = auto_activate
        self.topic = topic

    def to_dict(self) -> dict:
        d = dict()
        d[self.INTERFACE] = self.interface
        d[self.ENABLE_CAN_FD] = self.enaled_can_fd
        d[self.INTERVAL] = self.interval
        d[self.USE_BUS_TIME] = self.use_bus_time
        d[self.FILTERS] = self.filters
        d[self.AUTO_CONFIGURE] = self.auto_configure
        d[self.AUTO_ACTIVATE] = self.auto_activate
        d[self.TOPIC] = self.topic
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
        if self.TOPIC in d:
            self.topic = d[self.TOPIC]


class CANBridgeListConfig(ListConfig[CANBridge, str]):
    def __init__(self) -> None:
        super().__init__(
            uid=lambda obj: obj.interface,
            obj_type=CANBridge,
            uid_type=str
        )


class CANBridgeConfig:
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
        self._can_bridges.remove_all()
        for b in can_bridges:
            bridge = CANBridge()
            bridge.from_dict(b)
            self._can_bridges.add(bridge)

