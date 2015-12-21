from .base import SystemdDbusObject


class Path(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Path interface"""

    __dbus_interace__ = 'org.freedesktop.systemd1.Path'

