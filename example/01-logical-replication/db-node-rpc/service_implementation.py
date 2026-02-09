import json
import logging
import sql_queries

from microesb import microesb

logger = logging.getLogger(__name__)


class System(microesb.ClassHandler):

    def __init__(self):
        super().__init__()

    def update_network_topology(self):

        self.json_transform()

        net_config = {}
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
        self.db_con = False
        self.db_con_autoconnect = True
        self.db_host = '127.0.0.1'
        self.db_user = 'postgres'
        self.db_name = 'postgres'

        with open('/tmp/net-config.json', 'r') as fh:
            self.netconf = json.loads(fh.read())

    def connect(self):
        self.db_con = psycopg2.connect(
            "dbname='{}' user='{}' host='{}'".format(
                self.db_name,
                self.db_user,
                self.db_host
            )
        )
        self.db_con.autocommit = self.db_con_autoconnect

    def init_db(self):
        with self.db_con.cursor() as crs:
            crs.execute(sql_queries.init_db)

    def create_replica_table(self):
        pass

    def create_publication(self):
        with self.db_con.cursor() as crs:
            crs.execute(
                sql_queries.create_publication, {
                    'table_name': self.Table.name,
                    'publication_id': self._gen_publication_id()
                }
            )

    def subscribe_to_others(self):
        host_list = self.netconf['NetworkTopology']['TopologyHost']
        for node in reversed(host_list):
            with self.db_con.cursor() as crs:
                crs.execute(
                    sql_queries.create_subscription, {
                        'host_ip': node['ipv4'],
                        'subscription_id': self._gen_subscription_id(node['name'])
                        'publication_id': 'pub-{}-{}'.format(node['name'], self.Table.name)
                    }
                )

    def subscribe_to_node(self, node_id):
        pass

    def _gen_publication_id(self):
        return 'pub-{}-{}'.format(
            self.netconf['Network']['hostname'],
            self.Table.name
        )

    def _gen_subscription_id(self, node_id):
        return 'sub-{}-{}'.format(
            node_id,
            self.Table.name
        )

class Table(microesb.ClassHandler):

    def __init__(self):
        super().__init__()


class Column(microesb.MultiClassHandler):

    def __init__(self):
        super().__init__()
        self.primary_key = False
        self.name = None
        self.type = None
        self.default = None
