#!/usr/bin/env python

import psutil
from more_itertools import unique_everseen
import subprocess
import tempfile


def get_cpuload(interval): return psutil.cpu_percent(interval)


def get_mem_stat():
    mem = list(psutil.virtual_memory())
    # convert Bytes to GB
    mem_all = round(mem[0]/10**9, 1)
    mem_free = round(mem[1]/10**9, 1)
    mem_used = round(mem_all - mem_free, 1)
    mem_stat = 'Used: %s Gb, Free: %s Gb, Total: %s Gb' % (mem_used, mem_free, mem_all)
    return mem_stat


def get_disk_stat():
    disk_stat = []
    for dev in (psutil.disk_partitions()):
        disk_stat.append('%s (%s): Free: %s Gb, Used: %s Gb, Total: %s Gb' % (dev[0], dev[1], \
                                                                            # convert Bytes to GB and round
                                                                            round(int(psutil.disk_usage(dev[1])[2])/10**9, 1), \
                                                                            round(int(psutil.disk_usage(dev[1])[1])/10**9, 1), \
                                                                            round(int(psutil.disk_usage(dev[1])[0])/10**9, 1)))
    return '\n'.join(disk_stat)


def get_temp():
    acpitemp_file = '/sys/class/thermal/thermal_zone0/temp'
    if psutil.os.path.isfile(acpitemp_file) is True:
        temperature = open(acpitemp_file, 'r').read()
        # convert thousands of degrees Celcius to degrees
        return int(temperature)/1000
    else:
        return '%s not found!' % acpitemp_file


def get_proclist():
    proclist = []
    for pid in psutil.pids():
         proc = psutil.Process(pid)
         proclist.append(proc.name())
    return '\n'.join(list(unique_everseen(proclist)))


def grep_proc(procname):
    if procname in get_proclist():
        return procname
    else:
        return False


def get_top_screenshot():
    top_path = '/tmp/top_screenshot.png'
    try:
        top = subprocess.Popen(['top', '-n1', '-b'], stdout=subprocess.PIPE)
        subprocess.check_output(['convert','-pointsize', '20', '-font', 'Courier', '-fill', 'black', '-background', 'white', 'label:@-', '%s' % top_path], stdin=top.stdout)
        top.wait()
        return top_path
    except Exception as e:
        print(e)
        return False


def get_ifconfig_screenshot():
    ifconfig_path = '/tmp/ifconfig_screenshot.png'
    try:
        ifconfig = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
        subprocess.check_output(['convert','-pointsize', '20', '-font', 'Courier', '-fill', 'black', '-background', 'white', 'label:@-', '%s' % ifconfig_path], stdin=ifconfig.stdout)
        ifconfig.wait()
        return ifconfig_path
    except Exception as e:
        print(e)
        return False
