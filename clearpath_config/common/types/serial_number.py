from clearpath_config.common.types.platform import Platform


# SerialNumber
# - Clearpath Robots Serial Number
# - ex. cpr-j100-0100
# - drop 'cpr' prefix as it is not required
class SerialNumber:
    SERIAL_NUMBER = "serial_number"

    def __init__(self, sn: str) -> None:
        self.model, self.unit = SerialNumber.parse(sn)

    def __str__(self) -> str:
        return self.get_serial()

    def from_dict(self, config: dict) -> None:
        assert isinstance(config, dict), (
            "Config must be of type 'dict'"
        )
        assert self.SERIAL_NUMBER in config, (
            "Key '%s' must be in config" % self.SERIAL_NUMBER
        )
        self.model, self.unit = SerialNumber.parse(config[self.SERIAL_NUMBER])

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
