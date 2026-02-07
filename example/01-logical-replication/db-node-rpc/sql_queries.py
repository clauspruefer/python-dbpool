init_db = '''
ALTER SYSTEM SET wal_level = logical;
ALTER SYSTEM SET max_replication_slots = 10;
ALTER SYSTEM SET max_wal_senders = 10;

CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator';
CREATE ROLE testreader WITH LOGIN PASSWORD 'testreader';
CREATE ROLE testwriter WITH LOGIN PASSWORD 'testwriter';
'''

create_table = '''
CREATE TABLE %(table_name)s (
 {table_columns}
);

GRANT SELECT ON TABLE %(table_name)s TO replicator;
GRANT SELECT ON TABLE %(table_name)s TO testreader;
GRANT INSERT ON TABLE %(table_name)s TO testwriter;
'''

create_publication = '''
CREATE PUBLICATION %(publication_id)s FOR TABLE %(table_name)s;
'''

create_subscription = '''
CREATE SUBSCRIPTION %(subscription_id)s CONNECTION 'host=%(host_ip)s dbname=postgres port=5432' PUBLICATION %(publication_id)s WITH (copy_data = false, origin = none);
'''
