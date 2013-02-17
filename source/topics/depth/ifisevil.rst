If Is Evil
==========

Directive if has problems when used in location context, in some cases it
doesn't do what you expect but something completely different instead. In some
cases it even segfaults. It's generally a good idea to avoid it if possible.

The only 100% safe things which may be done inside if in location context are:

* return [...];
* rewrite [...];

Anything else may possibly cause unpredictable behaviour, including potential
SIGSEGV.

It is important to note that the behaviour of if is not inconsistent, given two
identical requests it will not randomly fail on one and work on the other, with
proper testing and understanding ifs can be used. The advice to use other
directives where available still very much apply, though.

There are cases where you simply cannot avoid using an if, for example if you
need to test a variable which has no equivalent directive.::

    if ($request_method = POST ) {
        return 405;
    }
    if ($args ~ post=140){
        rewrite ^ http://example.com/ permanent;
    }

What to do instead
------------------

Use try_files if it suits your needs. Use the "return ..." or "rewrite ... last"
in other cases. In some cases it's also possible to move ifs to server level
(where it's safe as only other rewrite module directives are allowed within it).

E.g. the following may be used to safely change location which will be used to
process request::

    location / {
        error_page 418 = @other;
        recursive_error_pages on;

        if ($something) {
            return 418;
        }

        # some configuration
        [...]
    }

    location @other {
        # some other configuration
        [...]
    }

In some cases it may be good idea to use embedded scripting modules (embedded
perl, or various 3rd party modules) to do the scripting.

Examples
--------

Here are some examples which explain why if is evil. Don't try this at home. You
were warned.::

        # Here is collection of unexpectedly buggy configurations to show that
        # if inside location is evil.

        # only second header will be present in response
        # not really bug, just how it works

        location /only-one-if {
            set $true 1;

            if ($true) {
                add_header X-First 1;
            }

            if ($true) {
                add_header X-Second 2;
            }

            return 204;
        }

        # request will be sent to backend without uri changed
        # to '/' due to if

        location /proxy-pass-uri {
            proxy_pass http://127.0.0.1:8080/;

            set $true 1;

            if ($true) {
                # nothing
            }
        }

        # try_files wont work due to if

        location /if-try-files {
             try_files  /file  @fallback;

             set $true 1;

             if ($true) {
                 # nothing
             }
        }

        # nginx will SIGSEGV

        location /crash {

            set $true 1;

            if ($true) {
                # fastcgi_pass here
                fastcgi_pass  127.0.0.1:9000;
            }

            if ($true) {
                # no handler here
            }
        }

        # alias with captures isn't correcly inherited into implicit nested
        # location created by if

        location ~* ^/if-and-alias/(?<file>.*) {
            alias /tmp/$file;

            set $true 1;

            if ($true) {
                # nothing
            }
        }

Why This Behavior Isn't a Bug
-----------------------------

Directive "if" is part of rewrite module which evaluates instructions
imperatively. On the other hand, nginx configuration in general is declarative.
At some point due to users demand an attempt was made to enable some non-rewrite
directives inside "if", and this lead to situation we have now. It mostly works,
but... see above.

Looks like the only correct fix would be to disable non-rewrite directives
inside if completely. It would break many configuration out there though, so
wasn't done yet.
