from clearpath_config.common import Hostname, IP
from typing import List

# Host
# - hostname and config pair
class Host():

    def __init__(self, hostname: str = "hostname", ip: str = "0.0.0.0") -> None:
        self.hostname = Hostname()
        self.ip = IP()
        self.set_hostname(hostname)
        self.set_ip(ip)

    def __eq__(self, other) -> bool:
        return self.hostname == other.hostname and self.ip == other.ip

    def __str__(self) -> str:
        return "{ hostname: %s, ip: %s }" % (str(self.hostname), str(self.ip))

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

# HostsConfig
# - these are the hosts that are involved in this system
class HostsConfig():

    def __init__(self, platform: Host = None, onboard: List[Host] = [], remote: List[Host] = []) -> None:
        self.platform = Host()
        self.onboard = list()
        self.remote = list()

    def assert_unique_host(self, host: Host) -> None:
        # check host
        self.assert_unique_hostname(host.get_hostname())
        # check ip
        self.assert_unique_ip(host.get_ip())

    def assert_unique_hostname(self, hostname: str) -> None:
        # check platform hostname
        assert hostname != self.get_platform_hostname(), "Hostname %s is already the platform's hostname" % hostname
        # check onboard hostnames
        assert hostname not in [host.get_hostname() for host in self.get_onboard()], "Hostname %s is already an onboard host" % hostname
        # check remote hostnames
        assert hostname not in [host.get_hostname() for host in self.get_remote()], "Hostname %s is already a remote host" % hostname

    def assert_unique_ip(self, ip: str) -> None:
        # check platform ip
        assert ip != self.get_platform_ip(), "IP %s is already the platform's IP." % ip
        # check onboard ip's
        assert ip not in [host.get_ip() for host in self.get_onboard()], "IP %s is already an onboard host IP" % ip
        # check remote ip's
        assert ip not in [host.get_ip() for host in self.get_remote()], "IP %s is already a remote host IP" % ip

    # Platform:
    # - the main computer for tis system (i.e. the robot's computer)
    def get_platform(self) -> Host:
        return self.platform

    def get_platform_hostname(self) -> str:
        return self.platform.get_hostname()

    def get_platform_ip(self) -> str:
        return self.platform.get_ip()

    def set_platform(self, platform: Host) -> None:
        self.assert_unique_host(platform)
        self.platform = platform

    def set_platform_hostname(self, hostname: str) -> None:
        self.assert_unique_hostname(hostname)
        self.platform.set_hostname(hostname)

    def set_platform_ip(self, ip: str) -> None:
        self.assert_unique_ip(ip)
        self.platform.set_ip(ip)

    # HostList:
    # - general functions to set, add, and remove from a list of hosts
    def set_hostlist(self, destination: list, hostlist: List[Host]) -> List[Host]:
        assert isinstance(hostlist, list), "Onboard/Remote list must be list of Hosts" 
        for host in hostlist:
            assert isinstance(host, Host), "Onboard/Remote list must be list of Hosts"
            self.assert_unique_host(host)
        destination.clear()
        destination.extend(hostlist)
        return destination

    def add_host(self, destination: list, host: Host = None, hostname:str = None, ip: str = None) -> List[Host]:
        assert isinstance(destination, list), "Destination list must be of type List"
        if host:
            assert isinstance(host, Host), "Onboard/Remote host entry must be of type Host"
            self.assert_unique_host(host)
            destination.append(host)
        else:
            assert hostname and ip, "Onboard/Remote entry needs both hostname and ip if Host type is not passed"
            self.assert_unique_host(Host(hostname, ip))
            destination.append(Host(hostname,ip))
        return destination

    def remove_host(self, destination: list, host: Host = None, hostname: str = None, ip: str = None) -> List[Host]:
        assert isinstance(destination, list), "Destination list must be of type List"
        assert host or hostname or ip, "One of Host, hostname, or ip must be specified to be removed"
        if host:
            assert host in destination, "Host %s does not exist in hosts" % host
            destination.remove(host)
            return destination
        elif hostname:
            for host in destination:
                if host.get_hostname() == hostname:
                    destination.remove(host)
                    return destination
        elif ip:
            for host in destination:
                if host.get_ip() == ip:
                    destination.remove(host)
                    return destination
        else:
            return destination

    # Onboard:
    # - these are additional on-board computer
    def get_onboard(self) -> List[Host]:
        if self.onboard:
            return self.onboard
        else:
            return []

    def set_onboard(self, onboard: List[Host]) -> None:
        self.onboard = self.set_hostlist(destination=self.onboard, hostlist=onboard)

    def add_onboard(self, host: Host = None, hostname: str = None, ip: str = None) -> None:
        self.onboard = self.add_host(destination=self.get_onboard(), host=host, hostname=hostname, ip=ip)
        return

    def remove_onboard(self, host: Host = None, hostname: str = None, ip: str = None) -> bool:
        self.onboard = self.remove_host(destination=self.get_onboard(), host=host, hostname=hostname, ip=ip)
        return

    # Remote:
    # - these are remote machines which need to interact with the system
    # - ex. laptops or other robots
    def get_remote(self) -> List[Host]:
        if self.remote:
            return self.remote
        else:
            return []

    def set_remote(self, remote: List[Host]) -> None:
        self.remote = self.set_hostlist(remote, self.remote)
        return

    def add_remote(self, host: Host = None, hostname: str = None, ip: str = None) -> None:
        self.remote = self.add_host(self.remote, host, hostname, ip)
        return

    def remove_remote(self, host: Host = None, hostname: str = None, ip: str = None) -> bool:
        self.remote = self.remove_host(self.remote, host, hostname, ip)
        return

# SystemConfig:
# - system level configuration options
class SystemConfig():
    def __init__(self, _self: str = None, hosts: HostsConfig = None) -> None:
        self._self = str
        self.hosts = HostsConfig()
        if _self:
            self.set_self(_self)
        if hosts:
            self.set_hosts(hosts)

    # Self:
    # - the hostname of the computer that this config was created on/going to be used on
    def get_self(self) -> str:
        return self._self

    def set_self(self, _self: str) -> None:
        assert isinstance(_self, str), "Self hostname must be a string"
        assert len(_self.split(" ")) == 1, "Self hostname must not contain spaces"
        self._self = _self

    # Hosts:
    # - hosts that are involved in this system
    def get_hosts(self) -> HostsConfig:
        return self.hosts
 
    def set_hosts(self, hosts: HostsConfig) -> None:
        assert isinstance(hosts, HostsConfig), "Hosts must be of type HostsConfig"
        self.hosts = hosts
