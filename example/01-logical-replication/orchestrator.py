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


# load system configuration
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
count_nodes = network_config_scale['max_nodes']

# start containers
for i in range(0, count_nodes):

    node_id = 'node'+str(i)
    node_ip = next(network_ipv4_addresses)

    node_cfg = {
        'name': node_id,
        'ipv4': str(node_ip),
        'index': i
    }

    svc_net_topology['TopologyHost'].append(node_cfg)

    cmd_run_container = []
    cmd_run_container.append('./run-container.sh')
    cmd_run_container.append(node_id)
    cmd_run_container.append(str(node_ip))
    cmd_run_container.append(network['id'])

    subprocess.run(cmd_run_container, capture_output=True, check=True)

    cmd_start_server = 'docker exec {} /json-rpc-server/start-server.sh'.format(node_id)
    res = subprocess.run(cmd_start_server, shell=True, capture_output=True, check=True)

client_conn = {}

# setup node connections
for node in svc_net_topology['TopologyHost']:
    client_conn[node['name']] = mm_connect(node['ipv4'])

# init database / create table / subscribe to others
for node in svc_net_topology['TopologyHost']:

    svc_net['hostname'] = node['name']
    svc_net['domain'] = network_config['net']['domain']
    svc_net['address_v4'] = node['ipv4']

    svc_system['node_index'] = node['index']
    svc_system['node_id'] = node['name']

    res = mm_send(client_conn[node['name']], svc_call_metadata.update_net_topology)
    print(res)

    res = mm_send(client_conn[node['name']], svc_call_metadata.init_database)
    print(res)

    res = mm_send(client_conn[node['name']], svc_call_metadata.create_repl_table)
    print(res)

    # subscribe others to node
    for i in range(node['index'], 0, -1):

        node_item = svc_net_topology['TopologyHost'][i-1]
        print('Index:{} NodeItem:{}'.format(i-1, node_item))

        svc_call_metadata.subscribe_dst_node['data'][0]['Database']['subscribe_dst_node'] = node['name']
        res = mm_send(client_conn[node_item['name']], svc_call_metadata.subscribe_dst_node)
        print(res)
