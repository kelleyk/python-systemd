from .base import SystemdDbusObject


class Socket(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Socket interface"""

    __dbus_interace__ = 'org.freedesktop.systemd1.Socket'
