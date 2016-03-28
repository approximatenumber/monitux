#!/usr/bin/env python

import psutil
from more_itertools import unique_everseen


def get_proclist():
    proclist = []
    for pid in psutil.pids():
         proc = psutil.Process(pid)
         proclist.append(proc.name())
    return '\n'.join(list(unique_everseen(proclist)))


def get_cpuload(interval):
    return psutil.cpu_percent(interval=interval)


def grep_proc(procname):
    if procname in get_proclist():
        return True
    else:
        return False



print(get_proclist())
print("cpuload: %s" % get_cpuload(None))
