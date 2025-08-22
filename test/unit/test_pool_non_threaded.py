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
def connection_config_single():
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
                'autocommit': False
            }
        }
    }
    return config

@pytest.fixture
def connection_config_multi():
    config = {
        'db':
        [
            {
                'host': '127.0.0.1',
                'name': 'testdb1',
                'user': 'dbuser',
                'pass': 'dbpass',
                'ssl': 'off',
                'connect_timeout': 10,
                'connection_retry_sleep': 0.05,
                'query_timeout': 10,
                'session_tmp_buffer': 256
            },
            {
                'host': '127.0.0.2',
                'name': 'testdb1',
                'user': 'dbuser',
                'pass': 'dbpass',
                'ssl': 'off',
                'connect_timeout': 10,
                'connection_retry_sleep': 0.05,
                'query_timeout': 10,
                'session_tmp_buffer': 256
            }
        ],
        'groups': {
            'group1': {
                'connection_count': 2,
                'autocommit': False
            }
        }
    }
    return config


class TestMultiDB:

    def test_base_iteration(self, monkeypatch, connection_config_multi, caplog):

        caplog.set_level(logging.DEBUG)

        monkeypatch.setattr(psycopg2, 'connect', patched_connect)

        pool.Connection.init(connection_config_multi)

        with pool.Handler('group1') as db:
            db.query('sql1')

        with pool.Handler('group1') as db:
            db.query('sql2')

        with pool.Handler('group1') as db:
            db.query('sql3')

        with pool.Handler('group1') as db:
            db.query('sql4')
