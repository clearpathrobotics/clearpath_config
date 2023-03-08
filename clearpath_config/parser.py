from clearpath_config.common import Platform
from clearpath_config.clearpath_config import ClearpathConfig
from clearpath_config.platform.decorations import Decorations, BaseDecorationsConfig
from clearpath_config.platform.pacs import PACS
from clearpath_config.platform.platform import PlatformConfig
from clearpath_config.platform.a200 import A200DecorationsConfig, A200PACSConfig
from clearpath_config.platform.j100 import J100DecorationsConfig
from clearpath_config.system.system import SystemConfig, HostsConfig, Host
from typing import List
import os
import yaml


class BaseConfigParser:
    @staticmethod
    def check_key_exists(key: str, config: dict) -> bool:
        return key in config

    @staticmethod
    def assert_key_exists(key: str, config: dict) -> None:
        assert BaseConfigParser.check_key_exists(
            key, config
        ), "Key '%s' must be in YAML"

    @staticmethod
    def get_required_val(key: str, config: dict):
        BaseConfigParser.assert_key_exists(key, config)
        return config[key]

    @staticmethod
    def get_optional_val(key: str, config: dict, default=None):
        if BaseConfigParser.check_key_exists(key, config):
            return config[key]
        else:
            return default


class HostsConfigParser(BaseConfigParser):
    # Key
    HOSTS = "hosts"
    # Host Keys
    PLATFORM = "platform"
    ONBOARD = "onboard"
    REMOTE = "remote"

    def __new__(cls, config: dict) -> HostsConfig:
        htsconfig = HostsConfig()
        # Hosts
        hosts = cls.get_required_val(cls.HOSTS, config)
        # Hosts.Platform
        platform = cls.get_platform_host(config=hosts)
        htsconfig.set_platform(platform)
        # Hosts.Onboard
        htsconfig.set_onboard(cls.get_hostlists(cls.ONBOARD, hosts))
        # Hosts.Remote
        htsconfig.set_remote(cls.get_hostlists(cls.REMOTE, hosts))
        print(htsconfig.get_remote())
        return htsconfig

    @classmethod
    def get_platform_host(cls, config) -> Host:
        platform = cls.get_required_val(cls.PLATFORM, config)
        assert isinstance(platform, dict), "Platform host must be a dictionary"
        entries = list(platform.items())
        assert (
            len(entries) == 1
        ), "Platform must have exactly one ('hostname': 'ip') entry"
        hostname, ip = entries[0]
        return Host(hostname, ip)

    @classmethod
    def get_hostlists(cls, key, config) -> List[Host]:
        hostlist = cls.get_optional_val(key, config)
        if not hostlist:
            return []
        assert isinstance(hostlist, dict), (
            "%s host list must be a dictionary" % key.title()
        )
        hosts = []
        for hostname, value in hostlist.items():
            hosts.append(Host(hostname, value))
        return hosts


class SystemConfigParser(BaseConfigParser):
    # Key
    SYSTEM = "system"
    # System Keys
    SELF = "self"
    HOSTS = "hosts"

    def __new__(cls, config: dict) -> SystemConfig:
        sysconfig = SystemConfig()
        # System
        system = cls.get_required_val(cls.SYSTEM, config)
        # System.Self
        sysconfig.set_self(cls.get_required_val(cls.SELF, system))
        # System.Hosts
        sysconfig.set_hosts(HostsConfigParser(system))
        return sysconfig


class PACSConfigParser(BaseConfigParser):
    # Key
    PACS_KEY = "pacs"
    # PACS Keys
    FULL_RISERS = "full_risers"
    ROW_RISERS = "row_risers"
    BRACKETS = "brackets"

    @classmethod
    def get_full_risers(cls, config: dict) -> List[PACS.FullRiser]:
        pacs_full_risers = []
        config_full_risers = cls.get_optional_val(cls.FULL_RISERS, config)
        if not config_full_risers:
            return []
        assert isinstance(config_full_risers, list), "Full Risers must be a list"
        assert all(
            [isinstance(entry, dict) for entry in config_full_risers]
        ), "Full Risers must be a list of 'dict's"
        for riser in config_full_risers:
            level = cls.get_required_val("level", riser)
            height = cls.get_required_val("height", riser)
            pacs_full_risers.append(PACS.FullRiser(level, height))
        return pacs_full_risers

    @classmethod
    def get_row_risers(cls, config: dict) -> List[PACS.RowRiser]:
        pacs_row_risers = []
        config_row_risers = cls.get_optional_val(cls.ROW_RISERS, config)
        if not config_row_risers:
            return []
        assert isinstance(config_row_risers, list), "Row Risers must be a list"
        assert all(
            [isinstance(entry, dict) for entry in config_row_risers]
        ), "Row Risers must be a list of 'dict's"
        for riser in config_row_risers:
            row = cls.get_required_val("row", riser)
            level = cls.get_required_val("level", riser)
            height = cls.get_required_val("height", riser)
            pacs_row_risers.append(PACS.RowRiser(level, row, height))
        return pacs_row_risers

    @classmethod
    def get_brackets(cls, config: dict) -> List[PACS.Bracket]:
        pacs_brackets = []
        config_brackets = cls.get_optional_val(cls.BRACKETS, config)
        if not config_brackets:
            return []
        assert isinstance(config_brackets, dict), "Brackets must be a dict"
        for name, bracket in config_brackets.items():
            model = cls.get_optional_val("model", bracket, PACS.Bracket.DEFAULT)
            parent = cls.get_required_val("parent", bracket)
            extension = cls.get_optional_val("extension", bracket, 0.0)
            xyz = cls.get_optional_val("xyz", bracket, [0.0, 0.0, 0.0])
            rpy = cls.get_optional_val("rpy", bracket, [0.0, 0.0, 0.0])
            pacs_brackets.append(PACS.Bracket(name, parent, model, extension, xyz, rpy))
        return pacs_brackets

    class A200(BaseConfigParser):
        def __new__(cls, config: dict) -> A200DecorationsConfig:
            pacsconfig = A200PACSConfig()
            # PACS
            pacs = cls.get_optional_val(PACSConfigParser.PACS_KEY, config)
            if not pacs:
                pacsconfig.disable()
                return pacsconfig
            # PACS.Full_Risers
            pacsconfig.full_risers = PACSConfigParser.get_full_risers(pacs)
            # PACS.Row_Risers
            pacsconfig.row_risers = PACSConfigParser.get_row_risers(pacs)
            # PACS.Brackets
            pacsconfig.brackets = PACSConfigParser.get_brackets(pacs)
            return pacsconfig

    """
    PACS Config
    """
    MODEL_CONFIGS = {Platform.A200: A200}

    def __new__(cls, model: str, config: dict):
        assert model in cls.MODEL_CONFIGS, "Model '%s' must be one of %s" % (
            model,
            cls.MODEL_CONFIGS.keys(),
        )
        return cls.MODEL_CONFIGS[model](config)


class BumperConfigParser(BaseConfigParser):
    # Bumper Keys
    ENABLE = "enable"
    EXTENSION = "extension"
    MODEL = "model"

    def __new__(cls, key: str, config: dict) -> Decorations.Bumper:
        bmpconfig = Decorations.Bumper()
        # Bumper
        bumper = cls.get_optional_val(key, config)
        if not bumper:
            return bmpconfig
        # Bumper.Enable
        if cls.get_required_val(cls.ENABLE, bumper):
            bmpconfig.enable()
        else:
            bmpconfig.disable()
        # Bumper.Extension
        bmpconfig.set_extension(cls.get_required_val(cls.EXTENSION, bumper))
        # Bumper.Model
        bmpconfig.set_model(cls.get_required_val(cls.MODEL, bumper))
        return bmpconfig


class TopPlateConfigParser(BaseConfigParser):
    # Top Plate Keys
    ENABLE = "enable"
    MODEL = "model"

    def __new__(cls, key: str, config: dict) -> Decorations.A200.TopPlate:
        topconfig = Decorations.A200.TopPlate()
        # Top_Plate
        top_plate = cls.get_optional_val(key, config)
        if not top_plate:
            return topconfig
        # Top_Plate.Enable
        if cls.get_required_val(cls.ENABLE, top_plate):
            topconfig.enable()
        else:
            topconfig.disable()
        # Top_Plate.Model
        topconfig.set_model(cls.get_required_val(cls.MODEL, top_plate))
        return topconfig


class DecorationsConfigParser(BaseConfigParser):
    # Key
    DECORATIONS = "decorations"

    class A200:
        # A200 Husky Decoration Keys
        FRONT_BUMPER = "front_bumper"
        REAR_BUMPER = "rear_bumper"
        TOP_PLATE = "top_plate"
        PACS = "pacs"

        def __new__(cls, config: dict) -> A200DecorationsConfig:
            dcnconfig = A200DecorationsConfig()
            dcnparser = DecorationsConfigParser
            # Decorations
            decorations = dcnparser.get_required_val(dcnparser.DECORATIONS, config)
            # Decorations.Front_Bumper
            dcnconfig.front_bumper = BumperConfigParser(cls.FRONT_BUMPER, decorations)
            # Decorations.Rear_Bumper
            dcnconfig.rear_bumper = BumperConfigParser(cls.REAR_BUMPER, decorations)
            # Decorations.Top_Plate
            dcnconfig.top_plate = TopPlateConfigParser(cls.TOP_PLATE, decorations)
            # Decorations.PACS
            dcnconfig.pacs = PACSConfigParser(Platform.A200, decorations)
            return dcnconfig

    class J100:
        # J100 Jackal Decoration Keys
        FRONT_BUMPER = "front_bumper"
        REAR_BUMPER = "rear_bumper"

        def __new__(cls, config: dict) -> J100DecorationsConfig:
            dcnconfig = J100DecorationsConfig()
            dcnparser = DecorationsConfigParser
            # Decorations
            decorations = dcnparser.get_required_val(dcnparser.DECORATIONS, config)
            # Decorations.Front_Bumper
            dcnconfig.front_bumper = BumperConfigParser(cls.FRONT_BUMPER, decorations)
            # Decorations.Rear_Bumper
            dcnconfig.rear_bumper = BumperConfigParser(cls.REAR_BUMPER, decorations)
            return dcnconfig

    MODEL_CONFIGS = {Platform.A200: A200, Platform.J100: J100}

    def __new__(cls, model: str, config: dict) -> BaseDecorationsConfig:
        assert model in Platform.ALL, "Model '%s' must be one of %s" % (
            model,
            Platform.ALL,
        )
        return DecorationsConfigParser.MODEL_CONFIGS[model](config)


class PlatformConfigParser(BaseConfigParser):
    # Key
    PLATFORM = "platform"
    # Platform Keys
    SERIAL_NUMBER = "serial_number"
    DECORATIONS = "decorations"
    EXTRAS = "extras"
    # Platform Extras KEys
    URDF = "urdf"
    CONTROL = "control"

    def __new__(cls, config: dict) -> PlatformConfig:
        pfmconfig = PlatformConfig()
        # Platform
        platform = cls.get_required_val(cls.PLATFORM, config)
        # Platform.SerialNumber
        pfmconfig.set_serial_number(cls.get_required_val(cls.SERIAL_NUMBER, platform))
        # Platform.Decorations
        pfmconfig.decorations = DecorationsConfigParser(pfmconfig.get_model(), platform)
        # Platform.Extras
        extras = cls.get_optional_val(cls.EXTRAS, platform)
        if extras:
            pfmconfig.extras.set_urdf_extras(cls.get_optional_val(cls.URDF, extras, ""))
            pfmconfig.extras.set_control_extras(
                cls.get_optional_val(cls.CONTROL, extras, "")
            )
        return pfmconfig


# Clearpath Configuration Parser
class ClearpathConfigParser(BaseConfigParser):
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
        path = ClearpathConfigParser.find_valid_path(path, os.getcwd())
        assert path, "YAML file '%s' could not be found" % path
        # Check YAML can be Opened
        try:
            config = yaml.load(open(path), Loader=yaml.SafeLoader)
        except yaml.scanner.ScannerError:
            raise AssertionError("YAML file '%s' is not well formed" % path)
        except yaml.constructor.ConstructorError:
            raise AssertionError(
                "YAML file '%s' is attempting to create unsafe objects" % path
            )
        # Check contents are a Dictionary
        assert isinstance(config, dict), "YAML file '%s' is not a dictionary" % path
        return config

    @staticmethod
    def write_yaml(path: str, config: dict) -> None:
        yaml_file = open(path, "w+")
        yaml.dump(
            config,
            yaml_file,
            sort_keys=False,
            default_flow_style=None,
            allow_unicode=True,
        )

    """
    ConfigParser():
        - will take a config file path or a config and return a ClearpathConfig
    """

    def __new__(self, config):
        # Path: if config is path to config file, read YAML
        if isinstance(config, str):
            config = self.read_yaml(config)
        # Dict: if not path, it must be of type config
        assert isinstance(config, dict), "Configuration must be of type 'dict'"
        # ClearpathConfig
        cprconfig = ClearpathConfig()
        # SystemConfig
        cprconfig.system = SystemConfigParser(config)
        # PlatformConfig
        cprconfig.platform = PlatformConfigParser(config)
        return cprconfig
