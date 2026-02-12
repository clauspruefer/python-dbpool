import json
import logging
import psycopg2
import subprocess
import sql_queries

from microesb import microesb

logger = logging.getLogger(__name__)


class System(microesb.ClassHandler):

    def __init__(self):
        super().__init__()

    def update_network_topology(self):

        self.json_transform()

        net_config = {}
        net_config['System'] = self.json_dict
        net_config['Network'] = self.Network.json_dict
        net_config['NetworkTopology'] = self.NetworkTopology.TopologyHost.json_dict

        with open('/tmp/net-config.json', 'w') as fh:
            fh.write(json.dumps(net_config))


class Network(microesb.ClassHandler):

    def __init__(self):
        super().__init__()


class NetworkTopology(microesb.ClassHandler):

    def __init__(self):
        super().__init__()


class NetIPv4(microesb.ClassHandler):

    def __init__(self):
        super().__init__()


class NetIPv6(microesb.ClassHandler):

    def __init__(self):
        super().__init__()


class TopologyHost(microesb.MultiClassHandler):

    def __init__(self):
        super().__init__()


class Database(microesb.ClassHandler):

    def __init__(self):
        super().__init__()
        self.conn = False
        self.host = '127.0.0.1'
        self.user = 'postgres'
        self.autocommit = True

        with open('/tmp/net-config.json', 'r') as fh:
            self.netconf = json.loads(fh.read())

    def _connect(self):
        self.conn = psycopg2.connect(
            "dbname='{}' user='{}' host='{}'".format(
                self.name,
                self.user,
                self.host
            )
        )
        self.conn.autocommit = self.autocommit

    def init_db(self):

        cmd_alter_db = "psql -U postgres -c '{}'".format(sql_queries.init_database)
        subprocess.run(cmd_alter_db, shell=True, capture_output=True)

        self._connect()

        with self.conn.cursor() as crs:
            crs.execute(sql_queries.init_roles)

    def create_replica_table(self):

        self._connect()

        ct_sql = sql_queries.create_table.format(
            table_name=self.Table.name,
            table_columns=self.Table.get_table_sql()
        )

        logger.debug('create_replica_table sql:{}'.format(ct_sql))

        with self.conn.cursor() as crs:
            crs.execute(ct_sql)

        self._create_publication()
        self._subscribe_to_others()

    def _create_publication(self):
        with self.conn.cursor() as crs:
            crs.execute(
                sql_queries.create_publication.format(
                    table_name=self.Table.name,
                    publication_id=self._gen_publication_id()
                )
            )

    def _subscribe_to_others(self):

        node_index = self.netconf['System']['node_index']

        if node_index > 0:

            host_list = self.netconf['NetworkTopology']['TopologyHost']
            host_list_cut = host_list[0:node_index]
            logger.debug('host_list_cut:{}'.format(host_list_cut))

            for node in reversed(host_list_cut):
                with self.conn.cursor() as crs:
                    crs.execute(
                        sql_queries.create_subscription.format(
                            host_ip=node['ipv4'],
                            subscription_id=self._gen_subscription_id(node['name']),
                            publication_id='pub_{}_{}'.format(node['name'], self.Table.name)
                        )
                    )

    def subscribe_to_node(self):

        self._connect()

        dst_node = self._get_node_by_id(self.subscribe_dst_node)

        logger.debug('subscribe2node sys_node:{} dst_node:{}'.format(
                self.netconf['System']['node_id'],
                self.subscribe_dst_node
            )
        )

        with self.conn.cursor() as crs:
            crs.execute(
                sql_queries.create_subscription.format(
                    host_ip=dst_node['ipv4'],
                    subscription_id=self._gen_subscription_id(dst_node['name']),
                    publication_id='pub_{}_{}'.format(dst_node['name'], self.Table.name)
                )
            )

    def _gen_publication_id(self):
        return 'pub_{}_{}'.format(
            self.netconf['Network']['hostname'],
            self.Table.name
        )

    def _gen_subscription_id(self, dst_node_id):
        return 'sub_{}_{}_{}'.format(
            self.netconf['System']['node_id'],
            dst_node_id,
            self.Table.name
        )

    def _get_node_by_id(self, node_id):
        # we should use ordered dict in the future
        host_list = self.netconf['NetworkTopology']['TopologyHost']
        return next((elm for elm in host_list if elm['name'] == node_id))


class Table(microesb.ClassHandler):

    def __init__(self):
        super().__init__()

    def get_table_sql(self):
        ret_string = ''
        for val in self._gen_table_sql():
            ret_string += val
        return ret_string

    def _gen_table_sql(self):
        for class_ref in self.Column:
            yield class_ref.get_column_sql()
        if self.add_timestamp_cols is True:
            yield 'created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP, '
            yield 'modified_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP'


class Column(microesb.MultiClassHandler):

    def __init__(self):
        super().__init__()
        self.primary_key = False
        self.default = False
        self.not_null = False

    def get_column_sql(self):
        ret_string = ''
        for val in self._gen_column_sql():
            ret_string += val
        return ret_string

    def _gen_column_sql(self):
        yield '{} {}'.format(self.name, self.type)
        if self.default is True:
            yield ' DEFAULT {}'.format(self.default)
        if self.primary_key is True:
            yield ' PRIMARY KEY'
        if self.not_null is True:
            yield ' NOT NULL'
        yield ', '
