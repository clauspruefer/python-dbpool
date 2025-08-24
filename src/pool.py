import os
import time
import json
import logging
import threading
import psycopg2

from psycopg2 import extras


class DBConnectionError(Exception):
    """
    Exception Class, raised on Database Connection Error.
    """


class DBQueryError(Exception):
    """
    Exception Class, raised on Database Query Error.
    """


class DBOfflineError(Exception):
    """
    Exception Class, raised on Database Not Reachable Error.
    """


class UnconfiguredGroupError(Exception):
    """
    Exception Class, raised on Invalid Group Configuration Error.
    """


global_lock = threading.Lock()


def conn_iter(connection_group):
    """
    Global Connection Iterator.
    """

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


class Connection(object):
    """
    Connection Class.
    """

    @classmethod
    def init(cls, config):
        """ Initialize "static" Class Instance.

        :param dict config: single configuration data
        :param list of dict config: multiple configuration data
        """

        cls.logger = logging.getLogger(__name__)
        cls._config = config
        cls._init_class()

    @classmethod
    def _init_class(cls):
        """
        Initialize "static" Class Instance.

        - setup global config data
        - setup groups (call _setup_groups())
        """

        # convert single dict to list type
        if isinstance(cls._config['db'], dict):
            db_config = cls._config['db']
            cls._config['db'] = [cls._config['db']]

        # setup db connection iterator
        cls._dbiter_ref = cls._dbiter()

        db_config = cls._config['db'][0]
        statement_timeout = 'statement_timeout={}'.format(db_config['query_timeout'])
        temp_buffers = 'temp_buffers={}MB'.format(db_config['session_tmp_buffer'])

        os.environ['PGOPTIONS'] = '-c {timeout} -c {buffers}'.format(
            timeout = statement_timeout,
            buffers = temp_buffers
        )

        cls._setup_groups()

    @classmethod
    def _dbiter(cls):
        """
        DB Connection Iterator.
        """

        while True:
            for config in cls._config['db']:
                yield config

    @classmethod
    def _setup_groups(cls):
        """
        Setup "group" Config / Iterator(s).
        
        - for each group, call _setup_connections(group_name)
        """

        for group in cls._config['groups']:
            cls._config['groups'][group]['connection_iter'] = conn_iter(group)
            cls._setup_connections(group)

    @classmethod
    def _setup_connections(cls, group):
        """ Setup Connections per "group".
        
        :param str group: group name

        - init DB connection for range (0, group.conn_count)
        """

        group_container = cls._config['groups'][group]
        group_container['connections'] = []
        connection_container = group_container['connections']

        for conn_id in range(0, group_container['connection_count']):
            connection_container.append(
                (None, 'connecting')
            )
            cls.connect((group, conn_id))
        cls.logger.debug('configuration:{}'.format(cls._config))

    @classmethod
    def get_threading_model(cls):
        """ Return Threading Model / Type.

        :return: threading model (threaded | non-threaded)
        :rtype: string
        """

        return 'threaded' if 'type' not in cls._config else cls._config.get('type')

    @classmethod
    def get_max_pool_size(cls, group):
        """ Get Connection-Pool Size by "group name".
        
        :param str group: group name
        :return: connection count
        :rtype: int
        """
        return cls._config['groups'][group]['connection_count']

    @classmethod
    def get_connection_iter_container(cls, group):
        """ Get Connection Iterator Container by "group name".

        :param str group: group name
        :return: connection iterator
        :rtype: iterator
        """
        return cls._config['groups'][group]['connection_iter']

    @classmethod
    def get_connection_container(cls, connection):
        """ Get Connection Container by Connection.

        :param tuple connection: (group name, group id)
        :return: connection tuple (conn object ref, conn status)
        :rtype: tuple
        """
        (group, conn_id) = connection
        return cls._config['groups'][group]['connections'][conn_id]

    @classmethod
    def get_connection(cls, connection):
        """
        Alias for "get_connection_container()".
        """
        return cls.get_connection_container(connection)

    @classmethod
    def get_connection_count(cls, connection):
        """ Get Connection Count by Connection.

        :param tuple connection: (group name, group id)
        :return: connection count
        :rtype: int
        """

        connection_count = 0
        (group, group_id) = connection
        cls.logger.debug('connection get_connection_count() group_id:{}'.format(group_id))
        connections = cls._config['groups'][group]['connections']
        for (conn_ref, status) in connections:
            cls.logger.debug('connection get_connection_count() conn_ref:{} status:{}'.format(conn_ref, status))
            if status == 'occupied':
                connection_count += 1
        return connection_count

    @classmethod
    def set_connection_status(cls, connection, status):
        """ Set Connection Status.

        :param tuple connection: (group name, group id)
        :param str status: occupied | free.
        """
        assert status in ['occupied', 'free'], 'status must be free or occupied'

        (group, group_id) = connection
        connections = cls._config['groups'][group]['connections']
        connection_by_id = connections[group_id]
        new_connection = (connection_by_id[0], status)
        connections[group_id] = new_connection
        cls.logger.debug('connection set_connection_status() group_id:{} status:{} con_ref:{}'.format(
                group_id,
                status,
                new_connection[0]
            )
        )

    @classmethod
    def get_next_connection(cls, group):
        """ Get Iterators next() Connection by "group name".

        :param str group: group name
        :return: connection object
        :rtype: object
        """
        try:
            return next(cls.get_connection_iter_container(group))
        except KeyError:
            raise UnconfiguredGroupError

    @classmethod
    def connect(cls, connection):
        """ Connect to Database.

        :param tuple connection: (group name, group id)
        """

        (conn_group, conn_id) = connection

        try:
            db_container = next(cls._dbiter_ref)
            group_container = cls._config['groups'][conn_group]

            cls.logger.debug('connection connect() db_config:{}'.format(db_container))

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

        except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.InternalError) as e:
            cls.logger.debug('connection connect() exception:{}'.format(repr(e)))
            raise DBConnectionError

    @classmethod
    def reconnect(cls, connection):
        """ Re-connect to Database.

        :param tuple connection: (group name, group id)
        """
        try:
            Query.check_db(connection)
        except DBOfflineError:
            for i in range(0, 10):
                try:
                    cls.logger.debug('connection reconnect() try nr:{}'.format(i))
                    Connection.connect(connection)
                    return
                except DBConnectionError as e:
                    cls.logger.debug('connection reconnect() exception:{}'.format(repr(e)))
                    time.sleep(cls._config['db']['connection_retry_sleep'])


class Query(object):
    """
    Query Class.
    """

    @staticmethod
    def execute_prepared(connection, sql_params):
        """ Execute a System Prepared Query.

        See https://github.com/WEBcodeX1/pg_extensions/tree/main/prep_queries.

        :param tuple connection: (group name, group id)
        :param str sql_params: SQL stored procedure parameters
        """

        assert sql_params is not None, 'sql_params must be given.'

        Connection.reconnect(connection)
        (conn_ref, status) = Connection.get_connection(connection)
        Connection.logger.debug('query execute_prepared() connection status:{}'.format(status))

        try:
            tmpCursor = conn_ref.cursor(cursor_factory=psycopg2.extras.DictCursor)
            tmpCursor.callproc('"SQLPrepare"."ExecuteQuery"', sql_params)
            rec = tmpCursor.fetchone()
            return rec[0]
        except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.ProgrammingError) as e:
            ErrorJSON = {}
            ErrorJSON['error'] = True
            ErrorJSON['exception'] = type(e).__name__
            ErrorJSON['exceptionCause'] = e.message
            return json.dumps(ErrorJSON)

    @staticmethod
    def execute(connection, sql_statement, sql_params=None):
        """ Execute SQL Query String.

        :param tuple connection: (group name, group id)
        :param str sql_statement: SQL statement
        :param str sql_params: SQL parameters
        """

        Connection.reconnect(connection)
        (conn_ref, status) = Connection.get_connection(connection)
        Connection.logger.debug('query execute() connection status:{}'.format(status))

        try:
            tmpCursor = conn_ref.cursor(cursor_factory=psycopg2.extras.DictCursor)
            tmpCursor.execute(sql_statement, sql_params)
            return tmpCursor
        except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.ProgrammingError) as e:
            Connection.logger.debug('query execute() exception:{}'.format(repr(e)))
            raise DBQueryError(repr(e))

    @staticmethod
    def check_db(connection):
        """ Check Database Connection.

        Check Database Connection is alive by sending simple now() request.

        :param tuple connection: (group name, group id)
        """
        (conn_ref, status) = Connection.get_connection(connection)
        Connection.logger.debug('query check_db() connection status:{}'.format(status))

        try:
            tmpCursor = conn_ref.cursor(cursor_factory=psycopg2.extras.DictCursor)
            tmpCursor.execute("SELECT to_char(now(), 'HH:MI:SS') AS result")
            tmpCursor.fetchone()
        except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.InternalError) as e:
            Connection.logger.debug('query check_db() exception:{}'.format(repr(e)))
            raise DBOfflineError


class Handler(object):
    """ (Query) Handler Class.


    :example:

    >>> dbpool.Connection.init(config_dict)
    >>>
    >>> sql = 'select * from table1'
    >>>
    >>> with dbpool.Handler('group1') as db:
    >>>     for rec in db.query(sql):
    >>>         print(str(rec))
    """

    def __init__(self, group):
        """ Initialize Handler.

        :param str group: group name
        """

        self.logger = logging.getLogger(__name__)
        self._group = group

        threading_model = Connection.get_threading_model()
        assert threading_model in ['threaded', 'non-threaded'], 'threading model must be threaded or non-threaded.'
        self.logger.info('handler() __init__() threading_model:{}'.format(threading_model))

        while True:
            try:
                if threading_model == 'threaded':
                    with global_lock:
                        self._process()
                else:
                    self._process()
                return
            except TypeError:
                time.sleep(0.1)

    def __enter__(self):
        """ Overloaded __enter__.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Overloaded __exit__.

        Call _cleanup() on exit.
        """
        self._cleanup()

    def query(self, statement, params=None):
        """ Query Wrapper Class.
        """

        return Query.execute(self._connection, statement, params)

    def commit(self):
        """ Commit Transaction.

        Manual commit() procedure used for `autocommit=False` connections.
        """
        self.conn_ref.commit()

    def query_prepared(self, params):
        """
        Query Prepared Wrapper Class.
        """

        return Query.execute_prepared(self._connection, params)

    def _process(self):
        """
        Process next() Connection.
        """

        (self._conn_id, self.conn_ref) = Connection.get_next_connection(self._group)
        self._connection = (self._group, self._conn_id)
        self.logger.debug('handler() connection:{}'.format(self._connection))

    def _cleanup(self):
        """ Cleanup Connection.

        Cleanup Connection (exit **with** block).
        
        - Try to commit() on no autocommit if still unfinished transaction(s)
        - Set connection status to 'free'
        """

        self.logger.debug('cleanup connection:{}'.format(self._connection))

        try:
            self.conn_ref.commit()
        except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.InternalError) as e:
            self.logger.debug('cleanup connection:{}'.format(repr(e)))

        Connection.set_connection_status(
            (self._group, self._conn_id),
            'free'
        )
