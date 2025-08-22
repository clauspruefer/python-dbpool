import time
import pytest
import logging
import psycopg2
import threading

from pgdbpool import pool


class DBCursorPatch(object):

    def __init__(self):
        pass

    def callproc(self, statement):
        return statement

    def execute(self, statement, params=None):
        return statement

    def fetchone(self):
        return { 'column1': 'value1' }


class DBPatch(object):

    def __init__(self):
        pass

    def query(self, statement):
        return statement

    def commit(self):
        pass

    def cursor(self, cursor_factory):
        return DBCursorPatch()


def patched_connect(*, dbname, user, host, password, sslmode, connect_timeout):
    return DBPatch()


@pytest.fixture
def connection_config():
    config = {
        'db': {
            'host': '127.0.0.1',
            'name': 'testdb',
            'user': 'dbuser',
            'pass': 'dbpass',
            'ssl': 'require',
            'connect_timeout': 30,
            'connection_retry_sleep': 1,
            'query_timeout': 30,
            'session_tmp_buffer': 128
        },
        'groups': {
            'group1': {
                'connection_count': 5,
                'autocommit': False,
            }
        }
    }
    return config


class TestFunctional:

    def test_handler_existing_group(self, monkeypatch, connection_config):

        monkeypatch.setattr(psycopg2, 'connect', patched_connect)

        pool.Connection.init(connection_config)

        with pool.Handler('group1') as db:
            db.query('SELECT * FROM test')

    def test_handler_non_existing_group(self, monkeypatch, connection_config):

        monkeypatch.setattr(psycopg2, 'connect', patched_connect)

        pool.Connection.init(connection_config)

        with pytest.raises(pool.UnconfiguredGroupError):

            with pool.Handler('group2') as db:
                db.query('SELECT * FROM test')

    def test_handler_connection_rotating(self, monkeypatch, connection_config):

        monkeypatch.setattr(psycopg2, 'connect', patched_connect)

        pool.Connection.init(connection_config)

        db_comp1 = None
        db_comp2 = None
        db_comp3 = None
        db_comp4 = None
        db_comp5 = None
        db_comp6 = None
        db_comp7 = None
        db_comp8 = None
        db_comp9 = None
        db_comp10 = None

        with pool.Handler('group1') as db1:
            db1.query('SELECT * FROM test')
            db_comp1 = db1

        with pool.Handler('group1') as db2:
            db2.query('SELECT * FROM test')
            db_comp2 = db2

        with pool.Handler('group1') as db3:
            db3.query('SELECT * FROM test')
            db_comp3 = db3

        with pool.Handler('group1') as db4:
            db4.query('SELECT * FROM test')
            db_comp4 = db4

        with pool.Handler('group1') as db5:
            db5.query('SELECT * FROM test')
            db_comp5 = db5

        with pool.Handler('group1') as db6:
            db6.query('SELECT * FROM test')
            db_comp6 = db6

        with pool.Handler('group1') as db7:
            db7.query('SELECT * FROM test')
            db_comp7 = db7

        with pool.Handler('group1') as db8:
            db8.query('SELECT * FROM test')
            db_comp8 = db8

        with pool.Handler('group1') as db9:
            db9.query('SELECT * FROM test')
            db_comp9 = db9

        with pool.Handler('group1') as db10:
            db10.query('SELECT * FROM test')
            db_comp10 = db10

        assert db_comp1.conn_ref == db_comp6.conn_ref
        assert db_comp2.conn_ref == db_comp7.conn_ref
        assert db_comp3.conn_ref == db_comp8.conn_ref
        assert db_comp4.conn_ref == db_comp9.conn_ref
        assert db_comp5.conn_ref == db_comp10.conn_ref


class TestThreading:

    def test_threaded_wait_free_connection(self, monkeypatch, connection_config):

        class ThreadBlocking(threading.Thread):

            def __init__(self):
                super().__init__()

            def run(self):
                with pool.Handler('group1') as db:
                    db.query('SELECT * FROM test1')
                    time.sleep(3)

        class ThreadNonBlocking(threading.Thread):

            def __init__(self):
                super().__init__()

            def run(self):
                with pool.Handler('group1') as db:
                    db.query('SELECT * FROM test2')
                    time.sleep(0.5)

        monkeypatch.setattr(psycopg2, 'connect', patched_connect)

        pool.Connection.init(connection_config)

        t1 = ThreadBlocking()
        t2 = ThreadBlocking()
        t3 = ThreadBlocking()
        t4 = ThreadBlocking()
        t5 = ThreadBlocking()
        t6 = ThreadBlocking()
        t7 = ThreadBlocking()
        t8 = ThreadNonBlocking()
        t9 = ThreadNonBlocking()
        t10 = ThreadNonBlocking()
        t11 = ThreadNonBlocking()
        t12 = ThreadNonBlocking()

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()
        t9.start()
        t10.start()
        t11.start()
        t12.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        t10.join()
        t11.join()
        t12.join()
