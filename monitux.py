#!/usr/bin/env python

import psutil
from more_itertools import unique_everseen
import subprocess
import time


def get_cpuload(interval):
    return psutil.cpu_percent(interval)


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
    current_time = time.time()
    uptime = time.gmtime(current_time - boot_time)
    return uptime


def get_temp():
    acpitemp_file = '/sys/class/thermal/thermal_zone0/temp'
    try:
        temperature = open(acpitemp_file, 'r').read()
        # convert thousands of degrees Celcius to degrees
        return int(temperature)/1000
    except Exception as e:
        return 'Can`t detect temperature: %s' % e


def get_proclist():
    proclist = []
    for pid in psutil.pids():
         proc = psutil.Process(pid)
         proclist.append(proc.name())
    return '\n'.join(list(unique_everseen(proclist)))


def make_screenshot(cmd):
    file = '/tmp/screenshot.png'
    convert = 'convert -pointsize 20 -font Courier -fill black -background white label:@-'
    run_cmd = subprocess.Popen("%s | %s %s" % (cmd, convert, file), shell=True)
    run_cmd.wait()
    return file
