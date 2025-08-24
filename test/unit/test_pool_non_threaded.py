import time
import pytest
import logging
import psycopg2
import threading

from pgdbpool import pool

logger = logging.getLogger(__name__)


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
        'type': 'non-threaded',
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
        'type': 'non-threaded',
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


class TestConnectionMultiDB:

    def test_connection_setup(self, monkeypatch, connection_config_multi, caplog):

        caplog.set_level(logging.DEBUG)

        monkeypatch.setattr(psycopg2, 'connect', patched_connect)

        pool.Connection.init(connection_config_multi)

        assert "'host': '127.0.0.1'" in caplog.messages[0]
        assert "'host': '127.0.0.2'" in caplog.messages[1]

    def test_connection_iteration(self, monkeypatch, connection_config_multi, caplog):

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

        with pool.Handler('group1') as db:
            db.query('sql5')

        with pool.Handler('group1') as db:
            db.query('sql6')

        assert "group:group1 id:0" in caplog.messages[4]
        assert "group:group1 id:1" in caplog.messages[12]
        assert "group:group1 id:0" in caplog.messages[20]
        assert "group:group1 id:1" in caplog.messages[28]
        assert "group:group1 id:0" in caplog.messages[36]
        assert "group:group1 id:1" in caplog.messages[44]


class TestConnectionSingleDB:

    def test_connection_conn_count(self, monkeypatch, connection_config_single, caplog):

        caplog.set_level(logging.DEBUG)

        monkeypatch.setattr(psycopg2, 'connect', patched_connect)

        pool.Connection.init(connection_config_single)

        assert "'host': '127.0.0.1'" in caplog.messages[0]
        assert "'host': '127.0.0.1'" in caplog.messages[1]
        assert "'host': '127.0.0.1'" in caplog.messages[2]
        assert "'host': '127.0.0.1'" in caplog.messages[3]
        assert "'host': '127.0.0.1'" in caplog.messages[4]

        with pool.Handler('group1') as db:
            db.query('sql1')

        with pool.Handler('group1') as db:
            db.query('sql2')

        with pool.Handler('group1') as db:
            db.query('sql3')

        with pool.Handler('group1') as db:
            db.query('sql4')

        with pool.Handler('group1') as db:
            db.query('sql5')

        with pool.Handler('group1') as db:
            db.query('sql6')

        with pool.Handler('group1') as db:
            db.query('sql7')

        with pool.Handler('group1') as db:
            db.query('sql8')

        with pool.Handler('group1') as db:
            db.query('sql9')

        with pool.Handler('group1') as db:
            db.query('sql10')

        with pool.Handler('group1') as db:
            db.query('sql11')

        assert "group:group1 id:0" in caplog.messages[7]
        assert "group:group1 id:1" in caplog.messages[15]
        assert "group:group1 id:2" in caplog.messages[23]
        assert "group:group1 id:3" in caplog.messages[31]
        assert "group:group1 id:4" in caplog.messages[39]

        assert "group:group1 id:0" in caplog.messages[47]
        assert "group:group1 id:1" in caplog.messages[55]
        assert "group:group1 id:2" in caplog.messages[63]
        assert "group:group1 id:3" in caplog.messages[71]
        assert "group:group1 id:4" in caplog.messages[79]

        assert "group:group1 id:0" in caplog.messages[87]
