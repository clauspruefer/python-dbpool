.. api

=============
API Reference
=============

Complete API documentation for pgdbpool classes and functions.

pgdbpool Module
===============

Core Classes
------------

.. automodule:: pgdbpool.pool
   :members: Connection, Handler, Query
   :special-members: __init__, __enter__, __exit__
   :exclude-members: __weakref__
   :show-inheritance:

Utility Functions
-----------------

.. automodule:: pgdbpool.pool
   :members: conn_iter
   :exclude-members: __weakref__

Exception Classes
-----------------

.. automodule:: pgdbpool.pool
   :members: DBConnectionError, DBQueryError, DBOfflineError, UnconfiguredGroupError
   :exclude-members: __weakref__
   :show-inheritance:

Class Method Reference
======================

Connection Class Methods
-------------------------

The Connection class provides static methods for pool management:

- **init(config)**: Initialize connection pool with configuration
- **get_threading_model()**: Return current threading model ('threaded' or 'non-threaded')
- **get_max_pool_size(group)**: Get maximum connections for a group
- **get_next_connection(group)**: Get next available connection from group
- **connect(connection)**: Establish database connection
- **reconnect(connection)**: Reconnect failed database connection
- **check_db(connection)**: Verify database connection health

Handler Context Manager
-----------------------

The Handler class provides a context manager for database operations:

- **__init__(group)**: Initialize handler for connection group
- **__enter__()**: Enter context, acquire connection
- **__exit__()**: Exit context, release connection
- **query(statement, params=None)**: Execute SQL query
- **query_prepared(params)**: Execute prepared statement  
- **commit()**: Commit transaction (for autocommit=False groups)

Query Static Methods
--------------------

The Query class provides static methods for SQL execution:

- **execute(connection, sql_statement, sql_params=None)**: Execute SQL statement
- **execute_prepared(connection, sql_params)**: Execute prepared statement
