.. config

=============
Configuration
=============

Configuration guide for pgdbpool. See :ref:`examples-label` for detailed working examples (including Apache WSGI scripts).

1. Root Configuration Structure
===============================

The root configuration dictionary must contain:

- ``db``: Database connection configuration (dict or list of dicts for multi-DB support)
- ``groups``: Connection group configuration  
- ``type`` (optional): Threading model specification (``threaded`` or ``non-threaded``)

.. code-block:: python

    config = {
        'db': {
            # Single database configuration
        },
        # OR for multiple databases:
        # 'db': [
        #     { # Database 1 config },
        #     { # Database 2 config }
        # ],
        'groups': {
            # Connection groups
        },
        'type': 'threaded'  # optional, defaults to 'threaded'
    }

2. Database Connection Configuration
====================================

The database connection configuration supports both single and multiple database endpoints.

**Single Database Configuration:**

.. code-block:: python

    config = {
        'db': {
            'host': 'hostname',
            'name': 'dbname',
            'user': 'username',
            'pass': 'userpass',
            'ssl': False,
            'connect_timeout': 30,
            'connection_retry_sleep': 1,
            'query_timeout': 120,
            'session_tmp_buffer': 128
        }
    }

**Multiple Database Configuration (Load Balancing):**

.. code-block:: python

    config = {
        'db': [
            {
                'host': 'db1.example.com',
                'name': 'dbname',
                'user': 'username',
                'pass': 'userpass',
                'ssl': False,
                'connect_timeout': 30,
                'connection_retry_sleep': 1,
                'query_timeout': 120,
                'session_tmp_buffer': 128
            },
            {
                'host': 'db2.example.com',
                'name': 'dbname',
                'user': 'username',
                'pass': 'userpass',
                'ssl': False,
                'connect_timeout': 30,
                'connection_retry_sleep': 1,
                'query_timeout': 120,
                'session_tmp_buffer': 128
            }
        ]
    }


3. Threading Model Configuration
==================================

The threading model can be configured to optimize for different deployment scenarios:

.. code-block:: python

    config = {
        'type': 'threaded',  # or 'non-threaded'
        'db': { ... },
        'groups': { ... }
    }

**Threading Models:**

- ``threaded`` (default): Uses thread-safe connection handling with locks. Optimal for threaded web servers (Apache, Gunicorn with threads).
- ``non-threaded``: Removes locking overhead. Optimal for process-based servers (Gunicorn with workers) or single-threaded applications.

4. Database Connection Properties
=================================

.. list-table:: Database Connection Properties
   :widths: 15 10 10 10 10 30
   :header-rows: 1

   * - Property
     - Type
     - Unit
     - Opt
     - Def
     - Description
   * - host
     - string
     - 
     - 
     - 
     - Database Hostname
   * - name
     - string
     - 
     - 
     - 
     - Database Name
   * - user
     - string
     - 
     - 
     - 
     - Database Auth Username
   * - pass
     - string
     - 
     - 
     - 
     - Database Auth Password
   * - ssl
     - bool
     - 
     - x
     - False
     - Use SSL / TLS
   * - connect_timeout
     - int
     - Seconds
     - x
     - 30
     - Connect Timeout
   * - connection_retry_sleep
     - int
     - Seconds
     - x
     - 1
     - Sleep Between Connect Retry
   * - query_timeout
     - int
     - Seconds
     - x
     - 120
     - Query Timeout
   * - session_tmp_buffer
     - int
     - Kilobytes
     - x
     - 128
     - Session Buffer Memory

5. Group Configuration
======================

.. code-block:: python

    config = {
        'db': {
            ...
        },
        'groups': {
            'groupname': {
                'connection_count': 20,
                'autocommit': False
            }
        }


6. Group Configuration Properties
=================================

.. list-table:: Group Properties
   :widths: 15 10 10 10 10 30
   :header-rows: 1

   * - Property
     - Type
     - Unit
     - Opt
     - Def
     - Description
   * - connection_count
     - int
     - Quantity
     - 
     -
     - Connection Count
   * - autocommit
     - bool
     - 
     - x
     - True
     - Autocommit on / off

7. Internal Default Values
============================

The following schema represents the internal Python structures. Some values (e.g., ``groups.id.connections``) are used internally and should not be modified manually.

.. code-block:: python

    config = {
        'db': {
            'host': 'hostname',
            'name': 'database',
            'user': 'dbuser',
            'pass': 'dbpass',
            'ssl': False,
            'connect_timeout': 30,
            'connection_retry_sleep': 1,
            'query_timeout': 120,
            'session_tmp_buffer': 128
        },
        'groups': {
            'group1': {
                'connection_count': 20,
                'autocommit': False,
                'connections': [
                    (conn, status),
                ],
                'connection_iter': None
            }
        }
    }

8. Multi-Group Configuration Example
======================

Example configuration with separate groups for autocommit and non-autocommit connections to the same database endpoint:

.. code-block:: python

    config = {
        'db': {
            'host': 'db1.internal.domain',
            'name': 'db1',
            'user': 'dbuser',
            'pass': 'dbpass'
        },
        'groups': {
            'group1': {
                'connection_count': 50,
                'autocommit': True
            },
            'group2': {
                'connection_count': 30,
                'autocommit': False
            }
        }
    }

9. Multi-Database Load Balancing Example
=========================================

Configure multiple database endpoints for automatic load balancing and failover:

.. code-block:: python

    config = {
        'type': 'threaded',
        'db': [
            {
                'host': 'primary-db.example.com',
                'name': 'myapp',
                'user': 'appuser',
                'pass': 'securepassword',
                'ssl': 'require',
                'connect_timeout': 30,
                'query_timeout': 120
            },
            {
                'host': 'secondary-db.example.com',
                'name': 'myapp',
                'user': 'appuser', 
                'pass': 'securepassword',
                'ssl': 'require',
                'connect_timeout': 30,
                'query_timeout': 120
            }
        ],
        'groups': {
            'read_write': {
                'connection_count': 20,
                'autocommit': True
            },
            'transactions': {
                'connection_count': 10,
                'autocommit': False
            }
        }
    }
