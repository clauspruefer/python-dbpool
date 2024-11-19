.. config

=============
Configuration
=============

Basic configuration explanation. See :ref:`examples-label` subsection for more detailed information
(working Apache WSGI Script).

Root Dict 
=========

The root dictionary must contain keys `db` for **Database Connection Config** (see ) and `groups`
for **Group Config** (see ) .

.. code-block:: python

    config = {
        'db': {
        },
        'groups': {
        }
    }

Database Connection 
===================

The Database Connection Configuration JSON schema. It consists of base configuration properties
and the "groups" dictionary to specify (multiple) group data.

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


Database Connection Properties
==============================

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
     - Database Auth Usern
   * - pass
     - string
     - 
     - 
     - 
     - Database Auth Pass
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

Group Configuration
===================

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


Group Configuration Properties
==============================

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

Internal Default (Values)
=========================

The following schema represensts the internal Python structures. Some values (e.g. groups.id.connections)
are used to internally store values and should not be overwritten.

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

Multi Group Example
===================

To specify a) autocommit and b) non autocommit database connection to the same endpoint.

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
