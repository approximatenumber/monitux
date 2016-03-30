#!/usr/bin/env python

import psutil
from more_itertools import unique_everseen
import subprocess


def get_cpuload(interval): return psutil.cpu_percent(interval)


def get_proclist():
    proclist = []
    for pid in psutil.pids():
         proc = psutil.Process(pid)
         proclist.append(proc.name())
    return '\n'.join(list(unique_everseen(proclist)))


def grep_proc(procname):
    if procname in get_proclist():
        return True
    else:
        return False


def make_top_screenshot():
    top_path = '/tmp'
    top_file = 'screenshot.png'
    try:
        top = subprocess.Popen(['top', '-n1', '-b'], stdout=subprocess.PIPE)
        subprocess.check_output(['convert','-pointsize', '16', '-font', 'Courier', '-fill', 'white', '-background', 'black', 'label:@-', '%s/%s' % (top_path, top_file)], stdin=top.stdout)
        top.wait()
    except Exception as e:
        print(e)
        return False
