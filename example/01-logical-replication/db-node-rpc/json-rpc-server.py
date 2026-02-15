import sys
import jsocket
import logging
import subprocess

from microesb import microesb

from class_reference import references as class_reference
from service_properties import service_properties
from class_mapping import class_mapping

logging.getLogger().addHandler(
    logging.FileHandler(filename='/tmp/app.log')
)

logging.getLogger().setLevel(
    logging.DEBUG
)


def get_current_ip_address():
    cmd_get_ip = 'ip -h addr show dev eth0 | grep inet | cut -d " " -f 6'
    res = subprocess.run(cmd_get_ip, shell=True, capture_output=True)
    raw_ip = res.stdout.strip()
    raw_ip_sep = raw_ip.find(b'/')
    return raw_ip[:raw_ip_sep]


class JSONServer(jsocket.JsonServer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _process_message(self, call_obj):
        if isinstance(call_obj, dict):
            logging.info('RPC call obj:{}'.format(call_obj))
            class_mapper_ref = microesb.ClassMapper(
                class_references=class_reference[call_obj['SYSServiceID']],
                class_mappings=class_mapping[call_obj['SYSServiceID']],
                class_properties=service_properties
            )
            res = microesb.ServiceExecuter().execute(
                class_mapper=class_mapper_ref,
                service_data=call_obj
            )
            logging.info('RPC result:{}'.format(res))
            return { "Status": "ok" }
        return { "Status": "error - objtype not dict()" }


server = JSONServer(
    address=get_current_ip_address(),
    port=64000
).server_loop()
