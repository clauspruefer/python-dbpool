.. intro

==========================
Intro / Module Description
==========================

The **pgdbpool** Python Module is a tiny PostgreSQL Database Connection De-Multiplexer primarily scoped for Web- / Application Server.

Dependencies
============

**psycopg2** PostgreSQL Python Module is required. Do installation preferable with OS Package Manager.

.. code-block:: bash

    # install psycopg2
    apt-get install python3-psycopg2

On current Debian 12 / Ubuntu 22.04.3, 24.04.1 install the following additional packages (Documentation Rendering & Testing).

.. code-block:: bash

    # install packages
    apt-get install python3-pip python3-sphinx python3-sphinx-rtd-theme

    # install pytest to run integration and unit tests
    apt-get install python3-pytest python3-pytest-pep8

Current Features
================

- Connection Pooling in (threaded) Web-Server Environment (Single Destination DB-Node)
- Automatic DB Reconnection

Feature Requests
================
