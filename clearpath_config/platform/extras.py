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
        urdf = None if self._is_default(self._urdf, self.URDF) else str(self._urdf)
        self.set_config_param(
            key=self.KEYS[self.URDF],
            value=urdf
        )
        return urdf

    @urdf.setter
    def urdf(self, value: str) -> None:
        if value is None or value == "None":
            return
        self._urdf = File(path=str(value))

    @property
    def control(self) -> str:
        control = None if self._is_default(self._control, self.CONTROL) else str(self._control)
        self.set_config_param(
            key=self.KEYS[self.CONTROL],
            value=control
        )
        return control

    @control.setter
    def control(self, value: str) -> None:
        if value is None or value == "None":
            return
        self._control = File(path=str(value))

    def _is_default(self, curr: str, key: str) -> bool:
        return curr == str(File(self.DEFAULTS[key]))
