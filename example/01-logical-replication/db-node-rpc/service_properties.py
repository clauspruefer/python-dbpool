service_properties = {
    'System': {
        'properties': {
            'id': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'System id'
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
        },
        'methods': [
            'update'
        ]
    },
    'NetIPv4': {
        'properties': {
            'subnet': {
                'type': 'str',
                'required': True,
                'description': 'IPv4 subnet'
            },
            'netmask': {
                'type': 'str',
                'required': True,
                'description': 'IPv4 netmask'
            },
            'netbits': {
                'type': 'int',
                'required': True,
                'description': 'IPv4 netmask bits'
            },
            'gateway': {
                'type': 'str',
                'required': True,
                'description': 'IPv4 gateway address'
            },
            'hostaddress': {
                'type': 'str',
                'required': False,
                'description': 'IPv4 docker host address'
            }
        }
    },
    'NetIPv6': {
        'properties': {
        }
    },
    'HostNode': {
        'properties': {
            'name': {
                'type': 'str',
                'required': True,
                'description': 'Hostname'
            },
            'ipv4': {
                'type': 'str',
                'required': False,
                'description': 'IPv4 address'
            },
            'ipv6': {
                'type': 'str',
                'required': False,
                'description': 'IPv6 address'
            }
        }
    },
    'Database': {
        'properties': {
            'id': {
                'type': 'str',
                'default': None,
                'required': True,
                'description': 'Database id'
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
                'description': 'Column id'
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
            }
        }
    }
}
