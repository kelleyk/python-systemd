from .automount import Automount
from .device import Device
from .job import Job
from .manager import Manager
from .path import Path
from .service import Service
from .socket import Socket
from .swap import Swap
from .target import Target
from .timer import Timer
from .unit import Unit


VERSION = (0, 1, 0, 'planning', 0)


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        if VERSION[3] != 'final':
            version = '%s %s %s' % (version, VERSION[3], VERSION[4])
    return version

__all__ = (
    'VERSION', 'get_version',
    'Automount', 'Device', 'Job', 'Manager', 'Path', 'Service', 'Socket', 'Swap', 'Target', 'Timer', 'Unit',
)
