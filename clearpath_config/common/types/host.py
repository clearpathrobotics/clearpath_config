from clearpath_config.common.types.hostname import Hostname
from clearpath_config.common.types.ip import IP


# Host
# - hostname and config pair
class Host:
    def __init__(
            self,
            hostname: str = "hostname",
            ip: str = "0.0.0.0"
            ) -> None:
        self.hostname = Hostname()
        self.ip = IP()
        self.set_hostname(hostname)
        self.set_ip(ip)

    def __eq__(self, other) -> bool:
        return self.hostname == other.hostname and self.ip == other.ip

    def __str__(self) -> str:
        return "{ hostname: %s, ip: %s }" % (str(self.hostname), str(self.ip))

    def to_dict(self) -> dict:
        return {str(self.hostname): str(self.ip)}

    # Hostname:
    # - the hostname of this host
    def get_hostname(self) -> str:
        return str(self.hostname)

    def set_hostname(self, hostname: str) -> None:
        self.hostname = Hostname(hostname)

    # IP
    # - the ip of this host
    def get_ip(self) -> str:
        return str(self.ip)

    def set_ip(self, ip: str) -> None:
        self.ip = IP(ip)
