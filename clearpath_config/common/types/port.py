
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
