berrystats
==========

berrystats is a tiny Flask/Jinja2 web app to report various stats about a Raspberry Pi running Linux.
This was developed on Arch, but should run on any recent Linux distribution.

**Requires: Nginx, Python 2, Flask, Jinja 2, and Flup**

Sample Output:

![Home page](https://raw.github.com/willroberts/berrystats/master/templates/preview_home.png)

![System page](https://raw.github.com/willroberts/berrystats/master/templates/preview_system.png)

![About page](https://raw.github.com/willroberts/berrystats/master/templates/preview_about.png)

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
