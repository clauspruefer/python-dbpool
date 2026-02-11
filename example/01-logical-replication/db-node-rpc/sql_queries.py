init_database = '''
ALTER SYSTEM SET max_replication_slots = 10;
ALTER SYSTEM SET max_wal_senders = 10;
'''

init_roles = '''
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator';
CREATE ROLE testreader WITH LOGIN PASSWORD 'testreader';
CREATE ROLE testwriter WITH LOGIN PASSWORD 'testwriter';
'''

create_table = '''
CREATE TABLE {table_name} (
 {table_columns}
);

GRANT SELECT ON TABLE {table_name} TO replicator;
GRANT SELECT ON TABLE {table_name} TO testreader;
GRANT INSERT ON TABLE {table_name} TO testwriter;
'''

create_publication = '''
CREATE PUBLICATION {publication_id} FOR TABLE {table_name};
'''

create_subscription = '''
CREATE SUBSCRIPTION {subscription_id} CONNECTION 'host={host_ip} dbname=postgres port=5432' PUBLICATION {publication_id} WITH (copy_data = false, origin = none);
'''
