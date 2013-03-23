#!/usr/bin/env python

import flask
import logging
import os
import time


def increment_counter():
    try:
        with open("data/counter", "r") as counter:
            count = int(counter.read()) + 1
    except IOError:
        count = 1
    with open("data/counter", "w") as counter:
        counter.write(str(count))
    return count

def get_distribution():
    with open("/etc/issue", "r") as issue:
        return issue.read().split("\\")[0].strip()

def get_kernel_version():
    with open("/proc/sys/kernel/osrelease", "r") as kernel_version:
        return kernel_version.read().strip()

def get_uptime():
    with open("/proc/uptime", "r") as uptime:
        up_data = uptime.read().strip()
        up_s = float(up_data.split()[0])
        up_d, remainder = divmod(up_s, 86400)
        up_h, remainder = divmod(remainder, 3600)
        up_m, remainder = divmod(remainder, 60)
        return "%d days, %d hours, %d minutes" % (int(up_d), int(up_h), int(up_m))

def get_load():
    with open("/proc/loadavg", "r") as loadavg:
        load = loadavg.read().strip().split()
        return "%s %s %s" % (load[0], load[1], load[2])

def get_memory_usage():
    with open("/proc/meminfo", "r") as memory:
        memory_entries = memory.read().strip().split("\n")
    memory_data = {}
    for entry in memory_entries:
        if any(word in entry for word in ("Total", "Free")):
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
    disk_stats = os.statvfs("/")
    mb_total = float(disk_stats.f_blocks * disk_stats.f_bsize) / 1048576
    mb_free = float(disk_stats.f_bavail * disk_stats.f_frsize) / 1048576
    mb_used = (mb_total - mb_free)
    gb_used = mb_used / 1024
    gb_total = mb_total / 1024
    return "%.1fg of %.1fg" % (gb_used, gb_total)

def get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def get_user_addr():
    try:
        return flask.request.headers['X-Real-Ip']
    except:
        return ""

def get_user_agent():
    try:
        return flask.request.headers['User-Agent']
    except:
        return ""

def write_log_entry():
    with open('logs/access.log', 'a') as log_file:
        log_file.write('%s, %s, %s\n' % (get_timestamp(),get_user_addr(),get_user_agent()))

# instantiate global variables
# these fields won't change between requests,
# so we only poll them once instead of on every request.
_distribution = get_distribution()
_kernel = get_kernel_version()

# instantiate flask
app = flask.Flask(__name__)

# routing
@app.route('/')
def home_page():

    counter = increment_counter()
    write_log_entry()

    now = get_timestamp()
    uptime = get_uptime()

    content = flask.render_template("home_page.html",
        time=now,
        distribution=_distribution,
        kernel=_kernel,
        uptime=uptime,
        counter=counter)

    return content

@app.route("/system")
def system_page():

    counter = increment_counter()
    write_log_entry()

    load = get_load()
    memory, swap = get_memory_usage()
    disk = get_disk_usage()

    content = flask.render_template("system_page.html",
        load=load,
        memory=memory,
        swap=swap,
        disk=disk)

    return content

@app.route("/about")
def about_page():

    counter = increment_counter()
    write_log_entry()

    content = flask.render_template("about_page.html")
    return content

@app.route("/style.css")
def style_page():
    return flask.send_file("templates/style.css", mimetype="text/css")

if __name__ == '__main__':

    # create required directories (only matters when berrystats.py is called directly)
    for directory in ["data", "logs"]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # set up logging
    logging.basicConfig(filename='logs/debug.log',level=logging.DEBUG)

    # run the web app
    try:
        app.run(debug=True)
    except Exception, e:
        logging.exception(e)
