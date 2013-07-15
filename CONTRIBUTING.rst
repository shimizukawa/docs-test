Contributing to Ngx CC Docs
===========================

How To
------

To make a contribution to the documentation:

# Fork
# Edit
# Pull

If it seems like too many steps, it's because we broke it down to be as easy to
follow as possible. Once you follow the process one time, you should find it
incredibly easy to repeat. You only need to clone the repository one time. You
can submit future edits from the same fork you created initially.

Fork
~~~~

# Log into your github account (or create one)
# Go to https://github.com/ngx/docs
# Click the "Fork" button in the top right

Edit
~~~~

If you're not familiar, then navigate to any file and click the "Edit" button,
make your changes, and then click the "Commit Changes" button. Skip the rest of
this section.

If you're familiar with github, then you can simply work on the repository as
you would any other repository.

Example for advanced usage:

* After creating the fork
* git clone git@github.com:ngx/docs.git
* cd docs
* git remote set-url --push origin git@github.com:<YourGithubID>/docs.git

That's it. For the future, you can refresh your copy with 'git pull' and, make
changes, and then push the copy with 'git push' and follow the pull request. :)

Pull
~~~~

# Make sure these are the changes you're looking for
# Make sure you've reviewed the Edit Requirements below
# In the file browser (not file edit/view pages), click "Pull Request"
# Review the changes that will be made
# Click "Click here to create a pull request for this comparison"
# Fill in details and review your changes
# Click "Send pull request"
# Wait for our review

Edit Requirements
-----------------

The Ngx CC team strives for high quality documentation. We won't skimp on
quality just for the sake of having something out there. This means that we
have approved of every piece of content on this site. If it's here, you're free
to yell at us and punch us in the thigh if it's poor quality. We don't want to
be punched, so we require that all edits keep that from happening.

* Content must be useful
* Content must conform to the standards presented in the existing documentation
** One blank line between pretty much everything
** 80 character width (except code blocks)
** Look at http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
** Yes, that's generic but not hard to follow. If needed, we'll ad more here.
* Content must be published under the license found in LICENSE.txt
* All pages must be linked to in a sensible way

Edit Tips
---------

Tips to help with editing:

The ``:txt:`` Role
~~~~~~~~~~~~~~~~~~

You can use ``:txt:\`http://\``` to force http:// to be rendered at text
instead of being transformed into a link. It strips formatting from any text
within.

The ``.. ngx::`` Directive
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to create an Ngx code block, then:

    .. ngx::

        server {
            server_name domain.tld;
            # [...]
        }

If you want to create a "bad" example of the code block, then use the warn flag:

    .. ngx:: warn

        server {
            server_name example.com;
            # [...]
        }

This will cause the code block to be rendered with a red background.

Syntax Highlighting
~~~~~~~~~~~~~~~~~~~

Any code block ``.. code-block::`` or Ngx block ``.. ngx::`` must have correct
syntax inside of the block. Not doing so will cause the code to either not
render or render incorrectly.

Immediate Rebuild
~~~~~~~~~~~~~~~~~

As soon as an edit is pulled into the main branch, the documentation is
rebuilt. Please keep this in mind when submitting pull requests. Don't make
iterative pull requests for the same document. Keep them in your own repo
until you're ready to release your knowledge into the wild.

Licensing
~~~~~~~~~

The license applied to this entire repository is found in LICENSE.txt. If you
are unable to make your contribution under this license, then we won't be able
to accept it. You are responsible for ensuring that the content can be
published with this license.
