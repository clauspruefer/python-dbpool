import abc
import json
import logging
import datetime

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

        with open('/tmp/net-config.json', 'w')as fh:
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

    def init_db(self):
        pass

    def create_replica_table(self):
        pass


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
