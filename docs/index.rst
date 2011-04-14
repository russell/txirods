.. txiRODS documentation master file, created by
   sphinx-quickstart on Tue Feb  2 11:23:52 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to txiRODS's documentation!
===================================

txIRODS is an implementation of the IRODS binary protocol using python
and the asynchronous networking tool kit Twisted. The project started
as a means of providing a JSON interface to iRODS for use with web
application that run within stand alone python servers like Plone,
Pylons and CherryPy. The primary reason is that these multiuser
systems requred individual user logins which wasn't possible with the
PyRods C wrapper due to limitations and instabilities with the client
libraries.


Contents:

.. toctree::
   :maxdepth: 2

   clients
   supported

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

