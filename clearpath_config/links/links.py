# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
# @copyright (c) 2023, Clearpath Robotics, Inc., All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Clearpath Robotics nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from clearpath_config.common.types.accessory import Accessory
from clearpath_config.common.types.config import BaseConfig
from clearpath_config.common.types.list import ListConfig
from clearpath_config.common.utils.dictionary import flip_dict
from clearpath_config.links.types.link import BaseLink
from clearpath_config.links.types.box import Box
from clearpath_config.links.types.cylinder import Cylinder
from clearpath_config.links.types.frame import Frame
from clearpath_config.links.types.mesh import Mesh
from clearpath_config.links.types.sphere import Sphere
from typing import List


class Link():
    FRAME = Frame.LINK_TYPE
    BOX = Box.LINK_TYPE
    CYLINDER = Cylinder.LINK_TYPE
    SPHERE = Sphere.LINK_TYPE
    MESH = Mesh.LINK_TYPE

    TYPE = {
        FRAME: Frame,
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

    def __new__(cls, _type: str, name: str) -> BaseLink:
        cls.assert_type(_type)
        return cls.TYPE[_type](name=name)


# LinkListConfig
class LinkListConfig(ListConfig[BaseLink, str]):
    def __init__(self) -> None:
        super().__init__(
            uid=lambda obj: obj.get_name(),
            obj_type=BaseLink,
            uid_type=str
        )

    def to_dict(self) -> List[dict]:
        d = []
        for link in self.get_all():
            d.append(link.to_dict())
        return d


# Links Config
class LinksConfig(BaseConfig):

    LINKS = "links"
    BOX = "box"
    CYLINDER = "cylinder"
    FRAME = "frame"
    MESH = "mesh"
    SPHERE = "sphere"

    TEMPLATE = {
        LINKS: {
            BOX: BOX,
            CYLINDER: CYLINDER,
            FRAME: FRAME,
            MESH: MESH,
            SPHERE: SPHERE,
        }
    }

    KEYS = flip_dict(TEMPLATE)

    DEFAULTS = {
        BOX: [],
        CYLINDER: [],
        FRAME: [],
        MESH: [],
        SPHERE: []
    }

    def __init__(
            self,
            config: dict = {},
            box: List[Box] = DEFAULTS[BOX],
            cylinder: List[Cylinder] = DEFAULTS[CYLINDER],
            frame: List[Frame] = DEFAULTS[FRAME],
            mesh: List[Mesh] = DEFAULTS[MESH],
            sphere: List[Mesh] = DEFAULTS[SPHERE]
            ) -> None:
        # Initialization
        self.box = box
        self.cylinder = cylinder
        self.frame = frame
        self.mesh = mesh
        self.sphere = sphere
        # Template
        template = {
            self.KEYS[self.BOX]: LinksConfig.box,
            self.KEYS[self.CYLINDER]: LinksConfig.cylinder,
            self.KEYS[self.FRAME]: LinksConfig.frame,
            self.KEYS[self.MESH]: LinksConfig.mesh,
            self.KEYS[self.SPHERE]: LinksConfig.sphere
        }
        super().__init__(template, config, self.LINKS)

    @property
    def frame(self) -> LinkListConfig:
        self.set_config_param(
            key=self.KEYS[self.FRAME],
            value=self._frame.to_dict()
        )
        return self._frame

    @frame.setter
    def frame(self, value: List[dict] | LinkListConfig) -> None:
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                "Links must be list of type 'dict'"
            )
            links = LinkListConfig()
            link_list = []
            for d in value:
                link = Frame(name="frame")
                link.from_dict(d)
                link_list.append(link)
            links.set_all(link_list)
            self._frame = links
        else:
            assert isinstance(value, list), (
                "Links must be list of type 'dict'"
            )

    @property
    def box(self) -> LinkListConfig:
        self.set_config_param(
            key=self.KEYS[self.BOX],
            value=self._box.to_dict()
        )
        return self._box

    @box.setter
    def box(self, value: List[dict] | LinkListConfig) -> None:
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                "Links must be list of type 'dict'"
            )
            links = LinkListConfig()
            link_list = []
            for d in value:
                link = Box(name="box")
                link.from_dict(d)
                link_list.append(link)
            links.set_all(link_list)
            self._box = links
        else:
            assert isinstance(value, list), (
                "Links must be list of type 'dict'"
            )

    @property
    def cylinder(self) -> LinkListConfig:
        self.set_config_param(
            key=self.KEYS[self.CYLINDER],
            value=self._cylinder.to_dict()
        )
        return self._cylinder

    @cylinder.setter
    def cylinder(self, value: List[dict] | LinkListConfig) -> None:
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                "Links must be list of type 'dict'"
            )
            links = LinkListConfig()
            link_list = []
            for d in value:
                link = Cylinder(name="cylinder")
                link.from_dict(d)
                link_list.append(link)
            links.set_all(link_list)
            self._cylinder = links
        else:
            assert isinstance(value, list), (
                "Links must be list of type 'dict'"
            )

    @property
    def mesh(self) -> LinkListConfig:
        self.set_config_param(
            key=self.KEYS[self.MESH],
            value=self._mesh.to_dict()
        )
        return self._mesh

    @mesh.setter
    def mesh(self, value: List[dict] | LinkListConfig) -> None:
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                "Links must be list of type 'dict'"
            )
            links = LinkListConfig()
            link_list = []
            for d in value:
                link = Mesh(name="mesh")
                link.from_dict(d)
                link_list.append(link)
            links.set_all(link_list)
            self._mesh = links
        else:
            assert isinstance(value, list), (
                "Links must be list of type 'dict'"
            )

    @property
    def sphere(self) -> LinkListConfig:
        self.set_config_param(
            key=self.KEYS[self.SPHERE],
            value=self._sphere.to_dict()
        )
        return self._sphere

    @sphere.setter
    def sphere(self, value: List[dict] | LinkListConfig) -> None:
        if isinstance(value, list):
            assert all([isinstance(i, dict) for i in value]), (
                "Links must be list of type 'dict'"
            )
            links = LinkListConfig()
            link_list = []
            for d in value:
                link = Sphere(name="sphere")
                link.from_dict(d)
                link_list.append(link)
            links.set_all(link_list)
            self._sphere = links
        else:
            assert isinstance(value, list), (
                "Links must be list of type 'dict'"
            )

    def get_all_links(self) -> List[BaseLink]:
        links = []
        # Frame
        links.extend(self.get_all_frames())
        # Box
        links.extend(self.get_all_boxes())
        # Cylinder
        links.extend(self.get_all_cylinders())
        # Sphere
        links.extend(self.get_all_spheres())
        # Mesh
        links.extend(self.get_all_meshes())
        return links

    # Frame: Add by Object or Parameters
    def add_frame(
            self,
            # By Object
            frame: Frame = None,
            # By Parameters
            name: str = None,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseLink.XYZ,
            offset_rpy: List[float] = BaseLink.RPY
            ) -> None:
        assert frame or name, (
            "Frame object or name must be passed"
        )
        if not frame and name:
            frame = Frame(
                name=name,
                parent=parent,
                xyz=xyz,
                rpy=rpy,
                offset_xyz=offset_xyz,
                offset_rpy=offset_rpy
            )
        self._frame.add(frame)

    # Frame: Remove by Object or Name
    def remove_frame(
            self,
            # By Object
            frame: Frame | str
            ) -> None:
        self._frame.remove(frame)

    # Frame: Get Single Object by Name
    def get_frame(
            self,
            frame: str
            ) -> Frame:
        return self._frame.get(frame)

    # Frame: Get All Objects
    def get_all_frames(self) -> List[Frame]:
        return self._frame.get_all()

    # Frame: Set Single Object by Name
    def set_frame(self, frame: Frame) -> None:
        self._frame.set(frame)

    # Frame: Set All Objects
    def set_all_frames(self, frames: List[Frame]) -> None:
        self._frame.set_all(frames)

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
            offset_xyz: List[float] = BaseLink.XYZ,
            offset_rpy: List[float] = BaseLink.RPY
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
            offset_xyz: List[float] = BaseLink.XYZ,
            offset_rpy: List[float] = BaseLink.RPY
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
            offset_xyz: List[float] = BaseLink.XYZ,
            offset_rpy: List[float] = BaseLink.RPY
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
            visual: dict = Mesh.VISUAL,
            parent: str = Accessory.PARENT,
            xyz: List[float] = Accessory.XYZ,
            rpy: List[float] = Accessory.RPY,
            offset_xyz: List[float] = BaseLink.XYZ,
            offset_rpy: List[float] = BaseLink.RPY
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
