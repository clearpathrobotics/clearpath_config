from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.list import ListConfig
from clearpath_config.accessories.types.accessory import BaseAccessory
from clearpath_config.accessories.types.box import Box
from clearpath_config.accessories.types.cylinder import Cylinder
from clearpath_config.accessories.types.link import Link
from clearpath_config.accessories.types.mesh import Mesh
from clearpath_config.accessories.types.sphere import Sphere
from clearpath_config.common.utils.dictionary import flip_dict
from typing import List


class URDFAccessory():
    LINK = Link.ACCESSORY_TYPE
    BOX = Box.ACCESSORY_TYPE
    CYLINDER = Cylinder.ACCESSORY_TYPE
    SPHERE = Sphere.ACCESSORY_TYPE
    MESH = Mesh.ACCESSORY_TYPE

    TYPE = {
        LINK: Link,
        BOX: Box,
        CYLINDER: Cylinder,
        SPHERE: Sphere,
        MESH: Mesh
    }

    @classmethod
    def assert_type(cls, _type: str) -> None:
        assert _type in cls.TYPE, (
            "Sensor type '%s' must be one of: '%s'" % (
                _type,
                cls.TYPE.keys()
            )
        )

    def __new__(cls, _type: str, name: str) -> BaseAccessory:
        cls.assert_type(_type)
        return cls.TYPE[_type](name=name)


# AccessoryListConfig
class AccessoryListConfig(ListConfig[BaseAccessory, str]):
    def __init__(self) -> None:
        super().__init__(
            uid=lambda obj: obj.get_name(),
            obj_type=BaseAccessory,
            uid_type=str
        )

    def to_dict(self) -> List[dict]:
        d = []
        for accessory in self.get_all():
            d.append(accessory.to_dict())
        return d


# Accessory Config
class AccessoryConfig(BaseConfig):

    ACCESSORIES = "accessories"
    BOX = "box"
    CYLINDER = "cylinder"
    LINK = "link"
    MESH = "mesh"
    SPHERE = "sphere"

    TEMPLATE = {
        ACCESSORIES: {
            BOX: BOX,
            CYLINDER: CYLINDER,
            LINK: LINK,
            MESH: MESH,
            SPHERE: SPHERE,
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        BOX: [],
        CYLINDER: [],
        LINK: [],
        MESH: [],
        SPHERE: []
    }

    def __init__(
            self,
            config: dict = {},
            box: List[Box] = DEFAULTS[BOX],
            cylinder: List[Cylinder] = DEFAULTS[CYLINDER],
            link: List[Link] = DEFAULTS[LINK],
            mesh: List[Mesh] = DEFAULTS[MESH],
            sphere: List[Mesh] = DEFAULTS[SPHERE]
            ) -> None:
        # Initialization
        self.box = box
        self.cylinder = cylinder
        self.link = link
        self.mesh = mesh
        self.sphere = sphere
        # Template
        template = {
            self.KEYS[self.BOX]: AccessoryConfig.box,
            self.KEYS[self.CYLINDER]: AccessoryConfig.cylinder,
            self.KEYS[self.LINK]: AccessoryConfig.link,
            self.KEYS[self.MESH]: AccessoryConfig.mesh,
            self.KEYS[self.SPHERE]: AccessoryConfig.sphere
        }
        super().__init__(template, config, self.ACCESSORIES)

    @property
    def link(self) -> AccessoryListConfig:
        self.set_config_param(
            key=self.KEYS[self.LINK],
            value=self._link.to_dict()
        )
        return self._link

    @link.setter
    def link(self, value: List[dict] | AccessoryListConfig) -> None:
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                "Accessories must be list of type 'dict'"
            )
            accessories = AccessoryListConfig()
            accessory_list = []
            for d in value:
                accessory = Link(name="link")
                accessory.from_dict(d)
                accessory_list.append(accessory)
            accessories.set_all(accessory_list)
            self._link = accessories
        else:
            assert isinstance(value, list), (
                "Accessories must be list of type 'dict'"
            )

    @property
    def box(self) -> AccessoryListConfig:
        self.set_config_param(
            key=self.KEYS[self.BOX],
            value=self._box.to_dict()
        )
        return self._box

    @box.setter
    def box(self, value: List[dict] | AccessoryListConfig) -> None:
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                "Accessories must be list of type 'dict'"
            )
            accessories = AccessoryListConfig()
            accessory_list = []
            for d in value:
                accessory = Box(name="box")
                accessory.from_dict(d)
                accessory_list.append(accessory)
            accessories.set_all(accessory_list)
            self._box = accessories
        else:
            assert isinstance(value, list), (
                "Accessories must be list of type 'dict'"
            )

    @property
    def cylinder(self) -> AccessoryListConfig:
        self.set_config_param(
            key=self.KEYS[self.CYLINDER],
            value=self._cylinder.to_dict()
        )
        return self._cylinder

    @cylinder.setter
    def cylinder(self, value: List[dict] | AccessoryListConfig) -> None:
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                "Accessories must be list of type 'dict'"
            )
            accessories = AccessoryListConfig()
            accessory_list = []
            for d in value:
                accessory = Cylinder(name="cylinder")
                accessory.from_dict(d)
                accessory_list.append(accessory)
            accessories.set_all(accessory_list)
            self._cylinder = accessories
        else:
            assert isinstance(value, list), (
                "Accessories must be list of type 'dict'"
            )

    @property
    def mesh(self) -> AccessoryListConfig:
        self.set_config_param(
            key=self.KEYS[self.MESH],
            value=self._mesh.to_dict()
        )
        return self._mesh

    @mesh.setter
    def mesh(self, value: List[dict] | AccessoryListConfig) -> None:
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                "Accessories must be list of type 'dict'"
            )
            accessories = AccessoryListConfig()
            accessory_list = []
            for d in value:
                accessory = Mesh(name="mesh")
                accessory.from_dict(d)
                accessory_list.append(accessory)
            accessories.set_all(accessory_list)
            self._mesh = accessories
        else:
            assert isinstance(value, list), (
                "Accessories must be list of type 'dict'"
            )

    @property
    def sphere(self) -> AccessoryListConfig:
        self.set_config_param(
            key=self.KEYS[self.SPHERE],
            value=self._sphere.to_dict()
        )
        return self._sphere

    @sphere.setter
    def sphere(self, value: List[dict] | AccessoryListConfig) -> None:
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                "Accessories must be list of type 'dict'"
            )
            accessories = AccessoryListConfig()
            accessory_list = []
            for d in value:
                accessory = Sphere(name="sphere")
                accessory.from_dict(d)
                accessory_list.append(accessory)
            accessories.set_all(accessory_list)
            self._sphere = accessories
        else:
            assert isinstance(value, list), (
                "Accessories must be list of type 'dict'"
            )

    def get_all_accessories(self) -> List[BaseAccessory]:
        accessories = []
        # Link
        accessories.extend(self.get_all_links())
        # Box
        accessories.extend(self.get_all_boxes())
        # Cylinder
        accessories.extend(self.get_all_cylinders())
        # Sphere
        accessories.extend(self.get_all_spheres())
        # Mesh
        accessories.extend(self.get_all_meshes())
        return accessories

    # Link: Add by Object or Parameters
    def add_link(
            self,
            # By Object
            link: Link = None,
            # By Parameters
            name: str = None,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseAccessory.XYZ,
            offset_rpy: List[float] = BaseAccessory.RPY
            ) -> None:
        assert link or name, (
            "Link object or name must be passed"
        )
        if not link and name:
            link = Link(
                name=name,
                parent=parent,
                xyz=xyz,
                rpy=rpy,
                offset_xyz=offset_xyz,
                offset_rpy=offset_rpy
            )
        self._link.add(link)

    # Link: Remove by Object or Name
    def remove_link(
            self,
            # By Object
            link: Link | str
            ) -> None:
        self._link.remove(link)

    # Link: Get Single Object by Name
    def get_link(
            self,
            link: str
            ) -> Link:
        return self._link.get(link)

    # Link: Get All Objects
    def get_all_links(self) -> List[Link]:
        return self._link.get_all()

    # Link: Set Single Object by Name
    def set_link(self, link: Link) -> None:
        self._link.set(link)

    # Link: Set All Objects
    def set_all_links(self, links: List[Link]) -> None:
        self._link.set_all(links)

    # Box: Add by Object or Parameters
    def add_box(
            self,
            # By Object
            box: Box = None,
            # By Parameters
            name: str = None,
            size: List[float] = Box.SIZE,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseAccessory.XYZ,
            offset_rpy: List[float] = BaseAccessory.RPY
            ) -> None:
        assert box or name, (
            "Box object or name must be passed"
        )
        if not box and name:
            box = Box(
                name=name,
                size=size,
                parent=parent,
                xyz=xyz,
                rpy=rpy,
                offset_xyz=offset_xyz,
                offset_rpy=offset_rpy
            )
        self._box.add(box)

    # Box: Remove by Object or Name
    def remove_box(self, box: Box | str) -> None:
        self._box.remove(box)

    # Box: Get Single Object by Name
    def get_box(self, box: str) -> Box:
        return self._box.get(box)

    # Box: Get All Objects
    def get_all_boxes(self) -> List[Box]:
        return self._box.get_all()

    # Box: Set Single Object by Name
    def set_box(self, box: Box) -> None:
        self._box.set(box)

    # Box: Set All Objects
    def set_all_boxes(self, boxes: List[Box]) -> None:
        self._box.set_all(boxes)

    # Cylinder: Add by Object or Parameters
    def add_cylinder(
            self,
            # By Object
            cylinder: Cylinder = None,
            # By Parameters
            name: str = None,
            radius: float = Cylinder.RADIUS,
            length: float = Cylinder.LENGTH,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseAccessory.XYZ,
            offset_rpy: List[float] = BaseAccessory.RPY
            ) -> None:
        assert cylinder or name, (
            "Cylinder object or name must be passed"
        )
        if not cylinder and name:
            cylinder = Cylinder(
                name=name,
                radius=radius,
                length=length,
                parent=parent,
                xyz=xyz,
                rpy=rpy,
                offset_xyz=offset_xyz,
                offset_rpy=offset_rpy
            )
        self._cylinder.add(cylinder)

    # Cylinder: Remove by Object or Name
    def remove_cylinder(self, cylinder: Cylinder | str) -> None:
        self._cylinder.remove(cylinder)

    # Cylinder: Get Single Object by Name
    def get_cylinder(self, cylinder: str) -> Cylinder:
        return self._cylinder.get(cylinder)

    # Cylinder: Get All Objects
    def get_all_cylinders(self) -> List[Cylinder]:
        return self._cylinder.get_all()

    # Cylinder: Set Single Object by Name
    def set_cylinder(self, cylinder: Cylinder) -> None:
        self._cylinder.set(cylinder)

    # Cylinder: Set All Objects
    def set_all_cylinders(self, cylinders: List[Cylinder]) -> None:
        self._cylinder.set_all(cylinders)

    # Sphere: Add by Object or Parameters
    def add_sphere(
            self,
            # By Object
            sphere: Sphere = None,
            # By Parameters
            name: str = None,
            radius: float = Sphere.RADIUS,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseAccessory.XYZ,
            offset_rpy: List[float] = BaseAccessory.RPY
            ) -> None:
        assert sphere or name, (
            "Sphere object or name must be passed"
        )
        if not sphere and name:
            sphere = Sphere(
                name=name,
                radius=radius,
                parent=parent,
                xyz=xyz,
                rpy=rpy,
                offset_xyz=offset_xyz,
                offset_rpy=offset_rpy
            )
        self._sphere.add(sphere)

    # Sphere: Remove by Object or Name
    def remove_sphere(self, sphere: Sphere | str) -> None:
        self._sphere.remove(sphere)

    # Sphere: Get Single Object by Name
    def get_sphere(self, sphere: str) -> Sphere:
        return self._sphere.get(sphere)

    # Sphere: Get All Objects
    def get_all_spheres(self) -> List[Sphere]:
        return self._sphere.get_all()

    # Sphere: Set Single Object by Name
    def set_sphere(self, sphere: Sphere) -> None:
        self._sphere.set(sphere)

    # Sphere: Set All Objects
    def set_all_spheres(self, spheres: List[Sphere]) -> None:
        self._sphere.set_all(spheres)

    # Mesh: Add by Object or Parameters
    def add_mesh(
            self,
            # By Object
            mesh: Mesh = None,
            # By Parameters
            name: str = None,
            visual: float = Mesh.VISUAL,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseAccessory.XYZ,
            offset_rpy: List[float] = BaseAccessory.RPY
            ) -> None:
        assert mesh or name, (
            "Mesh object or name must be passed"
        )
        if not mesh and name:
            mesh = Mesh(
                name=name,
                visual=visual,
                parent=parent,
                xyz=xyz,
                rpy=rpy,
                offset_xyz=offset_xyz,
                offset_rpy=offset_rpy
            )
        self._mesh.add(mesh)

    # Mesh: Remove by Object or Name
    def remove_mesh(
            self,
            # By Object
            mesh: Mesh | str
            ) -> None:
        self._mesh.remove(mesh)

    # Mesh: Get Single Object by Name
    def get_mesh(
            self,
            mesh: str
            ) -> Mesh:
        return self._mesh.get(mesh)

    # Mesh: Get All Objects
    def get_all_meshes(self) -> List[Mesh]:
        return self._mesh.get_all()

    # Mesh: Set Single Object by Name
    def set_mesh(self, mesh: Mesh) -> None:
        self._mesh.set(mesh)

    # Mesh: Set All Objects
    def set_all_meshes(self, meshes: List[Mesh]) -> None:
        self._mesh.set_all(meshes)
