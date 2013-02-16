.. _contents:

.. _warning: Read all of this! ALL OF IT!

Pitfalls and Common Mistakes
============================

New and old users alike can run into a pitfall. Below we outline issues that we
see frequently as well as explain how to resolve those issues. In the #nginx IRC
channel on Freenode, we see these issues frequently.

This Guide Says
---------------

The most frequent issue we see happens when someone attempts to just copy and
paste a configuration snippet from some other guide. Not all guides out there
are wrong, but a scary number of them are. Even the Linode library has poor
quality information that some Nginx community members have futily attempted to
correct.

The Ngx CC Docs were created and reviewed by community members that work
directly with all types of Nginx users. This specific document exists only
because of the volume of common and recurring issues that community members see.

My Issue Isn't Listed
---------------------

You don't see something in here related to your specific issue. Maybe we didn't
point you here because of the exact issue you're experiencing. Don't skim this
page and assume you were sent here for no reason. You were sent here because
something you did wrong is listed here.

When it comes to supporting many users on many issues, community members don't
want to support broken configurations. Fix your configuration before asking for
help. Fix your configuration by reading through this. Don't just skim it.

Root inside Location Block
--------------------------

BAD:

    server {
        server_name www.domain.com;
          location / {
              root /var/www/nginx-default/;
              [...]
          }
          location /foo {
              root /var/www/nginx-default/;
              [...]
          }
          location /bar {
              root /var/www/nginx-default/;
              [...]
          }
    }

This works. Putting root inside of a location block will work and it's perfectly
valid. What's wrong is when you start adding location blocks. If you add a root
to every location block then a location block that isn't matched will have no
root. Let's look at a good configuration.

GOOD:

    server {
        server_name www.domain.tld;
        root /var/www/nginx-default/;
        location / {
            [...]
      }
      location /foo {
          [...]
      }
      location /bar {
          [...]
      }
    }

Multiple Index Directives
-------------------------

BAD:

    http {
        index index.php index.htm index.html;
        server {
            server_name www.domain.tld;
            location / {
                index index.php index.htm index.html;
                [...]
            }
        }
        server {
            server_name domain.tld;
            location / {
                index index.php index.htm index.html;
                [...]
            }
            location /foo {
                index index.php;
                [...]
            }
        }
    }

Why repeat so many lines when not needed. Simply use the "index" directive one
time. It only needs to occur in your http { } block and it will be inherited
below.

GOOD:

    http {
        index index.php index.htm index.html;
        server {
            server_name www.domain.com;
            location / {
                [...]
            }
        }
        server {
            server_name domain.com;
            location / {
                [...]
            }
            location /foo {
                [...]
            }
        }
    }

Using If
--------

BAD:

    server {
        server_name domain.tld *.domain.tld;
            if ($host ~* ^www\.(.+)) {
                set $raw_domain $1;
                rewrite ^/(.*)$ $raw_domain/$1 permanent;
            }
            [...]
        }
    }

There are actually three problems here. The first being the if. That's what we
care about now. Why is this bad? Did you read If is Evil? When nginx receives a
request no matter what is the subdomain being requested, be it www.domain.tld or
just the plain domain.com this if directive is always evaluated. Since you're
requesting nginx to check for the Host header for every request. It's extremely
inefficient. You should avoid it. Instead use two server directives like the
example below. 


