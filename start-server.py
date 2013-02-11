#!/usr/bin/env python

print("Importing os...")
import os

print("Importing WSGIServer from flup.server.fcgi...")
from flup.server.fcgi import WSGIServer

print("Setting up required directories...")
for directory in ["data", "logs"]:
    if not os.path.exists(directory):
        os.makedirs(directory)

print("Importing app from berrystats...")
from berrystats import app

if __name__ == "__main__":

    print("Started!")

    # run the app
    WSGIServer(app, bindAddress="/srv/http/berrystats/data/flup.sock").run()
