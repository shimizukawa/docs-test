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

BAD::

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

GOOD::

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

BAD::

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

GOOD::

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

There is a little page about using if statements. It's called IfIsEvil and you
really should check it out. Let's take a look at a few uses of if that are bad.

.. seealso:: :doc:`If Is Evil </topics/depth/ifisevil>`

Server Name (If)
----------------

BAD::

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
just the plain domain.com this if directive is **always** evaluated. Since
you're requesting nginx to check for the Host header for **every request**.
It's extremely inefficient. You should avoid it. Instead use two server
directives like the example below. 

GOOD::

    server {
        server_name www.domain.com;
        return 301 $scheme://domain.com$request_uri;
    }
    server {
          server_name domain.com;
          [...]
    }

Besides making the configuration file easier to read. This approach decreases
nginx processing requirements. We got rid of the spurious if. We're also using
$scheme which doesn't hardcodes the URI scheme you're using, be it http or
https.

Check (If) File Exists
----------------------

Using if to ensure a file exists is horrible. It's mean. If you have any recent
version of Nginx you should look at try_files which just made life much easier.

BAD::

    server {
        root /var/www/domain.com;
        location / {
            if (!-f $request_filename) {
                break;
            }
        }
    }

GOOD::

    server {
        root /var/www/domain.com;
        location / {
            try_files $uri $uri/ /index.html;
        }
    }

What we changed is that we try to see if $uri exists without requiring an if.
Using try_files mean that you can test a sequence. If $uri doesn't exist, try
$uri/, if that doesn't exist try a fallback location.

In this case it will see if the $uri file exists. If it does then serve it. If
it doesn't then tests if that directory exists. If not, then it will proceed to
serve index.html which you make sure exists. It's loaded but oh so simple. This
is another instance you can completely eliminate If.

Front Controller Pattern Web Apps
---------------------------------

"Front Controller Pattern" designs are popular and used on the many of the most
popular PHP software packages. A lot of examples are more complex than they need
to be. To get Drupal, Joomla, etc. to work, just use this::

    try_files $uri $uri/ /index.php?q=$uri&$args;

Note - the parameter names are different based on the package you're using. For
example:

* "q" is the parameter used by Drupal, Joomla, WordPress 
* "page" is used by CMS Made Simple

Some software doesn't even need the query string, and can read from REQUEST_URI
(WordPress supports this, for example)::

    try_files $uri $uri/ /index.php;

Of course, your mileage may vary and you may need more complex things based on
your needs, but for a basic sites, these will work perfectly. You should always
start simple and build from there.

You can also decide to skip the directory check and remove "$uri/" from it as
well, if you don't care about checking for the existence of directories.

Passing Uncontrolled Requests to PHP
------------------------------------

Many example Nginx configurations for PHP on the web advocate passing every URI
ending in .php to the PHP interpreter. Note that this presents a serious
security issue on most PHP setups as it may allow arbitrary code execution by
third parties.

The problem section usually looks like this::

    location ~* \.php$ {
        fastcgi_pass backend;
        [...]
    }

Here, every request ending in .php will be passed to the FastCGI backend. The
issue with this is that the default PHP configuration tries to guess which file
you want to execute if the full path does not lead to an actual file on the
filesystem.

For instance, if a request is made for `/forum/avatar/1232.jpg/file.php` which
does not exist but if `/forum/avatar/1232.jpg` does, the PHP interpreter will
process `/forum/avatar/1232.jpg` instead. If this contains embedded PHP code,
this code will be executed accordingly.

Options for avoiding this are:

* Set cgi.fix_pathinfo=0 in php.ini. This causes the PHP interpreter to only
  try the literal path given and to stop processing if the file is not found.
* Ensure that Nginx only passes specific PHP files for execution::

    location ~* (file_a|file_b|file_c)\.php$ {
        fastcgi_pass backend;
        [...]
    }

* Specifically disable the execution of PHP files in any directory containing
  user uploads::

    location /uploaddir {
        location ~ \.php$ {return 403;}
        [...]
    }

* Use the `try_files` directive to filter out the problem condition::

    location ~* \.php$ {
        try_files $uri =404;
        fastcgi_pass backend;
        [...]
    }

* Use a nested location to filter out the problem condition::

    location ~* \.php$ {
        location ~ \..*/.*\.php$ {return 404;}
        fastcgi_pass backend;
        [...]
    }

FastCGI Path in Script Filename
-------------------------------

So many guides out there like to rely on absolute paths to get to your
information. This is commonly seen in PHP blocks. When you install Nginx from a
repository you'll usually wind up being able to toss "include fastcgi_params;"
in your config. This is a file located in your Nginx root directory which is
usually around /etc/nginx/.

GOOD::

    fastcgi_param  SCRIPT_FILENAME    $document_root$fastcgi_script_name;

BAD::

    fastcgi_param  SCRIPT_FILENAME    /var/www/yoursite.com/$fastcgi_script_name;

Where is $document_root set? It's set by the root directive that should be in
your server block. Is your root directive not there? See the first pitfall.

Taxing Rewrites
---------------

Don't feel bad here, it's easy to get confused with regular expressions. In
fact, it's so easy to do that we should make an effort to keep them neat and
clean. Quite simply, don't add cruft.

BAD::

    rewrite ^/(.*)$ http://domain.com/$1 permanent;

GOOD::

    rewrite ^ http://domain.com$request_uri? permanent;

BETTER::

    return 301 http://domain.com$request_uri;

Look at the above. Then back here. Then up, and back here. OK. The first rewrite
captures the full URI minus the first slash. By using the built-in variable
$request_uri we can effectively avoid doing any capturing or matching at all.

Rewrite Missing http://
-----------------------

Very simply, rewrites are relative unless you tell nginx that they're not.
Making a rewrite absolute is simple. Add a scheme.

BAD::

    rewrite ^ domain.com permanent;

GOOD::

    rewrite ^ http://domain.com permanent;

In the above you will see that all we did was add "http://" to the rewrite. It's
simple, easy, and effective.

Proxy Everything
----------------

BAD::

    server {
        server_name _;
        root /var/www/site;
        location / {
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_pass unix:/tmp/phpcgi.socket;
        }
    }

Yucky. In this instance, you pass EVERYTHING to PHP. Why? Apache might do this,
you don't need to. Let me put it this way... The try_files directive exists for
an amazing reason. It tries files in a specific order. This means that Nginx can
first try to server the static content. If it can't, then it moves on. This
means PHP doesn't get involved at all. MUCH faster. Especially if you're serving
a 1MB image over PHP a few thousand times versus serving it directly. Let's take
a look at how to do that.

GOOD::

    server {
        server_name _;
        root /var/www/site;
        location / {
            try_files $uri $uri/ @proxy;
        }
        location @proxy {
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_pass unix:/tmp/phpcgi.socket;
        }
    }

Also GOOD::

    server {
        server_name _;
        root /var/www/site;
        location / {
            try_files $uri $uri/ /index.php;
        }
        location ~ \.php$ {
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_pass unix:/tmp/phpcgi.socket;
        }
    }

It's easy, right? You see if the requested URI exists and can be served by
Nginx. If not, is it a directory that can be served. If not, then you pass it to
your proxy. Only when Nginx can't serve that requested URI directly does your
proxy overhead get involved.

Now.. consider how much of your requests are static content, such as images,
css, javascript, etc. That's probably a lot of overhead you just saved.

Config Changes Not Reflected
----------------------------

Browser cache. Your configuration may be perfect but you'll sit there and beat
your head against a cement wall for a month. What's wrong is your browser cache.
When you download something, your browser stores it. It also stores how that
file was served. If you are playing with a types{} block you'll encounter this.

The fix:

* In Firefox press Ctrl+Shift+Delete, check Cache, click Clear Now. In
  any other browser just ask your favorite search engine. Do this after every
  change (unless you know it's not needed) and you'll save yourself a lot of
  headaches.
* Use curl.

VirtualBox
----------

If this does not work, and you're running nginx on a virtual machine in
VirtualBox, it may be sendfile() that is causing the trouble. Simply comment out
the sendfile directive or set it to "off". The directive is most likely found in
your nginx.conf file.::

    sendfile off;

Missing (disappearing) HTTP Headers
-----------------------------------

If you do not explicitly set `underscores_in_headers on`, nginx will silently
drop HTTP headers with underscores (which are perfectly valid according to the
HTTP standard). This is done in order to prevent ambiguities when mapping
headers to CGI variables as both dashes and underscores are mapped to
underscores during that process.

Chmod 777
---------

NEVER use 777. I't might be one nifty number, but even in testing it's a sign of
having no clue what you're doing. Look at the permissions in the whole path and
think through what's going on.

To easily display all the permissions on a path, you can use::

    namei -om /path/to/check
