.. pgdbpool documentation master file, created by
   sphinx-quickstart on Tue Feb  6 08:37:14 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pgdbpool Documentation
======================

PostgreSQL Database Connection Pool and Load Balancer

pgdbpool is a lightweight Python module that provides efficient connection pooling and load balancing for PostgreSQL databases, designed for web and application servers.

**Key Features:**

- Multi-database endpoint support with automatic load balancing
- Both threaded and non-threaded deployment models
- Automatic reconnection and failover capabilities
- Transaction control with manual commit support

**Quick Start:**

.. code-block:: python

    from pgdbpool import pool as dbpool
    
    config = {
        'db':
        [
         {'host': 'mypostgres-1', 'name': 'mydb', 'user': 'user', 'pass': 'pass'},
         {'host': 'mypostgres-2', 'name': 'mydb', 'user': 'user', 'pass': 'pass'}
        ],
        'groups': {'default': {'connection_count': 2, 'autocommit': True}}
    }
    
    dbpool.Connection.init(config)
    
    with dbpool.Handler('default') as db:
        results = db.query("SELECT * FROM users")

Documentation Contents
======================

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   intro
   build

.. toctree::
   :maxdepth: 2
   :caption: Configuration & Usage

   config
   examples

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics

   design
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
