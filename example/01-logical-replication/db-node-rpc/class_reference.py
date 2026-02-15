references = {
    'UpdateNetworkTopology': {
        'System': {
            'property_ref': 'System',
            'children': {
                'Network': {
                    'property_ref': 'Network'
                },
                'NetworkTopology': {
                    'property_ref': 'NetworkTopology',
                    'children': {
                        'NetIPv4': {
                            'property_ref': 'NetIPv4'
                        },
                        'NetIPv6': {
                            'property_ref': 'NetIPv6'
                        },
                        'TopologyHost': {
                            'property_ref': 'TopologyHost'
                        }
                    }
                }
            }
        }
    },
    'InitDatabase': {
        'Database': {
            'property_ref': 'Database',
            'children': {}
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
    },
    'SubscribeDstNode': {
        'Database': {
            'property_ref': 'Database',
            'children': {
                'Table': {
                    'property_ref': 'Table'
                }
            }
        }
    }
}
