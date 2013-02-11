#!/usr/bin/env python

from datetime import datetime
from flask import Flask, render_template
from os import statvfs
from time import strftime


"""
def log(line):
    log = open("logs/requests.log", "a")
    log.write(line)
    log.write("\n")
    log.close()

def start_timer():
    timer = datetime.now()
    return timer

def stop_timer(timer):
    now = datetime.now()
    milliseconds = (now - timer).total_seconds() * 1000
    return milliseconds
"""

def increment_counter():
    try:
        existing_count = open("data/counter", "r").read()
        if existing_count == "":
            count = 1
        else:
            count = int(existing_count) + 1
    except IOError:
        count = 1
    counter = open("data/counter", "w")
    counter.write(str(count))
    counter.close()
    return count

def reset_counter():
    counter = open("data/counter", "w")
    counter.write("0")
    counter.close()

def get_uptime():
    uptime_seconds = float(open("/proc/uptime", "r").read().strip().split()[0])
    uptime_days, remainder = divmod(uptime_seconds, 86400)
    uptime_hours, remainder = divmod(remainder, 3600)
    uptime_minutes, remainder = divmod(remainder, 60)
    uptime_string = "%d days, %d hours, %d minutes" % (int(uptime_days), int(uptime_hours), int(uptime_minutes))
    return uptime_string

def get_load():
    load = open("/proc/loadavg", "r").read().strip().split()
    load_string = "%s %s %s" % (load[0], load[1], load[2])
    return load_string

def get_memory_usage():
    memory_file = open("/proc/meminfo", "r").read().strip().split("\n")
    memory_data = {}
    for entry in memory_file:
        if "Total" or "Free" in entry:
            fields = entry.split()
            key = fields[0][:-1]
            val = fields[1]
            memory_data[key] = val

    memory_total = int(memory_data["MemTotal"]) / 1024
    memory_free = int(memory_data["MemFree"]) / 1024
    memory_used = (memory_total - memory_free)

    swap_total = int(memory_data["SwapTotal"]) / 1024
    swap_free = int(memory_data["SwapFree"]) / 1024
    swap_used = (swap_total - swap_free)

    memory_string = "%dm of %dm" % (memory_used, memory_total)
    swap_string = "%dm of %dm" % (swap_used, swap_total)
    return memory_string, swap_string

def get_disk_usage():
    disk_stats = statvfs("/")
    mb_total = float(disk_stats.f_blocks * disk_stats.f_bsize) / 1048576
    mb_free = float(disk_stats.f_bavail * disk_stats.f_frsize) / 1048576
    mb_used = (mb_total - mb_free)
    gb_used = mb_used / 1024
    gb_total = mb_total / 1024
    return "%.1fg of %.1fg" % (gb_used, gb_total)

reset_counter()

app = Flask(__name__)
@app.route('/')
def berrystats():

    # increment the counter
    c = increment_counter()

    # get our current stats
    t = strftime("%Y-%m-%d %H:%M:%S")
    u = get_uptime()
    l = get_load()
    m, s = get_memory_usage()
    d = get_disk_usage()

    # pass the content to the template renderer
    content = render_template("berrystats.html", time=t, uptime=u, counter=c, load=l, memory=m, swap=s, disk=d)

    # return the content to the fcgi socket
    return content

if __name__ == '__main__':
    app.run(debug=True)
