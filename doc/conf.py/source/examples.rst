.. examples

.. _examples-label:

========
Examples
========

The following example shows a working example for 1) Database Config 2) WSGI Python Script running on
Apache Web-Server.

.. note::
   This assumes a working Apache Python WSGI Config.

1. Database / Group Config
==========================

.. code-block:: python

    # File DBConfig.py
    import os

    DBName = 'db1'
    DBUser = 'db1'
    DBHost = 'mypostgres'
    DBPass = os.environ['PSQL_PWD']

    config1 = {
        'db': {
            'host': DBHost,
            'name': DBName,
            'user': DBUser,
            'pass': DBPass,
            'ssl': 'disable',
            'connect_timeout': 30,
            'connection_retry_sleep': 1,
            'query_timeout': 30000,
            'session_tmp_buffer': 128
        },
        'groups': {
            'db1': {
                'connection_count': 3,
                'autocommit': True,
            }
        }
    }

2. Apache WSGI Script
=====================

.. code-block:: python

    import DBConfig
    from dbpool import pool as dbpool

    dbpool.Connection.init(DBConfig.config1)

    def application(environ, start_response):

        if environ['REQUEST_METHOD'].upper() == 'POST':

            try:
                start_response('200 OK', [('Content-Type', 'application/json; charset=UTF-8')])

                sql = """SELECT col1, col2 FROM testtable1""";

                with dbpool.Handler('db1') as db:
                    for rec in db.query(sql):
                        yield rec
            except Exception as e:
                yield "500 Internal Server Error"
