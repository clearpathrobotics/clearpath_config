from typing import List
import os
import re

# Platform
# - all supported platforms
class Platform():
    DINGO_DIFF = "DingoD"
    DINGO_OMNI = "DingoO"
    JACKAL = "Jackal"
    HUSKY = "Husky"
    RIDGEBACK = "Ridgeback"
    WARTHOG = "Warthog"
    GENERIC = "Generic"

    ALL = [DINGO_DIFF,
           DINGO_OMNI,
           JACKAL,
           HUSKY,
           RIDGEBACK,
           WARTHOG,
           GENERIC]


# Hostname
# - hostname class
class Hostname():

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
    def is_valid(hostname: str):
        # Max 253 ASCII Characters
        if len(hostname) > 253:
            return False
        # No Trailing Dots
        # - not excatly a standard but generally undefined behaviour and should be avoided
        if hostname[-1] == ".":
            return False
        # Only [A-Z][0-9] and '-' Allowed
        # - cannot end or start with a hyphen ('-')
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

    @staticmethod
    def assert_valid(hostname: str):
        assert isinstance(hostname, str), "Hostname '%s' must be of type 'str'" % hostname
        # Max 253 ASCII Characters
        assert len(hostname) < 254, "Hostname '%s' exceeds 253 ASCII character limit." % hostname
        # No Trailing Dots
        assert hostname[-1] != ".", "Hostname '%s' should not end with a ('.') period." % hostname
        # Only [A-Z][0-9] and '-' Allowed
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        assert all(allowed.match(x) for x in hostname.split(".")), "Hostname '%s' cannot contain characters other than [A-Z][0-9] and hypens ('-')." % hostname


# IP
# - ip class
class IP():

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

    def  __str__(self) -> str:
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
        assert isinstance(ip, str), "IP '%s' must be string" % ip
        # Must have Four Fields Delimited by '.'
        fields = ip.split(".")
        assert len(fields) == 4, "IP '%s' must have four entries" % ip
        for field in fields: 
            # Fields Must be Integer
            assert field.isdecimal(), "IP '%s' entries must be integers" % ip
            # Fields Must be 8-Bits Wide
            field_int = int(field)
            assert 0 <= field_int < 256, "IP '%s' entries must in range 0 to 255" % ip


# File
# - file class
class File():

    def __init__(self, path: str, creatable=False, exists=False) -> None:
        path = File.clean(path)
        if creatable:
            assert File.is_creatable(path)
        if exists:
            assert File.is_exists(path)
        self.path = path

    def __str__(self) -> str:
        return self.file

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
            return None
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

# SerialNumber
# - Clearpath Robots Serial Number
# - ex. cpr-j100-0100
# - drop 'cpr' prefix as it is not required
class SerialNumber():
    DINGO_DIFF = "dd100"
    DINGO_OMNI = "do100"
    JACKAL = "j100"
    HUSKY = "a200"
    RIDGEBACK = "r100"
    WARTHOG = "w200"
    GENERIC = "generic"

    MODELS = [DINGO_DIFF,
              DINGO_OMNI,
              JACKAL,
              HUSKY,
              RIDGEBACK,
              WARTHOG,
              GENERIC]

    MODEL_NAMES = {DINGO_DIFF: Platform.DINGO_DIFF,
                   DINGO_OMNI: Platform.DINGO_OMNI,
                   JACKAL: Platform.JACKAL,
                   HUSKY: Platform.HUSKY,
                   RIDGEBACK: Platform.RIDGEBACK,
                   WARTHOG: Platform.WARTHOG,
                   GENERIC: Platform.GENERIC}

    def __init__(self, sn: str) -> None:
        self.model, self.unit = SerialNumber.parse(sn)

    @staticmethod
    def parse(sn: str) -> tuple:
        assert isinstance(sn, str), "Serial Number must be string"
        sn = sn.lower().strip().split("-")
        assert 1 < len(sn) < 4, "Serial Number must be delimited by hyphens ('-') and only have 3 (cpr-j100-0001) entries or 2 (j100-0001) entries"
        # Remove CPR Prefix
        if len(sn) == 3:
            assert sn[0] == "cpr", "Serial Number with three fields (cpr-j100-0001) must start with cpr"
            sn = sn[1:]
        # Match to Robot
        assert sn[0] in SerialNumber.MODELS, "Serial Number model entry must match one of %s" % SerialNumber.MODELS
        # Check Number
        assert sn[1].isdecimal(), "Serial Number unit entry must be an integer value"
        return (sn[0], sn[1])

    def get_model(self) -> str:
        return self.model

    def get_model_name(self) -> str:
        return self.MODEL_NAMES[self.model]

    def get_unit(self) -> str:
        return self.unit

    def get_serial(self, prefix = False) -> str:
        if prefix:
            return "-".join(["cpr", self.model, self.unit])
        else:
            return "-".join([self.model, self.unit])

class Accessory():

    def __init__(self,
                 name: str = "",
                 parent: str = "base_link",
                 xyz: List[float] = [0.0, 0.0, 0.0],
                 rpy: List[float] = [0.0, 0.0, 0.0]) -> None:
        self.name = name
        self.parent = parent
        self.xyz = xyz
        self.rpy = rpy

    def get_parent(self) -> str:
        return self.parent

    def set_parent(self, parent:str) -> None:
        assert isinstance(parent, str), "Parent must be a string"
        assert not parent[0].isdigit(), "Parent cannot start with a digit"
        self.parent = parent

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        assert isinstance(name, str), "name must be a string"
        assert not name[0].isdigit(), "name cannot start with a digit"
        self.name = name

    def get_xyz(self) -> List[float]:
        return self.xyz

    def set_xyz(self, xyz: List[float]) -> None:
        assert all([isinstance(i, float) for i in xyz]), "XYZ must have all float entries"
        assert len(xyz) == 3, "XYZ must be three float value"

    def get_rpy(self) -> List[float]:
        assert()