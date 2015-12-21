import dbus.exceptions

from .base import SystemdDbusObject
from .exceptions import SystemdError, raises_systemd_error


class Snapshot(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Snapshot interface"""

    __dbus_interace__ = 'org.freedesktop.systemd1.Snapshot'

    @raises_systemd_error
    def remove(self):
        self._interface.Remove()
