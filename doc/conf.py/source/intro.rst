.. intro

==========================
Intro / Module Description
==========================

The **pgdbpool** Python Module is a tiny PostgreSQL Database Connection De-Multiplexer primarily scoped for Web- / Application Server.

Basic Install
=============

.. code-block:: bash

    # install psycopg2
    pip3 install pgdbpool

Dependencies
============

**psycopg2** PostgreSQL Python Module is required. Preferable installation with OS Package Manager.

.. code-block:: bash

    # install psycopg2
    apt-get install python3-psycopg2

Build Dependencies
==================

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
- PostgreSQL Prepared Queries Module

Feature Requests
================

- Connection Load Balancing to multiple (auto-scaled) Database Nodes
