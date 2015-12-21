import dbus
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

from systemd.property import Property
from systemd.exceptions import SystemdError


# @KK: Is there a reason why this doesn't have the same layout as the other classes?
class Target(object):
    """Abstraction class to org.freedesktop.systemd1.Target interface"""
    
    def __init__(self, unit_path):
        self._bus = dbus.SystemBus()
        self._proxy = self._bus.get_object('org.freedesktop.systemd1', unit_path)
        self._interface = dbus.Interface(self._proxy, 'org.freedesktop.systemd1.Target')
