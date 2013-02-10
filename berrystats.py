#!/usr/bin/env python

from datetime import datetime
from flask import Flask, render_template
from time import strftime


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

def get_memory_info():
    memory_file = open("/proc/meminfo", "r").read().strip().split("\n")
    memory_data = {}
    for entry in memory_file:
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

app = Flask(__name__)
@app.route('/')
def berrystats():

    # increment the counter
    timer = start_timer()
    c = increment_counter()
    ms = stop_timer(timer)

    # get the current date and time
    timer = start_timer()
    t = strftime("%Y-%m-%d %H:%M:%S")
    ms = stop_timer(timer)
    log("\n==== %s ====" % t)

    # get the system uptime
    timer = start_timer()
    u = get_uptime()
    ms = stop_timer(timer)
    log("Reading uptime took %.2fms" % ms)

    # get load info 
    timer = start_timer()
    l = get_load()
    ms = stop_timer(timer)
    log("Reading load averages took %.2fms" % ms)

    # get memory info
    timer = start_timer()
    m, s = get_memory_info()
    ms = stop_timer(timer)
    log("Reading memory info took %.2fms" % ms)

    # pass the content to the template renderer
    timer = start_timer()
    content = render_template("berrystats.html", time=t, uptime=u, load=l, memory=m, swap=s, counter=c)
    ms = stop_timer(timer)
    log("Rendering Jinja2 template took %.2fms" % ms)

    # return the content to the fcgi socket
    return content

if __name__ == '__main__':
    app.run(debug=True)
