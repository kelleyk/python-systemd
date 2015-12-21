import functools

import dbus.exceptions


class SystemdError(Exception):
    def __init__(self, error):
        self.name = error.get_dbus_name().split('.')[3]
        self.message = error.get_dbus_message()

    def __str__(self):
        return '%s(%s)' % (self.name, self.message)

    def __repr__(self):
        return '%s(%s)' % (self.name, self.message)


def raises_systemd_error(fn):
    """If the wrapped function raises DBusException, it is wrapped in SystemdError and re-raised."""
    @functools.wraps(fn)
    def _wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except dbus.exceptions.DBusException as exc:
            raise SystemdError(exc)
    return _wrapper
