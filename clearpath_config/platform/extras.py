from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.file import File
from clearpath_config.common.utils.dictionary import flip_dict


# ExtrasConfig:
# - URDF extras: urdf.xacro with custom links and joints
# - Control extras: YAML with overwrites or extra ROS parameters
class ExtrasConfig(BaseConfig):

    EXTRAS = "extras"
    URDF = "urdf"
    CONTROL = "control"

    TEMPLATE = {
        EXTRAS: {
            URDF: URDF,
            CONTROL: CONTROL
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        URDF: "empty.urdf.xacro",
        CONTROL: "empty.yaml"
    }

    def __init__(
            self,
            config: dict = {},
            urdf: str = DEFAULTS[URDF],
            control: str = DEFAULTS[CONTROL]
            ) -> None:
        # Initialization
        self._config = {}
        self.urdf = urdf
        self.control = control
        # Setter Template
        setters = {
            self.KEYS[self.URDF]: ExtrasConfig.urdf,
            self.KEYS[self.CONTROL]: ExtrasConfig.control
        }
        # Set from Config
        super().__init__(setters, config, self.EXTRAS)

    @property
    def urdf(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.URDF],
            value=str(self._urdf)
        )
        return str(self._urdf)

    @urdf.setter
    def urdf(self, value: str) -> None:
        self._urdf = File(path=str(value))

    @property
    def control(self) -> str:
        self.set_config_param(
            key=self.KEYS[self.CONTROL],
            value=str(self._control)
        )
        return str(self._control)

    @control.setter
    def control(self, value: str) -> None:
        self._control = File(path=str(value))
