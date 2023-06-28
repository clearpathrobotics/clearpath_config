from clearpath_config.common import (
    Hostname,
    IP,
    Username,
    DomainID,
    File
)
from typing import List

from clearpath_config.system import (

)


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
