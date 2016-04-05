#!/usr/bin/env python

import psutil
from more_itertools import unique_everseen
import subprocess
import tempfile
import time


def get_cpuload(interval): return psutil.cpu_percent(interval)


def get_mem_stat():
    mem = list(psutil.virtual_memory())
    # convert Bytes to GB
    total = round(mem[0]/10**9, 1)
    free = round(mem[1]/10**9, 1)
    used = round(total - free, 1)
    mem_stat = [total, used, free]
    return mem_stat


def get_disk_stat():
    disk_stat = []
    for device in (psutil.disk_partitions()):
        partition = device[0]
        mounted = device[1]
        # convert bytes to Gb
        total = round(int(psutil.disk_usage(device[1])[0])/10**9, 1)
        used = round(int(psutil.disk_usage(device[1])[1])/10**9, 1)
        free = round(total - used, 1)
        disk_stat.append([partition, mounted, total, used, free])
    return sorted(disk_stat)


def get_uptime():
    boot_time = psutil.boot_time()
    cur_time = time.time()
    uptime = time.gmtime(cur_time - boot_time)
    return uptime


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
        return 'can`t '


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
