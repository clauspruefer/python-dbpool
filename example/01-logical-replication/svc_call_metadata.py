update_net_topology = {
    'SYSServiceID': 'UpdateNetworkTopology',
    'data': [
        {
            'SYSBackendMethod': { 'System': 'update_network_topology' },
            'System': {
                'id': 'db-loadbalancing-test',
                'node_index': None,
                'node_id': None,
                'Network': {},
                'NetworkTopology': {
                    'NetIPv4': {},
                    'TopologyHost': []
                }
            }
        }
    ]
}

init_database = {
    'SYSServiceID': 'InitDatabase',
    'data': [
        {
            'SYSBackendMethod': { 'Database': 'init_db' },
            'Database': {
                'createdb_name': 'lb-test'
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
                'name': 'lb-test',
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
