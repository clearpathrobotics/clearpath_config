
import re


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
