import json
import ipcalc


with open('../sysconfig.json', 'r') as fh:
    sysconfig = json.loads(fh.read())

config = {
    'db': [
    ],
    'groups': {
        'writer1': {
            'connection_count': 20,
            'autocommit': True
        },
        'writer2': {
            'connection_count': 10,
            'autocommit': True
        },
        'reader1': {
            'connection_count': 24,
            'autocommit': True
        },
        'reader2': {
            'connection_count': 48,
            'autocommit': True
        }
    }
}

netconfig = sysconfig['system']['networks'][0]['config']['net']['ipv4']

netconfig_net = netconfig['subnet']
netconfig_bits = netconfig['netbits']

net_segment = '{}/{}'.format(netconfig_net, netconfig_bits)
net_ipv4_addr = iter(ipcalc.Network(net_segment))

max_nodes = sysconfig['system']['networks'][0]['config']['scale']['max-nodes']

for i in range(0, max_nodes):
    config['db'].append(
        {
            'host': str(next(net_ipv4_addr)),
            'name': 'lb-test',
            'user': 'testwriter',
            'pass': 'testwriter',
        }
    )
