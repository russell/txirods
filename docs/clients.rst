Command Line Clients
====================

Since i have no real purpose for this library i have begun extending
it using CLI clients as a usecase.

.. contents::

iinit
-----
.. program:: iinit

This application initialises the `~/.irods` directory with `.irodsEnv`
and `.irodsA` files. These files store state and authentication
information respectively.::

   Usage: iinit [options]...

.. option:: -h, --help

   show this help message and exit

.. option:: -v, --verbose

   Increase verbosity (specify multiple times for more)

.. option:: -V, --version

   print version number and exit


ipwd
----
.. program:: ipwd

Read the current directory from the `.irodsEnv` file and print it if
it exists.::

   Usage: ipwd [options]...

.. option:: -h, --help

   show this help message and exit

.. option:: -v, --verbose

   Increase verbosity (specify multiple times for more)

.. option:: -V, --version

   print version number and exit


imiscsrvinfo
------------
.. program:: imiscsrvinfo

Print miscellaneous server info such as whether it's rCAT enabled, the
release version, api version, the zone and the uptime.::

   Usage: imiscsrvinfo [options]...

.. option:: -h, --help

   show this help message and exit

.. option:: -v, --verbose

   Increase verbosity (specify multiple times for more)

.. option:: -V, --version

   print version number and exit


imkdir
------
.. program:: imkdir

Make a new directory if ones doesn't already exist.::

   Usage: imkdir [options] DIRECTORY...

.. option:: -h, --help

   show this help message and exit

.. option:: -v, --verbose

   Increase verbosity (specify multiple times for more)

.. option:: -V, --version

   print version number and exit


icd
---
.. program:: icd

Change into another directory if it exists. If no path is specified
the you will be changed into the users home directory as specified in
the `.irodsEnv` file.::

   Usage: icd [options] FILE...

.. option:: -h, --help

   show this help message and exit

.. option:: -v, --verbose

   Increase verbosity (specify multiple times for more)

.. option:: -V, --version

   print version number and exit


ils
---
.. program:: ils

List the contest of the specified collection or the current one if no
path is specified.::

   Usage: ils [options] [file]...

.. option:: -h, --help

   show this help message and exit

.. option:: -v, --verbose

   Increase verbosity (specify multiple times for more)

.. option:: -V, --version

   print version number and exit


iput
----
.. program:: iput

Upload a file or directory to the iRODS server.::

   Usage: iput [options] SOURCE...
     or:  iput [options] SOURCE... DIRECTORY
     or:  iput [options] SOURCE DEST

.. option:: -r, --recursive

   copy directories recursively

.. option:: -h, --help

   show this help message and exit

.. option:: -v, --verbose

   Increase verbosity (specify multiple times for more)

.. option:: -V, --version

   print version number and exit


iget
----
.. program:: iget

Download a file or directory from the server.::

   Usage: iget [options] SOURCE...
     or:  iget [options] SOURCE... DIRECTORY
     or:  iget [options] SOURCE DEST

.. option:: -h, --help

   show this help message and exit

.. option:: -v, --verbose

   Increase verbosity (specify multiple times for more)

.. option:: -V, --version

   print version number and exit


irm
---
.. program:: irm

Remove files or directories from the server.::

   Usage: irm [options] FILE...

.. option:: -r, --recursive

   copy directories recursively

.. option:: -f, --force

   force deletion of files, skipping trash

.. option:: -h, --help

   show this help message and exit

.. option:: -v, --verbose

   Increase verbosity (specify multiple times for more)

.. option:: -V, --version

   print version number and exit


irmdir
------
.. program:: irmdir

Remove an empty directory from the server.::

   Usage: irmdir [options] DIRECTORY...

.. option:: -h, --help

   show this help message and exit

.. option:: -v, --verbose

   Increase verbosity (specify multiple times for more)

.. option:: -V, --version

   print version number and exit
