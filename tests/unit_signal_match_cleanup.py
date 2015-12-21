"""
Any arrangement other than list_units(watch=True) works well.
"""

import systemd.manager

mgr = systemd.manager.Manager()

print('A' * 20)
for unit in mgr.iter_units():
    print('A {}'.format(unit))
    unit._cleanup()

print('B' * 20)
for unit in mgr.iter_units(watch=False):
    print('B {}'.format(unit))
    
print('C' * 20)
for unit in mgr.list_units(watch=False):
    print('C {}'.format(unit))
