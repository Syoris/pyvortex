import ctypes
from enum import Enum
from pydantic import BaseModel
from abc import ABC

import Vortex  # noqa
# import vxatp3  # noqa


class VortexInterface(BaseModel, ABC):
    """Abstract class for a vortex interface. To list the name of the interface in the vortex scene.
    Here, interface intends to be the input, output, or parameter defined .
    """

    ...


class AppMode(Enum):
    EDITING = Vortex.kModeEditing
    SIMULATING = Vortex.kModeSimulating
    PLAYBACK = Vortex.kModePlayingBack


class Vector3(ctypes.Structure):
    _fields_ = ("x", ctypes.c_double), ("y", ctypes.c_double), ("z", ctypes.c_double)

    def __repr__(self):
        return "({0}, {1}, {2})".format(self.x, self.y, self.z)


class Vector4(ctypes.Structure):
    _fields_ = (
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
        ("z", ctypes.c_double),
        ("w", ctypes.c_double),
    )
