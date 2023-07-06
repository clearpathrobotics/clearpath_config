from clearpath_config.common.types.accessory import Accessory
from typing import List


class BaseDecoration(Accessory):
    """
    BaseDecoration
     - enable: whether decoration is enabled or not
     - model: what type of that decoration it is
    """
    DECORATION_MODEL = "base_decoration"
    ENABLED = True
    DEFAULT = "default"
    MODELS = [DEFAULT]

    def __init__(
            self,
            name: str = DECORATION_MODEL,
            enabled: bool = ENABLED,
            model: str = DEFAULT,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        super().__init__(name, parent, xyz, rpy)
        self.enabled: bool = bool(enabled)
        self.model: str = BaseDecoration.DEFAULT
        self.set_model(model)

    def to_dict(self) -> dict:
        d = {self.name: {
            'enabled': self.get_enabled(),
            'model': self.get_model(),
            'xyz': self.get_xyz(),
            'ryp': self.get_rpy()
        }}
        return d

    def from_dict(self, d: dict) -> None:
        if 'enabled' in d:
            self.set_enabled(d['enabled'])
        if 'model' in d:
            self.set_model(d['model'])
        if 'xyz' in d:
            self.set_xyz(d['xyz'])
        if 'rpy' in d:
            self.set_rpy(d['rpy'])

    def set_enabled(self, enable: bool) -> None:
        self.enabled = bool(enable)

    def get_enabled(self) -> bool:
        return self.enabled

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def get_model(self) -> str:
        return self.model

    def set_model(self, model: str) -> None:
        assert model in self.MODELS, (
            "%s model '%s' is not one of: '%s'" % (
                self.DECORATION_MODEL.title(),
                model,
                self.MODELS,
            )
        )
        self.model = model
