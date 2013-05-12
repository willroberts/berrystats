#!/usr/bin/env python

print("Starting...")

print("Importing required libraries...")
import os
from flup.server.fcgi import WSGIServer

print("Creating required directories...")
for directory in ["data", "logs"]:
    if not os.path.exists(directory):
        os.makedirs(directory)

print("Importing berrystats...")
import berrystats

if __name__ == "__main__":
    print("Started!")
    WSGIServer(berrystats.app,
               bindAddress="/srv/http/berrystats/data/flup.sock").run()
