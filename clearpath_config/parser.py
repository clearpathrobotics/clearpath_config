
from clearpath_config.system import SystemConfig, HostsConfig, Host
import os
import yaml


# Keys
class Keys():
    ASSERTION = True
    VERBOSE = True

    class System():
        # System
        SYSTEM = 'system'
        SELF = 'self'
        HOSTS = 'hosts'
        PLATFORM = 'platform'
        ONBOARD = 'onboard'
        REMOTE = 'remote'

        @staticmethod
        def is_valid(key, value):
            if key in [Keys.System.PLATFORM, Keys.System.ONBOARD, Keys.System.REMOTE]:
                # is dictionary
                if not isinstance(value, dict):
                    Keys.print("%s: is not dictionary" % key)
                    return False
                # PLATFORM has exactly one entry
                entries = list(value.items())
                if key == Keys.System.PLATFORM:
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
            else:
                return True

        @staticmethod
        def sanitize(key, value):
            if not Keys.System.is_valid(key, value):
                return None
            if key == Keys.System.PLATFORM:
                hostname, ip  = list(value.items())[0]
                return hostname, ip
            elif key in [Keys.System.ONBOARD, Keys.System.REMOTE]:
                hosts = []
                for hostname, ip in value.items():
                    hosts.append((hostname, ip))
                return hosts

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
    def print(cls, msg, end="\n"):
        if cls.VERBOSE:
            print(msg, end=end)
        if cls.ASSERTION:
            assert 0, msg

    @staticmethod
    def is_valid(key, value):
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

# Clearpath Configuration Parser
class ConfigParser():

    @staticmethod
    # Get Valid Path
    def find_valid_path(path, cwd=None):
        abspath = path
        if cwd:
            relpath = os.path.join(cwd, path)
        else:
            relpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        if not os.path.isfile(abspath) and not os.path.isfile(relpath):
            return None
        if os.path.isfile(abspath):
            path = abspath
        elif os.path.isfile(relpath):
            path = relpath
        return path

    @staticmethod
    def read_yaml(path: str) -> dict:
        # Check YAML Path
        path = ConfigParser.find_valid_path(path, os.getcwd())
        assert path, "YAML file '%s' could not be found" % path
        # Check YAML can be Opened
        try:
            config = yaml.load(open(path), Loader=yaml.SafeLoader)
        except yaml.scanner.ScannerError:
            raise AssertionError("YAML file '%s' is not well formed" % path)
        except yaml.constructor.ConstructorError:
            raise AssertionError("YAML file '%s' is attempting to create unsafe objects" % path)
        # Check contents are a Dictionary
        assert isinstance(config, dict), "YAML file '%s' is not a dictionary" % path
        return config

    @staticmethod 
    def write_yaml(path: str, config: dict) -> None:
        yaml_file = open(path, 'w+')
        yaml.dump(config, yaml_file, sort_keys=False, default_flow_style=None, allow_unicode=True)

    @staticmethod
    def load_system_config(config: dict) -> SystemConfig:
        sysconfig = SystemConfig()
        # System Configuration
        assert Keys.System.SYSTEM in config, "Key '%s' must be in YAML" % Keys.System.SYSTEM
        system = config[Keys.System.SYSTEM]
        # System.SELF
        assert Keys.System.SELF in system, "Key '%s' must be in YAML.System" % Keys.System.SELF
        sysconfig.set_self(system[Keys.System.SELF]) 
        # System.HOSTS
        assert Keys.System.HOSTS in system, "Key '%s' must be in YAML.System" % Keys.System.HOSTS
        hosts = system[Keys.System.HOSTS]
        # System.HOSTS.PLATOFRM
        assert Keys.System.PLATFORM in hosts, "Key '%s' must be in YAML.System.Hosts" % Keys.System.PLATFORM
        platform = hosts[Keys.System.PLATFORM]
        hostname, ip = Keys.System.sanitize(Keys.System.PLATFORM, platform)
        sysconfig.hosts.set_platform(Host(hostname=hostname, ip=ip))
        # System.HOSTS.ONBOARD
        if Keys.System.ONBOARD in hosts:
            onboard_hosts = hosts[Keys.System.ONBOARD]
            onboard_hosts = Keys.System.sanitize(Keys.System.ONBOARD, onboard_hosts)
            for onboard_host in onboard_hosts:
                sysconfig.hosts.add_onboard(hostname=onboard_host[0], ip=onboard_host[1])
        # System.HOSTS.REMOTE
        if Keys.System.REMOTE in hosts:
            remote_hosts = hosts[Keys.System.REMOTE]
            remote_hosts = Keys.System.sanitize(Keys.System.REMOTE, remote_hosts)
            for remote_host in remote_hosts:
                sysconfig.hosts.add_remote(hostname=remote_host[0], ip=remote_host[1])
        return sysconfig