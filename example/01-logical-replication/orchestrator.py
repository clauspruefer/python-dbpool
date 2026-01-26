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


sysconfig = None

with open('sysconfig.json', 'r') as fh:
    sysconfig = json.loads(fh.read())

network = sysconfig['system']['networks'][0]

network_id = network['id']
network_config = network['config']

network_segment = '{}/{}'.format(
    network_config['net']['ipv4']['subnet'],
    network_config['net']['ipv4']['netbits']
)

network_ipv4_addresses = iter(ipcalc.Network(network_segment))

svc_net_topology = svc_call_metadata.update_net_topology['data'][0]['System']['NetworkTopology']
svc_net_topology['NetIPv4'] = network_config['net']['ipv4']

# start containers
for i in range(0, 3):

    node_id = 'node-'+str(i)
    node_ip = next(network_ipv4_addresses)

    node_cfg = {
        'name': node_id,
        'ipv4': node_ip
    }

    svc_net_topology['HostNode'].append(node_cfg)

    cmd_run_container = []
    cmd_run_container.append('./run-container.sh')
    cmd_run_container.append(node_id)
    cmd_run_container.append(str(node_ip))
    cmd_run_container.append(network['id'])

    subprocess.run(cmd_run_container, capture_output=True)

    cmd_start_server = 'docker exec {} /json-rpc-server/start-server.sh'.format(node_id)
    res = subprocess.run(cmd_start_server, shell=True, capture_output=True)
    test = res.stdout.strip()
    print(test)
