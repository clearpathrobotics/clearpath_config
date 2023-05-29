from clearpath_config.common import (
    Hostname,
    IP,
    Username,
    DomainID,
    File
)
from typing import List
import re


class Namespace:
    def __init__(
            self,
            name: str = "/"
            ) -> None:
        self.assert_valid(name)
        self.name = name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Namespace):
            return self.name == other.name
        else:
            return False

    def __str__(self) -> str:
        return str(self.name)

    @staticmethod
    def is_valid(name: str) -> bool:
        # Must not be Empty
        if name == "":
            return False
        # Must Contain:
        #  - [0-9|a-z|A-Z]
        #  - Underscores (_)
        #  - Forward Slashed (/)
        allowed = re.compile("[a-z|0-9|_|/|~]", re.IGNORECASE)
        if not all(allowed.match(c) for c in name):
            return False
        # May start with (~) but be followed by (/)
        if name[0] == "~":
            if name[1] != "/":
                return False
        # Must not Start with Digit [0-9], May Start with (~)
        if str(name[0]).isdigit():
            return False
        # Must not End with Forward Slash (/)
        if name[-1] == "/":
            return False
        # Must not contain any number of repeated forward slashed (/)
        if "//" in name:
            return False
        # Must not contain any number of repeated underscores (_)
        if "__" in name:
            return False

    @staticmethod
    def assert_valid(name: str) -> None:
        # Empty
        assert name != "", (
            "Namespace cannot be empty"
        )
        # Allowed characters
        allowed = re.compile("[a-z|0-9|_|/|~]", re.IGNORECASE)
        assert all(allowed.match(c) for c in name), ("\n".join([
            "Namespace can only contain:",
            " - [A-Z|a-z|0-9]",
            " - underscores (_)",
            " - forward slahes (/)",
            " - leading tilde (~)"
        ]))
        # Leading Tilde (~)
        if name[0] == "~":
            assert name[1] == "/", (
                "Namespace starting with (~) must be followed by (/)"
            )
        # Leading Digit
        assert not str(name[0]).isdigit(), (
            "Namespace may not start with a digit"
        )
        # Ending Forward Slash (/)
        assert len(name) == 1 or name[-1] != "/", (
            "Namespace may not end with a forward slash (/)"
        )
        # Repeated Forward Slash (/)
        assert "//" not in name, (
            "Namespace may not contain repeated forward slashes (/)"
        )
        # Repeated Underscores (/)
        assert "__" not in name, (
            "Namespace may not contain repeated underscores (_)"
        )


class RMWImplementation:
    CONNEXT = "rmw_connext_cpp"
    CYCLONE_DDS = "rmw_cyclonedds_cpp"
    FAST_RTPS = "rmw_fastrtps_cpp"
    GURUM_DDS = "rmw_gurumdds_cpp"

    MIDDLEWARE = [FAST_RTPS]

    def __init__(
            self,
            rmw: str = FAST_RTPS
            ) -> None:
        self.assert_valid(rmw)
        self.rmw = rmw

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.rmw == other
        elif isinstance(other, RMWImplementation):
            return self.rmw == other.rmw
        else:
            return False

    def __str__(self) -> str:
        return self.rmw

    @classmethod
    def is_valid(cls, rmw: str) -> bool:
        return rmw in cls.MIDDLEWARE

    @classmethod
    def assert_valid(cls, rmw: str) -> None:
        assert cls.is_valid(rmw), ("\n".join[
            "RMW '%s' not supported." % rmw,
            "RMW must be one of: '%s'" % cls.MIDDLEWARE
        ])


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
class HostsConfig:
    def __init__(
            self,
            platform: Host = None,
            onboard: List[Host] = [],
            remote: List[Host] = []
            ) -> None:
        self.platform = Host()
        self.onboard = list()
        self.remote = list()
        if platform:
            assert isinstance(platform, Host), (
                "Platform host must be Host type."
            )
            self.platform = platform
        if onboard:
            assert isinstance(onboard, list), "Onboard must be a list"
            assert all(
                isinstance(host, Host) for host in onboard
            ), "Onboard hosts must all be of type Host"
            self.onboard = onboard
        if remote:
            assert isinstance(onboard, list), "Remote must be a list"
            assert all(
                isinstance(host, Host) for host in remote
            ), "Remote hosts must all be of type Host"
            self.remote = remote

    def assert_unique_host(self, host: Host) -> None:
        # check host
        self.assert_unique_hostname(host.get_hostname())
        # check ip
        self.assert_unique_ip(host.get_ip())

    def assert_unique_hostname(self, hostname: str) -> None:
        # check platform hostname
        assert hostname != self.get_platform_hostname(), (
            "Hostname %s is already the platform's hostname" % hostname
        )
        # check onboard hostnames
        assert hostname not in [
                host.get_hostname() for host in self.get_onboard()
            ], (
            "Hostname %s is already an onboard host" % hostname
            )
        # check remote hostnames
        assert hostname not in [
            host.get_hostname() for host in self.get_remote()
            ], (
            "Hostname %s is already a remote host" % hostname
            )

    def assert_unique_ip(self, ip: str) -> None:
        # check platform ip
        assert ip != self.get_platform_ip(), (
            "IP %s is already the platform's IP." % ip
        )
        # check onboard ip's
        assert ip not in [host.get_ip() for host in self.get_onboard()], (
            "IP %s is already an onboard host IP" % ip
        )
        # check remote ip's
        assert ip not in [host.get_ip() for host in self.get_remote()], (
            "IP %s is already a remote host IP" % ip
        )

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
    def set_hostlist(
            self,
            destination: list,
            hostlist: List[Host]
            ) -> List[Host]:
        assert isinstance(hostlist, list), (
            "Onboard/Remote list must be list of Hosts"
        )
        for host in hostlist:
            assert isinstance(host, Host), (
                "Onboard/Remote list must be list of Hosts"
            )
            self.assert_unique_host(host)
        destination.clear()
        destination.extend(hostlist)
        return destination

    def add_host(
            self,
            destination: list,
            host: Host = None,
            hostname: str = None,
            ip: str = None
            ) -> List[Host]:
        assert isinstance(destination, list), (
            "Destination list must be of type List"
        )
        if host:
            assert isinstance(
                host, Host
            ), "Host entry must be of type Host"
            self.assert_unique_host(host)
            destination.append(host)
        else:
            assert (
                hostname and ip
            ), "Host entry needs both hostname and ip if object not passed"
            self.assert_unique_host(Host(hostname, ip))
            destination.append(Host(hostname, ip))
        return destination

    def remove_host(
            self,
            destination: list,
            host: Host = None,
            hostname: str = None,
            ip: str = None
            ) -> List[Host]:
        assert isinstance(destination, list), (
            "Destination list must be of type List"
        )
        assert (
            host or hostname or ip
        ), "One of Host, hostname, or ip must be specified to be removed"
        if host:
            assert host in destination, (
                "Host %s does not exist in hosts" % host
            )
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
        self.onboard = self.set_hostlist(
            destination=self.get_onboard(), hostlist=onboard
        )

    def add_onboard(
        self, host: Host = None, hostname: str = None, ip: str = None
    ) -> None:
        self.onboard = self.add_host(
            destination=self.get_onboard(), host=host, hostname=hostname, ip=ip
        )
        return

    def remove_onboard(
        self, host: Host = None, hostname: str = None, ip: str = None
    ) -> bool:
        self.onboard = self.remove_host(
            destination=self.get_onboard(), host=host, hostname=hostname, ip=ip
        )
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
        self.remote = self.set_hostlist(
            destination=self.get_remote(),
            hostlist=remote
        )
        return

    def add_remote(
        self, host: Host = None, hostname: str = None, ip: str = None
    ) -> None:
        self.remote = self.add_host(
            destination=self.get_remote(), host=host, hostname=hostname, ip=ip
        )
        return

    def remove_remote(
        self, host: Host = None, hostname: str = None, ip: str = None
    ) -> bool:
        self.remote = self.remove_host(
            destination=self.get_remote(),
            host=host,
            hostname=hostname,
            ip=ip
        )
        return


# SystemConfig:
# - system level configuration options
class SystemConfig:
    def __init__(
            self, _self: str = None,
            hosts: HostsConfig = None,
            username: Username = None,
            namespace: Namespace = None,
            domain_id: DomainID = None,
            rmw: RMWImplementation = None,
            workspaces: List[File] = None,
            ) -> None:
        self._self = Hostname()
        self.hosts = HostsConfig()
        self.username = Username()
        self.namespace = Namespace()
        self.domain_id = DomainID()
        self.rmw = RMWImplementation()
        self.workspaces = []
        if _self is not None:
            self.set_self(_self)
        if hosts is not None:
            self.set_hosts(hosts)
        if username is not None:
            self.set_username(username)
        if namespace is not None:
            self.set_namespace(namespace)
        if domain_id is not None:
            self.set_domain_id(domain_id)
        if rmw is not None:
            self.set_rmw_implementation(rmw)
        if workspaces is not None:
            self.set_workspaces(workspaces)

    # Self:
    # - the hostname of the computer that this config was
    #   created on/going to be used on
    def get_self(self) -> str:
        return self._self

    def set_self(self, _self: str) -> None:
        self._self = Hostname(_self)

    # Hosts:
    # - hosts that are involved in this system
    def get_hosts(self) -> HostsConfig:
        return self.hosts

    def set_hosts(self, hosts: HostsConfig) -> None:
        assert isinstance(hosts, HostsConfig), (
          "Hosts must be of type HostsConfig"
        )
        self.hosts = hosts

    # Username:
    # - user that will be launching nodes
    def get_username(self) -> str:
        return str(self.username)

    def set_username(self, name: str) -> None:
        self.username = Username(name)

    # Namespace:
    def get_namespace(self) -> str:
        return str(self.namespace)

    def set_namespace(self, namespace: str) -> None:
        self.namespace = Namespace(namespace)

    # Domain ID:
    # - ROS2 domain ID
    def get_domain_id(self) -> int:
        return int(self.domain_id)

    def set_domain_id(self, domain_id: int) -> None:
        self.domain_id = DomainID(domain_id)

    # RMW Implementation
    # - middleware
    def get_rmw_implementation(self) -> str:
        return str(self.rmw)

    def set_rmw_implementation(self, rmw: str) -> None:
        self.rmw = RMWImplementation(rmw)

    # Workspaces
    # - list of workspaces pointing to setup.bash
    def get_workspaces(self) -> List[str]:
        return [str(ws) for ws in self.workspaces]

    def set_workspaces(self, workspaces: List[str]) -> None:
        self.workspaces = [File(str(ws)) for ws in workspaces]
