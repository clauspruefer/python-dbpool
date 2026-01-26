update_net_topology = {
    'SYSServiceID': 'UpdateNetworkTopology',
    'data': [
        {
            'SYSBackendMethod': { 'NetworkTopology': 'update' },
            'System': {
                'id': 'db-loadbalancing-test',
                'NetworkTopology': {
                    'NetIPv4': {},
                    'HostNode': []
                }
            }
        }
    ]
}

set_global_db_properties = {
    'SYSServiceID': 'InitDatabase',
    'data': [
        {
            'SYSBackendMethod': { 'Database': 'init_db' },
            'Database': {
                'id': 'lb-test'
            }
        }
    ]
}

create_repl_table = {
    'SYSServiceID': 'CreateReplicaTable',
    'data': [
        {
            'SYSBackendMethod': { 'Database': 'create_replica_table' },
            'Database': {
                'id': 'lb-test',
                'Table': {
                    'name': 'table1',
                    'add_timestamp_cols': True,
                    'attach_replication_trigger': True,
                    'Column': [
                        {
                            'name': 'id',
                            'type': 'serial',
                            'primary_key': True
                        },
                        {
                            'name': 'col1',
                            'type': 'varchar',
                            'default': 'default-value'
                        },
                        {
                            'name': 'col2',
                            'type': 'varchar'
                        }
                    ]
                }
            }
        }
    ]
}
