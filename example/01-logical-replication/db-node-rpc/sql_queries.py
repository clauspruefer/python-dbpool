init_roles = '''
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator';
CREATE ROLE testreader WITH LOGIN PASSWORD 'testreader';
CREATE ROLE testwriter WITH LOGIN PASSWORD 'testwriter';
'''

create_table = '''
CREATE TABLE {table_name} (
 {table_columns}
);

SELECT setval('{table_name}_id_seq', {table_seq_start}, true);

GRANT USAGE ON SCHEMA public TO replicator;
GRANT SELECT ON TABLE {table_name} TO replicator;
GRANT SELECT ON TABLE {table_name} TO testreader;
GRANT INSERT ON TABLE {table_name} TO testwriter;
GRANT ALL ON {table_name}_id_seq TO testwriter;
'''

create_publication = '''
CREATE PUBLICATION {publication_id} FOR TABLE {table_name};
'''

create_subscription = '''
CREATE SUBSCRIPTION {subscription_id} CONNECTION 'host={host_ip} dbname=lb-test user=replicator port=5432' PUBLICATION {publication_id} WITH (copy_data = false, origin = none);
'''
