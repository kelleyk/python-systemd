from .base import SystemdDbusObject


class Timer(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Timer interface"""

    __dbus_interace__ = 'org.freedesktop.systemd1.Timer'
