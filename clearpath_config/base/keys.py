class Keys():
    VERBOSE = True
    # System
    SYSTEM = 'system'
    SELF = 'self'
    HOSTS = 'hosts'
    PLATFORM = 'platform'
    ONBOARD = 'onboard'
    REMOTE = 'remote'
    # Sensors
    MODEL = 'model'
    NAME = 'name'
    SENSORS = 'sensors'
    MOUNTS = 'mounts'
    DECORATIONS = 'decorations'
    EXTRAS = 'extras'
    ENABLE = 'enable'
    PARENT_LINK = 'parent_link'
    ACCESSORY_LINK = 'accessory_link'
    XYZ = 'xyz'
    RPY = 'rpy'
    ANGLE = 'angle'
    TOPIC = 'topic'
    HEIGHT = 'height'
    SEPARATION = 'separation'
    RADIUS = 'radius'

    strings = []

    @classmethod
    def print(cls, str, end="\n"):
        if cls.VERBOSE:
            print(str, end=end)

    @staticmethod
    def is_valid(key, value):
        if key in [Keys.PLATFORM, Keys.ONBOARD, Keys.REMOTE]:
        # Hosts
            # is dictionary
            if not isinstance(value, dict):
                Keys.print("%s: is not dictionary" % key)
                return False
            # PLATFORM has exactly one entry
            entries = list(value.items())
            if key == Keys.PLATFORM:
                if len(entries) != 1:
                    Keys.print("%s: has more or less than one entry" % key)
                    return False
            for hostname, ip in entries:
                # hostname is string
                if not isinstance(hostname, str):
                    Keys.print("%s: hostname is not a string" % key)
                    return False
                # host ip is ip
                if not Keys.is_ip(ip):
                    Keys.print("%s: ip is not valid" % key)
                    return False
        return True

    @staticmethod
    def is_ip(ip):
        if not isinstance(ip, str):
            Keys.print("ip: is not string")
            return False
        fields = ip.split(".")
        if not len(fields) == 4:
            Keys.print("ip: does not have exactly four fields")
            return False
        for field in fields:
            if not field.isdecimal():
                Keys.print("ip: entry is not decimal")
                return False
            field_int = int(field)
            if not (0 < field_int < 256):
                Keys.print("ip: entry is not in range 0 to 256")
                return False
        return True