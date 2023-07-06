
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
