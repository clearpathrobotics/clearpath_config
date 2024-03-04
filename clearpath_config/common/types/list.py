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
from copy import deepcopy
from typing import (
    Callable,
    Generic,
    List,
    TypeVar
)


# ListConfigs: Generic Types
T = TypeVar("T")
U = TypeVar("U")


# ListConfigs
# - holds a list of an object type
# - generic class
class ListConfig(Generic[T, U]):

    def __init__(
            self,
            uid: Callable,
            obj_type: type,
            uid_type: type
            ) -> None:
        self.__list: List[T] = []
        self.__uid: Callable = uid
        self.__type_T: type = obj_type
        self.__type_U: type = uid_type

    def extend(self, other: list):
        self.__list.extend(other)
        return self

    def find(
            self,
            _obj: T | U,
            ) -> int:
        # Object: T: Template
        if isinstance(_obj, self.__type_T):
            uid = self.__uid(_obj)
        # Object: U: Unique ID
        elif isinstance(_obj, self.__type_U):
            uid = _obj
        # Error
        else:
            raise AssertionError(
                "Object must be of type %s or %s" % (
                    self.__type_T.__name__,
                    self.__type_U.__name__
                )
            )
        for idx, obj in enumerate(self.__list):
            if self.__uid(obj) == uid:
                return idx
        return None

    def add(
            self,
            obj: T,
            ) -> None:
        assert isinstance(obj, self.__type_T), (
            "Object must be of type %s" % (
                self.__type_T.__name__
            )
        )
        assert self.find(obj) is None, (
            "Object with uid %s is not unique." % (
                self.__uid(obj)
            )
        )
        self.__list.append(obj)

    def replace(
            self,
            obj: T,
            ) -> None:
        assert isinstance(obj, self.__type_T), (
            "Object must be of type %s" % T
        )
        assert self.find(obj) is not None, (
            "Object with uid %s cannot be replaced. Does not exist." % (
                self.__uid(obj)
            )
        )
        self.__list[self.find(obj)] = obj

    def remove(
            self,
            _obj: T | U,
            ) -> None:
        idx = self.find(_obj)
        if idx is not None:
            self.__list.remove(self.__list[idx])

    def remove_all(self) -> None:
        self.__list.clear()

    def get(
            self,
            _obj: T | U,
            ) -> T:
        idx = self.find(_obj)
        return None if idx is None else self.__list[idx]

    def get_all(self) -> List[T]:
        return self.__list

    def set(
            self,
            obj: T
            ) -> None:
        if obj is None:
            return
        if self.find(obj) is None:
            self.add(obj)
        else:
            self.replace(obj)

    def set_all(
            self,
            _list: List[T],
            ) -> None:
        # Copy and Clear
        tmp_list = deepcopy(self.__list)
        self.__list.clear()
        # Add One-by-One
        try:
            for obj in _list:
                self.add(obj)
        # Restore Save if Failure
        except AssertionError:
            self.__list = tmp_list

    # TODO: the below UID methods are not supported by most implementations of this class
    # Unique Identifier: Name
    @staticmethod
    def uid_name(T) -> str:
        return T.get_name()

    # Unique Identifier: Level
    @staticmethod
    def uid_level(T) -> int:
        return T.get_level()

    # Unique Identifier: Level-Row
    @staticmethod
    def uid_level_row(T) -> tuple:
        return (T.get_level(), T.get_row())


# OrderedListConfig
# - T must have the following methods:
#   - get_idx(): return an index from members
#   - set_idx(idx): set an index and update members
class OrderedListConfig(Generic[T]):

    def __init__(self, obj_type: type, start_idx: int = 0) -> None:
        self.start_idx = start_idx
        self.__type_T: type = obj_type
        self.__list: List[T] = []

    def set_index_offset(self, offset: int) -> None:
        self.start_idx = offset
        self.update()

    def find(
            self,
            obj: T | int
            ) -> int:
        if isinstance(obj, self.__type_T):
            idx = obj.get_idx()
        elif isinstance(obj, int):
            idx = obj
        else:
            raise AssertionError(
                "Object must of type %s or %s" % (
                    self.__type_T, int
                )
            )
        if self.start_idx <= idx < len(self.__list) + self.start_idx:
            return idx
        else:
            return None

    def update(self):
        for raw_idx, obj in enumerate(self.__list):
            idx = raw_idx + self.start_idx
            self.__list[raw_idx].set_idx(idx)

    def add(
            self,
            obj: T
            ) -> None:
        assert isinstance(obj, self.__type_T), (
            "Object must be of type %s" % T
        )
        self.__list.append(obj)
        self.update()

    def replace(
            self,
            obj: T,
            ) -> None:
        idx = self.find(obj)
        assert idx is not None, (
            "Object not found. Cannot be replaced"
        )
        self.__list[idx - self.start_idx] = obj
        self.update()

    def remove(
            self,
            obj: T | int
            ) -> None:
        idx = self.find(obj)
        if idx is not None:
            self.__list.remove(self.__list[idx - self.start_idx])
        self.update()

    def remove_all(self) -> None:
        self.__list.clear()

    def get(
            self,
            obj: T | int,
            ) -> T:
        idx = self.find(obj)
        return None if idx is None else self.__list[idx - self.start_idx]

    def get_all(
            self
            ) -> List[T]:
        return self.__list

    def set(
            self,
            obj: T
            ) -> None:
        if self.find(obj) is None:
            self.add(obj)
        else:
            self.replace(obj)

    def set_all(
            self,
            _list: List[T],
            ) -> None:
        # Copy and Clear
        tmp_list = deepcopy(self.__list)
        self.__list.clear()
        # If Empty Keep Empty
        if not _list:
            return
        # Add One-by-One
        try:
            for obj in _list:
                self.add(obj)
        # Restore Save if Failure
        except AssertionError:
            self.__list = tmp_list
        self.update()
