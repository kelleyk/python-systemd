from .base import SystemdDbusObject


class Service(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Service interface"""

    __dbus_interace__ = 'org.freedesktop.systemd1.Service'
