import json
import jsocket

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


sysconfig

{
    "dbpool-net-0": {
        "status": "active",
        "metrics": {
        }
    }
}
