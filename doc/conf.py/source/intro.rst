.. intro

==========================
Intro / Module Description
==========================

The **pgdbpool** Python Module is a lightweight PostgreSQL Database Connection Pool and Load Balancer primarily designed for Web and Application Servers.

1. Basic Install
================

.. code-block:: bash

    pip3 install pgdbpool

2. Dependencies
===============

**psycopg2** PostgreSQL Python Module is required. Preferable installation with OS Package Manager.

.. code-block:: bash

    # install psycopg2
    apt-get install python3-psycopg2

3. Build Dependencies
=====================

On current Debian 12 / Ubuntu 22.04+ / Ubuntu 24.04+ install the following additional packages for documentation rendering and testing:

.. code-block:: bash

    # install base packages
    apt-get install python3-pip python3-sphinx python3-sphinx-rtd-theme

    # install pytest for running unit and integration tests
    apt-get install python3-pytest python3-pytest-pep8

4. Tests
========

To run all tests (unit and integration) after pip package installation.

.. code-block:: bash

    # run pytest
    cd ./ && pytest

5. Current Features
===================

- **Multi-Database Support**: Connection pooling with multiple database endpoints for load balancing
- **Threading Models**: Support for both threaded and non-threaded environments
- **Connection Pooling**: Efficient connection pooling in Web-Server environments
- **Automatic Reconnection**: Automatic database reconnection on connection failures  
- **PostgreSQL Prepared Queries**: Support for prepared SQL statements
- **Transaction Control**: Manual commit() procedure for non-autocommit connections

6. Architecture Benefits
========================

- **Scalability**: Distributes connections across multiple database nodes
- **Reliability**: Automatic failover and reconnection capabilities
- **Performance**: Optimized connection reuse and reduced overhead
- **Flexibility**: Configurable for different deployment scenarios
