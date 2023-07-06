from typing import List


class Accessory():
    # Defaults
    PARENT = "base_link"
    XYZ = [0.0, 0.0, 0.0]
    RPY = [0.0, 0.0, 0.0]

    def __init__(
            self,
            name: str,
            parent: str = PARENT,
            xyz: List[float] = XYZ,
            rpy: List[float] = RPY
            ) -> None:
        self.name = str()
        self.parent = str()
        self.xyz = list()
        self.rpy = list()
        self.set_name(name)
        self.set_parent(parent)
        self.set_xyz(xyz)
        self.set_rpy(rpy)

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.assert_valid_link(name)
        self.name = name

    def get_parent(self) -> str:
        return self.parent

    def set_parent(self, parent: str) -> None:
        self.assert_valid_link(parent)
        self.parent = parent

    def get_xyz(self) -> List[float]:
        return self.xyz

    def set_xyz(self, xyz: List[float]) -> None:
        self.assert_valid_triplet(
            xyz,
            "XYZ must be a list of exactly three float values"
        )
        self.xyz = xyz

    def get_rpy(self) -> List[float]:
        return self.rpy

    def set_rpy(self, rpy: List[float]) -> None:
        self.assert_valid_triplet(
            rpy,
            "RPY must be a list of exactly three float values"
        )
        self.rpy = rpy

    @staticmethod
    def assert_valid_link(link: str) -> None:
        # Link name must be a string
        assert isinstance(link, str), "Link name '%s' must be string" % link
        # Link name must not be empty
        assert link, "Link name '%s' must not be empty" % link
        # Link name must not have spaces
        assert " " not in link, "Link name '%s' must no have spaces" % link
        # Link name must not start with a digit
        assert not link[0].isdigit(), (
            "Link name '%s' must not start with a digit" % link
        )

    @staticmethod
    def assert_valid_triplet(tri: List[float], msg: str = None) -> None:
        if msg is None:
            msg = "Triplet must be a list of three float values"
        # Triplet must be a list
        assert isinstance(tri, list), msg
        # Triplet must have a length of 3
        assert len(tri) == 3, msg
        # Triplet must be all floats
        assert all([isinstance(i, float) for i in tri])


class IndexedAccessory(Accessory):

    def __init__(
            self,
            idx: int = None,
            name: str = None,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY
            ) -> None:
        if name is None:
            name = self.get_name_from_idx(0)
        super().__init__(
            name,
            parent,
            xyz,
            rpy
        )
        # Index:
        # - index of sensor
        # - used to modify parameters to allow for multiple instances
        #   of the same sensor.
        self.idx = 0
        if idx is not None:
            self.set_idx(idx)

    @classmethod
    def get_name_from_idx(idx):
        return "accessory_%s" % idx

    def get_idx(self) -> str:
        return self.idx

    def set_idx(self, idx: int) -> None:
        assert isinstance(idx, int), "Index must be an integer"
        assert idx >= 0, "Index must be a positive integer"
        self.name = self.get_name_from_idx(idx)
