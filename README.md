berrystats
==========

berrystats is a tiny Flask/Jinja2 web app to report various stats about a Raspberry Pi running Linux.
This was developed on Arch, but should run on any recent Linux distribution.

**Requires: Nginx, Python 2, Flask, Jinja 2, and Flup**

Sample Output:

    berrystats is online.
    current time: 2013-02-09 19:02:46
    system uptime: 0 days, 2 hours, 13 minutes
    requests since last boot: 21
    load averages: 0.00 0.01 0.04
    memory usage: 81m of 209m
    swap usage: 0m of 210m
    disk usage: 2.6g of 14.5g

HTML:

    <!DOCTYPE html>
    <html>
     <head>
      <title>berrystats</title>
      <link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro" rel="stylesheet" type="text/css" />
      <style type="text/css">
       body { padding-left: 8px; font: 14px "Source Sans Pro" }
       a { color: green; text-decoration: none }
      </style>
     </head>

     <body>
      <p>berrystats is online.</p>
      <p>current time: 2013-02-09 19:02:46</p>
      <p>system uptime: 0 days, 2 hours, 13 minutes</p>
      <p>requests since last boot: 21</p>
      <p>load averages: 0.00 0.01 0.04</p>
      <p>memory usage: 81m of 209m</p>
      <p>swap usage: 0m of 210m</p>
      <p>disk usage: 2.6g of 14.5g</p>
     </body>
    </html>

Installation
------------

**Get the code:**

    $ git clone https://github.com/willroberts/berrystats.git

**Manually include the options from resources/nginx.conf in your /etc/nginx/nginx.conf.**

**Enable and start Nginx:**

    $ sudo systemctl enable nginx.service
    $ sudo systemctl start nginx.service

**Install the web application to /srv/http**

    $ sudo mv flask /srv/http/flask

**Run the web application:**

    $ python /srv/http/flask/start-server.py

**Warning: Never run web apps as the root user!** For best results, run the web app as the same user as Nginx (usually "http").

Troubleshooting / Debugging
---------------------------

You can see debug messages for the web application by running berrystats.py directly:

    $ python /srv/http/flask/berrystats.py &
    * Running on http://127.0.0.1:5000/
    $ curl localhost:5000
