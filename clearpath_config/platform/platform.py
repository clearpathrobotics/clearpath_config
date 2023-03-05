from clearpath_config.common import Accessory, File, Platform, SerialNumber
from clearpath_config.platform.decorations import BaseDecorationsConfig
from clearpath_config.platform.a200 import A200DecorationsConfig
from clearpath_config.platform.j100 import J100DecorationsConfig
from clearpath_config.platform.genx import GENXDecorationsConfig
from typing import List
'''
I was thinking about creating a directory: platform under which we could have platform.py, pacs.py, decorations.py, and all of the robots in their respective folders, i.e. a200.py, j100.py etc. or husky.py, jackal.py, etc.

    platform
        platform.py (PlatformConfig, DecorationsConfig, PACSConfig)
        decorations.py (BaseDecorationsConfig, Bumper, TopPlate, etc.)
        pacs.py (FullRiser, RowRiser, and Brackets)
        a200.py (A200DecorationsConfig(DecorationsConfig) and A200PACSConfig(PACSConfig))
        j100.py...

Where DecorationsConfig would still return the model config (e.g. A200DecorationsConfig depending on the model)
'''

# DecorationsConfig:
# - platform specific structures
# - each platform should have its own DecorationsConfig
class DecorationsConfig():

    '''
    DecorationsConfig
        - top level configuration for all models
        - returns appropriate config from sub-classes
    '''
    MODEL_CONFIGS = {Platform.DD100: None,
                     Platform.DO100: None,
                     Platform.A200: A200DecorationsConfig(),
                     Platform.J100: J100DecorationsConfig(),
                     Platform.R100: None,
                     Platform.W200: None,
                     Platform.GENX: GENXDecorationsConfig()}

    def __new__(self, model) -> None:
        assert model in Platform.ALL, "Model passed '%s' is not expected. must be one of the following: %s" % (model, Platform.ALL)
        return self.MODEL_CONFIGS[model]


# ExtrasConfig:
# - URDF extras: urdf.xacro with custom links and joints
# - Control extras: YAML with overwrites or extra ROS parameters
class ExtrasConfig():

    def __init__(self, urdf: str = "", control: str = "") -> None:
        self.urdf = File(path=urdf)
        self.control = File(path=control)

    def get_urdf_extras(self) -> str:
        return str(self.urdf)

    def set_urdf_extras(self, path: str) -> None:
        self.urdf = File(path=path)

    def get_control_extras(self) -> str:
        return str(self.control)

    def set_control_extras(self, path: str) -> None:
        self.control = File(path=path)


# PlatformConfig:
# - platform level configuration options
class PlatformConfig():

    def __init__(self, 
                 serial: str = "genx-0000",
                 decorations: BaseDecorationsConfig = None,
                 extras: ExtrasConfig = None) -> None:
        self.serial = SerialNumber(sn = serial)
        self.model = self.serial.get_model()
        self.decorations = DecorationsConfig(model=self.get_model())
        self.extras = ExtrasConfig()
        if decorations:
            assert isinstance(decorations, BaseDecorationsConfig), "Decorations must be of type DecorationsConfig, unexpected type: '%s'" % type(decorations)
            assert decorations.model == self.model, "Decorations do not match the model of the serial number"
            self.decorations = decorations
        if extras:
            assert isinstance(extras, ExtrasConfig), "Extras must be of type ExtrasConfig, unexpected type: '%s'" % type(extras)
            self.extras = extras

    def set_serial_number(self, serial_number: str) -> None:
        self.serial = SerialNumber(serial_number)
        self.decorations = DecorationsConfig(model=self.get_model())

    def get_serial_number(self, prefix: bool = False) -> str:
        return self.serial.get_serial(prefix)

    def get_unit_number(self) -> str:
        return self.serial.get_unit()

    def get_model(self) -> str:
        return self.serial.get_model()

