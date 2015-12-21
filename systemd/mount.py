from .base import SystemdDbusObject


class Mount(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Mount interface"""

    __dbus_interace__ = 'org.freedesktop.systemd1.Mount'
