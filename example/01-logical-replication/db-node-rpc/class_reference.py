references = {
    'UpdateNetworkTopology': {
        'System': {
            'property_ref': 'System',
            'children': {
                'NetworkTopology': {
                    'property_ref': 'NetworkTopology',
                    'children': {
                        'NetIPv4': {
                            'property_ref': 'NetIPv4'
                        },
                        'NetIPv6': {
                            'property_ref': 'NetIPv6'
                        },
                        'HostNode': {
                            'property_ref': 'HostNode'
                        }
                    }
                }
            }
        }
    },
    'InitDatabase': {
        'Database': {
            'property_ref': 'Database'
        }
    },
    'CreateReplicaTable': {
        'Database': {
            'property_ref': 'Database',
            'children': {
                'Table': {
                    'property_ref': 'Table',
                    'children': {
                        'Column': {
                            'property_ref': 'Column'
                        }
                    }
                }
            }
        }
    }
}
