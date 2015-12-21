from .base import SystemdDbusObject


class Device(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Device interface"""

    __dbus_interace__ = 'org.freedesktop.systemd1.Device'
