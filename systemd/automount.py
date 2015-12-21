from .base import SystemdDbusObject


class Automount(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Automount interface"""

    __dbus_interace__ = 'org.freedesktop.systemd1.Automount'
