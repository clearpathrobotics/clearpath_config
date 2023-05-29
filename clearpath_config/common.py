from collections.abc import MutableMapping
from copy import deepcopy
from typing import Callable, Generic, List, TypeVar
import os
import re


# Platform
# - all supported platforms
class Platform:
    # Dingo D V1
    DD100 = "dd100"
    # Dingo O V1
    DO100 = "do100"
    # Jackal V1
    J100 = "j100"
    # Husky V2
    A200 = "a200"
    # Ridgeback V1
    R100 = "r100"
    # Warthog V2
    W200 = "w200"
    # Genric Robot
    GENERIC = "generic"

    ALL = [DD100, DO100, J100, A200, R100, W200, GENERIC]


# Hostname
# - hostname class
class Hostname:
    def __init__(self, hostname: str = "hostname") -> None:
        self.assert_valid(hostname)
        self.hostname = hostname

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.hostname == other
        elif isinstance(other, Hostname):
            return self.hostname == other.hostname
        return False

    def __str__(self) -> str:
        return self.hostname

    @staticmethod
    def is_valid(hostname: str) -> bool:
        # Max 253 ASCII Characters
        if len(hostname) > 253:
            return False
        # No Trailing Dots
        # - not exactly a standard, but generally results in undefined
        #       behaviour and should be avoided
        if hostname[-1] == ".":
            return False
        # Only [A-Z][0-9] and '-' Allowed
        # - cannot end or start with a hyphen ('-')
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

    @staticmethod
    def assert_valid(hostname: str):
        assert isinstance(hostname, str), (
            "Hostname '%s' must be of type 'str'" % hostname
        )
        # Max 253 ASCII Characters
        assert len(hostname) < 254, (
            "Hostname '%s' exceeds 253 ASCII character limit." % hostname
        )
        # No Trailing Dots
        assert hostname[-1] != ".", (
            "Hostname '%s' should not end with a ('.') period." % hostname
        )
        # Only [A-Z][0-9] and '-' Allowed
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        assert all(allowed.match(x) for x in hostname.split(".")), (
            "Hostname '%s' cannot contain characters other than %s." % (
                hostname,
                "[A-Z][0-9] and hypens ('-')"
            )
        )


# Username
class Username:
    def __init__(self, username: str = "administrator") -> None:
        self.assert_valid(username)
        self.username = username

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.username == other
        elif isinstance(other, Username):
            return self.username == other.username
        return False

    def __str__(self) -> str:
        return self.username

    @staticmethod
    def is_valid(username: str):
        # Check Type
        if not isinstance(username, str):
            return False
        # Max 255 Characters
        if len(username) > 255:
            return False
        # Convention
        # - [a-z] lowercase characters
        # - [0-9] numbers
        # - underscores
        # - dashes
        # - may end in $
        allowed = re.compile(r"[-a-z0-9_]")
        return all(allowed.match(c) for c in username)

    @staticmethod
    def assert_valid(username: str):
        # Check Type
        assert isinstance(username, str), (
            "Username '%s' must of type 'str'"
        )
        # Max 255 Characters
        assert len(username) < 256, (
            "Username '%s' exceeds 255 ASCII character limit." % username
        )
        # Regex Convention
        allowed = re.compile(r"[-a-z0-9_]")
        assert all(allowed.match(c) for c in username), (
            "Username '%s' cannot contain characters other than: %s, %s, %s, %s" % (
                username,
                "lowercase letters",
                "digits",
                "underscores",
                "dashes"
            )
        )


class DomainID:
    def __init__(self, id: int = 0) -> None:
        self.assert_valid(id)
        self.id = id

    def __int__(self) -> int:
        return self.id

    @staticmethod
    def is_valid(id: int) -> bool:
        # Check Type
        if not isinstance(id, int):
            return False
        # 0-101 Range
        if not (0 <= id <= 101):
            return False
        return True

    @staticmethod
    def assert_valid(id: int) -> None:
        # Check Type
        assert isinstance(id, int), (
            "Domain ID must be an integer"
        )
        # 0 - 101 Range
        assert 0 <= id <= 101, (
            "Domain ID must be in range 0 - 101"
        )
        return


# IP
# - ip class
class IP:
    def __init__(self, ip: str = "0.0.0.0") -> None:
        self.assert_valid(ip)
        self.ip_str = ip

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.ip_str == other
        elif isinstance(other, IP):
            return self.ip_str == other.ip_str
        else:
            return False

    def __str__(self) -> str:
        return self.ip_str

    @staticmethod
    def is_valid(ip: str) -> bool:
        # Must be String
        if not isinstance(ip, str):
            return False
        # Must have Four Fields Delimited by '.'
        fields = ip.split(".")
        if not len(fields) == 4:
            return False
        # All Fields must be Integers and 8 Bit Wide
        for field in fields:
            if not field.isdecimal():
                return False
            field_int = int(field)
            if not (0 <= field_int < 256):
                return False
        return True

    @staticmethod
    def assert_valid(ip: str) -> None:
        # Must be String
        assert isinstance(ip, str), (
            "IP '%s' must be string" % ip)
        # Must have Four Fields Delimited by '.'
        fields = ip.split(".")
        assert len(fields) == 4, (
            "IP '%s' must have four entries" % ip)
        for field in fields:
            # Fields Must be Integer
            assert field.isdecimal(), (
                "IP '%s' entries must be integers" % ip)
            # Fields Must be 8-Bits Wide
            field_int = int(field)
            assert 0 <= field_int < 256, (
                "IP '%s' entries must in range 0 to 255" % ip)


# Port
# - TCP Port
class Port:
    def __init__(self, port: int) -> None:
        self.assert_valid(port)
        self.port = int(port)

    def __str__(self) -> str:
        return str(self.port)

    def __int__(self) -> int:
        return self.port

    def __eq__(self, other: object) -> bool:
        try:
            port = int(self)
            other = int(other)
        except Exception:
            return False
        return port == other

    @staticmethod
    def is_valid(port: int) -> None:
        # Must be an integer
        try:
            port = int(port)
        except Exception:
            return False
        # Must be in Range
        return 0 <= port < 65536

    @staticmethod
    def assert_valid(port: int) -> None:
        # Must be an integer
        try:
            port = int(port)
        except ValueError as e:
            raise AssertionError(e.args)
        # Must be in Range
        assert 0 <= port < 65536, (
            "Port '%s' must be between 0 and 65535" % port
        )


# File
# - file class
class File:
    def __init__(self, path: str, creatable=False, exists=False) -> None:
        if creatable:
            assert File.is_creatable(path)
        if exists:
            assert File.is_exists(path)
        self.path = File.clean(path)

    def __str__(self) -> str:
        return self.path

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.path == other
        elif isinstance(other, File):
            return self.path == other.path
        else:
            return False

    @staticmethod
    def clean(path: str) -> str:
        if not path:
            return ""
        path = os.path.expanduser(path)
        path = os.path.normpath(path)
        path = os.path.abspath(path)
        return path

    @staticmethod
    def is_creatable(path: str) -> bool:
        path = File.clean(path)
        dirname = os.path.dirname(path) or os.getcwd()
        return os.access(dirname, os.W_OK)

    @staticmethod
    def is_exists(path: str) -> bool:
        path = File.clean(path)
        return os.path.exists(path)

    def get_path(self) -> str:
        return self.path


# SerialNumber
# - Clearpath Robots Serial Number
# - ex. cpr-j100-0100
# - drop 'cpr' prefix as it is not required
class SerialNumber:
    def __init__(self, sn: str) -> None:
        self.model, self.unit = SerialNumber.parse(sn)

    @staticmethod
    def parse(sn: str) -> tuple:
        assert isinstance(sn, str), "Serial Number must be string"
        sn = sn.lower().strip().split("-")
        assert (
            0 < len(sn) < 4
        ), "Serial Number must be delimited by hyphens ('-') \
            and only have 3 (cpr-j100-0001) entries, \
            2 (j100-0001) entries, \
            or 1 (generic) entry"
        # Remove CPR Prefix
        if len(sn) == 3:
            assert (
                sn[0] == "cpr"
            ), "Serial Number with three fields (%s) must start with cpr" % (
                "cpr-j100-0001",
            )
            sn = sn[1:]
        # Match to Robot
        assert sn[0] in Platform.ALL, (
            "Serial Number model entry must match one of %s" % Platform.ALL
        )
        # Generic Robot
        if sn[0] == Platform.GENERIC:
            if len(sn) > 1:
                return (sn[0], sn[1])
            else:
                return (sn[0], "xxxx")
        # Check Number
        assert sn[1].isdecimal(), (
            "Serial Number unit entry must be an integer value")
        return (sn[0], sn[1])

    def get_model(self) -> str:
        return self.model

    def get_unit(self) -> str:
        return self.unit

    def get_serial(self, prefix=False) -> str:
        if prefix:
            return "-".join(["cpr", self.model, self.unit])
        else:
            return "-".join([self.model, self.unit])


class Accessory():
    # Defaults
    PARENT = "base_link"
    XYZ = [0.0, 0.0, 0.0]
    RPY = [0.0, 0.0, 0.0]

    def __init__(
            self,
            name: str,
            parent: str = PARENT,
            xyz: List[float] = XYZ,
            rpy: List[float] = RPY
            ) -> None:
        self.name = str()
        self.parent = str()
        self.xyz = list()
        self.rpy = list()
        self.set_name(name)
        self.set_parent(parent)
        self.set_xyz(xyz)
        self.set_rpy(rpy)

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.assert_valid_link(name)
        self.name = name

    def get_parent(self) -> str:
        return self.parent

    def set_parent(self, parent: str) -> None:
        self.assert_valid_link(parent)
        self.parent = parent

    def get_xyz(self) -> List[float]:
        return self.xyz

    def set_xyz(self, xyz: List[float]) -> None:
        self.assert_valid_triplet(
            xyz,
            "XYZ must be a list of exactly three float values"
        )
        self.xyz = xyz

    def get_rpy(self) -> List[float]:
        return self.rpy

    def set_rpy(self, rpy: List[float]) -> None:
        self.assert_valid_triplet(
            rpy,
            "RPY must be a list of exactly three float values"
        )
        self.rpy = rpy

    @staticmethod
    def assert_valid_link(link: str) -> None:
        # Link name must be a string
        assert isinstance(link, str), "Link name '%s' must be string" % link
        # Link name must not be empty
        assert link, "Link name '%s' must not be empty" % link
        # Link name must not have spaces
        assert " " not in link, "Link name '%s' must no have spaces" % link
        # Link name must not start with a digit
        assert not link[0].isdigit(), (
            "Link name '%s' must not start with a digit" % link
        )

    @staticmethod
    def assert_valid_triplet(tri: List[float], msg: str = None) -> None:
        if msg is None:
            msg = "Triplet must be a list of three float values"
        # Triplet must be a list
        assert isinstance(tri, list), msg
        # Triplet must have a length of 3
        assert len(tri) == 3, msg
        # Triplet must be all floats
        assert all([isinstance(i, float) for i in tri])


class IndexedAccessory(Accessory):

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if name is None:
            name = self.get_name_from_idx(0)
        super().__init__(
            name,
            parent,
            xyz,
            rpy
        )
        # Index:
        # - index of sensor
        # - used to modify parameters to allow for multiple instances
        #   of the same sensor.
        self.idx = 0
        if idx is not None:
            self.set_idx(idx)

    @classmethod
    def get_name_from_idx(idx):
        return "accessory_%s" % idx

    def get_idx(self) -> str:
        return self.idx

    def set_idx(self, idx: int) -> None:
        assert isinstance(idx, int), "Index must be an integer"
        assert idx >= 0, "Index must be a positive integer"
        self.name = self.get_name_from_idx(idx)


# ListConfigs: Generic Types
T = TypeVar("T")
U = TypeVar("U")


# ListConfigs
# - holds a list of an object type
# - generic class
class ListConfig(Generic[T, U]):

    def __init__(self, uid: Callable) -> None:
        self.__list: List[T] = []
        self.__uid: Callable = uid

    def find(
            self,
            _obj: T | U,
            ) -> int:
        # Object: T: Template
        if isinstance(_obj, self.__orig_class__.__args__[0]):
            uid = self.__uid(_obj)
        # Object: U: Unique ID
        elif isinstance(_obj, self.__orig_class__.__args__[1]):
            uid = _obj
        # Error
        else:
            raise AssertionError(
                "Object must be of type %s or %s" % (
                    self.__orig_class__.__args__[0].__name__,
                    self.__orig_class__.__args__[1].__name__
                )
            )
        for idx, obj in enumerate(self.__list):
            if self.__uid(obj) == uid:
                return idx
        return None

    def add(
            self,
            obj: T,
            ) -> None:
        assert isinstance(obj, self.__orig_class__.__args__[0]), (
            "Object must be of type %s" % T
        )
        assert self.find(obj) is None, (
            "Object with uid %s is not unique." % (
                self.__uid(obj)
            )
        )
        self.__list.append(obj)

    def replace(
            self,
            obj: T,
            ) -> None:
        assert isinstance(obj, self.__orig_class__.__args__[0]), (
            "Object must be of type %s" % T
        )
        assert self.find(obj) is not None, (
            "Object with uid %s cannot be replaced. Does not exist." % (
                self.__uid(obj)
            )
        )
        self.__list[self.find(obj)] = obj

    def remove(
            self,
            _obj: T | U,
            ) -> None:
        idx = self.find(_obj)
        if idx is not None:
            self.__list.remove(self.__list[idx])

    def get(
            self,
            _obj: T | U,
            ) -> T:
        idx = self.find(_obj)
        return None if idx is None else self.__list[idx]

    def get_all(self) -> List[T]:
        return self.__list

    def set(
            self,
            obj: T
            ) -> None:
        if obj is None:
            return
        if self.find(obj) is None:
            self.add(obj)
        else:
            self.replace(obj)

    def set_all(
            self,
            _list: List[T],
            ) -> None:
        # Copy and Clear
        tmp_list = deepcopy(self.__list)
        self.__list.clear()
        # Add One-by-One
        try:
            for obj in _list:
                self.add(obj)
        # Restore Save if Failure
        except AssertionError:
            self.__list = tmp_list

    # Unique Identifier: Name
    @staticmethod
    def uid_name(T) -> str:
        return T.get_name()

    # Unique Identifier: Level
    @staticmethod
    def uid_level(T) -> int:
        return T.get_level()

    # Unique Identifier: Level-Row
    @staticmethod
    def uid_level_row(T) -> tuple:
        return (T.get_level(), T.get_row())


# OrderedListConfig
# - T must have the following methods:
#   - get_idx(): return an index from members
#   - set_idx(idx): set an index and update members
class OrderedListConfig(Generic[T]):

    def __init__(self, start_idx: int = 0) -> None:
        self.start_idx = start_idx
        self.__list: List[T] = []

    def find(
            self,
            obj: T | int
            ) -> int:
        if isinstance(obj, self.__orig_class__.__args__[0]):
            idx = obj.get_idx()
        elif isinstance(obj, int):
            idx = obj
        else:
            raise AssertionError(
                "Object must of type %s or %s" % (
                    self.__orig_class__.__args__[0], int
                )
            )
        if self.start_idx <= idx < len(self.__list) + self.start_idx:
            return idx
        else:
            return None

    def update(self):
        for raw_idx, obj in enumerate(self.__list):
            idx = raw_idx + self.start_idx
            self.__list[raw_idx].set_idx(idx)

    def add(
            self,
            obj: T
            ) -> None:
        assert isinstance(obj, self.__orig_class__.__args__[0]), (
            "Object must be of type %s" % T
        )
        self.__list.append(obj)
        self.update()

    def replace(
            self,
            obj: T,
            ) -> None:
        idx = self.find(obj)
        assert idx is not None, (
            "Object not found. Cannot be replaced"
        )
        self.__list[idx - self.start_idx] = obj
        self.update()

    def remove(
            self,
            obj: T | int
            ) -> None:
        idx = self.find(obj)
        if idx is not None:
            self.__list.remove(self.__list[idx - self.start_idx])
        self.update()

    def get(
            self,
            obj: T | int,
            ) -> T:
        idx = self.find(obj)
        return None if idx is None else self.__list[idx - self.start_idx]

    def get_all(
            self
            ) -> List[T]:
        return self.__list

    def set(
            self,
            obj: T
            ) -> None:
        if self.find(obj) is None:
            self.add(obj)
        else:
            self.replace(obj)

    def set_all(
            self,
            _list: List[T],
            ) -> None:
        # Copy and Clear
        tmp_list = deepcopy(self.__list)
        self.__list.clear()
        # If Empty Keep Empty
        if not _list:
            return
        # Add One-by-One
        try:
            for obj in _list:
                self.add(obj)
        # Restore Save if Failure
        except AssertionError:
            self.__list = tmp_list
        self.update()


# Flatten Dictionary
def _flatten_dict_gen(d, parent_key, dlim):
    for k, v in d.items():
        new_key = parent_key + dlim + str(k) if parent_key else str(k)
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, dlim=dlim).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = '', dlim: str = '.'):
    return dict(_flatten_dict_gen(d, parent_key, dlim))
