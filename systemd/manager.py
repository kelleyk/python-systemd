#
# Copyright (c) 2010 Mandriva
#
# This file is part of python-systemd.
#
# python-systemd is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of
# the License, or (at your option) any later version.
#
# python-systemd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import dbus
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

from systemd.unit import Unit
from systemd.job import Job
from systemd.property import Property
from systemd.exceptions import SystemdError

from .base import SystemdDbusObject
from .exceptions import SystemdError, raises_systemd_error


class Manager(SystemdDbusObject):
    """Abstraction class to org.freedesktop.systemd1.Manager interface.

    The dbus interface is documented at https://wiki.freedesktop.org/www/Software/systemd/dbus/
    """
    
    def __init__(self):
        # XXX: For the time being, at least, we do NOT call the parent class's constructor because of the call to self.subscribe() here.
        # super(Manager, self).__init__('/org/freedesktop/systemd1')
        
        self._bus = dbus.SystemBus()
        self._proxy = self._bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        self._interface = dbus.Interface(self._proxy, 'org.freedesktop.systemd1.Manager')
        self.subscribe()

        self._properties_interface = dbus.Interface(self._proxy, 'org.freedesktop.DBus.Properties')
        self._on_properties_changed_match = self._properties_interface.connect_to_signal('PropertiesChanged', self._on_properties_changed)
        self._load_properties()

    def __del__(self):
        self.unsubscribe()
        super(Manager, self).__del__()

    @raises_systemd_error
    def subscribe(self):
        self._interface.Subscribe()

    @raises_systemd_error
    def clear_jobs(self):
        self._interface.ClearJobs()
        
    @raises_systemd_error
    def dump(self):
        self._interface.Dump()

    @raises_systemd_error
    def exit(self):
        self._interface.Exit()

    @raises_systemd_error
    def create_snapshot(self, name, cleanup):
        snapshot_path = self._interface.CreateSnapshot(name, cleanup)
        return str(snapshot_path)

    @raises_systemd_error
    def get_job(self, ID):
        """Get job by it ID.
        
        @param ID: Job ID.
        
        @raise SystemdError: Raised when no job is found with the given ID.
        
        @rtype: systemd.job.Job
        """
        job_path = self._interface.GetJob(ID)
        job = Job(job_path)
        return job

    @raises_systemd_error
    def get_unit(self, name):
        """Get unit by it name.
        
        @param name: Unit name (ie: network.service).
        
        @raise SystemdError: Raised when no unit is found with the given name.
        
        @rtype: systemd.unit.Unit
        """
        unit_path = self._interface.GetUnit(name)
        unit = Unit(unit_path)
        return unit

    @raises_systemd_error
    def get_unit_by_pid(self, pid):
        """Get unit by it PID.
        
        @param PID: Unit PID.
        
        @raise SystemdError: Raised when no unit with that PID is found.
        
        @rtype: systemd.unit.Unit
        """
        unit_path = self._interface.GetUnitByPID(pid)
        unit = Unit(unit_path)
        return unit

    @raises_systemd_error
    def halt(self):
        self._interface.Halt()

    @raises_systemd_error
    def k_exec(self):
        self._interface.KExec()
    
    @raises_systemd_error
    def kill_unit(self, name, who, mode, signal):
        """Kill unit.
        
        @param name: Unit name (ie: network.service).
        @param who: Must be one of main, control or all.
        @param mode: Must be one of control-group, process-group, process.
        @param signal: Must be one of the well know signal number such  as
        SIGTERM(15), SIGINT(2), SIGSTOP(19) or SIGKILL(9).
        
        @raise SystemdError: Raised when no unit is found with the given name.
        
        @rtype: L{systemd.job.Job}
        """
        self._interface.KillUnit(name, who, mode, signal)

    @raises_systemd_error
    def list_jobs(self):
        """List all jobs.
        
        @raise SystemdError, IndexError: Raised when dbus error or index error
        is raised.
        
        @rtype: A list of L{systemd.unit.Job}
        """
        jobs = []
        for job in self._interface.ListJobs():
            jobs.append(Job(job[4]))
        return jobs

    @raises_systemd_error
    def list_units(self, watch=True):
        """List all units, inactive units too.

        Warning: each Unit object listens to the corresponding D-Bus object (to be notified of changes).  There is a
        limit on the number of things that a single D-Bus client can monitor, so if there are too many systemd units,
        this function will fail.  You can either pass watch=False (to avoid watching for changes to each unit) or use
        iter_units() instead.
        
        @raise SystemdError: Raised when dbus error or index error
        is raised.
        
        @rtype: A list of L{systemd.unit.Unit}

        """
        units = []
        for unit in self._interface.ListUnits():
            units.append(Unit(unit[6], watch=watch))
        return units

    @raises_systemd_error
    def iter_units(self, watch=True):
        """Return an iterator over all units, including inactive ones.

        Iff watch is True, each object will not listen to the underlying D-Bus object for changes.
        
        @raise SystemdError: Raised when dbus error or index error
        is raised.
        
        @rtype: An iterator over L{systemd.unit.Unit} objects

        """
        for unit in self._interface.ListUnits():
            yield Unit(unit[6], watch=watch)

    @raises_systemd_error
    def load_unit(self, name):
        """Load unit by it name.
        
        @param name: Unit name (ie: network.service).
        
        @raise SystemdError: Raised when no unit is found with the given name.
        
        @rtype: L{systemd.unit.Unit}
        """
        unit_path = self._interface.LoadUnit(name)
        unit = Unit(unit_path)
        return unit

    @raises_systemd_error
    def power_off(self):
        self._interface.PowerOff()
        
    @raises_systemd_error
    def reboot(self):
        self._interface.Reboot()

    @raises_systemd_error
    def reexecute(self):
        self._interface.Reexecute()

    @raises_systemd_error
    def reload(self):
        self._interface.Reload()

    @raises_systemd_error
    def reload_or_restart_unit(self, name, mode):
        """Reload or restart unit.
        
        @param name: Unit name (ie: network.service).
        @param mode: Must be one of fail, replace or isolate.
        
        @raise SystemdError: Raised when no unit is found with the given name.
        
        @rtype: L{systemd.job.Job}
        """
        job_path = self._interface.ReloadOrRestartUnit(name, mode)
        job = Job(job_path)
        return job

    @raises_systemd_error
    def reload_or_try_restart_unit(self, name, mode):
        """Reload or try restart unit.
        
        @param name: Unit name (ie: network.service).
        @param mode: Must be one of fail, replace or isolate.
        
        @raise SystemdError: Raised when no unit is found with the given name.
        
        @rtype: L{systemd.job.Job}
        """
        job_path = self._interface.ReloadOrTryRestartUnit(name, mode)
        job = Job(job_path)
        return job

    @raises_systemd_error
    def reload_unit(self, name, mode):
        """Reload  unit.
        
        @param name: Unit name (ie: network.service).
        @param mode: Must be one of fail, replace.
        
        @raise SystemdError: Raised when no unit is found with the given name or
        mode is not corret.
        
        @rtype: L{systemd.job.Job}
        """
        job_path = self._interface.ReloadUnit(name, mode)
        job = Job(job_path)
        return job

    @raises_systemd_error
    def reset_failed(self):
        self._interface.ResetFailed()

    @raises_systemd_error
    def reset_failed_unit(self, name):
        self._interface.ResetFailedUnit(name)

    @raises_systemd_error
    def restart_unit(self, name, mode):
        """Restart unit.
        
        @param name: Unit name (ie: network.service).
        @param mode: Must be one of fail, replace or isolate.
        
        @raise SystemdError: Raised when no unit is found with the given name.
        
        @rtype: L{systemd.job.Job}
        """
        job_path = self._interface.RestartUnit(name, mode)
        job = Job(job_path)
        return job

    @raises_systemd_error
    def set_environment(self, names):
        self._interface.SetEnvironment(names)
        
    @raises_systemd_error
    def start_unit(self, name, mode):
        """Start unit.
        
        @param name: Unit name (ie: network.service).
        @param mode: Must be one of fail or replace.
        
        @raise SystemdError: Raised when no unit is found with the given name.
        
        @rtype: L{systemd.job.Job}
        """
        job_path = self._interface.StartUnit(name, mode)
        job = Job(job_path)
        return job

    @raises_systemd_error
    def start_unit_replace(self, old_unit, new_unit, mode):
        """Start unit replace.
        
        @param old_unit: Old unit.
        @param new_unit: New unit.
        @param mode: Must be one of fail, replace, isolate, rescue or emergency.
        
        @raise SystemdError: Raised when no unit is found with the given name.
        
        @rtype: L{systemd.job.Job}
        """
        job_path = self._interface.StartUnitReplace(old_unit, new_unit, mode)
        job = Job(job_path)
        return job

    @raises_systemd_error
    def stop_unit(self, name, mode):
        """Stop unit.
        
        @param name: Unit name (ie: network.service).
        @param mode:  Must be one of fail or replace.
        
        @raise SystemdError: Raised when no unit is found with the given name.
        
        @rtype: L{systemd.job.Job}
        """
        job_path = self._interface.StopUnit(name, mode)
        job = Job(job_path)
        return job

    @raises_systemd_error
    def try_restart_unit(self, name, mode):
        """Try restart unit.
        
        @param name: Unit name (ie: network.service).
        @param mode: Must be one of "fail" or "replace.
        
        @raise SystemdError: Raised when no unit is found with the given name or mode is invalid.
        
        @rtype: L{systemd.job.Job}
        """
        job_path = self._interface.TryRestartUnit(name, mode)
        job = Job(job_path)
        return job

    @raises_systemd_error
    def unset_environment(self, names):
        self._interface.UnsetEnvironment(names)

    @raises_systemd_error
    def unsubscribe(self):
        self._interface.Unsubscribe()

    @raises_systemd_error
    def enable_unit_files(self, files, runtime=False, force=False):
        """
        @param files: A list of paths (of unit files).
        @param runtime: If True, symlink unit into /run (enabled only for runtime); if False, symlink unit into /etc.
        @param force: If True, symlinks belonging to other units will be replaced if necessary.

        @raise SystemdError

        @rtype: 2-tuple of
            b       carries_install_info
            a(sss)  changes
        """
        carries_install_info, changes = self._interface.EnableUnitFiles(files, runtime, force)
        return carries_install_info, changes
        
    @raises_systemd_error
    def disable_unit_files(self, files, runtime=False):
        """
        @param files: A list of paths (of unit ifles).
        @param runtime: If True, remove symlinks from /run; if False, remove symlinks from /etc.

        @raise SystemdError

        @rtype: a(sss) changes
        """
        changes = self._interface.DisableUnitFiles(files, runtime)
        return changes
        
    @raises_systemd_error
    def reenable_unit_files(self, files, runtime=False, force=False):
        """Disable and then enable the given units.

        This has the effect of returning the units' configuration symlinks to their defaults.

        @param files: A list of paths (of unit files).
        @param runtime: If True, symlink unit into /run (enabled only for runtime); if False, symlink unit into /etc.
        @param force: If True, symlinks belonging to other units will be replaced if necessary.

        @raise SystemdError

        @rtype: 2-tuple of
            b       carries_install_info
            a(sss)  changes
        """
        carries_install_info, changes = self._interface.ReenableUnitFiles(files, runtime, force)
        return carries_install_info, changes

    @raises_systemd_error
    def list_unit_files(self):
        """Returns a list of each unit file and its enablement status.

        Enablement status is the same as the 'UnitFileState' property of the Unit.

        @rtype: list of 2-tuples of (unit file path, enablement status)
        """
        return self._interface.ListUnitFiles()

    @raises_systemd_error
    def get_unit_file_state(self, file_):
        """Returns the enablement status of the given unit.

        This is the same as the 'UnitFileState' property of the Unit.

        @param file_: The filename (not path) of a unit file.

        @rtype: enablement status; one of {'enabled', 'disabled', 'static', ...}
        """
        return self._interface.GetUnitFileState(file_)
        
    # def link_unit_files(self, files, runtime, force):
    #     pass

    # def preset_unit_files(self, files, runtime, force):
    #     pass

    # def mask_unit_files(self, files, runtime, force):
    #     pass

    # def unmask_unit_files(self, files, runtime, force):
    #     pass

    @raises_systemd_error
    def set_default_target(self, name):
        changes = self._interface.SetDefaultTarget(name)
        return changes

    @raises_systemd_error
    def get_default_target(self):
        """
        @rtype: string; the name of a target; e.g. "graphical.target", "multi-user.target"
        """
        return self._interface.GetDefaultTarget()
    
    # def set_unit_properties(name, runtime, properties):

    # def start_transient_unit(name, mode, properties, aux):
    
