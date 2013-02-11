berrystats
==========

berrystats is a tiny Flask/Jinja2 web app to report various stats about a Raspberry Pi running Linux.
This was developed on Arch, but should run on any recent Linux distribution.

**Requires: Nginx, Python 2, Flask, Jinja 2, Flup, and about 11MB of RAM**

Home page (now shows kernel version as well):

![Home page](https://raw.github.com/willroberts/berrystats/master/resources/preview_home.png)

System page

![System page](https://raw.github.com/willroberts/berrystats/master/resources/preview_system.png)

About page

![About page](https://raw.github.com/willroberts/berrystats/master/resources/preview_about.png)

Installation
------------

**Install dependencies:**

Arch:

    $ sudo pacman -S nginx
    $ sudo pacman -S python2
    $ sudo pacman -S python2-distribute
    $ sudo easy_install-2.7 pip
    $ sudo pip install flask # also installs jinja2
    $ sudo pip install flup

Debian:

    $ sudo apt-get install nginx
    $ sudo apt-get install python
    $ sudo apt-get install python-setuptools
    $ sudo easy_install pip
    $ sudo pip install flask # also installs jinja2
    $ sudo pip install flup

**Get the code:**

    $ git clone https://github.com/willroberts/berrystats.git

**Manually include the options from resources/nginx.conf in your /etc/nginx/nginx.conf.**

**Enable and start Nginx:**

Arch:

    $ sudo systemctl enable nginx.service
    $ sudo systemctl start nginx.service

Debian:

    $ sudo update-rc.d nginx enable
    $ sudo /etc/init.d/nginx start

**Install the web application to /srv/http**

    $ sudo mv berrystats /srv/http/berrystats

**Run the web application:**

Arch:

    $ sudo -u http python2 /srv/http/berrystats/start-server.py

Debian:

    $ sudo -u www-data python /srv/http/berrystats/start-server.py

**Warning: Never run web apps as the root user!** For best results, run the web app as the same user as Nginx (usually "http" or "www-data").
