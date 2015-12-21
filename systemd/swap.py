from .base import SystemdDbusObject


class Swap(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Swap interface"""

    __dbus_interace__ = 'org.freedesktop.systemd1.Swap'
