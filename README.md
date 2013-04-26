berrystats
==========

berrystats is a tiny Flask/Jinja2 web app to report various stats about a Raspberry Pi running Linux.
This was developed on Arch, but should run on any recent Linux distribution.

**Requires: Nginx, Python 2, Flask, Jinja 2, Flup, and about 10MB of RAM**

Screenshots
-----------

Home tab::

![home_page](http://i.imgur.com/kbqRfEj.png)

System tab:

![home_page](http://i.imgur.com/6zz0mty.png)

About tab:

![home_page](http://i.imgur.com/OQircAv.png)

Installation
------------

**Install dependencies:**

Arch:

    $ sudo pacman -S git nginx python2 python2-distribute
    $ sudo easy_install-2.7 pip
    $ sudo pip install flask flup

Debian:

    $ sudo apt-get install git nginx python python-setuptools
    $ sudo easy_install pip
    $ sudo pip install flask flup

**Get the code:**

    $ git clone https://github.com/willroberts/berrystats.git

**Manually include the options below in your /etc/nginx/nginx.conf:**

    http {
        limit_req_zone $binary_remote_addr zone=one:10m rate=4r/s;
        server {
            listen 80;
            server_name your-domain.net;
            location / {
                proxy_pass http://localhost:8000;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header User-Agent $http_user_agent;
                limit_req zone=one burst=4;
            }
        }
        server {
            listen 127.0.0.1:8000;
            root /srv/http/berrystats/;
            server_name localhost;
            access_log /var/log/nginx/flask_access.log;
            error_log /var/log/nginx/flask_error.log;
            location / { try_files $uri @app; }
            location @app {
                include fastcgi_params;
                fastcgi_param PATH_INFO $fastcgi_script_name;
                fastcgi_param SCRIPT_NAME "";
                fastcgi_pass unix:/srv/http/berrystats/data/flup.sock;
            }
        }
    }

**Enable and start Nginx:**

Arch:

    $ sudo systemctl enable nginx.service
    $ sudo systemctl start nginx.service

Debian:

    $ sudo update-rc.d nginx enable
    $ sudo /etc/init.d/nginx start

**Install the web application to /srv/http:**

    $ sudo mv berrystats /srv/http/berrystats

**Run the web application:**

Arch:

    $ sudo -u http python2 /srv/http/berrystats/start-server.py

Debian:

    $ sudo -u www-data python /srv/http/berrystats/start-server.py

**Warning: Never run web apps as the root user!**

For best results, run the web app as the same user as Nginx (usually "http" or "www-data").

Logging
-------
The latest release now contains support for request and error logging. You can find these logs in the logs/ directory.
