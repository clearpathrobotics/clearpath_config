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
from clearpath_config.mounts.types.mount import BaseMount
from typing import List


# PACS
# - all PACS structures
class PACS:
    MAX_ROWS = 8
    MAX_COLUMNS = 7

    class Riser(BaseMount):
        MOUNT_MODEL = "riser"
        THICKNESS = 0.00635

        def __init__(
                self,
                rows: int,
                columns: int,
                thickness: float = THICKNESS,
                parent: str = Accessory.PARENT,
                xyz: List[float] = Accessory.XYZ,
                rpy: List[float] = Accessory.RPY,
                ) -> None:
            super().__init__(
                name=PACS.Riser.get_name_from_idx(0),
                parent=parent,
                xyz=xyz,
                rpy=rpy
            )
            self.rows: int = 0
            self.set_rows(rows)
            self.columns: int = 0
            self.set_columns(columns)
            self.thickness: float = 0.0
            self.set_thickness(thickness)

        def to_dict(self) -> dict:
            d = super().to_dict()
            d['rows'] = self.get_rows()
            d['columns'] = self.get_columns()
            d['thickness'] = self.get_thickness()
            return d

        def from_dict(self, d: dict) -> None:
            super().from_dict(d)
            if 'rows' in d:
                self.set_rows(d['rows'])
            if 'columns' in d:
                self.set_columns(d['columns'])
            if 'thickness' in d:
                self.set_thickness(d['thickness'])

        def get_rows(self) -> int:
            return self.rows

        def set_rows(self, rows: int) -> None:
            assert isinstance(rows, int), (
                "Riser rows must be an integer."
            )
            assert 0 < rows <= PACS.MAX_ROWS, (
                "Riser rows must be between %s and %s" % (
                    0, PACS.MAX_ROWS
                )
            )
            self.rows = rows

        def get_columns(self) -> int:
            return self.columns

        def set_columns(self, columns: int):
            assert isinstance(columns, int), (
                "Riser columns must be an integer."
            )
            assert 0 < columns <= PACS.MAX_COLUMNS, (
                "Riser rows must be between %s and %s" % (
                    0, PACS.MAX_COLUMNS
                )
            )
            self.columns = columns

        def get_height(self) -> float:
            return self.height

        def set_height(self, height: float) -> None:
            assert height >= 0, "Height must be at least 0"
            self.height = height

        def get_thickness(self) -> None:
            return self.thickness

        def set_thickness(self, thickness: float) -> None:
            assert thickness > 0, "Thickness must be greater than 0"
            self.thickness = thickness

    class Bracket(BaseMount):
        MOUNT_MODEL = "bracket"
        HORIZONTAL = "horizontal"
        HORIZONTAL_LARGE = "large"
        VERTICAL = "vertical"
        DEFAULT = HORIZONTAL
        MODELS = [HORIZONTAL, HORIZONTAL_LARGE, VERTICAL]

        def __init__(
            self,
            parent: str = BaseMount.PARENT,
            model: str = DEFAULT,
            xyz: List[float] = [0.0, 0.0, 0.0],
            rpy: List[float] = [0.0, 0.0, 0.0],
        ) -> None:
            # Initialize Accessory
            super().__init__(
                name=PACS.Bracket.get_name_from_idx(0),
                parent=parent,
                xyz=xyz,
                rpy=rpy
            )
            # Model: type of bracket
            self.model = PACS.Bracket.DEFAULT
            if model:
                self.set_model(model)

        def to_dict(self) -> dict:
            d = super().to_dict()
            d['model'] = self.get_model()
            return d

        def from_dict(self, d: dict) -> None:
            super().from_dict(d)
            if 'model' in d:
                self.set_model(d['model'])

        def get_model(self) -> str:
            return self.model

        def set_model(self, model: str) -> None:
            assert model in self.MODELS, " ".join([
                "Unexpected Bracket model '%s'," % model,
                "it must be one of the following: %s" % self.MODELS
            ])
            self.model = model
