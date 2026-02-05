import json
import ipcalc
import jsocket
import subprocess

import svc_call_metadata


def mm_connect(dst_address, dst_port=64000):
    client = jsocket.JsonClient(address=dst_address, port=dst_port)
    assert client.connect() is True
    return client

def mm_send(client_ref, payload):
    client_ref.send_obj(payload)
    return client_ref.read_obj()

def mm_close(client_ref):
    client_ref.close()


# load configuration
with open('./sysconfig.json', 'r') as fh:
    sysconfig = json.loads(fh.read())

# model config parts
network = sysconfig['system']['networks'][0]

network_id = network['id']
network_config = network['config']
network_config_scale = network['config']['scale']

network_segment = '{}/{}'.format(
    network_config['net']['ipv4']['subnet'],
    network_config['net']['ipv4']['netbits']
)

# make network segment iterator
network_ipv4_addresses = iter(ipcalc.Network(network_segment))

svc_system = svc_call_metadata.update_net_topology['data'][0]['System']

svc_net = svc_system['Network']
svc_net_topology = svc_system['NetworkTopology']
svc_net_topology['NetIPv4'] = network_config['net']['ipv4']

# get node-count from config
count_nodes = network_config_scale['max-nodes']

# start containers
for i in range(0, count_nodes):

    node_id = 'node-'+str(i)
    node_ip = next(network_ipv4_addresses)
    #node_ip = '192.168.10.120'

    node_cfg = {
        'name': node_id,
        'ipv4': str(node_ip)
    }

    svc_net['hostname'] = node_id
    svc_net['domain'] = network_config['net']['domain']
    svc_net['address_v4'] = str(node_ip)

    svc_net_topology['TopologyHost'].append(node_cfg)

    cmd_run_container = []
    cmd_run_container.append('./run-container.sh')
    cmd_run_container.append(node_id)
    cmd_run_container.append(str(node_ip))
    cmd_run_container.append(network['id'])

    subprocess.run(cmd_run_container, capture_output=True, check=True)

    cmd_start_server = 'docker exec {} /json-rpc-server/start-server.sh'.format(node_id)
    res = subprocess.run(cmd_start_server, shell=True, capture_output=True, check=True)


for node in svc_net_topology['TopologyHost']:

    print(svc_call_metadata.update_net_topology)
    client = mm_connect(node['ipv4'])
    res = mm_send(client, svc_call_metadata.update_net_topology)
    print(res)
