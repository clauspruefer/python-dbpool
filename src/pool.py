import os
import time
import json
import copy
import logging
import threading

import psycopg2

from psycopg2 import extras


class DBConnectionError(Exception):
    """
    Exception Class, raised on Database Connection Error.
    """
    pass


class DBQueryError(Exception):
    """
    Exception Class, raised on Database Query Error.
    """
    pass


class DBOfflineError(Exception):
    """
    Exception Class, raised if Database is not pingable.
    """
    pass


class UnconfiguredGroupError(Exception):
    """
    Exception Class, raised if Group Configuration is invalid.
    """
    pass


def conn_iter(connection_group):

    logger = logging.getLogger(__name__)

    connection_id = 0
    max_pool_size = Connection.get_max_pool_size(connection_group)

    while True:
        connection = (connection_group, connection_id)
        (conn_ref, status) = Connection.get_connection(connection)
        logger.debug('iterator group:{} id:{} conn_ref:{} status:{}'.format(
                connection_group,
                connection_id,
                conn_ref,
                status
            )
        )

        if status == 'free':
            Connection.set_connection_status(connection, 'occupied')
            yield (connection_id, conn_ref)
            connection_id += 1
        else:
            connection_id += 1
            if Connection.get_connection_count(connection) == max_pool_size:
                yield None
        if connection_id == max_pool_size:
            connection_id = 0


def conn_iter_locked(iterator):
    lock = threading.Lock()
    while True:
        try:
            with lock:
                value = next(iterator)
                yield value
        except StopIteration:
            return


class Connection(object):
    """
    Connection Class.
    """

    @classmethod
    def init(cls, config):
        """
        """
        cls.logger = logging.getLogger(__name__)
        cls._config = config
        cls._init_class()

    @classmethod
    def _init_class(cls):
        """
        """

        db_config = cls._config['db']

        statement_timeout = 'statement_timeout={}'.format(db_config['query_timeout'])
        temp_buffers = 'temp_buffers={}MB'.format(db_config['session_tmp_buffer'])

        os.environ['PGOPTIONS'] = '-c {timeout} -c {buffers}'.format(
            timeout = statement_timeout,
            buffers = temp_buffers
        )

        cls._setup_groups()

    @classmethod
    def _setup_groups(cls):
        """
        """
        for group in cls._config['groups']:
            cls._config['groups'][group]['connection_iter'] = conn_iter_locked(
                conn_iter(group)
            )
            cls._setup_connections(group)

    @classmethod
    def _setup_connections(cls, group):
        """
        """

        group_container = cls._config['groups'][group]
        group_container['connections'] = []
        connection_container = group_container['connections']

        for id in range(0, group_container['connection_count']):
            connection_container.append(
                (None, 'connecting')
            )
            cls.connect((group, id))
        cls.logger.debug(cls._config)

    @classmethod
    def get_max_pool_size(cls, group):
        """
        """
        return cls._config['groups'][group]['connection_count']

    @classmethod
    def get_connection_iter_container(cls, group):
        """
        """
        return cls._config['groups'][group]['connection_iter']

    @classmethod
    def get_connection_container(cls, connection):
        """
        """
        (group, id) = connection
        return cls._config['groups'][group]['connections'][id]

    @classmethod
    def get_connection(cls, connection):
        """
        """
        return cls.get_connection_container(connection)

    @classmethod
    def get_connection_count(cls, connection):
        """
        """
        connection_count = 0
        (group, id) = connection
        connections = cls._config['groups'][group]['connections']
        for (conn_ref, status) in connections:
            if status == 'occupied':
                connection_count += 1
        return connection_count

    @classmethod
    def set_connection_status(cls, connection, status):
        """
        """
        assert status in ['occupied', 'free'], 'status must be free or occupied'
        lock = threading.Lock()
        with lock:
            (group, id) = connection
            connections = cls._config['groups'][group]['connections']
            connection = connections[id]
            new_connection = (connection[0], status)
            # del(connections[id])
            connections[id] = new_connection
            cls.logger.debug('set status id:{} status:{} con_ref:{}'.format(
                    id,
                    status,
                    new_connection[0]
                )
            )

    @classmethod
    def get_next_connection(cls, group):
        """
        """
        try:
            return next(cls.get_connection_iter_container(group))
        except KeyError:
            raise UnconfiguredGroupError

    @classmethod
    def connect(cls, connection):
        """
        """

        (conn_group, conn_id) = connection

        try:

            lock = threading.Lock()

            db_container = cls._config['db']
            group_container = cls._config['groups'][conn_group]

            with lock:

                group_container['connections'][conn_id] = (
                    psycopg2.connect(
                        dbname = db_container['name'],
                        user = db_container['user'],
                        host = db_container['host'],
                        password = db_container['pass'],
                        sslmode = db_container['ssl'],
                        connect_timeout = db_container['connect_timeout']
                    ),
                    'free'
                )

                conn_container = group_container['connections'][conn_id]
                connection = conn_container[0]

                if 'autocommit' in group_container and group_container['autocommit'] is True:
                    extension = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
                    connection.set_isolation_level(extension)

                if 'sqlprepare' in group_container and group_container['sqlprepare'] is True:
                    tmpCursor = connection.cursor(
                        cursor_factory = psycopg2.extras.DictCursor
                    )
                    tmpCursor.callproc('"SQLPrepare"."PrepareQueries"')

        except Exception as e:
            raise DBConnectionError

    @classmethod
    def reconnect(cls, connection):
        """
        """
        try:
            Query.check_db(connection)
        except DBOfflineError:
            for i in range(0, 10):
                try:
                    Connection.connect(connection)
                    return
                except Exception as e:
                    time.sleep(cls._config['db']['connection_retry_sleep'])


class Query(object):
    """
    Query Class.
    """

    @staticmethod
    def execute_prepared(connection, sql_params):
        """
        """

        assert sql_params is not None, "sql_params must be given."

        Connection.reconnect(connection)
        (conn_ref, status) = Connection.get_connection(connection)

        try:
            tmpCursor = conn_ref.cursor(cursor_factory=psycopg2.extras.DictCursor)
            tmpCursor.callproc('"SQLPrepare"."ExecuteQuery"', sql_params)
            rec = tmpCursor.fetchone()
            return rec[0]
        except Exception as e:
            ErrorJSON = {}
            ErrorJSON['error'] = True
            ErrorJSON['exception'] = type(e).__name__
            ErrorJSON['exceptionCause'] = e.message
            return json.dumps(ErrorJSON)

    @staticmethod
    def execute(connection, sql_statement, sql_params=None):
        """
        """

        Connection.reconnect(connection)
        (conn_ref, status) = Connection.get_connection(connection)

        try:
            tmpCursor = conn_ref.cursor(cursor_factory=psycopg2.extras.DictCursor)
            tmpCursor.execute(sql_statement, sql_params)
            return tmpCursor
        except Exception as e:
            raise DBQueryError(repr(e))

    @staticmethod
    def check_db(connection):
        """
        """
        (conn_ref, status) = Connection.get_connection(connection)
        try:
            tmpCursor = conn_ref.cursor(cursor_factory=psycopg2.extras.DictCursor)
            tmpCursor.execute("SELECT to_char(now(), 'HH:MI:SS') AS result")
            rec = tmpCursor.fetchone()
        except Exception as e:
            raise DBOfflineError


class Handler(object):
    """
    (Query) Handler Class.
    """

    def __enter__(self):
        """
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        """
        self._cleanup()

    def query(self, statement, params=None):
        """
        """
        return Query.execute(self._connection, statement, params)

    def query_prepared(self, params):
        """
        """
        return Query.execute_prepared(self._connection, params)

    def _cleanup(self):
        """
        """
        self.logger.debug('cleanup connection:{}'.format(self._connection))

        try:
            self.conn_ref.commit()
        except Exception as e:
            pass

        Connection.set_connection_status(
            (self._group, self._conn_id),
            'free'
        )
        return


    def __init__(self, group):
        """
        """

        self.logger = logging.getLogger(__name__)
        self._group = group

        while True:
            try:
                (self._conn_id, self.conn_ref) = Connection.get_next_connection(group)
                self._connection = (self._group, self._conn_id)
                self.logger.debug('handler connection:{}'.format(self._connection))
                return
            except TypeError:
                time.sleep(0.1)
