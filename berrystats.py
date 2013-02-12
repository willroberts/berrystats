#!/usr/bin/env python

import os
import datetime
import flask
import time


def update_counter(count):
    with open("data/counter", "w") as counter:
        counter.write(count)

def increment_counter():
    try:
        existing_count = open("data/counter", "r").read()
        if existing_count == "":
            count = 1
        else:
            count = int(existing_count) + 1
    except IOError:
        count = 1
    update_counter(str(count))
    return count

def get_distribution():
    issue_file = open("/etc/issue", "r").read().strip()
    distribution = issue_file.split("\\")[0].strip()
    return distribution

def get_kernel_version():
    kernel_version = open("/proc/sys/kernel/osrelease", "r").read().strip()
    return kernel_version

def get_uptime():
    up_data = open("/proc/uptime", "r").read().strip()
    up_s = float(up_data.split()[0])
    up_d, remainder = divmod(up_s, 86400)
    up_h, remainder = divmod(remainder, 3600)
    up_m, remainder = divmod(remainder, 60)
    up_string = "%d days, %d hours, %d minutes" % (int(up_d), int(up_h), int(up_m))
    return up_string

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
    disk_stats = os.statvfs("/")
    mb_total = float(disk_stats.f_blocks * disk_stats.f_bsize) / 1048576
    mb_free = float(disk_stats.f_bavail * disk_stats.f_frsize) / 1048576
    mb_used = (mb_total - mb_free)
    gb_used = mb_used / 1024
    gb_total = mb_total / 1024
    return "%.1fg of %.1fg" % (gb_used, gb_total)

# instantiate flask
app = flask.Flask(__name__)

# set up routing
@app.route('/')
def home_page():

    # increment the counter
    counter = increment_counter()

    # get general data
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    distribution = get_distribution()
    kernel = get_kernel_version()
    uptime = get_uptime()

    # pass the content to the template renderer
    content = flask.render_template("home_page.html",
        time=now,
        distribution=distribution,
        kernel=kernel,
        uptime=uptime,
        counter=counter)

    # return the content to the fcgi socket
    return content

@app.route("/system")
def system_page():

    # increment the counter
    counter = increment_counter()

    # get system data
    load = get_load()
    memory, swap = get_memory_usage()
    disk = get_disk_usage()

    # pass the content to the template renderer
    content = flask.render_template("system_page.html",
        load=load,
        memory=memory,
        swap=swap,
        disk=disk)

    # return the content to the fcgi socket
    return content

@app.route("/about")
def about_page():

    # increment the counter
    counter = increment_counter()

    # pass the content to the template renderer
    content = flask.render_template("about_page.html")

    # return the content to the fcgi socket
    return content

@app.route("/style.css")
def style_page():
    return flask.send_file("templates/style.css", mimetype="text/css")

@app.route("/berry.png")
def berry_image():
    return flask.send_file("templates/berry.png", mimetype="image/png")

if __name__ == '__main__':

    # create required directories (only matters when berrystats.py is called directly)
    for directory in ["data", "logs"]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # reset the counter
    update_counter("0")

    # run the web app
    app.run(debug=True)
