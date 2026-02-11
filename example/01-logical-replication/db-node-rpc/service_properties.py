service_properties = {
    'System': {
        'properties': {
            'id': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'System id'
            },
            'node_index': {
                'type': 'int',
                'default': None,
                'required': True,
                'description': 'Node index'
            },
            'node_id': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Node id (hostname)'
            }
        },
        'methods': [
            'update_network_topology'
        ]
    },
    'Network': {
        'properties': {
            'hostname': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Network host name'
            },
            'domain': {
                'type': 'str',
                'default': 'default.localnet',
                'required': True,
                'description': 'Network domain (name)'
            },
            'address_v4': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Network IPv4 address'
            },
            'address_v6': {
                'type': 'str',
                'default': None,
                'required': False,
                'description': 'Network IPv6 address'
            }
        }
    },
    'NetworkTopology': {
        'properties': {
            'type': {
                'type': 'str',
                'default': 'un-partitioned',
                'required': False,
                'description': 'Network topology type'
            }
        }
    },
    'NetIPv4': {
        'properties': {
            'subnet': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'IPv4 subnet'
            },
            'netmask': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'IPv4 netmask'
            },
            'netbits': {
                'type': 'int',
                'default': None,
                'required': True,
                'description': 'IPv4 netmask bits'
            },
            'gateway': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'IPv4 gateway address'
            },
            'hostaddress': {
                'type': 'str',
                'default': None,
                'required': False,
                'description': 'IPv4 docker host address'
            }
        }
    },
    'NetIPv6': {
        'properties': {
        }
    },
    'TopologyHost': {
        'properties': {
            'name': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Hostname'
            },
            'ipv4': {
                'type': 'str',
                'default': None,
                'required': False,
                'description': 'IPv4 address'
            },
            'ipv6': {
                'type': 'str',
                'default': None,
                'required': False,
                'description': 'IPv6 address'
            }
        }
    },
    'Database': {
        'properties': {
            'name': {
                'type': 'str',
                'default': 'postgres',
                'required': False,
                'description': 'Database name (to connect to)'
            },
            'createdb_name': {
                'type': 'str',
                'default': None,
                'required': False,
                'description': 'Database name (to create)'
            }
        },
        'methods': [
            'init_db',
            'create_replica_table'
        ]
    },
    'Table': {
        'properties': {
            'name': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Table name'
            },
            'add_timestamp_cols': {
                'type': 'bool',
                'default': True,
                'required': False,
                'description': 'Automatically add timestamp columns for insert and update'
            },
            'attach_replication_trigger':  {
                'type': 'bool',
                'default': True,
                'required': False,
                'description': 'Automatically attach replication check trigger (currently only update)'
            },
        }
    },
    'Column': {
        'properties': {
            'primary_key': {
                'type': 'bool',
                'default': False,
                'required': False,
                'description': 'Column primary key flag'
            },
            'name': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Column name'
            },
            'type': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Column type'
            },
            'default': {
                'type': 'str',
                'default': None,
                'required': False,
                'description': 'Column default value'
            },
            'not_null': {
                'type': 'bool',
                'default': False,
                'required': False,
                'description': 'Null constraint'
            }
        }
    }
}
