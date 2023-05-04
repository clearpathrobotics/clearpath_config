from clearpath_config.common import Accessory, ListConfig
from clearpath_config.accessories.base import BaseAccessory
from clearpath_config.accessories.link import Link
from clearpath_config.accessories.box import Box
from clearpath_config.accessories.cylinder import Cylinder
from clearpath_config.accessories.sphere import Sphere
from clearpath_config.accessories.mesh import Mesh
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


# Accessory Config
class AccessoryConfig:

    def __init__(self) -> None:
        # Link
        self.__link = ListConfig[Link, str](uid=ListConfig.uid_name)
        # Box
        self.__box = ListConfig[Box, str](uid=ListConfig.uid_name)
        # Cylinder
        self.__cylinder = ListConfig[Cylinder, str](uid=ListConfig.uid_name)
        # Sphere
        self.__sphere = ListConfig[Sphere, str](uid=ListConfig.uid_name)
        # Mesh
        self.__mesh = ListConfig[Mesh, str](uid=ListConfig.uid_name)

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
        self.__link.add(link)

    # Link: Remove by Object or Name
    def remove_link(
            self,
            # By Object
            link: Link | str
            ) -> None:
        self.__link.remove(link)

    # Link: Get Single Object by Name
    def get_link(
            self,
            link: str
            ) -> Link:
        return self.__link.get(link)

    # Link: Get All Objects
    def get_all_links(self) -> List[Link]:
        return self.__link.get_all()

    # Link: Set Single Object by Name
    def set_link(self, link: Link) -> None:
        self.__link.set(link)

    # Link: Set All Objects
    def set_all_links(self, links: List[Link]) -> None:
        self.__link.set_all(links)

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
        self.__box.add(box)

    # Box: Remove by Object or Name
    def remove_box(self, box: Box | str) -> None:
        self.__box.remove(box)

    # Box: Get Single Object by Name
    def get_box(self, box: str) -> Box:
        return self.__box.get(box)

    # Box: Get All Objects
    def get_all_boxes(self) -> List[Box]:
        return self.__box.get_all()

    # Box: Set Single Object by Name
    def set_box(self, box: Box) -> None:
        self.__box.set(box)

    # Box: Set All Objects
    def set_all_boxes(self, boxes: List[Box]) -> None:
        self.__box.set_all(boxes)

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
        self.__cylinder.add(cylinder)

    # Cylinder: Remove by Object or Name
    def remove_cylinder(self, cylinder: Cylinder | str) -> None:
        self.__cylinder.remove(cylinder)

    # Cylinder: Get Single Object by Name
    def get_cylinder(self, cylinder: str) -> Cylinder:
        return self.__cylinder.get(cylinder)

    # Cylinder: Get All Objects
    def get_all_cylinders(self) -> List[Cylinder]:
        return self.__cylinder.get_all()

    # Cylinder: Set Single Object by Name
    def set_cylinder(self, cylinder: Cylinder) -> None:
        self.__cylinder.set(cylinder)

    # Cylinder: Set All Objects
    def set_all_cylinders(self, cylinders: List[Cylinder]) -> None:
        self.__cylinder.set_all(cylinders)

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
        self.__sphere.add(sphere)

    # Sphere: Remove by Object or Name
    def remove_sphere(self, sphere: Sphere | str) -> None:
        self.__sphere.remove(sphere)

    # Sphere: Get Single Object by Name
    def get_sphere(self, sphere: str) -> Sphere:
        return self.__sphere.get(sphere)

    # Sphere: Get All Objects
    def get_all_spheres(self) -> List[Sphere]:
        return self.__sphere.get_all()

    # Sphere: Set Single Object by Name
    def set_sphere(self, sphere: Sphere) -> None:
        self.__sphere.set(sphere)

    # Sphere: Set All Objects
    def set_all_spheres(self, spheres: List[Sphere]) -> None:
        self.__sphere.set_all(spheres)

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
        self.__mesh.add(mesh)

    # Mesh: Remove by Object or Name
    def remove_mesh(
            self,
            # By Object
            mesh: Mesh | str
            ) -> None:
        self.__mesh.remove(mesh)

    # Mesh: Get Single Object by Name
    def get_mesh(
            self,
            mesh: str
            ) -> Mesh:
        return self.__mesh.get(mesh)

    # Mesh: Get All Objects
    def get_all_meshes(self) -> List[Mesh]:
        return self.__mesh.get_all()

    # Mesh: Set Single Object by Name
    def set_mesh(self, mesh: Mesh) -> None:
        self.__mesh.set(mesh)

    # Mesh: Set All Objects
    def set_all_meshes(self, meshes: List[Mesh]) -> None:
        self.__mesh.set_all(meshes)
