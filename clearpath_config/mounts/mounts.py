from clearpath_config.common import (
    Accessory,
    File,
    IP,
    List,
    ListConfig
)
from math import pi


class BaseMount(Accessory):
    MOUNTING_LINK = None

    def __init__(
        self,
        name: str,
        model: str,
        parent: str = Accessory.PARENT,
        mounting_link: str = MOUNTING_LINK,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
    ) -> None:
        super().__init__(name, parent, xyz, rpy)
        self.model = str()
        self.set_model(model)
        self.mounting_link = "%s_mount" % self.get_name()
        if mounting_link:
            self.set_mounting_link(mounting_link)

    def get_model(self) -> str:
        return self.model

    def set_model(self, model: str) -> None:
        assert model in Mount.MODEL, "Model '%s' must be one of '%s'" % (
            model,
            Mount.MODEL.keys(),
        )
        self.model = model

    def get_mounting_link(self) -> str:
        return self.mounting_link

    def set_mounting_link(self, mounting_link: str) -> None:
        self.assert_valid_link(mounting_link)
        self.mounting_link = mounting_link


class FathPivot(BaseMount):
    MOUNTING_LINK = None
    ANGLE = 0.0

    def __init__(
        self,
        name: str,
        parent: str = Accessory.PARENT,
        mounting_link: str = MOUNTING_LINK,
        angle: float = ANGLE,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
    ) -> None:
        super().__init__(
            name,
            Mount.FATH_PIVOT,
            parent,
            mounting_link,
            xyz,
            rpy)
        self.angle = 0.0
        if angle:
            self.set_angle(angle)

    def get_angle(self) -> float:
        return self.angle

    def set_angle(self, angle: float) -> None:
        assert -pi < angle <= pi, (
            "Angle '%s' must be in radian and  between pi and -pi"
        )
        self.angle = angle


class FlirPTU(BaseMount):
    # Default Values
    MOUNTING_LINK = None
    TTY_PORT = "/dev/ptu"
    TCP_PORT = 4000
    IP_ADDRESS = "192.168.131.70"
    LIMITS_ENABLED = False
    TTY = "tty"
    TCP = "tcp"
    CONNECTION_TYPE = TTY
    # TTY (uses tty_port)
    # TCP (uses ip_addr and tcp_port)
    CONNECTION_TYPES = [TTY, TCP]

    def __init__(
        self,
        name: str,
        parent: str = Accessory.PARENT,
        mounting_link: str = MOUNTING_LINK,
        xyz: List[float] = Accessory.XYZ,
        rpy: List[float] = Accessory.RPY,
        tty_port: str = TTY_PORT,
        tcp_port: int = TCP_PORT,
        ip: str = IP_ADDRESS,
        connection_type: str = CONNECTION_TYPE,
        limits_enabled: bool = LIMITS_ENABLED,
    ) -> None:
        super().__init__(
            name,
            Mount.FLIR_PTU,
            parent,
            mounting_link,
            xyz,
            rpy,
        )
        # Serial Port
        self.tty_port = File(self.TTY_PORT)
        self.set_tty_port(tty_port)
        # TCP Port
        self.tcp_port = self.TCP_PORT
        self.set_tcp_port(tcp_port)
        # IP
        self.ip = IP()
        self.set_ip(ip)
        # Connection Type
        self.connection_type = self.TTY
        self.set_connection_type(connection_type)
        # Limits
        self.limits_enabled = False
        self.set_limits_enabled(limits_enabled)

    def get_tty_port(self) -> str:
        return self.tty_port.get_path()

    def set_tty_port(self, tty_port: str) -> None:
        self.tty_port = File(tty_port)

    def get_tcp_port(self) -> str:
        return self.tcp_port

    def set_tcp_port(self, tcp_port: int) -> None:
        assert 1024 < tcp_port < 65536, (
            "TCP port '%s' must be in range 1024 to 65536" % tcp_port
        )
        self.tcp_port = tcp_port

    def get_ip(self) -> str:
        return str(self.ip)

    def set_ip(self, ip: str) -> None:
        self.ip = IP(ip)

    def get_connection_type(self) -> str:
        return self.connection_type

    def set_connection_type(self, connection_type: str) -> None:
        assert connection_type in self.CONNECTION_TYPES, (
            "Connection type '%s' must be one of '%s'" % (
                connection_type,
                self.CONNECTION_TYPES,
            )
        )
        self.connection_type = connection_type

    def get_limits_enabled(self) -> bool:
        return self.limits_enabled

    def set_limits_enabled(self, limits_enabled: bool) -> None:
        self.limits_enabled = limits_enabled


class Mount():
    FATH_PIVOT = "fath_pivot"
    FLIR_PTU = "flir_ptu"
    MODEL = {
        FATH_PIVOT: FathPivot,
        FLIR_PTU: FlirPTU,
    }

    def __new__(cls, name: str, model: str) -> BaseMount:
        assert model in Mount.MODEL, (
            "Model '%s' must be one of: '%s'" % (
                model,
                Mount.MODEL.keys()
            )
        )
        return Mount.MODEL[model](name)


class MountsConfig:
    def __init__(self, mounts: List[BaseMount] = []) -> None:
        self.__mounts = ListConfig[BaseMount, str](
            uid=lambda obj: obj.get_name()
        )
        self.set_mounts(mounts)

    def get_mount(
            self,
            name: str,
            ) -> BaseMount:
        return self.__mounts.get(name)

    def get_mounts(self) -> List[BaseMount]:
        return self.__mounts.get_all()

    def set_mount(
            self,
            mount: BaseMount,
            ) -> None:
        self.__mounts.set(mount)

    def set_mounts(self, mounts: List[BaseMount]) -> None:
        self.__mounts.set_all(mounts)

    def add_mount(
            self,
            # By Object
            mount: BaseMount = None,
            # By Required Parameters
            name: str = None,
            model: str = None,
            ) -> None:
        assert mount or (name and model), (
            "Mount object or name and model must be passed."
        )
        if (name and model) and not mount:
            mount = Mount(name, model)
        self.__mounts.add(mount)

    def remove_mount(
            self,
            mount: BaseMount = None,
            name: str = None
            ) -> None:
        assert mount or name, (
            "Mount object or name must be passed."
        )
        if name and not mount:
            self.__mounts.remove(name)
        else:
            self.__mounts.remove(mount)
