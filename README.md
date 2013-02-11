berrystats
==========

berrystats is a tiny (160kb!) Flask/Jinja2 web app to report various stats about a Raspberry Pi running Linux.
This was developed on Arch, but should run on any recent Linux distribution.

**Requires: Nginx, Python 2, Flask, Jinja 2, Flup, and about 11MB of RAM**

Sample Output:

![Home page](https://raw.github.com/willroberts/berrystats/master/resources/preview_home.png)

![System page](https://raw.github.com/willroberts/berrystats/master/resources/preview_system.png)

![About page](https://raw.github.com/willroberts/berrystats/master/resources/preview_about.png)

Installation
------------

**Install dependencies.**

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
