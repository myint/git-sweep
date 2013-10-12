git-sweep
=========

.. image:: https://travis-ci.org/myint/git-sweep.png?branch=master
   :target: https://travis-ci.org/myint/git-sweep
   :alt: Build status

A command-line tool that helps you clean up Git branches that have been merged
into master.

The problem
-----------

Your ``master`` branch is typically where all your code lands. All features
branches are meant to be short-lived and merged into ``master`` once they are
completed.

As time marches on, you can build up **a long list of branches that are no
longer needed**. They've been merged into ``master``, what do we do with them
now?

The answer
----------

Using ``git-sweep`` you can **safely remove remote branches that have been
merged into master**.

To install it run:

::

    pip install git-sweep

Try it for yourself (safely)
----------------------------

To see a list of branches that git-sweep detects are merged into your master branch:

You need to have your Git repository as your current working directory.

::

    $ cd myrepo

The ``--dry-run`` option doesn't make any changes to your repo.

::

    $ git sweep --dry-run
    Fetching from the remote
    These branches have been merged into master:

      branch1
      branch2
      branch3
      branch4
      branch5

    To delete them, run again without --dry-run

If you are happy with the list, you can run the command that deletes these
branches from the remote:

::

    $ git sweep
    Fetching from the remote
    These branches have been merged into master:

      branch1
      branch2
      branch3
      branch4
      branch5

    Delete these branches? (y/n) y
      deleting branch1 (done)
      deleting branch2 (done)
      deleting branch3 (done)
      deleting branch4 (done)
      deleting branch5 (done)

    All done!

    Tell everyone to run `git fetch --prune` to sync with this remote.
    (you don't have to, yours is synced)

*Note: this can take a little time, it's talking over the tubes to the remote.*

You can also give it a different name for your remote and master branches.

::

    $ git sweep --dry-run --master=develop --origin=github
    ...

Tell it to skip the ``git fetch`` that it does by default.

::

    $ git sweep --dry-run --nofetch
    These branches have been merged into master:

      branch1

    To delete them, run again without --dry-run

Make it skip certain branches.

::

    $ git sweep --dry-run --skip=develop
    Fetching from the remote
    These branches have been merged into master:

      important-upgrade
      upgrade-libs
      derp-removal

    To delete them, run again without --dry-run

Once git-sweep finds the branches, you'll be asked to confirm that you wish to
delete them.

::

    Delete these branches? (y/n)

You can use the ``--force`` option to bypass this and start deleting
immediately.

::

    $ git sweep --skip=develop --force
    Fetching from the remote
    These branches have been merged into master:

      important-upgrade
      upgrade-libs
      derp-removal

      deleting important-upgrade (done)
      deleting upgrade-libs (done)
      deleting derp-removal (done)

    All done!

    Tell everyone to run `git fetch --prune` to sync with this remote.
    (you don't have to, yours is synced)

Development
-----------

We also use Tox_. It will run the tests for Python 2.6 and 2.7.

::

    $ ./bin/tox

Requirements
------------

* Git >= 1.7
* Python >= 2.6

License
-------

Friendly neighborhood MIT license.

.. _Tox: http://pypi.python.org/pypi/tox
