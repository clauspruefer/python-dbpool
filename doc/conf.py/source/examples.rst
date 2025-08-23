.. examples

.. _examples-label:

========
Examples
========

Working examples for database configuration and web server integration with pgdbpool.

.. note::
   These examples assume a properly configured web server environment.

1. Single Database Configuration
=================================

Basic configuration for a single PostgreSQL database:

.. code-block:: python

    # file: DBConfig.py
    import os

    # database configuration
    DB_NAME = 'myapp_db'
    DB_USER = 'myapp_user'
    DB_HOST = 'localhost'
    DB_PASS = os.environ['PSQL_PASSWORD']

    config = {
        'type': 'threaded',  # threading model
        'db': {
            'host': DB_HOST,
            'name': DB_NAME,
            'user': DB_USER,
            'pass': DB_PASS,
            'ssl': 'prefer',  # use ssl when possible
            'connect_timeout': 30,
            'connection_retry_sleep': 1,
            'query_timeout': 30000,
            'session_tmp_buffer': 128
        },
        'groups': {
            'default': {
                'connection_count': 10,
                'autocommit': True
            },
            'transactions': {
                'connection_count': 5,
                'autocommit': False
            }
        }
    }

2. Apache WSGI Application
===========================

Example WSGI application using pgdbpool:

.. code-block:: python

    # file: app.py
    import DBConfig
    from pgdbpool import pool as dbpool

    # initialize connection pool
    dbpool.Connection.init(DBConfig.config)

    def application(environ, start_response):
        """WSGI application entry point."""
        
        if environ['REQUEST_METHOD'].upper() == 'GET':
            try:
                start_response('200 OK', [
                    ('Content-Type', 'application/json; charset=UTF-8')
                ])

                # simple query with autocommit
                sql = "SELECT id, name, email FROM users WHERE active = true"
                
                with dbpool.Handler('default') as db:
                    results = []
                    for row in db.query(sql):
                        results.append({
                            'id': row[0],
                            'name': row[1], 
                            'email': row[2]
                        })
                    
                import json
                yield json.dumps(results).encode('utf-8')
                
            except Exception as e:
                start_response('500 Internal Server Error', [
                    ('Content-Type', 'text/plain')
                ])
                yield b"Internal Server Error"

3. Multi-Database Load Balancing Configuration
===============================================

Configure multiple database endpoints for high availability:

.. code-block:: python

    # file: MultiDBConfig.py
    import os

    config = {
        'type': 'threaded',
        'db': [
            {
                'host': 'primary-db.example.com',
                'name': 'myapp',
                'user': 'appuser',
                'pass': os.environ['DB_PASSWORD'],
                'ssl': 'require',
                'connect_timeout': 30,
                'query_timeout': 120,
                'session_tmp_buffer': 256
            },
            {
                'host': 'replica-db.example.com', 
                'name': 'myapp',
                'user': 'appuser',
                'pass': os.environ['DB_PASSWORD'],
                'ssl': 'require',
                'connect_timeout': 30,
                'query_timeout': 120,
                'session_tmp_buffer': 256
            }
        ],
        'groups': {
            'read_pool': {
                'connection_count': 15,
                'autocommit': True
            },
            'write_pool': {
                'connection_count': 10,
                'autocommit': False
            }
        }
    }

4. Transaction Management Example
=================================

Example showing manual transaction control with commit():

.. code-block:: python

    from pgdbpool import pool as dbpool
    
    # initialize with multi-DB config
    dbpool.Connection.init(MultiDBConfig.config)
    
    def transfer_funds(from_account, to_account, amount):
        """Example transaction with manual commit."""
        
        try:
            with dbpool.Handler('write_pool') as db:
                # start transaction (autocommit=False for write_pool)
                
                # debit from source account
                db.query(
                    "UPDATE accounts SET balance = balance - %s WHERE id = %s",
                    (amount, from_account)
                )
                
                # credit to destination account  
                db.query(
                    "UPDATE accounts SET balance = balance + %s WHERE id = %s", 
                    (amount, to_account)
                )
                
                # log the transaction
                db.query(
                    "INSERT INTO transaction_log (from_id, to_id, amount) VALUES (%s, %s, %s)",
                    (from_account, to_account, amount)
                )
                
                # commit transaction
                db.commit()
                return True
                
        except Exception as e:
            # transaction will be automatically rolled back
            print(f"Transaction failed: {e}")
            return False

5. Non-Threaded Configuration
=============================

Configuration for process-based web servers (e.g., Gunicorn with workers):

.. code-block:: python

    # file: ProcessConfig.py
    config = {
        'type': 'non-threaded',  # removes locking overhead
        'db': {
            'host': 'localhost',
            'name': 'myapp',
            'user': 'appuser',
            'pass': os.environ['DB_PASSWORD'],
            'ssl': 'prefer'
        },
        'groups': {
            'worker_pool': {
                'connection_count': 5,  # fewer connections per process
                'autocommit': True
            }
        }
    }
