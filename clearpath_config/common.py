import re

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
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

    @staticmethod
    def assert_valid(hostname: str):
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
