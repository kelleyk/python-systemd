import dbus
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

from systemd.property import Property
from systemd.exceptions import SystemdError


class SystemdDbusObject(object):

    # Must be set by subclass; e.g. 'org.freedesktop.systemd1.*'
    __dbus_interace__ = None

    _on_properties_changed_match = None
    
    def __init__(self, obj_path, watch=True):
        
        self._bus = dbus.SystemBus()
        self._proxy = self._bus.get_object('org.freedesktop.systemd1', obj_path)
        self._interface = dbus.Interface(self._proxy, self.__dbus_interace__)
        self._properties_interface = dbus.Interface(self._proxy, 'org.freedesktop.DBus.Properties')
        
        if watch:
            # @KK: How do we clean this up?  This becomes a call to self._bus.add_signal_receiver(); it returns an
            # instance of 'dbus.connection.SignalMatch'.  BusConnection seems to do the bookkeeping for a "watch" based
            # on each match, and calls watch.cancel() in _clean_up_signal_match().  That is called only from
            # Connection.remove_signal_receiver(), and that is called only from SignalMatch.remove().
            self._on_properties_changed_match = self._properties_interface.connect_to_signal('PropertiesChanged', self._on_properties_changed)
            
        self._load_properties()

    def __del__(self):
        self._cleanup()

    def _cleanup(self):
        if self._on_properties_changed_match is not None:
            self._on_properties_changed_match.remove()
            self._on_properties_changed_match = None
        
    def _on_properties_changed(self, *args, **kargs):
        self._load_properties()

    def _load_properties(self):
        properties = self._properties_interface.GetAll(self._interface.dbus_interface)
        attr_property = Property()
        for key, value in properties.items():
            setattr(attr_property, key, value)
        setattr(self, 'properties', attr_property)
