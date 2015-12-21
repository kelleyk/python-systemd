import dbus
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

from .base import SystemdDbusObject
from .exceptions import SystemdError, raises_systemd_error


def job_if_exists(job_path):
    try:
        return Job(job_path)
    except dbus.exceptions.DBusException as error:
        if "Unknown interface 'org.freedesktop.systemd1.Job'." in str(error):
            return None
        raise
    

class Job(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Job interface"""

    __dbus_interace__ = 'org.freedesktop.systemd1.Job'

    @raises_systemd_error
    def cancel(self):
        self._interface.Cancel()
